
"""
MediAssist AI - Home Care Knowledge Base

Simple English educational health guidance.
No external API.
No automatic diagnosis.
No medicine prescriptions or dosage recommendations.

Home care does not replace professional medical treatment.
"""

import re


def normalize(text):
    text = str(text).lower()
    text = text.replace("_", " ").replace("-", " ")
    text = re.sub(r"[^\w\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def make_entry(
    title,
    overview,
    care,
    avoid,
    warning,
    followup
):
    return {
        "title": title,
        "overview": overview,
        "care": care,
        "avoid": avoid,
        "warning": warning,
        "followup": followup
    }


HOME_CARE = {

    # ----------------------------------------
    # COMMON SYMPTOMS
    # ----------------------------------------

    "fever": make_entry(
        "Fever",
        "Fever means your body temperature is higher than usual.",
        [
            "Take proper rest.",
            "Drink water and other fluids regularly.",
            "Wear comfortable, lightweight clothes.",
            "Check your temperature with a thermometer."
        ],
        [
            "Avoid heavy physical activity.",
            "Do not take antibiotics without medical advice."
        ],
        "Seek medical advice if fever persists, gets worse, "
        "or comes with concerning symptoms.",
        "How long have you had the fever?"
    ),

    "headache": make_entry(
        "Headache",
        "A headache is pain or discomfort in the head.",
        [
            "Rest in a quiet and comfortable place.",
            "Drink enough water.",
            "Take a break from screens.",
            "Try to maintain a regular sleep schedule."
        ],
        [
            "Avoid skipping meals.",
            "Avoid excessive screen time."
        ],
        "Get urgent help for a sudden extremely severe headache "
        "or a headache with confusion or new weakness.",
        "When did your headache start?"
    ),

    "cough": make_entry(
        "Cough",
        "Coughing helps clear the airways.",
        [
            "Drink warm fluids.",
            "Stay hydrated.",
            "Honey may soothe a cough for people older than one year.",
            "Rest and avoid smoke."
        ],
        [
            "Avoid smoking and second-hand smoke.",
            "Avoid unnecessary antibiotics."
        ],
        "Seek medical care if the cough is persistent or worsening. "
        "Breathing difficulty requires urgent assessment.",
        "Is your cough dry or accompanied by mucus?"
    ),

    "dry cough": make_entry(
        "Dry Cough",
        "A dry cough does not produce mucus.",
        [
            "Sip warm fluids.",
            "Honey may help soothe the throat if you are over one year old.",
            "Avoid dust and smoke.",
            "Rest your voice if your throat feels irritated."
        ],
        [
            "Avoid smoking.",
            "Avoid strong fumes."
        ],
        "Seek medical advice if the cough continues or worsens.",
        "How long have you had this dry cough?"
    ),

    "sore throat": make_entry(
        "Sore Throat",
        "A sore throat can cause pain or irritation when swallowing.",
        [
            "Drink comfortable warm or cool fluids.",
            "Rest your voice.",
            "Gargle with warm salt water if you can gargle safely.",
            "Avoid smoke."
        ],
        [
            "Avoid smoking.",
            "Avoid drinks that irritate your throat."
        ],
        "Get urgent medical help if you have difficulty breathing "
        "or cannot swallow fluids.",
        "Do you also have fever or cough?"
    ),

    "runny nose": make_entry(
        "Runny Nose",
        "A runny nose may happen with a cold or allergies.",
        [
            "Drink enough fluids.",
            "Rest.",
            "Use a suitable saline nasal spray if needed.",
            "Keep your surroundings clean."
        ],
        [
            "Avoid smoke.",
            "Avoid known allergy triggers."
        ],
        "Seek medical advice if symptoms persist or become severe.",
        "Do you also have sneezing or fever?"
    ),

    "nasal congestion": make_entry(
        "Blocked Nose",
        "Nasal congestion means your nose feels blocked.",
        [
            "Stay hydrated.",
            "Try a suitable saline nasal spray.",
            "Rest comfortably.",
            "Avoid smoke and dust."
        ],
        [
            "Avoid putting irritating substances inside your nose.",
            "Avoid smoke."
        ],
        "Seek medical advice if congestion is severe or persistent.",
        "How long has your nose been blocked?"
    ),

    "fatigue": make_entry(
        "Fatigue",
        "Fatigue means feeling unusually tired.",
        [
            "Get adequate sleep.",
            "Drink enough water.",
            "Eat regular balanced meals.",
            "Take comfortable breaks."
        ],
        [
            "Avoid pushing through severe tiredness.",
            "Avoid skipping meals."
        ],
        "Seek medical advice for persistent or unexplained fatigue.",
        "How long have you been feeling tired?"
    ),

    "dizziness": make_entry(
        "Dizziness",
        "Dizziness may make you feel lightheaded or unsteady.",
        [
            "Sit or lie down in a safe place.",
            "Stand up slowly.",
            "Drink water if you can swallow normally.",
            "Avoid sudden movements."
        ],
        [
            "Avoid driving while dizzy.",
            "Avoid climbing or working at heights."
        ],
        "Get urgent help if dizziness comes with fainting, "
        "chest pain, new weakness or difficulty speaking.",
        "Did the dizziness start suddenly?"
    ),

    "nausea": make_entry(
        "Nausea",
        "Nausea is the feeling that you may vomit.",
        [
            "Take small sips of water.",
            "Rest.",
            "Try small, simple meals when comfortable.",
            "Avoid strong food smells if they make you feel worse."
        ],
        [
            "Avoid large heavy meals.",
            "Avoid foods that trigger nausea."
        ],
        "Seek medical help if you cannot keep fluids down "
        "or develop signs of dehydration.",
        "Are you also vomiting?"
    ),

    "vomiting": make_entry(
        "Vomiting",
        "Vomiting can lead to loss of fluids.",
        [
            "Take small, frequent sips of fluids.",
            "Use oral rehydration solution when appropriate.",
            "Rest.",
            "Resume simple foods gradually when tolerated."
        ],
        [
            "Avoid large meals immediately after vomiting.",
            "Avoid dehydration."
        ],
        "Seek urgent medical help for severe dehydration, "
        "blood in vomit or severe abdominal pain.",
        "How many times have you vomited?"
    ),

    "diarrhea": make_entry(
        "Diarrhea",
        "Diarrhea means passing loose or watery stools.",
        [
            "Drink fluids regularly.",
            "Use properly prepared oral rehydration solution.",
            "Eat normal, tolerated foods.",
            "Wash your hands regularly."
        ],
        [
            "Avoid unsafe drinking water.",
            "Avoid self-medicating with antibiotics."
        ],
        "Seek medical care for dehydration, blood in stool "
        "or persistent symptoms.",
        "How long have you had loose stools?"
    ),

    "constipation": make_entry(
        "Constipation",
        "Constipation means difficulty passing stool.",
        [
            "Drink enough fluids.",
            "Eat fibre-containing foods.",
            "Maintain regular comfortable movement.",
            "Try to follow a regular toilet routine."
        ],
        [
            "Avoid repeatedly ignoring the urge to pass stool.",
            "Avoid unnecessary self-medication."
        ],
        "Seek medical care for severe pain, vomiting, "
        "blood in stool or persistent constipation.",
        "How long have you had constipation?"
    ),

    "stomach pain": make_entry(
        "Stomach Pain",
        "Stomach pain can have many different causes.",
        [
            "Rest comfortably.",
            "Drink fluids if tolerated.",
            "Notice where the pain occurs.",
            "Avoid foods that clearly make the discomfort worse."
        ],
        [
            "Avoid unnecessary medication.",
            "Do not ignore worsening pain."
        ],
        "Severe or worsening abdominal pain requires prompt "
        "medical assessment.",
        "Where exactly do you feel the pain?"
    ),

    "abdominal pain": make_entry(
        "Abdominal Pain",
        "Abdominal pain means discomfort in the belly area.",
        [
            "Rest comfortably.",
            "Stay hydrated if tolerated.",
            "Monitor whether the pain changes."
        ],
        [
            "Avoid ignoring persistent pain.",
            "Avoid unnecessary self-medication."
        ],
        "Seek urgent medical care for severe or worsening pain.",
        "Where is the pain located?"
    ),

    "insomnia": make_entry(
        "Sleep Difficulty",
        "Insomnia means difficulty falling asleep or staying asleep.",
        [
            "Maintain a regular sleep schedule.",
            "Keep your bedroom comfortable.",
            "Reduce screen use before bedtime.",
            "Try a relaxing bedtime routine."
        ],
        [
            "Avoid caffeine close to bedtime.",
            "Avoid using sleeping medicines without medical advice."
        ],
        "Seek professional advice if sleep problems continue "
        "or affect daily activities.",
        "Do you have difficulty falling asleep or staying asleep?"
    ),

    "sleeplessness": make_entry(
        "Sleeplessness",
        "Sleeplessness means having trouble getting enough sleep.",
        [
            "Follow a consistent bedtime.",
            "Keep your sleeping environment comfortable.",
            "Avoid late caffeine.",
            "Try relaxing before bedtime."
        ],
        [
            "Avoid irregular sleep schedules.",
            "Avoid self-prescribed sleeping pills."
        ],
        "Seek advice if the problem continues.",
        "How long have you had difficulty sleeping?"
    ),

    "high blood pressure": make_entry(
        "High Blood Pressure",
        "High blood pressure must be assessed using proper readings.",
        [
            "Record your blood pressure readings.",
            "Follow the treatment plan given by your clinician.",
            "Maintain regular physical activity as appropriate.",
            "Choose balanced meals."
        ],
        [
            "Do not stop prescribed medicines yourself.",
            "Do not rely on symptoms alone to judge blood pressure."
        ],
        "Very high readings with chest pain, breathing difficulty "
        "or new neurological symptoms require emergency assessment.",
        "Do you have a recent blood pressure reading?"
    ),

    # ----------------------------------------
    # COMMON INFECTIONS
    # ----------------------------------------

    "common cold": make_entry(
        "Common Cold",
        "The common cold is usually caused by a virus.",
        [
            "Rest.",
            "Drink enough fluids.",
            "Try saline nasal spray for congestion.",
            "Use honey for cough if older than one year."
        ],
        [
            "Avoid unnecessary antibiotics.",
            "Avoid smoking."
        ],
        "Seek medical advice if symptoms become severe or persistent.",
        "How many days have you had cold symptoms?"
    ),

    "influenza": make_entry(
        "Influenza (Flu)",
        "Influenza is a viral respiratory infection.",
        [
            "Rest.",
            "Stay hydrated.",
            "Monitor your symptoms.",
            "Avoid close contact with others while unwell."
        ],
        [
            "Avoid unnecessary antibiotics.",
            "Avoid heavy physical activity while ill."
        ],
        "Seek medical advice promptly if you are at higher risk "
        "or symptoms are worsening. Breathing difficulty needs urgent care.",
        "When did your symptoms begin?"
    ),

    "covid 19": make_entry(
        "COVID-19",
        "COVID-19 is a respiratory infection caused by a virus.",
        [
            "Rest and drink fluids.",
            "Follow current local public-health guidance.",
            "Avoid close contact with others while infectious.",
            "Monitor your symptoms."
        ],
        [
            "Avoid unnecessary antibiotics.",
            "Do not ignore worsening breathing symptoms."
        ],
        "Seek urgent help for difficulty breathing or chest pain.",
        "Have you taken a COVID-19 test?"
    ),

    "malaria": make_entry(
        "Malaria",
        "Malaria is a mosquito-borne infection that requires "
        "medical testing and specific treatment.",
        [
            "Arrange prompt medical assessment and testing.",
            "Rest while waiting for medical care.",
            "Drink fluids if tolerated.",
            "Follow the clinician's prescribed treatment."
        ],
        [
            "Do not try to cure malaria using home remedies.",
            "Do not delay testing.",
            "Do not self-prescribe antimalarial medicines."
        ],
        "Malaria can become serious. Confusion, breathing difficulty "
        "or marked weakness requires emergency care.",
        "Have you been tested for malaria?"
    ),

    "typhoid": make_entry(
        "Typhoid Fever",
        "Typhoid is a bacterial infection requiring professional "
        "assessment and appropriate treatment.",
        [
            "Seek medical evaluation.",
            "Drink safe water and maintain hydration.",
            "Rest.",
            "Follow prescribed treatment carefully.",
            "Wash hands regularly."
        ],
        [
            "Do not rely on home remedies as a cure.",
            "Avoid unsafe drinking water.",
            "Do not self-prescribe antibiotics."
        ],
        "Severe abdominal pain, confusion or significant worsening "
        "requires urgent medical attention.",
        "Has a clinician confirmed typhoid?"
    ),

    "dengue": make_entry(
        "Dengue",
        "Dengue is a mosquito-borne viral infection that needs "
        "careful monitoring.",
        [
            "Seek medical assessment.",
            "Rest.",
            "Maintain hydration.",
            "Follow your clinician's monitoring advice.",
            "Prevent mosquito bites."
        ],
        [
            "Do not rely on home remedies as a cure.",
            "Avoid aspirin and ibuprofen unless a clinician "
            "specifically advises otherwise."
        ],
        "Severe abdominal pain, persistent vomiting, bleeding "
        "or unusual drowsiness needs urgent assessment.",
        "Have you been tested for dengue?"
    ),

    "chikungunya": make_entry(
        "Chikungunya",
        "Chikungunya is a mosquito-borne viral infection.",
        [
            "Rest.",
            "Drink fluids.",
            "Seek medical assessment.",
            "Prevent further mosquito bites."
        ],
        [
            "Avoid self-prescribing medicines.",
            "Avoid assuming it is not dengue without assessment."
        ],
        "Seek medical care for persistent fever, severe pain "
        "or worsening symptoms.",
        "Have you received a medical diagnosis?"
    ),

    "pneumonia": make_entry(
        "Pneumonia",
        "Pneumonia is an infection affecting the lungs.",
        [
            "Seek medical assessment.",
            "Rest.",
            "Stay hydrated if tolerated.",
            "Follow the prescribed treatment plan."
        ],
        [
            "Do not rely only on home remedies.",
            "Avoid smoke."
        ],
        "Breathing difficulty, chest pain or confusion "
        "requires urgent medical care.",
        "Has a clinician diagnosed pneumonia?"
    ),

    "tuberculosis": make_entry(
        "Tuberculosis",
        "Tuberculosis is an infection that needs medical testing "
        "and a complete treatment course.",
        [
            "Seek professional testing.",
            "Follow prescribed treatment.",
            "Maintain adequate nutrition.",
            "Follow infection-prevention advice."
        ],
        [
            "Do not stop treatment without medical advice.",
            "Do not use home remedies instead of treatment."
        ],
        "Persistent cough, fever or unexplained weight changes "
        "should be medically assessed.",
        "Have you had a TB test?"
    ),

    "urinary tract infection": make_entry(
        "Urinary Tract Infection",
        "A UTI is an infection affecting part of the urinary system.",
        [
            "Seek medical advice for appropriate testing and treatment.",
            "Drink fluids normally unless advised otherwise.",
            "Avoid delaying urination."
        ],
        [
            "Do not self-prescribe antibiotics.",
            "Do not rely on home remedies to clear an infection."
        ],
        "Fever, back pain or vomiting with urinary symptoms "
        "requires prompt assessment.",
        "Do you have burning or pain while urinating?"
    ),

    "food poisoning": make_entry(
        "Food Poisoning",
        "Food poisoning can happen after consuming contaminated food.",
        [
            "Drink safe fluids.",
            "Use oral rehydration solution when appropriate.",
            "Rest.",
            "Resume tolerated foods gradually."
        ],
        [
            "Avoid unsafe food and water.",
            "Avoid unnecessary antibiotics."
        ],
        "Seek medical care for dehydration, blood in stool "
        "or persistent vomiting.",
        "Are you experiencing vomiting or diarrhea?"
    ),

    # ----------------------------------------
    # DIGESTIVE CONDITIONS
    # ----------------------------------------

    "acid reflux": make_entry(
        "Acid Reflux",
        "Acid reflux happens when stomach contents move back "
        "towards the food pipe.",
        [
            "Eat smaller meals.",
            "Avoid lying down immediately after eating.",
            "Notice which foods trigger symptoms.",
            "Maintain a comfortable meal schedule."
        ],
        [
            "Avoid personal food triggers.",
            "Avoid large meals before bedtime."
        ],
        "Persistent symptoms or difficulty swallowing "
        "should be medically assessed.",
        "Does the discomfort happen after eating?"
    ),

    "gastritis": make_entry(
        "Gastritis",
        "Gastritis means inflammation of the stomach lining.",
        [
            "Seek medical advice if symptoms continue.",
            "Eat foods you can comfortably tolerate.",
            "Avoid personal food triggers."
        ],
        [
            "Avoid unnecessary pain medicines.",
            "Avoid irritating foods if they worsen symptoms."
        ],
        "Severe pain or signs of gastrointestinal bleeding "
        "require urgent medical care.",
        "Do you have burning pain in your upper abdomen?"
    ),

    "indigestion": make_entry(
        "Indigestion",
        "Indigestion can cause discomfort after eating.",
        [
            "Try smaller meals.",
            "Eat slowly.",
            "Avoid lying down immediately after meals.",
            "Identify foods that trigger discomfort."
        ],
        [
            "Avoid overeating.",
            "Avoid personal food triggers."
        ],
        "Persistent or severe symptoms should be assessed.",
        "Does the discomfort usually start after meals?"
    ),

    "bloating": make_entry(
        "Bloating",
        "Bloating can make the abdomen feel full or swollen.",
        [
            "Eat slowly.",
            "Try smaller meals.",
            "Maintain comfortable regular movement.",
            "Notice any food triggers."
        ],
        [
            "Avoid overeating.",
            "Avoid foods that repeatedly trigger discomfort."
        ],
        "Persistent bloating with pain or other concerning "
        "symptoms needs medical assessment.",
        "Does bloating happen after particular foods?"
    ),

    "irritable bowel syndrome": make_entry(
        "Irritable Bowel Syndrome",
        "IBS is a digestive condition that can affect bowel habits.",
        [
            "Maintain regular meals.",
            "Track symptoms and food triggers.",
            "Drink adequate fluids.",
            "Discuss persistent symptoms with a clinician."
        ],
        [
            "Avoid unnecessary restrictive diets.",
            "Avoid self-prescribing medicines."
        ],
        "Blood in stool, persistent fever or unexplained "
        "symptoms need medical assessment.",
        "Are constipation or loose stools more common?"
    ),

    # ----------------------------------------
    # SKIN CONDITIONS
    # ----------------------------------------

    "acne": make_entry(
        "Acne",
        "Acne is a common skin condition.",
        [
            "Wash your face gently.",
            "Use suitable non-comedogenic skincare.",
            "Keep your hands away from spots.",
            "Seek advice for persistent or painful acne."
        ],
        [
            "Avoid squeezing pimples.",
            "Avoid harsh scrubbing."
        ],
        "Severe, painful or persistent acne may need professional care.",
        "Is your acne mild or causing significant discomfort?"
    ),

    "eczema": make_entry(
        "Eczema",
        "Eczema can cause dry, itchy and irritated skin.",
        [
            "Use a fragrance-free moisturizer.",
            "Wash with lukewarm water.",
            "Avoid known triggers.",
            "Keep fingernails clean and short."
        ],
        [
            "Avoid harsh soaps.",
            "Avoid scratching irritated skin."
        ],
        "Seek medical care if skin becomes painful, infected "
        "or symptoms worsen.",
        "Which area of your skin is affected?"
    ),

    "contact dermatitis": make_entry(
        "Contact Dermatitis",
        "Contact dermatitis is skin irritation after contact "
        "with a triggering substance.",
        [
            "Avoid the suspected trigger.",
            "Wash the affected area gently.",
            "Use a suitable fragrance-free moisturizer."
        ],
        [
            "Avoid harsh skincare products.",
            "Avoid repeated contact with the trigger."
        ],
        "Seek medical advice for severe or spreading irritation.",
        "Did symptoms start after using a new product?"
    ),

    "sunburn": make_entry(
        "Sunburn",
        "Sunburn is skin irritation caused by too much UV exposure.",
        [
            "Move out of direct sunlight.",
            "Cool the skin gently.",
            "Drink fluids.",
            "Use a suitable gentle moisturizer."
        ],
        [
            "Avoid further sun exposure.",
            "Avoid irritating the affected skin."
        ],
        "Severe sunburn or signs of dehydration require "
        "medical assessment.",
        "Which area is affected?"
    ),

    "dandruff": make_entry(
        "Dandruff",
        "Dandruff causes flakes on the scalp.",
        [
            "Wash hair regularly using a suitable shampoo.",
            "Avoid harsh scalp products.",
            "Seek advice if symptoms persist."
        ],
        [
            "Avoid aggressive scratching.",
            "Avoid irritating hair products."
        ],
        "Persistent redness, pain or scalp changes "
        "should be medically assessed.",
        "Is your scalp also itchy?"
    ),

    # ----------------------------------------
    # ALLERGIES AND RESPIRATORY CONDITIONS
    # ----------------------------------------

    "allergic rhinitis": make_entry(
        "Allergic Rhinitis",
        "Allergic rhinitis can cause sneezing, a runny nose "
        "and nasal irritation.",
        [
            "Avoid known allergy triggers.",
            "Keep your surroundings clean.",
            "Consider a suitable saline nasal spray.",
            "Discuss persistent symptoms with a clinician."
        ],
        [
            "Avoid smoke.",
            "Avoid known triggers where possible."
        ],
        "Seek urgent help for breathing difficulty or "
        "a severe allergic reaction.",
        "Do symptoms occur around dust or pollen?"
    ),

    "asthma": make_entry(
        "Asthma",
        "Asthma is a condition affecting the airways.",
        [
            "Follow your clinician's asthma action plan.",
            "Use prescribed treatment as directed.",
            "Avoid known triggers.",
            "Keep regular medical follow-ups."
        ],
        [
            "Do not stop prescribed controller treatment yourself.",
            "Avoid smoke and known triggers."
        ],
        "Severe breathing difficulty or symptoms not responding "
        "to prescribed rescue treatment require emergency help.",
        "Have you previously been diagnosed with asthma?"
    ),

    "sinusitis": make_entry(
        "Sinusitis",
        "Sinusitis means inflammation of the sinuses.",
        [
            "Rest.",
            "Stay hydrated.",
            "Use a suitable saline nasal spray.",
            "Seek medical advice if symptoms persist."
        ],
        [
            "Avoid smoke.",
            "Avoid unnecessary antibiotics."
        ],
        "Severe headache, swelling around the eye or "
        "worsening symptoms need prompt assessment.",
        "How long have you had nasal congestion?"
    ),

    # ----------------------------------------
    # LONG-TERM HEALTH CONDITIONS
    # ----------------------------------------

    "diabetes": make_entry(
        "Diabetes",
        "Diabetes is a condition affecting blood glucose regulation.",
        [
            "Follow your prescribed care plan.",
            "Monitor glucose as advised by your clinician.",
            "Eat regular balanced meals.",
            "Maintain appropriate physical activity."
        ],
        [
            "Do not stop prescribed medication yourself.",
            "Do not replace medical treatment with home remedies."
        ],
        "Confusion, fainting or severe illness in a person "
        "with diabetes requires urgent assessment.",
        "Are you asking about diabetes symptoms or general care?"
    ),

    "hypothyroidism": make_entry(
        "Hypothyroidism",
        "Hypothyroidism happens when the thyroid produces "
        "too little thyroid hormone.",
        [
            "Follow your prescribed treatment plan.",
            "Attend recommended thyroid tests.",
            "Maintain balanced meals and regular sleep."
        ],
        [
            "Do not change prescribed medicine yourself.",
            "Avoid unverified thyroid supplements."
        ],
        "Persistent or worsening symptoms need medical review.",
        "Have you had a thyroid blood test?"
    ),

    "hyperthyroidism": make_entry(
        "Hyperthyroidism",
        "Hyperthyroidism happens when the thyroid produces "
        "too much thyroid hormone.",
        [
            "Seek professional assessment.",
            "Follow prescribed treatment.",
            "Attend recommended monitoring appointments."
        ],
        [
            "Avoid self-prescribing thyroid medicines.",
            "Do not replace treatment with home remedies."
        ],
        "Severe palpitations, confusion or significant worsening "
        "requires urgent assessment.",
        "Has a clinician diagnosed hyperthyroidism?"
    ),

    "iron deficiency anemia": make_entry(
        "Iron Deficiency Anemia",
        "Iron deficiency anemia happens when the body does not "
        "have enough iron to make healthy red blood cells.",
        [
            "Seek medical assessment to confirm the cause.",
            "Include suitable iron-containing foods.",
            "Follow prescribed treatment if needed."
        ],
        [
            "Avoid taking iron supplements without appropriate advice.",
            "Do not ignore persistent fatigue."
        ],
        "Severe weakness, fainting or breathing difficulty "
        "needs prompt assessment.",
        "Have you had a hemoglobin or iron test?"
    ),

    "migraine": make_entry(
        "Migraine",
        "Migraine is a neurological condition that can cause "
        "recurrent headaches.",
        [
            "Rest in a quiet, comfortable room.",
            "Maintain hydration.",
            "Follow a regular sleep and meal schedule.",
            "Track possible triggers."
        ],
        [
            "Avoid known personal triggers.",
            "Avoid frequent unsupervised pain medicine use."
        ],
        "A sudden unusual severe headache or new neurological "
        "symptoms requires urgent assessment.",
        "Have you experienced similar headaches before?"
    ),

    "osteoarthritis": make_entry(
        "Osteoarthritis",
        "Osteoarthritis affects joints and may cause pain "
        "or stiffness.",
        [
            "Maintain comfortable movement.",
            "Try gentle low-impact activity as appropriate.",
            "Follow professional exercise advice.",
            "Allow rest when needed."
        ],
        [
            "Avoid activities that significantly worsen pain.",
            "Avoid prolonged complete inactivity."
        ],
        "A suddenly hot, swollen or very painful joint "
        "needs medical assessment.",
        "Which joint is affected?"
    ),

    "back pain": make_entry(
        "Back Pain",
        "Back pain can have several possible causes.",
        [
            "Keep gently active as tolerated.",
            "Avoid staying in one position too long.",
            "Try a comfortable warm or cool compress.",
            "Maintain comfortable posture."
        ],
        [
            "Avoid heavy lifting if it worsens pain.",
            "Avoid prolonged bed rest."
        ],
        "New weakness, loss of bladder or bowel control, "
        "or severe pain after an injury needs urgent care.",
        "Is the pain in your upper or lower back?"
    ),

    "muscle strain": make_entry(
        "Muscle Strain",
        "A muscle strain happens when a muscle is overstretched.",
        [
            "Rest from activities that worsen pain.",
            "Use a wrapped cold pack for short periods initially.",
            "Resume gentle movement as comfortable."
        ],
        [
            "Avoid forcing painful movement.",
            "Avoid placing ice directly on skin."
        ],
        "Severe pain or inability to use the affected area "
        "needs medical assessment.",
        "Which muscle or body area is affected?"
    ),

    # ----------------------------------------
    # EYE AND EAR CONDITIONS
    # ----------------------------------------

    "conjunctivitis": make_entry(
        "Conjunctivitis",
        "Conjunctivitis can cause red or irritated eyes.",
        [
            "Wash your hands regularly.",
            "Avoid touching or rubbing your eyes.",
            "Use a clean cool compress.",
            "Avoid sharing towels."
        ],
        [
            "Avoid sharing eye products.",
            "Avoid using unprescribed eye medicines."
        ],
        "Eye pain, light sensitivity or vision changes "
        "need prompt medical assessment.",
        "Is one eye affected or both?"
    ),

    "dry eyes": make_entry(
        "Dry Eyes",
        "Dry eyes may cause irritation or a gritty feeling.",
        [
            "Take regular screen breaks.",
            "Blink normally while using screens.",
            "Avoid direct airflow towards your eyes.",
            "Ask a pharmacist or clinician about suitable lubricating drops."
        ],
        [
            "Avoid rubbing your eyes.",
            "Avoid irritating eye products."
        ],
        "Pain or changes in vision require medical assessment.",
        "Do symptoms become worse during screen use?"
    ),

    "ear infection": make_entry(
        "Ear Infection",
        "An ear infection can cause ear discomfort and other symptoms.",
        [
            "Seek medical assessment when needed.",
            "Keep the ear dry if advised.",
            "Rest."
        ],
        [
            "Do not insert objects into your ear.",
            "Do not put unprescribed substances inside the ear."
        ],
        "Severe pain, swelling around the ear or hearing changes "
        "need medical attention.",
        "Do you have ear pain or hearing difficulty?"
    ),

    # ----------------------------------------
    # MOUTH AND DENTAL HEALTH
    # ----------------------------------------

    "mouth ulcer": make_entry(
        "Mouth Ulcer",
        "A mouth ulcer is a small sore inside the mouth.",
        [
            "Maintain gentle oral hygiene.",
            "Drink enough water.",
            "Choose foods that are comfortable to eat.",
            "Avoid irritating the sore."
        ],
        [
            "Avoid foods that worsen discomfort.",
            "Avoid touching the sore repeatedly."
        ],
        "Seek dental or medical advice if the ulcer does not heal "
        "or keeps returning.",
        "How long have you had the ulcer?"
    ),

    "toothache": make_entry(
        "Toothache",
        "Toothache can have several dental causes.",
        [
            "Arrange a dental appointment.",
            "Maintain gentle oral hygiene.",
            "Avoid chewing on the painful side if uncomfortable."
        ],
        [
            "Avoid putting chemicals or medicines directly on the tooth.",
            "Do not ignore worsening pain."
        ],
        "Facial swelling, fever or difficulty swallowing "
        "requires urgent dental or medical assessment.",
        "Which tooth or side is painful?"
    ),

    "gingivitis": make_entry(
        "Gingivitis",
        "Gingivitis means inflammation of the gums.",
        [
            "Brush gently twice daily.",
            "Clean between your teeth appropriately.",
            "Arrange a dental check-up."
        ],
        [
            "Avoid smoking.",
            "Avoid neglecting oral hygiene."
        ],
        "Persistent bleeding or swelling needs dental assessment.",
        "Do your gums bleed while brushing?"
    ),

    # ----------------------------------------
    # OTHER COMMON CONDITIONS
    # ----------------------------------------

    "dehydration": make_entry(
        "Dehydration",
        "Dehydration happens when the body loses more fluid "
        "than it takes in.",
        [
            "Drink fluids regularly if able.",
            "Use oral rehydration solution when appropriate.",
            "Rest in a comfortable environment."
        ],
        [
            "Avoid prolonged heat exposure.",
            "Avoid ignoring worsening symptoms."
        ],
        "Confusion, fainting or inability to drink "
        "requires urgent medical help.",
        "Are you able to drink and keep fluids down?"
    ),

    "heat exhaustion": make_entry(
        "Heat Exhaustion",
        "Heat exhaustion can happen after excessive heat exposure.",
        [
            "Move to a cooler place.",
            "Rest.",
            "Loosen tight clothing.",
            "Sip cool fluids if fully alert and able to swallow."
        ],
        [
            "Avoid further heat exposure.",
            "Avoid strenuous activity."
        ],
        "Confusion, collapse or severe symptoms require "
        "emergency help because heatstroke may be present.",
        "Are you now in a cooler place?"
    ),

    "motion sickness": make_entry(
        "Motion Sickness",
        "Motion sickness can cause nausea during travel.",
        [
            "Look towards a stable distant point.",
            "Get fresh air if possible.",
            "Take breaks during travel.",
            "Avoid heavy meals immediately before travelling."
        ],
        [
            "Avoid reading if it worsens symptoms.",
            "Avoid strong smells that trigger nausea."
        ],
        "Persistent vomiting or dehydration requires medical advice.",
        "Does this happen mainly during road travel?"
    ),

    "menstrual cramps": make_entry(
        "Menstrual Cramps",
        "Menstrual cramps can cause discomfort around menstruation.",
        [
            "Try a comfortably warm heating pad with a protective layer.",
            "Rest when needed.",
            "Maintain comfortable gentle movement.",
            "Stay hydrated."
        ],
        [
            "Avoid placing excessive heat directly on skin.",
            "Do not ignore unusually severe pain."
        ],
        "Severe, unusual or persistent pain should be "
        "medically assessed.",
        "Is this pain similar to your usual cramps?"
    ),

    "pcos": make_entry(
        "Polycystic Ovary Syndrome",
        "PCOS is a hormonal condition that needs individual "
        "medical assessment.",
        [
            "Attend recommended medical follow-ups.",
            "Maintain balanced regular meals.",
            "Choose enjoyable physical activity.",
            "Follow your clinician's treatment plan."
        ],
        [
            "Avoid unverified hormonal supplements.",
            "Do not self-prescribe treatment."
        ],
        "Persistent menstrual changes or other concerning "
        "symptoms should be assessed.",
        "Are you asking about PCOS symptoms or general care?"
    ),

    "anxiety": make_entry(
        "Anxiety",
        "Anxiety can involve worry, tension or feeling overwhelmed.",
        [
            "Try slow, comfortable breathing.",
            "Take a break in a calm place.",
            "Maintain regular sleep and meals.",
            "Talk with someone you trust."
        ],
        [
            "Avoid relying on unprescribed medicines.",
            "Avoid excessive caffeine if it worsens symptoms."
        ],
        "Seek support from a qualified professional if anxiety "
        "persists or interferes with daily life.",
        "Would you like simple relaxation techniques?"
    ),

    "stress": make_entry(
        "Stress",
        "Stress is a response to demanding situations.",
        [
            "Take regular breaks.",
            "Maintain a comfortable sleep routine.",
            "Try relaxing activities.",
            "Talk to a trusted person."
        ],
        [
            "Avoid ignoring persistent stress.",
            "Avoid excessive caffeine if it worsens symptoms."
        ],
        "Seek professional support if stress becomes difficult "
        "to manage or affects daily activities.",
        "Is your stress related to study, work or something else?"
    )
}


