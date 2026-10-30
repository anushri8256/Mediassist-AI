

"""
MediAssist AI - Local Disease Knowledge Base
Educational information only.
No external API.
"""

import re


DISEASES = {
    "diabetes": {
        "aliases": ["diabetes", "sugar disease", "diabetic"],
        "symptoms": (
            "Frequent urination, increased thirst, increased hunger, "
            "fatigue, blurry vision and unexplained weight loss."
        ),
        "information": (
            "Diabetes is a condition involving high blood glucose. "
            "Some people have few or no noticeable symptoms."
        ),
        "follow_up": "Would you like to know how diabetes is tested?"
    },

    "covid-19": {
        "aliases": ["covid", "covid 19", "covid-19", "coronavirus"],
        "symptoms": (
            "Fever, cough, sore throat, fatigue, headache, "
            "body aches, congestion and sometimes loss of taste or smell."
        ),
        "information": (
            "COVID-19 is a contagious viral illness. "
            "Symptoms alone cannot confirm whether someone has COVID-19."
        ),
        "follow_up": "Would you like to know about COVID-19 testing?"
    },

    "malaria": {
        "aliases": ["malaria", "malarial fever"],
        "symptoms": (
            "Fever, chills, headache, muscle aches, tiredness, "
            "nausea and sometimes vomiting."
        ),
        "information": (
            "Malaria is caused by parasites transmitted mainly through "
            "infected mosquito bites. Suspected malaria needs prompt "
            "medical assessment and appropriate testing."
        ),
        "follow_up": "Would you like to know how malaria is diagnosed?"
    },

    "typhoid": {
        "aliases": ["typhoid", "typhoid fever", "enteric fever"],
        "symptoms": (
            "Prolonged fever, weakness, headache, stomach pain, "
            "loss of appetite, constipation or diarrhoea."
        ),
        "information": (
            "Typhoid is a bacterial infection commonly transmitted "
            "through contaminated food or water. Medical assessment "
            "and appropriate testing are important."
        ),
        "follow_up": "Would you like to know how typhoid is diagnosed?"
    }
}


def answer_disease_question(message):
    text = message.lower().replace("-", " ")

    question_words = [
        "what", "symptom", "sign", "tell me",
        "explain", "about", "meaning", "kya",
        "batao", "information", "diagnos", "test"
    ]

    # Only answer explicit disease-information questions.
    # Do not infer a disease from someone's symptoms.
    if not any(word in text for word in question_words):
        return None

    for disease, details in DISEASES.items():
        for alias in details["aliases"]:
            alias = alias.replace("-", " ")

            if re.search(
                r"(?<!\w)" + re.escape(alias) + r"(?!\w)",
                text
            ):
                return (
                    f"{disease.upper()}\n\n"
                    f"Information: {details['information']}\n\n"
                    f"Common symptoms: {details['symptoms']}\n\n"
                    f"{details['follow_up']}\n\n"
                    "Important: These symptoms can overlap with "
                    "other conditions. This information cannot "
                    "confirm a diagnosis. Consult a qualified "
                    "healthcare professional for assessment."
                )

    return None
