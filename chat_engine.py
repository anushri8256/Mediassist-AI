
"""
MediAssist AI - Local Bilingual Health Assistant

English + Hinglish conversation
Local ML + Home Care + Conversation Memory
No external AI API.

Medical information is educational, not a diagnosis.
"""

from pathlib import Path
import re
import random
import joblib
import numpy as np

from memory import ConversationMemory
from disease_knowledge import answer_disease_question
from homecare import HOME_CARE, ALIASES, get_homecare, format_homecare


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "trained_model"

DISCLAIMER = (
    "This is general educational information, "
    "not a medical diagnosis or prescription."
)

UNKNOWN_REPLY = (
    "I do not have enough reliable local information to answer "
    "that question yet. Please rephrase it or ask about common "
    "symptoms and health conditions. For personal medical advice, "
    "consult a qualified healthcare professional."
)


class ChatEngine:

    HINGLISH_MARKERS = set("""
        mujhe mere mera meri mai main mujhko tum tumhara
        aap aapka hai hain hu ho raha rahi rha rhi
        kya kaise kese kyu kyun batao btao bukhar
        bukhaar bhukhar bhukhaar bhukar khansi khaansi
        dard kal nahi nhi aur bhi kitne shukriya
        theek thik haan hn accha acha baat naam
        pet sir sar neend saans dikkat tabiyat se
        ghar ilaaj upay chakkar ulti balgam
        dost hoon kr rhi rhe mujhme
    """.split())

    FOLLOWUP_WORDS = {
        "since yesterday", "yesterday", "today",
        "since morning", "dry", "with mucus",
        "better", "same", "worse", "another one",
        "one more", "fine", "good", "okay", "great",
        "yes", "no", "thanks"
    }

    def __init__(self, model_name=None):

        print("[MediAssist] Loading local model...")

        self.model = joblib.load(
            MODEL_DIR / "deeper_candidate.pkl"
        )

        self.features = list(
            joblib.load(MODEL_DIR / "deeper_features.pkl")
        )

        self.memory = ConversationMemory(max_history=4)

        self.aliases = {
            "headache": [
                "headache", "head pain", "pain in my head",
                "my head hurts", "sir dard", "sar dard",
                "sir mein dard", "sar mein dard",
                "sir me dard", "sar me dard"
            ],
            "fever": [
                "fever", "high temperature",
                "bukhar", "bukhaar", "bhukhar",
                "bhukhaar", "bhukar", "bukharrr",
                "bhukharrr", "bukhaarrr",
                "bukhr", "bukhar hai", "bhukhar hai"
            ],
            "cough": [
                "cough", "coughing", "khansi",
                "khaansi", "khasi", "khaasi"
            ],
            "nausea": [
                "nausea", "nauseous", "ji machlana"
            ],
            "vomiting": [
                "vomiting", "vomit", "throwing up", "ulti"
            ],
            "dizziness": [
                "dizziness", "dizzy", "chakkar"
            ],
            "fatigue": [
                "fatigue", "tiredness", "tired",
                "thakan", "kamzori"
            ],
            "diarrhea": [
                "diarrhea", "diarrhoea",
                "loose motion", "loose motions", "dast"
            ],
            "constipation": [
                "constipation", "constipated",
                "kabz", "kabj", "pet saaf nahi ho raha"
            ],
            "stomach pain": [
                "stomach pain", "stomachache",
                "stomach ache", "abdominal pain",
                "pet dard", "pet mein dard", "pet me dard"
            ],
            "abdominal pain": [
                "abdominal pain", "stomach pain",
                "stomachache", "pet dard", "pet mein dard"
            ],
            "insomnia": [
                "insomnia", "can't sleep", "cannot sleep",
                "cant sleep", "difficulty sleeping",
                "neend nahi aa rahi", "neend nhi aa rhi"
            ],
            "sleeplessness": [
                "sleeplessness", "can't sleep",
                "cannot sleep", "neend nahi aa rahi"
            ],
            "high blood pressure": [
                "high bp", "bp high",
                "high blood pressure", "hypertension"
            ],
            "shortness of breath": [
                "shortness of breath", "difficulty breathing",
                "breathing difficulty", "saans lene mein dikkat"
            ]
        }

        self.response_language = "english"
        self.reset_context()

        print("[MediAssist] Model loaded!")
        print("[MediAssist] Features:", len(self.features))
        print("[MediAssist] Classes:", len(self.model.classes_))
        print("[MediAssist] Home-care entries:", len(HOME_CARE))
        print("[MediAssist] Bilingual engine ready!")

    # =====================================
    # TEXT UTILITIES
    # =====================================

    @staticmethod
    def normalize(value):

        text = str(value).lower()
        text = text.replace("_", " ").replace("-", " ")
        text = re.sub(r"[^\w\s']", " ", text)

        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def contains_phrase(text, phrase):

        return bool(
            re.search(
                r"(?<!\w)" + re.escape(phrase) + r"(?!\w)",
                text
            )
        )

    def has_any(self, text, phrases):

        return any(
            self.contains_phrase(text, self.normalize(p))
            for p in phrases
        )

    # =====================================
    # LANGUAGE DETECTION
    # =====================================

    def detect_language(self, message):

        text = self.normalize(message)
        words = set(text.split())

        if words & self.HINGLISH_MARKERS:
            return "hinglish"

        if re.search(
            r"\b(?:b+h+u+k+h*a+r+|b+u+k+h*a+r+)\b",
            text
        ):
            return "hinglish"

        if text in self.FOLLOWUP_WORDS:
            return self.response_language

        if re.fullmatch(
            r"(?:since |for )?\d+\s*"
            r"(?:days?|hours?|weeks?|months?)",
            text
        ):
            return self.response_language

        return "english"

    def say(self, english, hinglish):

        if self.response_language == "hinglish":
            return hinglish

        return english

    def localize_reply(self, reply):

        if self.response_language != "hinglish":
            return reply

        # Preserve detailed medical knowledge instead of
        # performing unreliable word-by-word translation.

        replacements = {
            "Current symptoms:": "Aapke current symptoms:",
            "Duration:": "Kitne time se:",
            "Cough type:": "Cough ka type:",
            "Progress:": "Abhi condition:",
            "Follow-up:": "Agla sawaal:",

            "How long have you had these symptoms?":
                "Ye symptoms kitne time se ho rahe hain?",

            "Is your cough dry or accompanied by mucus?":
                "Kya aapki cough dry hai ya mucus bhi aa raha hai?",

            "Are your symptoms improving, staying the same or getting worse?":
                "Symptoms better ho rahe hain, same hain ya badh rahe hain?",

            "Do you have any other symptoms? Please mention only symptoms you actually have.":
                "Kya aapko aur symptoms hain? Sirf wahi batayein jo actually ho rahe hain.",

            "Would you like general information about any of these symptoms?":
                "Kya aap in symptoms ke baare mein aur information chahenge?",

            DISCLAIMER:
                "Ye general educational information hai, "
                "medical diagnosis ya prescription nahi."
        }

        for english, hinglish in replacements.items():
            reply = reply.replace(english, hinglish)

        return reply

    def save_exchange(self, message, reply):

        reply = self.localize_reply(reply)

        self.memory.add_message("user", message)
        self.memory.add_message("assistant", reply)

        return reply

    def reset_context(self):

        self.current_symptoms = set()
        self.awaiting_followup = False
        self.last_question = None
        self.casual_context = None

        self.details = {
            "duration": None,
            "cough_type": None,
            "progress": None
        }

        # Language is deliberately not reset here.

    # =====================================
    # FLEXIBLE GREETING RECOGNITION
    # =====================================

    def is_greeting(self, text):

        greetings = {
            "hi", "hello", "hey", "hey there",
            "hello there", "good morning",
            "good afternoon", "good evening",
            "namaste", "namaskar"
        }

        if text in greetings:
            return True

        # Supports hiiii, hiiee, helloooo, heyyyy.
        patterns = [
            r"h+i+[ie]*",
            r"h+e+l+o+",
            r"h+e+y+",
            r"h+e+l+l+o+",
            r"h+e+y+\s+there"
        ]

        return any(
            re.fullmatch(pattern, text)
            for pattern in patterns
        )

    # =====================================
    # BASIC CONVERSATION
    # =====================================

    def answer_basic_conversation(self, text):

        t = text

        if self.is_greeting(t):

            self.casual_context = "greeting"

            return self.say(
                "Hello! How can I help you today?",
                "Namaste! Aaj main aapki kaise help kar sakta hoon?"
            )

        if self.has_any(t, [
            "how are you", "how r you", "how are u",
            "how's it going", "how is it going",
            "tum kaise ho", "aap kaise ho",
            "kaise ho", "kese ho", "kaisi ho"
        ]):

            self.casual_context = "how_are_you"

            return self.say(
                "I'm doing well, thank you! How are you?",
                "Main theek hoon, thank you! Aap kaise ho?"
            )

        if (
            self.casual_context == "how_are_you"
            and t in {
                "i am good", "i'm good", "im good",
                "i am fine", "i'm fine", "im fine",
                "good", "fine", "great", "very good",
                "doing well", "not bad", "i am okay",
                "i'm okay", "okay", "i am well",
                "main theek hoon", "mai thik hu",
                "mai theek hu", "main thik hu",
                "main accha hu", "main acha hu",
                "badhiya", "badhiya hu"
            }
        ):

            self.casual_context = None

            return self.say(
                "Glad to hear that! What would you like to talk about?",
                "Achha laga sunkar! Aap kis baare mein baat karna chahenge?"
            )

        if self.has_any(t, [
            "are you my friend", "can you be my friend",
            "will you be my friend", "are we friends",
            "can we be friends", "kya tum mere friend ho",
            "kya tum mere dost ho", "mere friend banoge",
            "mere dost banoge", "kya hum dost hain"
        ]):

            self.casual_context = "friendship"

            return self.say(
                "I can be your friendly AI assistant. "
                "I'm here to chat and help you learn. "
                "What's on your mind?",

                "Main aapka friendly AI assistant hoon. "
                "Hum baat kar sakte hain aur main learning "
                "mein help kar sakta hoon. Bataiye, kya baat hai?"
            )

        if self.has_any(t, [
            "what is your name", "what's your name",
            "whats your name", "your name", "who are you",
            "tumhara naam kya hai", "aapka naam kya hai",
            "tera naam kya hai", "naam kya hai",
            "tum kaun ho"
        ]):

            self.casual_context = "identity"

            return self.say(
                "My name is MediAssist AI. I'm a locally "
                "built educational health assistant.",

                "Mera naam MediAssist AI hai. Main ek locally "
                "built educational health assistant hoon."
            )

        if self.has_any(t, [
            "who created you", "who made you",
            "who developed you", "who built you",
            "tumhe kisne banaya", "tumko kisne banaya",
            "kisne banaya"
        ]):

            return self.say(
                "I was developed as a local AI health assistant "
                "using Python, a locally trained machine-learning "
                "model and a health knowledge base.",

                "Mujhe Python, locally trained ML model aur "
                "health knowledge base se develop kiya gaya hai."
            )

        if self.has_any(t, [
            "are you human", "are you a human",
            "are you real", "are you a robot",
            "are you an ai", "kya tum insan ho",
            "kya tum robot ho"
        ]):

            return self.say(
                "I'm an AI assistant, not a human. "
                "I answer supported questions using my local knowledge.",

                "Main human nahi, ek AI assistant hoon. "
                "Main apni local knowledge se supported questions "
                "ka answer deta hoon."
            )

        if self.has_any(t, [
            "what are you doing", "what r you doing",
            "what are u doing", "are you busy",
            "kya kar rahe ho", "kya kr rhe ho", "busy ho"
        ]):

            self.casual_context = "casual"

            return self.say(
                "I'm here and ready to help! "
                "What would you like to discuss?",

                "Main yahin hoon aur help ke liye ready hoon! "
                "Kya baat karni hai?"
            )

        if self.has_any(t, [
            "can we talk", "talk to me", "let's talk",
            "lets talk", "can i talk to you",
            "baat kar sakte hain", "mujhse baat karo",
            "baat karoge"
        ]):

            self.casual_context = "casual"

            return self.say(
                "Of course! What's on your mind?",
                "Bilkul! Bataiye, kya baat karni hai?"
            )

        if self.has_any(t, [
            "tell me a joke", "say a joke", "make me laugh",
            "do you know a joke", "joke sunao",
            "joke batao", "mazak sunao"
        ]):

            self.casual_context = "joke"

            return self.say(
                "Why did the computer visit the doctor? "
                "Because it had a virus!",

                "Computer doctor ke paas kyun gaya? "
                "Kyunki usmein virus tha!"
            )

        if self.casual_context == "joke" and t in {
            "another", "another one", "one more",
            "more", "tell me another", "again",
            "aur sunao", "ek aur", "aur ek"
        }:

            return self.say(
                "Why was the computer cold? "
                "It left its Windows open!",

                "Computer ko thand kyun lag rahi thi? "
                "Uski Windows khuli thi!"
            )

        if self.has_any(t, [
            "thank you", "thanks", "thank you so much",
            "thanks a lot", "thank u", "shukriya",
            "dhanyavad", "bahut thanks"
        ]):

            self.casual_context = None

            return self.say(
                "You're welcome!",
                "Aapka welcome hai!"
            )

        if t in {
            "bye", "goodbye", "see you",
            "see you later", "good night",
            "talk to you later", "alvida",
            "phir milte hain"
        }:

            self.casual_context = None

            return self.say(
                "Goodbye! Take care and have a wonderful day!",
                "Phir milte hain! Apna khayal rakhiye!"
            )

        if self.has_any(t, [
            "what can you do", "how can you help me",
            "what do you do", "tum kya kar sakte ho",
            "kya help kar sakte ho"
        ]):

            return self.say(
                "I can chat, provide general health education, "
                "discuss common symptoms and share supportive "
                "home-care guidance. I cannot diagnose medical conditions.",

                "Main chat kar sakta hoon, general health information "
                "aur common symptoms par guidance de sakta hoon. "
                "Main medical diagnosis nahi kar sakta."
            )

        if self.has_any(t, [
            "i am bored", "i'm bored", "im bored",
            "bore ho raha", "bore ho rahi"
        ]):

            return self.say(
                "We could chat, try a simple quiz or discuss "
                "a science topic. What sounds good?",

                "Hum chat kar sakte hain, ek simple quiz try "
                "kar sakte hain ya science topic discuss kar sakte hain."
            )

        if self.has_any(t, [
            "you are helpful", "you are nice",
            "you are smart", "good job", "well done",
            "tum ache ho", "bahut achhe ho"
        ]):

            return self.say(
                "Thank you! I'm glad my response was useful.",
                "Thank you! Achha laga ki mera answer useful tha."
            )

        return None

    # =====================================
    # NEGATION
    # =====================================

    def is_negated(self, text, match):

        before = text[max(0, match.start() - 45):match.start()]
        after = text[match.end():match.end() + 25]

        patterns = [
            r"\bno\s*$",
            r"\bwithout\s*$",
            r"\bnot having\s*$",
            r"\bdon't have\s*$",
            r"\bdo not have\s*$",
            r"\bi have no\s*$"
        ]

        if any(re.search(p, before) for p in patterns):
            return True

        return bool(
            re.match(
                r"\s+(?:nahi|nhi)\s+(?:hai|h)\b",
                after
            )
        )

    # =====================================
    # HEALTH TOPICS
    # =====================================

    def find_health_topic(self, text):

        candidates = [
            (self.normalize(key), key)
            for key in HOME_CARE
        ]

        candidates += [
            (self.normalize(alias), self.normalize(target))
            for alias, target in ALIASES.items()
        ]

        candidates.sort(
            key=lambda item: len(item[0]),
            reverse=True
        )

        for phrase, target in candidates:

            if not phrase:
                continue

            pattern = (
                r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
            )

            for match in re.finditer(pattern, text):

                if not self.is_negated(text, match):
                    if get_homecare(target) is not None:
                        return target

        return None

    def is_educational_question(self, text):

        phrases = [
            "what is", "what are", "tell me about",
            "explain", "information about", "about",
            "meaning of", "symptoms of", "causes of",
            "treatment for", "prevention of",
            "how to prevent", "how to manage",
            "how to treat", "how can i", "what can i",
            "what should i", "what do i do",
            "what to do", "home care", "home remedy",
            "home remedies", "remedies for",
            "remedy for", "care for", "cure",
            "curable", "is it dangerous",
            "is it serious", "kya hai", "kya karu",
            "kya karna chahiye", "kaise thik",
            "kaise theek", "upay", "ilaaj"
        ]

        return self.has_any(text, phrases)

    def is_cure_question(self, text):

        return self.has_any(text, [
            "can home remedies cure",
            "can home remedy cure",
            "home remedies cure",
            "home remedy cure",
            "cure with home remedies",
            "cured by home remedies",
            "can it be cured at home",
            "can i cure",
            "ghar par cure",
            "ghar par thik",
            "ghar par theek"
        ])

    def answer_cure_question(self, condition):

        entry = get_homecare(condition)

        if entry is None:
            return None

        serious = {
            "malaria", "typhoid", "dengue",
            "chikungunya", "pneumonia", "tuberculosis",
            "hepatitis a", "hepatitis b", "measles",
            "whooping cough", "strep throat",
            "urinary tract infection"
        }

        if condition in serious:

            return (
                "No. Home remedies should not be considered "
                "a cure for " + entry["title"] + ".\n\n"
                "This condition requires appropriate medical "
                "assessment and, when indicated, specific "
                "medical treatment.\n\n"
                "Rest and hydration may provide supportive "
                "care but cannot replace professional treatment."
                "\n\nWhen to seek medical help:\n"
                + entry["warning"]
                + "\n\n" + DISCLAIMER
            )

        return (
            "Home care may help manage some symptoms of "
            + entry["title"]
            + ", but it does not guarantee a cure. "
            "Treatment depends on the cause and severity.\n\n"
            + format_homecare(condition)
        )

    def answer_topic_question(self, text):

        if not self.is_educational_question(text):
            return None

        condition = self.find_health_topic(text)

        if condition is None:
            return None

        if self.is_cure_question(text):
            return self.answer_cure_question(condition)

        return format_homecare(condition)

    # =====================================
    # SYMPTOM EXTRACTION
    # =====================================

    def extract_symptoms(self, message):

        text = self.normalize(message)
        found = set()

        for feature in self.features:

            key = self.normalize(feature)

            alternatives = [key]
            alternatives.extend(self.aliases.get(key, []))

            for alternative in alternatives:

                alternative = self.normalize(alternative)

                if not alternative:
                    continue

                pattern = (
                    r"(?<!\w)"
                    + re.escape(alternative)
                    + r"(?!\w)"
                )

                for match in re.finditer(pattern, text):

                    if not self.is_negated(text, match):
                        found.add(feature)
                        break

                if feature in found:
                    break

            # Flexible recognition for fever spelling variations.
            if key == "fever" and feature not in found:

                fever_pattern = (
                    r"(?<!\w)"
                    r"(?:b+h+u+k+h*a+r+|b+u+k+h*a+r+)"
                    r"(?!\w)"
                )

                for match in re.finditer(fever_pattern, text):

                    if not self.is_negated(text, match):
                        found.add(feature)
                        break

        return sorted(found)

    # =====================================
    # LOCAL ML
    # =====================================

    def run_local_model(self):

        if not self.current_symptoms:
            return None

        vector = np.array(
            [[
                int(f in self.current_symptoms)
                for f in self.features
            ]],
            dtype=np.uint8
        )

        try:

            scores = self.model.predict_proba(vector)[0]
            index = int(np.argmax(scores))

            result = {
                "experimental_class":
                    str(self.model.classes_[index]),

                "model_score":
                    float(scores[index]),

                "symptom_count":
                    len(self.current_symptoms)
            }

            # Experimental result: not a medical diagnosis.
            print("[MediAssist] Internal ML:", result)

            return result

        except Exception as error:

            print("[MediAssist] ML error:", error)
            return None

    # =====================================
    # HOME CARE
    # =====================================

    def feature_to_care_key(self, feature):

        key = self.normalize(feature)

        if key in HOME_CARE:
            return key

        return ALIASES.get(key, key)

    def get_care_section(self, condition):

        entry = get_homecare(condition)

        if entry is None:
            return None

        care = "\n".join(
            "- " + item for item in entry["care"]
        )

        avoid = "\n".join(
            "- " + item for item in entry["avoid"]
        )

        return (
            entry["title"]
            + "\n\n" + entry["overview"]
            + "\n\nWhat you can do now:\n" + care
            + "\n\nWhat to avoid:\n" + avoid
            + "\n\nWhen to seek medical help:\n"
            + entry["warning"]
        )

    def get_combined_homecare(self, new_symptoms=None):

        sections = []
        used = set()

        selected = (
            new_symptoms
            if new_symptoms is not None
            else sorted(self.current_symptoms)
        )

        for feature in selected:

            key = self.feature_to_care_key(feature)

            key = {
                "abdominal pain": "stomach pain",
                "sleeplessness": "insomnia"
            }.get(key, key)

            if key in used:
                continue

            used.add(key)

            section = self.get_care_section(key)

            if section:
                sections.append(section)

        if not sections:

            return (
                "Different health conditions can share these "
                "symptoms. Rest if needed, monitor your symptoms "
                "and seek medical advice if they persist or worsen."
            )

        return "\n\n--------------------\n\n".join(sections)

    # =====================================
    # FOLLOW-UP DETAILS
    # =====================================

    def extract_duration(self, text):

        phrases = [
            "since yesterday", "yesterday",
            "since morning", "today",
            "kal se", "aaj se", "subah se"
        ]

        for phrase in phrases:

            if self.contains_phrase(text, phrase):
                return phrase

        match = re.search(
            r"\b(?:since |for |from )?"
            r"\d+\s*"
            r"(?:days?|hours?|weeks?|din|hafte|months?)"
            r"(?: ago| se)?\b",
            text
        )

        return match.group(0) if match else None

    def detect_cough_type(self, text):

        if self.has_any(text, [
            "dry", "dry cough",
            "sukhi khansi", "sukhi khaansi"
        ]):
            return "dry"

        if self.has_any(text, [
            "mucus", "phlegm", "balgam",
            "balgham", "wet cough"
        ]):
            return "with mucus"

        return None

    def detect_progress(self, text):

        if self.has_any(text, [
            "getting worse", "worse",
            "badhta ja raha", "zyada ho raha"
        ]):
            return "getting worse"

        if self.has_any(text, [
            "better", "improving", "kam ho raha"
        ]):
            return "improving"

        if self.has_any(text, [
            "same", "staying the same", "waisa hi hai"
        ]):
            return "staying the same"

        return None

    def update_details(self, text):

        duration = self.extract_duration(text)

        if duration:
            self.details["duration"] = duration

        if "cough" in self.current_symptoms:

            cough_type = self.detect_cough_type(text)

            if cough_type:
                self.details["cough_type"] = cough_type

        progress = self.detect_progress(text)

        if progress:
            self.details["progress"] = progress

    def context_summary(self):

        summary = (
            "Current symptoms: "
            + ", ".join(sorted(self.current_symptoms))
            + "."
        )

        if self.details["duration"]:
            summary += "\nDuration: " + self.details["duration"]

        if self.details["cough_type"]:
            summary += "\nCough type: " + self.details["cough_type"]

        if self.details["progress"]:
            summary += "\nProgress: " + self.details["progress"]

        return summary

    def next_question(self, analysis=None):

        if (
            "cough" in self.current_symptoms
            and not self.details["cough_type"]
        ):
            return "Is your cough dry or accompanied by mucus?"

        if not self.details["duration"]:
            return "How long have you had these symptoms?"

        if not self.details["progress"]:

            return (
                "Are your symptoms improving, "
                "staying the same or getting worse?"
            )

        if (
            analysis is not None
            and analysis["symptom_count"] < 3
        ):

            return (
                "Do you have any other symptoms? "
                "Please mention only symptoms you actually have."
            )

        return (
            "Would you like general information "
            "about any of these symptoms?"
        )

    # =====================================
    # GENERAL HEALTH QUESTIONS
    # =====================================

    def answer_general_question(self, text):

        if self.has_any(text, [
            "normal bp", "normal blood pressure",
            "bp range", "blood pressure range",
            "what is bp", "bp kitna hona chahiye"
        ]):

            return (
                "For most adults, normal blood pressure is below "
                "120/80 mmHg. Children and teenagers have different "
                "age-based standards. A single reading cannot "
                "establish a diagnosis."
            )

        if self.has_any(text, [
            "what is fever", "what is a fever",
            "normal body temperature", "normal temperature"
        ]):

            return (
                "Body temperature varies, but is often around "
                "37°C (98.6°F). A temperature of 38°C (100.4°F) "
                "or above is generally considered a fever."
            )

        if self.has_any(text, [
            "what is bmi", "bmi meaning", "body mass index"
        ]):

            return (
                "BMI means Body Mass Index. It is one screening "
                "measure, not a diagnosis. For teenagers, "
                "interpretation requires age-specific standards."
            )

        return None

    # =====================================
    # EMERGENCY FILTER
    # =====================================

    def detect_emergency(self, text):

        if self.has_any(text, [
            "what is", "what are the signs",
            "tell me about", "explain"
        ]):
            return False

        phrases = [
            "severe chest pain",
            "severe bleeding",
            "heavy bleeding",
            "unconscious",
            "cannot breathe",
            "can't breathe",
            "cant breathe",
            "difficulty breathing right now",
            "severe difficulty breathing",
            "saans nahi aa rahi",
            "saans nhi aa rhi",
            "seene mein tez dard",
            "fainted and not waking up"
        ]

        for phrase in phrases:

            pattern = (
                r"(?<!\w)"
                + re.escape(self.normalize(phrase))
                + r"(?!\w)"
            )

            for match in re.finditer(pattern, text):

                if not self.is_negated(text, match):
                    return True

        return False

    # =====================================
    # MAIN CHAT
    # =====================================

    def chat(self, user_message: str) -> str:

        message = str(user_message).strip()

        if not message:

            return self.say(
                "Please type your question.",
                "Apna sawaal type kijiye."
            )

        text = self.normalize(message)

        self.response_language = self.detect_language(message)

        # 1. Emergency

        if self.detect_emergency(text):

            self.awaiting_followup = False

            return self.save_exchange(
                message,
                self.say(
                    "These symptoms may require urgent medical "
                    "attention. Please contact local emergency "
                    "medical services or seek immediate medical help.",

                    "Ye symptoms urgent ho sakte hain. Kripya "
                    "local emergency medical services ko contact "
                    "karein ya turant medical help lein."
                )
            )

        # 2. Reset

        if text in {
            "clear", "reset", "new chat",
            "start again", "nayi chat"
        }:

            self.reset_context()

            return self.save_exchange(
                message,
                self.say(
                    "New discussion started. How can I help you?",
                    "Nayi discussion shuru ho gayi. "
                    "Main kaise help kar sakta hoon?"
                )
            )

        # 3. General health information

        general = self.answer_general_question(text)

        if general is not None:
            return self.save_exchange(message, general)

        # 4. Educational disease questions

        topic_answer = self.answer_topic_question(text)

        if topic_answer is not None:
            return self.save_exchange(message, topic_answer)

        # 5. Basic conversation

        casual_answer = self.answer_basic_conversation(text)

        if casual_answer is not None:
            return self.save_exchange(message, casual_answer)

        # 6. Previous symptom follow-up

        if self.awaiting_followup and self.current_symptoms:

            duration = self.extract_duration(text)
            cough_type = self.detect_cough_type(text)
            progress = self.detect_progress(text)

            if (
                duration
                or progress
                or (
                    cough_type
                    and "cough" in self.current_symptoms
                )
            ):

                self.update_details(text)

                analysis = self.run_local_model()
                question = self.next_question(analysis)

                self.last_question = question

                reply = self.context_summary()

                if (
                    cough_type == "dry"
                    and "cough" in self.current_symptoms
                ):

                    section = self.get_care_section("dry cough")

                    if section:
                        reply += "\n\n" + section

                elif (
                    cough_type == "with mucus"
                    and "cough" in self.current_symptoms
                ):

                    section = self.get_care_section("cough")

                    if section:
                        reply += "\n\n" + section

                else:

                    reply += "\n\n" + self.say(
                        "Continue the basic care discussed earlier "
                        "and monitor your symptoms.",

                        "Pehle batayi gayi basic care follow karein "
                        "aur symptoms monitor karein."
                    )

                reply += (
                    "\n\nFollow-up: " + question
                    + "\n\n"
                    + self.say(
                        "Seek medical advice if symptoms persist, "
                        "worsen or concern you.",

                        "Agar symptoms bane rahein, badhein ya "
                        "concern ho, toh medical advice lein."
                    )
                )

                return self.save_exchange(message, reply)

        # 7. New or additional symptoms

        symptoms = self.extract_symptoms(message)

        if symptoms:

            continuing = (
                self.awaiting_followup
                and self.has_any(text, [
                    "also", "along with", "as well",
                    "and i have", "aur", "bhi"
                ])
            )

            if not continuing:
                self.reset_context()

            previous = set(self.current_symptoms)

            self.current_symptoms.update(symptoms)
            self.awaiting_followup = True

            self.update_details(text)

            new_symptoms = self.current_symptoms - previous

            analysis = self.run_local_model()
            question = self.next_question(analysis)

            self.last_question = question

            if continuing and new_symptoms:

                care = self.get_combined_homecare(
                    sorted(new_symptoms)
                )

            else:

                care = self.get_combined_homecare()

            reply = (
                self.context_summary()
                + "\n\n" + care
                + "\n\nFollow-up: " + question
                + "\n\n" + DISCLAIMER
            )

            return self.save_exchange(message, reply)

        # 8. Existing local disease knowledge

        disease_answer = answer_disease_question(message)

        if disease_answer is not None:

            return self.save_exchange(
                message,
                disease_answer
            )

        # 9. Unknown question

        return self.save_exchange(
            message,
            self.say(
                UNKNOWN_REPLY,

                "Mere local knowledge base mein abhi is sawaal "
                "ke liye enough reliable information nahi hai. "
                "Kripya sawaal ko dobara likhein. Personal "
                "medical advice ke liye qualified healthcare "
                "professional se baat karein."
            )
        )


# =====================================
# DIRECT LOCAL TESTING
# =====================================

if __name__ == "__main__":

    bot = ChatEngine()

    print("\nMediAssist AI is ready!")
    print("Type exit to stop.\n")

    while True:

        user = input("You: ").strip()

        if user.lower() in {"exit", "quit"}:
            print("MediAssist: Goodbye!")
            break

        print("\nMediAssist:", bot.chat(user), "\n")