# ----------------------------------------
# ALTERNATIVE NAMES
# ----------------------------------------

ALIASES = {
    "bukhar": "fever",
    "bukhaar": "fever",
    "sir dard": "headache",
    "sar dard": "headache",
    "khansi": "cough",
    "khaansi": "cough",
    "sukhi khansi": "dry cough",
    "sukhi khaansi": "dry cough",
    "pet dard": "stomach pain",
    "pet mein dard": "stomach pain",
    "kabz": "constipation",
    "kabj": "constipation",
    "ulti": "vomiting",
    "dast": "diarrhea",
    "loose motion": "diarrhea",
    "neend nahi aa rahi": "insomnia",
    "neend nhi aa rhi": "insomnia",
    "high bp": "high blood pressure",
    "bp high": "high blood pressure",
    "sugar disease": "diabetes",
    "flu": "influenza",
    "cold": "common cold",
    "covid": "covid 19",
    "covid 19": "covid 19",
    "uti": "urinary tract infection",
    "ibs": "irritable bowel syndrome",
    "thyroid low": "hypothyroidism",
    "thyroid high": "hyperthyroidism",
    "pcod": "pcos"
}


# ----------------------------------------
# RESPONSE FORMATTING
# ----------------------------------------

def get_homecare(condition):

    key = normalize(condition)

    key = ALIASES.get(key, key)

    return HOME_CARE.get(key)


