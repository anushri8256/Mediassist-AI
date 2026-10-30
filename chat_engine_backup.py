
"""
MediAssist AI - Local Self-Trained Chat Engine

Features:
- Self-trained Random Forest model
- Local disease knowledge base
- English and Hinglish symptom recognition
- General health Q&A
- Basic conversation memory
- No external AI APIs

Educational information only.
Not a medical diagnosis system.
"""

from pathlib import Path
import re

import joblib
import pandas as pd

from memory import ConversationMemory
from disease_knowledge import answer_disease_question


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "trained_model"


class ChatEngine:

    def __init__(self, model_name=None):

        print("[MediAssist] Loading local trained model...")

        self.model = joblib.load(
            MODEL_DIR / "model.pkl"
        )

        self.features = list(
            joblib.load(
                MODEL_DIR / "feature_columns.pkl"
            )
        )

        self.memory = ConversationMemory(max_history=4)

        self.current_symptoms = set()
        self.awaiting_followup = False

        # Alternative English and Hinglish symptom expressions
        self.aliases = {
            "headache": [
                "headache", "head pain", "pain in my head",
                "my head hurts", "head is hurting",
                "sir dard", "sar dard", "sir mein dard",
                "sar mein dard"
            ],

            "fever": [
                "fever", "bukhar", "bukhaar",
                "high temperature"
            ],

            "cough": [
                "cough", "coughing",
                "khansi", "khaansi"
            ],

            "nausea": [
                "nausea", "nauseous",
                "ji machlana", "jee machlana"
            ],

            "vomiting": [
                "vomiting", "vomit", "throwing up",
                "ulti"
            ],

            "dizziness": [
                "dizziness", "dizzy",
                "chakkar", "chakkar aa rahe"
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
                "pet dard", "pet mein dard"
            ],

            "abdominal pain": [
                "abdominal pain", "stomachache",
                "stomach pain", "pet dard",
                "pet mein dard"
            ],

            "insomnia": [
                "insomnia", "can't sleep",
                "cannot sleep", "cant sleep",
                "difficulty sleeping",
                "neend nahi aa rahi"
            ],

            "sleeplessness": [
                "sleeplessness", "can't sleep",
                "cannot sleep", "difficulty sleeping",
                "neend nahi aa rahi"
            ],

            "high blood pressure": [
                "high bp", "bp high",
                "high blood pressure", "hypertension"
            ],

            "shortness of breath": [
                "shortness of breath",
                "difficulty breathing",
                "breathing difficulty",
                "saans lene mein dikkat"
            ]
        }

        # Educational symptom guidance
        self.guidance = {
            "fever": (
                "Fever can occur with different illnesses. "
                "Rest, drink fluids, and monitor your symptoms.",
                "How long have you had the fever?"
            ),

            "headache": (
                "Headaches can have several causes. "
                "Resting somewhere comfortable and staying hydrated "
                "may help with some common headaches.",
                "When did your headache start?"
            ),

            "cough": (
                "Cough can occur for different reasons. "
                "Stay hydrated and monitor your symptoms.",
                "Is your cough dry or accompanied by mucus?"
            ),

            "stomach pain": (
                "Stomach pain can have several possible causes.",
                "Where exactly do you feel the pain?"
            ),

            "abdominal pain": (
                "Abdominal pain can have several possible causes.",
                "Where exactly do you feel the pain?"
            ),

            "constipation": (
                "Adequate fluids, regular movement, and "
                "fibre-containing foods may help with constipation.",
                "How long have you had constipation?"
            ),

            "insomnia": (
                "A consistent sleep schedule and a comfortable "
                "sleep environment may help with sleep difficulties.",
                "Are you having trouble falling asleep or staying asleep?"
            ),

            "sleeplessness": (
                "A consistent sleep schedule may help with "
                "some sleep difficulties.",
                "How long have you had difficulty sleeping?"
            ),

            "high blood pressure": (
                "Blood pressure cannot be assessed from symptoms alone. "
                "A properly taken reading is important.",
                "Do you have a recent blood pressure reading?"
            )
        }

        print("[MediAssist] ML model loaded successfully!")
        print("[MediAssist] Training features:", len(self.features))

    # --------------------------------------------------
    # TEXT UTILITIES
    # --------------------------------------------------

    @staticmethod
    def normalize(text):
        text = str(text).lower()
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
            self.contains_phrase(
                text,
                self.normalize(phrase)
            )
            for phrase in phrases
        )

    def save_exchange(self, message, reply):
        self.memory.add_message("user", message)
        self.memory.add_message("assistant", reply)
        return reply

    # --------------------------------------------------
    # GENERAL HEALTH QUESTIONS
    # --------------------------------------------------

    def answer_general_question(self, text):

        if self.has_any(text, [
            "normal bp", "normal blood pressure",
            "bp range", "blood pressure range",
            "what is bp", "bp kitna hona chahiye"
        ]):
            return (
                "For most adults, normal blood pressure is "
                "below 120/80 mmHg. A single reading does not "
                "establish a diagnosis. Children and teenagers "
                "have different age-based standards.\n\n"
                "Are you asking about a particular BP reading?"
            )

        if self.has_any(text, [
            "what is fever", "what is a fever",
            "normal body temperature",
            "normal temperature"
        ]):
            return (
                "Normal body temperature varies, but is often "
                "around 37°C (98.6°F). A temperature of 38°C "
                "(100.4°F) or above is generally considered a fever."
            )

        if self.has_any(text, [
            "what is bmi", "bmi meaning",
            "body mass index"
        ]):
            return (
                "BMI stands for Body Mass Index. It relates "
                "weight to height and is one screening measure, "
                "not a diagnosis. For children and teenagers, "
                "interpretation requires age- and sex-specific "
                "growth standards."
            )

        if self.has_any(text, [
            "what is dehydration", "dehydration meaning"
        ]):
            return (
                "Dehydration occurs when the body loses more "
                "fluid than it takes in. Symptoms may include "
                "thirst, dry mouth, and dizziness. Severe "
                "dehydration requires prompt medical assessment."
            )

        if self.has_any(text, [
            "who are you", "what can you do",
            "tell me about yourself"
        ]):
            return (
                "I am MediAssist AI, a locally built educational "
                "health assistant. I use a self-trained ML model "
                "and a local health knowledge base. "
                "I cannot provide medical diagnoses."
            )

        return None

    # --------------------------------------------------
    # SYMPTOM EXTRACTION
    # --------------------------------------------------

    def extract_symptoms(self, message):

        text = self.normalize(message)
        found = set()

        for feature in self.features:

            key = self.normalize(feature)

            alternatives = [key]
            alternatives.extend(
                self.aliases.get(key, [])
            )

            for alternative in alternatives:

                alternative = self.normalize(alternative)

                if not alternative:
                    continue

                if not self.contains_phrase(text, alternative):
                    continue

                negatives = [
                    "no " + alternative,
                    "not having " + alternative,
                    "don't have " + alternative,
                    "do not have " + alternative,
                    "without " + alternative
                ]

                if any(
                    self.contains_phrase(text, item)
                    for item in negatives
                ):
                    continue

                found.add(feature)
                break

        return sorted(found)

    # --------------------------------------------------
    # SELF-TRAINED MODEL INFERENCE
    # --------------------------------------------------

    def run_local_model(self):

        if not self.current_symptoms:
            return

        input_data = {
            feature: [int(feature in self.current_symptoms)]
            for feature in self.features
        }

        input_df = pd.DataFrame(
            input_data,
            columns=self.features
        )

        try:
            prediction = self.model.predict(input_df)[0]

            # Experimental prediction is not shown to users.
            # Current accuracy is insufficient for diagnosis.
            print(
                "[MediAssist] Internal experimental prediction:",
                prediction
            )

        except Exception as error:
            print("[MediAssist] ML inference error:", error)

    # --------------------------------------------------
    # MAIN CHAT FUNCTION
    # --------------------------------------------------

    def chat(self, user_message: str) -> str:

        message = str(user_message).strip()

        if not message:
            return "Please type your health question."

        text = self.normalize(message)

        # 1. Emergency check

        emergency_terms = [
            "severe chest pain",
            "unconscious",
            "severe bleeding",
            "cannot breathe",
            "can't breathe",
            "saans nahi aa rahi",
            "seene mein tez dard"
        ]

        if self.has_any(text, emergency_terms):
            self.awaiting_followup = False

            return self.save_exchange(
                message,
                "These symptoms may require urgent medical attention. "
                "Please contact local emergency medical services "
                "or seek immediate medical help."
            )

        # 2. Greetings

        if text in ["hi", "hii", "hello", "hey", "namaste"]:
            return self.save_exchange(
                message,
                "Hello! I am MediAssist AI. "
                "You can ask basic health questions or describe "
                "your symptoms in English or Hinglish."
            )

        if text in ["thanks", "thank you", "shukriya"]:
            return self.save_exchange(
                message,
                "You're welcome! Take care."
            )

        # 3. Reset

        if text in ["clear", "reset", "new chat", "start again"]:
            self.current_symptoms.clear()
            self.awaiting_followup = False

            return self.save_exchange(
                message,
                "Okay! We can start a new discussion. "
                "What would you like to ask?"
            )

        # 4. Local disease knowledge base

        disease_answer = answer_disease_question(message)

        if disease_answer is not None:
            self.awaiting_followup = False
            self.current_symptoms.clear()

            return self.save_exchange(
                message,
                disease_answer
            )

        # 5. General health questions

        general_answer = self.answer_general_question(text)

        if general_answer is not None:
            self.awaiting_followup = False
            self.current_symptoms.clear()

            return self.save_exchange(
                message,
                general_answer
            )

        # 6. Symptom recognition

        symptoms = self.extract_symptoms(message)

        if symptoms:

            continuing = self.has_any(text, [
                "also", "along with", "as well",
                "and i have", "aur", "bhi"
            ])

            if not continuing:
                self.current_symptoms.clear()

            self.current_symptoms.update(symptoms)
            self.awaiting_followup = True

            # Run our self-trained ML model internally.
            self.run_local_model()

            symptom_text = ", ".join(
                sorted(self.current_symptoms)
            )

            advice = (
                "Different health conditions can share these symptoms."
            )

            follow_up = (
                "How long have you been experiencing these symptoms?"
            )

            for feature in symptoms:

                key = self.normalize(feature)

                if key in self.guidance:
                    advice, follow_up = self.guidance[key]
                    break

            reply = (
                f"Recognized symptoms: {symptom_text}.\n\n"
                f"{advice}\n\n"
                f"Follow-up: {follow_up}\n\n"
                "This is educational information, not a medical "
                "diagnosis. Consult a qualified healthcare "
                "professional if symptoms persist, worsen, "
                "or concern you."
            )

            return self.save_exchange(message, reply)

        # 7. Short follow-up messages

        followup_phrases = [
            "yes", "no", "haan", "nahi",
            "today", "yesterday",
            "since yesterday", "since morning",
            "kal se", "aaj se",
            "better", "worse", "same",
            "improving", "getting worse",
            "dry", "with mucus"
        ]

        duration_pattern = re.fullmatch(
            r"(?:from |since |for )?"
            r"\d+\s*"
            r"(?:day|days|hour|hours|week|weeks|"
            r"din|hafte|month|months)"
            r"(?: ago| se)?",
            text
        )

        is_short_followup = (
            self.has_any(text, followup_phrases)
            or bool(duration_pattern)
        )

        if (
            self.awaiting_followup
            and self.current_symptoms
            and is_short_followup
            and len(text.split()) <= 6
        ):

            symptom_text = ", ".join(
                sorted(self.current_symptoms)
            )

            reply = (
                f"Thanks for the additional information. "
                f"We were discussing: {symptom_text}.\n\n"
                "Are your symptoms improving, staying the same, "
                "or getting worse?\n\n"
                "If symptoms persist, worsen, or concern you, "
                "please consult a qualified healthcare professional."
            )

            return self.save_exchange(message, reply)

        # 8. Unknown question

        self.awaiting_followup = False

        reply = (
            "I understand your question, but my current local "
            "knowledge base does not have a reliable answer for it.\n\n"
            "You can rephrase your question or ask about common "
            "symptoms and diseases such as fever, headache, "
            "diabetes, COVID-19, malaria, or typhoid. "
            "For personal medical advice, consult a qualified "
            "healthcare professional."
        )

        return self.save_exchange(message, reply)