def format_homecare(condition):

    entry = get_homecare(condition)

    if entry is None:
        return None

    care_text = "\n".join(
        "- " + item
        for item in entry["care"]
    )

    avoid_text = "\n".join(
        "- " + item
        for item in entry["avoid"]
    )

    reply = (
        entry["title"]
        + "\n\n"
        + entry["overview"]
        + "\n\nWhat you can do now:\n"
        + care_text
        + "\n\nWhat to avoid:\n"
        + avoid_text
        + "\n\nWhen to seek medical help:\n"
        + entry["warning"]
        + "\n\nFollow-up: "
        + entry["followup"]
        + "\n\nThis is general educational information, "
        "not a medical diagnosis or prescription."
    )

    return reply


# ----------------------------------------
# SEARCH CONDITIONS IN USER MESSAGE
# ----------------------------------------

def find_homecare(message):

    text = normalize(message)

    # Match longer phrases first.
    possible_names = sorted(
        list(HOME_CARE.keys()) + list(ALIASES.keys()),
        key=len,
        reverse=True
    )

    for name in possible_names:

        normalized_name = normalize(name)

        if re.search(
            r"(?<!\w)"
            + re.escape(normalized_name)
            + r"(?!\w)",
            text
        ):

            condition = ALIASES.get(
                normalized_name,
                normalized_name
            )

            return format_homecare(condition)

    return None


# ----------------------------------------
# TEST
# ----------------------------------------

if __name__ == "__main__":

    print("MediAssist Home Care Knowledge Base")
    print("Available entries:", len(HOME_CARE))

    print("\nExample response:\n")
    print(format_homecare("fever"))
