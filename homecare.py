
"""
MediAssist AI - Home Care Knowledge Base
Version 2.0

100+ common health topics.
Simple English educational guidance.
No external API.
No automatic diagnosis.
No prescriptions or medicine dosages.

IMPORTANT:
Home care is supportive. It does not replace medical treatment.
"""

import re


DISCLAIMER = (
    "This is general educational information, "
    "not a medical diagnosis or prescription."
)

GENERAL_WARNING = (
    "Seek medical advice if symptoms persist, worsen, "
    "or concern you."
)

URGENT_WARNING = (
    "Seek urgent medical help for severe symptoms, "
    "breathing difficulty, confusion, fainting, or rapid worsening."
)


def normalize(text):
    text = str(text).lower()
    text = text.replace("_", " ").replace("-", " ")
    text = re.sub(r"[^\w\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def make_entry(title, overview, care, avoid, warning, followup):
    return {
        "title": title,
        "overview": overview,
        "care": care,
        "avoid": avoid,
        "warning": warning,
        "followup": followup
    }


HOME_CARE = {}


def add(key, title, overview, care, avoid=None,
        warning=None, followup=None):

    HOME_CARE[normalize(key)] = make_entry(
        title,
        overview,
        care,
        avoid or ["Avoid unnecessary self-medication."],
        warning or GENERAL_WARNING,
        followup or "How long have you had these symptoms?"
    )


# ==================================================
# 1. COMMON SYMPTOMS
# ==================================================

add(
    "fever", "Fever",
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
    "Seek medical advice if fever persists, worsens, or comes "
    "with concerning symptoms.",
    "How long have you had the fever?"
)

add(
    "headache", "Headache",
    "A headache is pain or discomfort in the head.",
    [
        "Rest in a quiet and comfortable place.",
        "Drink enough water.",
        "Take breaks from screens.",
        "Maintain regular sleep and meals."
    ],
    ["Avoid skipping meals.", "Avoid excessive screen time."],
    "A sudden extremely severe headache or headache with "
    "new weakness or confusion needs urgent medical care.",
    "When did your headache start?"
)

add(
    "cough", "Cough",
    "Coughing helps clear the airways.",
    [
        "Drink warm fluids.",
        "Stay hydrated.",
        "Honey may soothe coughing for people older than one year.",
        "Rest and avoid smoke."
    ],
    ["Avoid smoking.", "Avoid unnecessary antibiotics."],
    "Breathing difficulty needs urgent assessment. "
    "Seek advice for persistent or worsening cough.",
    "Is your cough dry or accompanied by mucus?"
)

add(
    "dry cough", "Dry Cough",
    "A dry cough does not produce mucus.",
    [
        "Sip comfortable warm fluids.",
        "Honey may soothe the throat if you are older than one year.",
        "Avoid dust and smoke.",
        "Rest your voice if your throat feels irritated."
    ],
    ["Avoid smoke.", "Avoid strong fumes."],
    "Seek medical advice if coughing continues or worsens.",
    "How long have you had this dry cough?"
)

add(
    "sore throat", "Sore Throat",
    "A sore throat causes irritation or discomfort in the throat.",
    [
        "Drink comfortable warm or cool fluids.",
        "Rest your voice.",
        "Gargle with warm salt water if you can gargle safely.",
        "Avoid smoke."
    ],
    ["Avoid smoking.", "Avoid foods that irritate your throat."],
    "Difficulty breathing or swallowing fluids requires urgent care.",
    "Do you also have fever or cough?"
)

add(
    "runny nose", "Runny Nose",
    "A runny nose can occur with infections or allergies.",
    [
        "Drink enough fluids.",
        "Rest.",
        "Consider a suitable saline nasal spray.",
        "Keep your surroundings clean."
    ],
    ["Avoid smoke.", "Avoid known allergy triggers."],
    followup="Do you also have sneezing or fever?"
)

add(
    "nasal congestion", "Blocked Nose",
    "Nasal congestion means your nose feels blocked.",
    [
        "Stay hydrated.",
        "Consider a suitable saline nasal spray.",
        "Rest comfortably.",
        "Avoid dust and smoke."
    ],
    ["Do not put irritating substances inside your nose."],
    followup="How long has your nose been blocked?"
)

add(
    "fatigue", "Fatigue",
    "Fatigue means feeling unusually tired.",
    [
        "Get adequate sleep.",
        "Drink enough water.",
        "Eat regular balanced meals.",
        "Take comfortable breaks."
    ],
    ["Avoid pushing through severe tiredness."],
    "Persistent or unexplained fatigue needs medical assessment.",
    "How long have you been feeling tired?"
)

add(
    "dizziness", "Dizziness",
    "Dizziness can make you feel lightheaded or unsteady.",
    [
        "Sit or lie down safely.",
        "Stand up slowly.",
        "Drink water if you can swallow normally.",
        "Avoid sudden movements."
    ],
    ["Avoid driving while dizzy.", "Avoid climbing."],
    "Dizziness with fainting, chest pain, difficulty speaking "
    "or new weakness requires urgent medical care.",
    "Did the dizziness start suddenly?"
)

add(
    "nausea", "Nausea",
    "Nausea means feeling like you may vomit.",
    [
        "Take small sips of water.",
        "Rest.",
        "Try small simple meals when comfortable.",
        "Avoid strong food smells if they worsen nausea."
    ],
    ["Avoid large heavy meals."],
    "Seek help if you cannot keep fluids down or become dehydrated.",
    "Are you also vomiting?"
)

add(
    "vomiting", "Vomiting",
    "Vomiting can cause loss of body fluids.",
    [
        "Take small frequent sips of fluids.",
        "Use oral rehydration solution when appropriate.",
        "Rest.",
        "Resume simple foods gradually when tolerated."
    ],
    ["Avoid large meals immediately after vomiting."],
    "Blood in vomit, severe abdominal pain or dehydration "
    "requires urgent medical assessment.",
    "Are you able to keep fluids down?"
)

add(
    "diarrhea", "Diarrhea",
    "Diarrhea means passing loose or watery stools.",
    [
        "Drink safe fluids regularly.",
        "Use properly prepared oral rehydration solution.",
        "Eat normal foods that you tolerate.",
        "Wash your hands regularly."
    ],
    ["Avoid unsafe drinking water.", "Avoid self-prescribed antibiotics."],
    "Blood in stool, dehydration or persistent symptoms "
    "need medical assessment.",
    "How long have you had loose stools?"
)

add(
    "constipation", "Constipation",
    "Constipation means difficulty passing stool.",
    [
        "Drink enough fluids.",
        "Eat fibre-containing foods.",
        "Maintain regular comfortable movement.",
        "Follow a regular toilet routine."
    ],
    ["Avoid repeatedly ignoring the urge to pass stool."],
    "Severe pain, vomiting, bleeding or persistent constipation "
    "needs medical assessment.",
    "How long have you had constipation?"
)

add(
    "stomach pain", "Stomach Pain",
    "Stomach pain can have several possible causes.",
    [
        "Rest comfortably.",
        "Drink fluids if tolerated.",
        "Notice where the pain occurs.",
        "Avoid foods that clearly worsen discomfort."
    ],
    ["Avoid unnecessary medication.", "Do not ignore worsening pain."],
    "Severe or worsening abdominal pain requires prompt assessment.",
    "Where exactly do you feel the pain?"
)

add(
    "abdominal pain", "Abdominal Pain",
    "Abdominal pain means discomfort in the belly area.",
    [
        "Rest comfortably.",
        "Stay hydrated if tolerated.",
        "Monitor whether the pain changes."
    ],
    ["Do not ignore persistent or worsening pain."],
    "Severe or worsening pain requires urgent assessment.",
    "Where is the pain located?"
)

add(
    "insomnia", "Sleep Difficulty",
    "Insomnia means difficulty falling asleep or staying asleep.",
    [
        "Maintain a regular sleep schedule.",
        "Keep your bedroom comfortable.",
        "Reduce screen use before bedtime.",
        "Try a relaxing bedtime routine."
    ],
    ["Avoid caffeine close to bedtime.",
     "Avoid sleeping medicines without medical advice."],
    "Seek advice if sleep problems continue or affect daily life.",
    "Is it difficult to fall asleep or stay asleep?"
)

add(
    "sleeplessness", "Sleeplessness",
    "Sleeplessness means having trouble getting enough sleep.",
    [
        "Follow a consistent bedtime.",
        "Keep your sleeping environment comfortable.",
        "Avoid late caffeine.",
        "Try relaxing before bedtime."
    ],
    ["Avoid irregular sleep schedules."],
    followup="How long have you had difficulty sleeping?"
)

add(
    "high blood pressure", "High Blood Pressure",
    "High blood pressure must be assessed using proper readings.",
    [
        "Record your blood pressure readings.",
        "Follow your clinician's treatment plan.",
        "Choose balanced meals.",
        "Maintain suitable regular activity."
    ],
    ["Do not stop prescribed medicines yourself.",
     "Do not judge blood pressure using symptoms alone."],
    "Very high readings with chest pain, breathing difficulty "
    "or new neurological symptoms require emergency assessment.",
    "Do you have a recent blood pressure reading?"
)

add(
    "shortness of breath", "Shortness of Breath",
    "Breathing difficulty can have several causes.",
    [
        "Stop strenuous activity.",
        "Sit in a comfortable position.",
        "Seek prompt medical assessment."
    ],
    ["Do not ignore new breathing difficulty."],
    "Severe, sudden or worsening breathing difficulty "
    "requires emergency medical help.",
    "Is your breathing difficulty happening right now?"
)

add(
    "dehydration", "Dehydration",
    "Dehydration occurs when the body loses more fluid than it takes in.",
    [
        "Drink fluids regularly if able.",
        "Use oral rehydration solution when appropriate.",
        "Rest in a comfortable environment."
    ],
    ["Avoid prolonged heat exposure."],
    "Confusion, fainting or inability to drink requires urgent care.",
    "Are you able to drink and keep fluids down?"
)


# ==================================================
# 2. INFECTIONS AND COMMUNICABLE DISEASES
# ==================================================

add(
    "common cold", "Common Cold",
    "The common cold is usually caused by a virus.",
    [
        "Rest.",
        "Drink enough fluids.",
        "Try saline nasal spray for congestion.",
        "Honey may soothe cough if older than one year."
    ],
    ["Avoid unnecessary antibiotics.", "Avoid smoking."],
    followup="How many days have you had cold symptoms?"
)

add(
    "influenza", "Influenza",
    "Influenza is a viral respiratory infection.",
    [
        "Rest and stay hydrated.",
        "Monitor your symptoms.",
        "Avoid close contact with others while infectious.",
        "Seek medical advice promptly if you are at higher risk."
    ],
    ["Avoid unnecessary antibiotics."],
    "Breathing difficulty or significant worsening needs urgent care.",
    "When did your symptoms begin?"
)

add(
    "covid 19", "COVID-19",
    "COVID-19 is a viral respiratory infection.",
    [
        "Rest and drink fluids.",
        "Follow current local public-health guidance.",
        "Avoid close contact with others while infectious.",
        "Monitor your symptoms."
    ],
    ["Avoid unnecessary antibiotics."],
    "Breathing difficulty or chest pain requires urgent assessment.",
    "Have you taken a COVID-19 test?"
)

add(
    "malaria", "Malaria",
    "Malaria is a mosquito-borne infection requiring testing "
    "and specific medical treatment.",
    [
        "Arrange prompt medical testing.",
        "Rest while waiting for medical care.",
        "Drink fluids if tolerated.",
        "Follow the clinician's prescribed treatment."
    ],
    [
        "Do not try to cure malaria with home remedies.",
        "Do not delay testing.",
        "Do not self-prescribe antimalarial medicines."
    ],
    "Malaria can become serious. Confusion, breathing difficulty "
    "or marked weakness requires emergency care.",
    "Have you been tested for malaria?"
)

add(
    "typhoid", "Typhoid Fever",
    "Typhoid is a bacterial infection requiring professional treatment.",
    [
        "Seek medical evaluation.",
        "Drink safe water and maintain hydration.",
        "Rest.",
        "Follow prescribed treatment.",
        "Wash hands regularly."
    ],
    ["Do not rely on home remedies as a cure.",
     "Do not self-prescribe antibiotics."],
    "Severe abdominal pain, confusion or significant worsening "
    "requires urgent medical attention.",
    "Has a clinician confirmed typhoid?"
)

add(
    "dengue", "Dengue",
    "Dengue is a mosquito-borne viral infection requiring careful monitoring.",
    [
        "Seek medical assessment.",
        "Rest.",
        "Maintain hydration.",
        "Follow your clinician's monitoring advice.",
        "Prevent mosquito bites."
    ],
    [
        "Do not rely on home remedies as a cure.",
        "Avoid aspirin and ibuprofen unless a clinician advises otherwise."
    ],
    "Severe abdominal pain, persistent vomiting, bleeding "
    "or unusual drowsiness needs urgent assessment.",
    "Have you been tested for dengue?"
)

add(
    "chikungunya", "Chikungunya",
    "Chikungunya is a mosquito-borne viral infection.",
    [
        "Rest and drink fluids.",
        "Seek medical assessment.",
        "Prevent mosquito bites.",
        "Follow your clinician's treatment advice."
    ],
    ["Avoid self-prescribing medicines.",
     "Do not assume dengue has been excluded without assessment."],
    followup="Have you received a medical diagnosis?"
)

add(
    "pneumonia", "Pneumonia",
    "Pneumonia is an infection affecting the lungs.",
    [
        "Seek medical assessment.",
        "Rest.",
        "Stay hydrated if tolerated.",
        "Follow the prescribed treatment plan."
    ],
    ["Do not rely only on home remedies.", "Avoid smoke."],
    "Breathing difficulty, chest pain or confusion requires urgent care.",
    "Has a clinician diagnosed pneumonia?"
)

add(
    "tuberculosis", "Tuberculosis",
    "Tuberculosis is an infection requiring medical testing "
    "and a complete treatment course.",
    [
        "Seek professional testing.",
        "Follow prescribed treatment.",
        "Maintain adequate nutrition.",
        "Follow infection-prevention advice."
    ],
    ["Do not stop treatment without medical advice.",
     "Do not replace treatment with home remedies."],
    "Persistent cough, fever or unexplained weight changes "
    "should be medically assessed.",
    "Have you had a TB test?"
)

add(
    "urinary tract infection", "Urinary Tract Infection",
    "A UTI affects part of the urinary system.",
    [
        "Seek medical advice for testing and treatment.",
        "Drink fluids normally unless advised otherwise.",
        "Avoid delaying urination."
    ],
    ["Do not self-prescribe antibiotics.",
     "Do not rely on home remedies to clear an infection."],
    "Fever, back pain or vomiting with urinary symptoms "
    "requires prompt assessment.",
    "Do you have burning while urinating?"
)

add(
    "food poisoning", "Food Poisoning",
    "Food poisoning can occur after consuming contaminated food.",
    [
        "Drink safe fluids.",
        "Use oral rehydration solution when appropriate.",
        "Rest.",
        "Resume tolerated foods gradually."
    ],
    ["Avoid unsafe food and water.", "Avoid unnecessary antibiotics."],
    "Dehydration, blood in stool or persistent vomiting needs care.",
    "Are you experiencing vomiting or diarrhea?"
)

add(
    "chickenpox", "Chickenpox",
    "Chickenpox is a contagious viral infection.",
    [
        "Rest and drink enough fluids.",
        "Keep skin clean.",
        "Keep fingernails short.",
        "Avoid contact with others until all spots have crusted."
    ],
    ["Avoid scratching.", "Avoid close contact with vulnerable people."],
    "Seek medical advice for severe symptoms or higher-risk patients.",
    "Has chickenpox been confirmed?"
)

add(
    "measles", "Measles",
    "Measles is a highly contagious viral infection.",
    [
        "Seek medical advice promptly.",
        "Rest and stay hydrated.",
        "Avoid contact with other people.",
        "Follow public-health instructions."
    ],
    ["Avoid attending school while infectious.",
     "Do not rely on home remedies as a cure."],
    "Breathing difficulty or significant worsening needs urgent care.",
    "Have you contacted a healthcare professional?"
)

add(
    "mumps", "Mumps",
    "Mumps is a viral infection that can cause swollen salivary glands.",
    [
        "Rest.",
        "Drink fluids.",
        "Choose comfortable foods.",
        "Follow medical advice about avoiding contact with others."
    ],
    ["Avoid sharing drinking glasses."],
    followup="Do you have swelling near your jaw?"
)

add(
    "rubella", "Rubella",
    "Rubella is a contagious viral infection.",
    [
        "Seek medical advice.",
        "Rest and maintain hydration.",
        "Avoid close contact with others.",
        "Follow public-health advice."
    ],
    ["Avoid contact with pregnant people.",
     "Do not assume every rash is rubella."],
    "Medical assessment is important because rubella "
    "can be dangerous during pregnancy.",
    "Has a clinician assessed the rash?"
)

add(
    "hand foot and mouth disease", "Hand, Foot and Mouth Disease",
    "This is a contagious viral illness.",
    [
        "Rest.",
        "Drink fluids regularly.",
        "Choose comfortable foods.",
        "Wash hands and frequently touched surfaces."
    ],
    ["Avoid sharing utensils.",
     "Avoid foods that irritate mouth sores."],
    "Seek care if drinking becomes difficult or dehydration develops.",
    "Are mouth sores making drinking difficult?"
)

add(
    "viral gastroenteritis", "Viral Gastroenteritis",
    "This viral infection affects the stomach and intestines.",
    [
        "Drink fluids regularly.",
        "Use oral rehydration solution when appropriate.",
        "Rest.",
        "Wash hands carefully."
    ],
    ["Avoid preparing food for others while infectious.",
     "Avoid unnecessary antibiotics."],
    "Dehydration or persistent symptoms require assessment.",
    "Are you able to keep fluids down?"
)

add(
    "strep throat", "Strep Throat",
    "Strep throat is a bacterial throat infection.",
    [
        "Seek medical testing and appropriate treatment.",
        "Drink comfortable fluids.",
        "Rest.",
        "Follow prescribed treatment."
    ],
    ["Avoid self-prescribing antibiotics.",
     "Avoid sharing drinking glasses."],
    "Difficulty breathing or swallowing requires urgent assessment.",
    "Have you had a throat test?"
)

add(
    "tonsillitis", "Tonsillitis",
    "Tonsillitis means inflammation of the tonsils.",
    [
        "Drink enough fluids.",
        "Rest.",
        "Choose comfortable foods.",
        "Seek medical advice if symptoms persist."
    ],
    ["Avoid smoking.", "Avoid unnecessary antibiotics."],
    "Difficulty breathing or swallowing requires urgent assessment.",
    "Do you also have fever?"
)

add(
    "bronchitis", "Bronchitis",
    "Bronchitis means inflammation of the bronchial airways.",
    [
        "Rest.",
        "Drink enough fluids.",
        "Avoid smoke.",
        "Seek assessment if symptoms persist."
    ],
    ["Avoid smoking.", "Avoid unnecessary antibiotics."],
    "Breathing difficulty or chest pain needs prompt medical attention.",
    "How long have you been coughing?"
)

add(
    "whooping cough", "Whooping Cough",
    "Whooping cough is a contagious bacterial respiratory infection.",
    [
        "Seek medical assessment promptly.",
        "Follow prescribed treatment.",
        "Maintain hydration.",
        "Follow infection-prevention instructions."
    ],
    ["Avoid close contact with infants.",
     "Do not rely on home remedies as treatment."],
    "Breathing difficulty requires urgent care, especially in infants.",
    "Have you been assessed by a clinician?"
)

add(
    "hepatitis a", "Hepatitis A",
    "Hepatitis A is a viral infection affecting the liver.",
    [
        "Seek medical assessment.",
        "Rest as needed.",
        "Maintain hydration and nutrition.",
        "Wash hands carefully."
    ],
    ["Avoid unverified liver remedies.",
     "Follow medical advice about preventing transmission."],
    "Confusion or severe worsening requires urgent assessment.",
    "Has hepatitis A been confirmed?"
)

add(
    "hepatitis b", "Hepatitis B",
    "Hepatitis B is a viral infection affecting the liver.",
    [
        "Seek specialist medical assessment.",
        "Follow recommended monitoring and treatment.",
        "Discuss prevention for close contacts."
    ],
    ["Avoid sharing personal items that may contain blood.",
     "Avoid unverified liver remedies."],
    "Worsening jaundice or severe illness needs medical attention.",
    "Are you asking about prevention or general care?"
)


# ==================================================
# 3. DIGESTIVE HEALTH
# ==================================================

add(
    "acid reflux", "Acid Reflux",
    "Acid reflux occurs when stomach contents move towards the food pipe.",
    [
        "Eat smaller meals.",
        "Avoid lying down immediately after eating.",
        "Notice personal food triggers.",
        "Maintain a regular meal schedule."
    ],
    ["Avoid large meals before bedtime."],
    "Persistent symptoms or difficulty swallowing needs assessment.",
    "Does discomfort happen after eating?"
)

add(
    "gastritis", "Gastritis",
    "Gastritis means inflammation of the stomach lining.",
    [
        "Seek medical advice if symptoms continue.",
        "Eat foods you comfortably tolerate.",
        "Avoid personal food triggers."
    ],
    ["Avoid unnecessary pain medicines."],
    "Severe pain or signs of gastrointestinal bleeding need urgent care.",
    "Do you have burning pain in your upper abdomen?"
)

add(
    "indigestion", "Indigestion",
    "Indigestion can cause discomfort after eating.",
    [
        "Try smaller meals.",
        "Eat slowly.",
        "Avoid lying down immediately after meals.",
        "Identify food triggers."
    ],
    ["Avoid overeating."],
    followup="Does discomfort usually start after meals?"
)

add(
    "bloating", "Bloating",
    "Bloating can make the abdomen feel full or swollen.",
    [
        "Eat slowly.",
        "Try smaller meals.",
        "Maintain comfortable regular movement.",
        "Notice food triggers."
    ],
    ["Avoid overeating."],
    followup="Does bloating happen after particular foods?"
)

add(
    "irritable bowel syndrome", "Irritable Bowel Syndrome",
    "IBS is a digestive condition that affects bowel habits.",
    [
        "Maintain regular meals.",
        "Track symptoms and food triggers.",
        "Drink adequate fluids.",
        "Discuss persistent symptoms with a clinician."
    ],
    ["Avoid unnecessary restrictive diets."],
    "Blood in stool, persistent fever or unexplained symptoms "
    "need medical assessment.",
    "Are constipation or loose stools more common?"
)

add(
    "lactose intolerance", "Lactose Intolerance",
    "Lactose intolerance can cause discomfort after dairy consumption.",
    [
        "Notice whether dairy triggers symptoms.",
        "Discuss suitable alternatives with a clinician or dietitian.",
        "Maintain balanced nutrition."
    ],
    ["Avoid unnecessary broad food restrictions."],
    followup="Do symptoms appear after milk or dairy foods?"
)

add(
    "celiac disease", "Celiac Disease",
    "Celiac disease is an immune condition triggered by gluten.",
    [
        "Seek appropriate medical testing.",
        "Follow a clinician-guided gluten-free diet after diagnosis.",
        "Discuss nutritional needs with a dietitian."
    ],
    ["Do not start a gluten-free diet before diagnostic testing "
     "unless medically advised."],
    "Persistent digestive symptoms need medical assessment.",
    "Has celiac disease been medically confirmed?"
)

add(
    "hemorrhoids", "Hemorrhoids",
    "Hemorrhoids are swollen blood vessels near the anus or rectum.",
    [
        "Drink enough fluids.",
        "Include fibre-containing foods.",
        "Avoid straining during bowel movements.",
        "Maintain gentle hygiene."
    ],
    ["Avoid prolonged straining.",
     "Do not assume all rectal bleeding is hemorrhoids."],
    "Rectal bleeding or severe pain needs assessment.",
    "Are you experiencing pain or bleeding?"
)

add(
    "anal fissure", "Anal Fissure",
    "An anal fissure is a small tear near the anal opening.",
    [
        "Maintain hydration.",
        "Include fibre-containing foods.",
        "Avoid straining.",
        "Seek advice if symptoms continue."
    ],
    ["Avoid forcing bowel movements."],
    "Persistent bleeding or severe pain needs assessment.",
    "Does discomfort occur during bowel movements?"
)

add(
    "kidney stones", "Kidney Stones",
    "Kidney stones are hard deposits in the urinary system.",
    [
        "Seek medical assessment.",
        "Drink fluids normally if able and not medically restricted.",
        "Follow your clinician's treatment advice."
    ],
    ["Avoid delaying assessment for severe pain.",
     "Avoid unverified remedies."],
    "Fever, inability to urinate or severe pain requires urgent care.",
    "Has a kidney stone been confirmed?"
)

add(
    "gallstones", "Gallstones",
    "Gallstones are deposits inside the gallbladder.",
    [
        "Seek medical assessment.",
        "Notice foods that trigger discomfort.",
        "Follow professional dietary and treatment advice."
    ],
    ["Avoid unverified gallbladder cleanses."],
    "Severe abdominal pain, fever or yellowing of the eyes "
    "requires urgent assessment.",
    "Has an ultrasound confirmed gallstones?"
)

add(
    "fatty liver disease", "Fatty Liver Disease",
    "Fatty liver disease means excess fat has accumulated in the liver.",
    [
        "Attend recommended medical follow-ups.",
        "Maintain regular balanced meals.",
        "Choose suitable enjoyable physical activity.",
        "Follow your clinician's care plan."
    ],
    ["Avoid unverified liver detox products."],
    "New jaundice or significant abdominal symptoms need assessment.",
    "Was fatty liver found during a medical test?"
)

add(
    "jaundice", "Jaundice",
    "Jaundice causes yellowing of the skin or eyes and can have serious causes.",
    [
        "Arrange prompt medical assessment.",
        "Drink fluids normally if tolerated.",
        "Follow the clinician's advice."
    ],
    ["Avoid unverified liver remedies.",
     "Do not assume jaundice has a harmless cause."],
    "Jaundice needs medical assessment. Confusion or severe illness "
    "requires emergency care.",
    "Have you noticed yellowing of your eyes?"
)


# ==================================================
# 4. SKIN CONDITIONS
# ==================================================

add(
    "acne", "Acne",
    "Acne is a common skin condition.",
    [
        "Wash your face gently.",
        "Use suitable non-comedogenic skincare.",
        "Avoid picking spots.",
        "Seek advice for persistent or painful acne."
    ],
    ["Avoid squeezing pimples.", "Avoid harsh scrubbing."],
    followup="Is your acne causing pain or discomfort?"
)

add(
    "eczema", "Eczema",
    "Eczema can cause dry, itchy and irritated skin.",
    [
        "Use a fragrance-free moisturizer.",
        "Wash with lukewarm water.",
        "Avoid known triggers.",
        "Keep fingernails clean and short."
    ],
    ["Avoid harsh soaps.", "Avoid scratching."],
    "Painful, infected or worsening skin needs medical assessment.",
    "Which area is affected?"
)

add(
    "contact dermatitis", "Contact Dermatitis",
    "Contact dermatitis is irritation after touching a triggering substance.",
    [
        "Avoid the suspected trigger.",
        "Wash the area gently.",
        "Use a suitable fragrance-free moisturizer."
    ],
    ["Avoid harsh skincare products."],
    followup="Did symptoms begin after using a new product?"
)

add(
    "sunburn", "Sunburn",
    "Sunburn is skin irritation caused by excessive UV exposure.",
    [
        "Move out of direct sunlight.",
        "Cool the skin gently.",
        "Drink fluids.",
        "Use a suitable gentle moisturizer."
    ],
    ["Avoid further sun exposure.",
     "Avoid irritating the affected skin."],
    "Severe sunburn or dehydration requires medical assessment.",
    "Which area is affected?"
)

add(
    "dandruff", "Dandruff",
    "Dandruff causes flakes on the scalp.",
    [
        "Wash hair regularly with a suitable shampoo.",
        "Avoid harsh scalp products.",
        "Seek advice if symptoms persist."
    ],
    ["Avoid aggressive scratching."],
    followup="Is your scalp also itchy?"
)

add(
    "ringworm", "Ringworm",
    "Ringworm is a fungal skin infection, not a worm infection.",
    [
        "Keep affected skin clean and dry.",
        "Avoid sharing towels.",
        "Seek advice about appropriate antifungal treatment.",
        "Wash clothing and towels regularly."
    ],
    ["Avoid scratching.",
     "Avoid steroid creams without medical advice."],
    "Widespread, persistent or scalp infection needs assessment.",
    "Which body area is affected?"
)

add(
    "athletes foot", "Athlete's Foot",
    "Athlete's foot is a fungal infection affecting the feet.",
    [
        "Keep feet clean and dry.",
        "Change socks regularly.",
        "Allow footwear to dry.",
        "Seek advice about antifungal treatment."
    ],
    ["Avoid sharing towels.",
     "Avoid walking barefoot in shared wet areas."],
    followup="Is the irritation between your toes?"
)

add(
    "jock itch", "Jock Itch",
    "Jock itch is a fungal infection affecting the groin.",
    [
        "Keep the area clean and dry.",
        "Wear comfortable breathable clothing.",
        "Seek advice about antifungal treatment."
    ],
    ["Avoid scratching.",
     "Avoid unprescribed steroid creams."],
    followup="How long has the irritation been present?"
)

add(
    "scabies", "Scabies",
    "Scabies is a contagious skin condition caused by mites.",
    [
        "Seek medical assessment and treatment.",
        "Follow advice for treating close contacts.",
        "Wash relevant bedding and clothing as advised."
    ],
    ["Do not rely on home remedies as a cure."],
    "Infected skin or persistent symptoms need medical care.",
    "Is itching worse at night?"
)

add(
    "hives", "Hives",
    "Hives are raised itchy patches on the skin.",
    [
        "Avoid known triggers.",
        "Use a comfortably cool compress.",
        "Wear loose clothing.",
        "Seek advice if symptoms continue."
    ],
    ["Avoid scratching."],
    "Tongue or throat swelling or breathing difficulty is an emergency.",
    "Did the rash appear after a new food or product?"
)

add(
    "psoriasis", "Psoriasis",
    "Psoriasis is a long-term inflammatory skin condition.",
    [
        "Moisturize regularly.",
        "Use gentle skincare.",
        "Follow prescribed treatment.",
        "Attend recommended follow-ups."
    ],
    ["Avoid harsh scrubbing.",
     "Do not stop prescribed treatment yourself."],
    "Severe symptoms or new joint pain needs assessment.",
    "Which area is affected?"
)

add(
    "boils", "Boils",
    "A boil is a painful skin infection.",
    [
        "Keep the area clean.",
        "Apply a comfortably warm clean compress.",
        "Cover draining skin with a clean dressing.",
        "Wash hands regularly."
    ],
    ["Do not squeeze or pierce a boil.",
     "Avoid sharing towels."],
    "Fever, spreading redness or a boil on the face "
    "needs medical assessment.",
    "Where is the boil located?"
)

add(
    "insect bite", "Insect Bite",
    "An insect bite may cause local itching or irritation.",
    [
        "Wash the area gently.",
        "Use a wrapped cool compress.",
        "Avoid scratching.",
        "Monitor for worsening symptoms."
    ],
    ["Avoid applying irritating substances."],
    "Breathing difficulty or tongue or throat swelling "
    "requires emergency care.",
    "Is there swelling around the bite?"
)


# ==================================================
# 5. RESPIRATORY AND ALLERGY CONDITIONS
# ==================================================

add(
    "allergic rhinitis", "Allergic Rhinitis",
    "Allergic rhinitis can cause sneezing and nasal irritation.",
    [
        "Avoid known allergy triggers.",
        "Keep surroundings clean.",
        "Consider a suitable saline nasal spray.",
        "Discuss persistent symptoms with a clinician."
    ],
    ["Avoid smoke and known triggers."],
    "Severe allergic reactions require urgent help.",
    "Do symptoms occur around dust or pollen?"
)

add(
    "asthma", "Asthma",
    "Asthma is a condition affecting the airways.",
    [
        "Follow your clinician's asthma action plan.",
        "Use prescribed treatment as directed.",
        "Avoid known triggers.",
        "Keep regular medical follow-ups."
    ],
    ["Do not stop prescribed controller treatment yourself.",
     "Avoid smoke."],
    "Severe breathing difficulty or symptoms not responding "
    "to prescribed rescue treatment require emergency care.",
    "Have you previously been diagnosed with asthma?"
)

add(
    "sinusitis", "Sinusitis",
    "Sinusitis means inflammation of the sinuses.",
    [
        "Rest.",
        "Stay hydrated.",
        "Consider a suitable saline nasal spray.",
        "Seek advice if symptoms persist."
    ],
    ["Avoid smoke.", "Avoid unnecessary antibiotics."],
    "Severe headache or swelling around an eye needs prompt assessment.",
    "How long have you had nasal congestion?"
)

add(
    "dust allergy", "Dust Allergy",
    "Dust allergy can cause sneezing and nasal or eye irritation.",
    [
        "Reduce exposure to dust.",
        "Clean bedding regularly.",
        "Use a damp cloth when cleaning.",
        "Discuss persistent symptoms with a clinician."
    ],
    ["Avoid smoke.", "Avoid known triggers."],
    followup="Do symptoms worsen while cleaning?"
)

add(
    "pollen allergy", "Pollen Allergy",
    "Pollen allergy can cause seasonal allergy symptoms.",
    [
        "Reduce exposure when pollen levels are high.",
        "Wash hands and face after outdoor exposure.",
        "Keep your sleeping area clean.",
        "Seek advice for persistent symptoms."
    ],
    ["Avoid known triggers where possible."],
    followup="Do symptoms occur during a particular season?"
)


# ==================================================
# 6. LONG-TERM HEALTH CONDITIONS
# ==================================================

add(
    "diabetes", "Diabetes",
    "Diabetes affects blood glucose regulation.",
    [
        "Follow your prescribed care plan.",
        "Monitor glucose as advised.",
        "Eat regular balanced meals.",
        "Maintain appropriate physical activity."
    ],
    ["Do not stop prescribed medication yourself.",
     "Do not replace treatment with home remedies."],
    "Confusion, fainting or severe illness requires urgent assessment.",
    "Are you asking about symptoms or general care?"
)

add(
    "hypothyroidism", "Hypothyroidism",
    "Hypothyroidism occurs when the thyroid produces too little hormone.",
    [
        "Follow prescribed treatment.",
        "Attend recommended thyroid tests.",
        "Maintain balanced meals and regular sleep."
    ],
    ["Do not change prescribed medicine yourself.",
     "Avoid unverified thyroid supplements."],
    followup="Have you had a thyroid blood test?"
)

add(
    "hyperthyroidism", "Hyperthyroidism",
    "Hyperthyroidism occurs when the thyroid produces too much hormone.",
    [
        "Seek professional assessment.",
        "Follow prescribed treatment.",
        "Attend recommended monitoring appointments."
    ],
    ["Avoid self-prescribing thyroid medicines."],
    "Severe palpitations, confusion or significant worsening "
    "requires urgent assessment.",
    "Has a clinician diagnosed hyperthyroidism?"
)

add(
    "iron deficiency anemia", "Iron Deficiency Anemia",
    "Iron deficiency anemia affects healthy red blood cell production.",
    [
        "Seek assessment to confirm the cause.",
        "Include suitable iron-containing foods.",
        "Follow prescribed treatment if needed."
    ],
    ["Avoid taking iron supplements without appropriate advice."],
    "Severe weakness, fainting or breathing difficulty "
    "needs prompt assessment.",
    "Have you had a hemoglobin or iron test?"
)

add(
    "migraine", "Migraine",
    "Migraine is a neurological condition that can cause recurrent headaches.",
    [
        "Rest in a quiet comfortable room.",
        "Maintain hydration.",
        "Follow regular sleep and meal schedules.",
        "Track possible triggers."
    ],
    ["Avoid known triggers.",
     "Avoid frequent unsupervised pain medicine use."],
    "A sudden unusual severe headache or new neurological "
    "symptoms requires urgent assessment.",
    "Have you experienced similar headaches before?"
)

add(
    "osteoarthritis", "Osteoarthritis",
    "Osteoarthritis affects joints and may cause pain or stiffness.",
    [
        "Maintain comfortable movement.",
        "Try gentle low-impact activity.",
        "Follow professional exercise advice.",
        "Allow rest when needed."
    ],
    ["Avoid activities that significantly worsen pain."],
    "A suddenly hot swollen joint needs medical assessment.",
    "Which joint is affected?"
)

add(
    "osteoporosis", "Osteoporosis",
    "Osteoporosis causes bones to become weaker.",
    [
        "Follow your clinician's care plan.",
        "Discuss suitable bone-strengthening activities.",
        "Maintain balanced nutrition.",
        "Reduce fall hazards."
    ],
    ["Avoid unverified supplements."],
    "New severe pain after a fall requires assessment.",
    "Are you asking about prevention or general care?"
)

add(
    "vitamin d deficiency", "Vitamin D Deficiency",
    "Vitamin D deficiency may affect bone and muscle health.",
    [
        "Discuss appropriate testing with a clinician.",
        "Include suitable dietary sources.",
        "Follow professional supplement advice."
    ],
    ["Avoid high-dose supplements without medical advice."],
    followup="Have you had a vitamin D test?"
)

add(
    "vitamin b12 deficiency", "Vitamin B12 Deficiency",
    "Vitamin B12 deficiency can affect blood cells and nerves.",
    [
        "Seek assessment to confirm the cause.",
        "Include suitable dietary sources.",
        "Follow prescribed treatment when needed."
    ],
    ["Do not ignore persistent numbness."],
    "New or progressive neurological symptoms need prompt assessment.",
    "Have you had a B12 blood test?"
)

add(
    "pcos", "Polycystic Ovary Syndrome",
    "PCOS is a hormonal condition needing individual assessment.",
    [
        "Attend recommended medical follow-ups.",
        "Maintain balanced regular meals.",
        "Choose enjoyable physical activity.",
        "Follow your clinician's treatment plan."
    ],
    ["Avoid unverified hormonal supplements."],
    followup="Are you asking about PCOS symptoms or general care?"
)

add(
    "gout", "Gout",
    "Gout is an inflammatory joint condition.",
    [
        "Seek medical assessment.",
        "Rest the painful joint.",
        "Maintain normal hydration unless advised otherwise.",
        "Follow prescribed treatment."
    ],
    ["Avoid self-prescribing medicines."],
    "A suddenly hot swollen joint with fever needs urgent assessment.",
    "Which joint is painful?"
)


# ==================================================
# 7. MUSCLE, BONE AND JOINT CONDITIONS
# ==================================================

add(
    "back pain", "Back Pain",
    "Back pain can have several causes.",
    [
        "Keep gently active as tolerated.",
        "Avoid staying in one position too long.",
        "Try a comfortable warm or cool compress.",
        "Maintain comfortable posture."
    ],
    ["Avoid heavy lifting if it worsens pain.",
     "Avoid prolonged bed rest."],
    "New weakness, loss of bladder or bowel control, "
    "or severe pain after injury needs urgent care.",
    "Is the pain in your upper or lower back?"
)

add(
    "muscle strain", "Muscle Strain",
    "A muscle strain occurs when a muscle is overstretched.",
    [
        "Rest from activities that worsen pain.",
        "Use a wrapped cold pack for short periods initially.",
        "Resume gentle movement as comfortable."
    ],
    ["Avoid forcing painful movement.",
     "Avoid placing ice directly on skin."],
    "Severe pain or inability to use the area needs assessment.",
    "Which body area is affected?"
)

add(
    "sprain", "Sprain",
    "A sprain affects the ligaments around a joint.",
    [
        "Rest from activities that worsen pain.",
        "Use a wrapped cold pack for short periods initially.",
        "Support the area comfortably.",
        "Seek assessment if movement is difficult."
    ],
    ["Avoid forcing movement.",
     "Avoid placing ice directly on skin."],
    "Severe pain, deformity or inability to bear weight "
    "requires assessment.",
    "Which joint is affected?"
)

add(
    "neck pain", "Neck Pain",
    "Neck pain may occur for several reasons.",
    [
        "Maintain gentle movement as tolerated.",
        "Take breaks from prolonged sitting.",
        "Try a comfortable warm or cool compress.",
        "Keep screens at a comfortable height."
    ],
    ["Avoid forcing painful stretches."],
    "Neck pain with fever, new weakness or significant injury "
    "needs urgent assessment.",
    "Did the pain begin after an injury?"
)

add(
    "knee pain", "Knee Pain",
    "Knee pain can have different causes.",
    [
        "Reduce activities that worsen pain.",
        "Use a wrapped cold pack if recently injured.",
        "Maintain gentle movement as tolerated.",
        "Seek assessment if symptoms continue."
    ],
    ["Avoid forcing painful exercise."],
    "A hot swollen knee, deformity or inability to walk "
    "needs prompt assessment.",
    "Was there a recent injury?"
)

add(
    "heel pain", "Heel Pain",
    "Heel pain can affect walking and daily activities.",
    [
        "Wear comfortable supportive footwear.",
        "Reduce activities that worsen discomfort.",
        "Try gentle movement as tolerated.",
        "Seek advice if pain continues."
    ],
    ["Avoid forcing painful exercise."],
    "Severe pain after injury or inability to walk needs assessment.",
    "Is pain worse during your first steps in the morning?"
)

add(
    "plantar fasciitis", "Plantar Fasciitis",
    "Plantar fasciitis causes irritation along the bottom of the foot.",
    [
        "Use comfortable supportive footwear.",
        "Reduce activities that worsen symptoms.",
        "Try gentle stretches as tolerated.",
        "Seek advice if symptoms persist."
    ],
    ["Avoid forcing painful stretches."],
    followup="Is heel pain worse after resting?"
)

add(
    "tennis elbow", "Tennis Elbow",
    "Tennis elbow can cause pain around the outer elbow.",
    [
        "Reduce activities that trigger pain.",
        "Take breaks from repetitive movements.",
        "Maintain gentle movement.",
        "Seek advice if symptoms persist."
    ],
    ["Avoid repeatedly forcing painful movements."],
    followup="Does gripping objects worsen the pain?"
)

add(
    "shoulder pain", "Shoulder Pain",
    "Shoulder pain can occur due to different joint or muscle problems.",
    [
        "Avoid activities that worsen discomfort.",
        "Maintain gentle movement as tolerated.",
        "Try a comfortable warm or cool compress.",
        "Seek assessment if pain continues."
    ],
    ["Avoid forcing painful movement."],
    "Severe pain after injury or inability to move the arm "
    "needs prompt assessment.",
    "Did your shoulder pain begin after an injury?"
)


# ==================================================
# 8. EYE, EAR AND DENTAL HEALTH
# ==================================================

add(
    "conjunctivitis", "Conjunctivitis",
    "Conjunctivitis can cause red or irritated eyes.",
    [
        "Wash hands regularly.",
        "Avoid rubbing your eyes.",
        "Use a clean cool compress.",
        "Avoid sharing towels."
    ],
    ["Avoid sharing eye products.",
     "Avoid unprescribed eye medicines."],
    "Eye pain, light sensitivity or vision changes "
    "need prompt assessment.",
    "Is one eye affected or both?"
)

add(
    "dry eyes", "Dry Eyes",
    "Dry eyes may cause irritation or a gritty feeling.",
    [
        "Take regular screen breaks.",
        "Blink normally while using screens.",
        "Avoid direct airflow towards your eyes.",
        "Ask a pharmacist or clinician about suitable lubricating drops."
    ],
    ["Avoid rubbing your eyes."],
    "Pain or vision changes require medical assessment.",
    "Do symptoms worsen during screen use?"
)

add(
    "ear infection", "Ear Infection",
    "An ear infection can cause ear discomfort.",
    [
        "Seek medical assessment when needed.",
        "Keep the ear dry if advised.",
        "Rest."
    ],
    ["Do not insert objects into your ear.",
     "Do not put unprescribed substances inside the ear."],
    "Severe pain, swelling around the ear or hearing changes "
    "need medical attention.",
    "Do you have ear pain or hearing difficulty?"
)

add(
    "earwax buildup", "Earwax Buildup",
    "Earwax can sometimes block the ear canal.",
    [
        "Seek professional advice if hearing feels blocked.",
        "Keep the outer ear clean.",
        "Use only professionally recommended care."
    ],
    ["Do not insert cotton buds or sharp objects into the ear."],
    "Pain, discharge or sudden hearing loss needs assessment.",
    "Is your hearing affected?"
)

add(
    "mouth ulcer", "Mouth Ulcer",
    "A mouth ulcer is a small sore inside the mouth.",
    [
        "Maintain gentle oral hygiene.",
        "Drink enough water.",
        "Choose comfortable foods.",
        "Avoid irritating the sore."
    ],
    ["Avoid foods that worsen discomfort."],
    "An ulcer that does not heal needs dental or medical advice.",
    "How long have you had the ulcer?"
)

add(
    "toothache", "Toothache",
    "Toothache can have several dental causes.",
    [
        "Arrange a dental appointment.",
        "Maintain gentle oral hygiene.",
        "Avoid chewing on the painful side if uncomfortable."
    ],
    ["Do not put chemicals or medicines directly on the tooth."],
    "Facial swelling, fever or difficulty swallowing "
    "requires urgent assessment.",
    "Which tooth or side is painful?"
)

add(
    "gingivitis", "Gingivitis",
    "Gingivitis means inflammation of the gums.",
    [
        "Brush gently twice daily.",
        "Clean between teeth appropriately.",
        "Arrange a dental check-up."
    ],
    ["Avoid smoking.", "Avoid neglecting oral hygiene."],
    "Persistent bleeding or swelling needs dental assessment.",
    "Do your gums bleed while brushing?"
)

add(
    "bad breath", "Bad Breath",
    "Bad breath can have several oral or medical causes.",
    [
        "Brush teeth regularly.",
        "Clean your tongue gently.",
        "Clean between your teeth.",
        "Stay hydrated.",
        "Arrange a dental check-up if persistent."
    ],
    ["Avoid relying only on mouth fresheners."],
    followup="Have you also noticed gum problems?"
)


# ==================================================
# 9. OTHER COMMON HEALTH TOPICS
# ==================================================

add(
    "heat exhaustion", "Heat Exhaustion",
    "Heat exhaustion can occur after excessive heat exposure.",
    [
        "Move to a cooler place.",
        "Rest.",
        "Loosen tight clothing.",
        "Sip cool fluids if fully alert and able to swallow."
    ],
    ["Avoid further heat exposure."],
    "Confusion, collapse or severe symptoms require emergency care.",
    "Are you now in a cooler place?"
)

add(
    "motion sickness", "Motion Sickness",
    "Motion sickness can cause nausea during travel.",
    [
        "Look towards a stable distant point.",
        "Get fresh air if possible.",
        "Take travel breaks.",
        "Avoid heavy meals immediately before travelling."
    ],
    ["Avoid reading if it worsens symptoms."],
    followup="Does this happen mainly during road travel?"
)

add(
    "menstrual cramps", "Menstrual Cramps",
    "Menstrual cramps can cause discomfort around menstruation.",
    [
        "Try a comfortably warm heating pad with a protective layer.",
        "Rest when needed.",
        "Maintain gentle movement.",
        "Stay hydrated."
    ],
    ["Avoid excessive heat directly on skin."],
    "Severe, unusual or persistent pain needs medical assessment.",
    "Is this pain similar to your usual cramps?"
)

add(
    "anxiety", "Anxiety",
    "Anxiety can involve worry, tension or feeling overwhelmed.",
    [
        "Try slow comfortable breathing.",
        "Take a break in a calm place.",
        "Maintain regular sleep and meals.",
        "Talk with someone you trust."
    ],
    ["Avoid unprescribed medicines.",
     "Avoid excessive caffeine if it worsens symptoms."],
    "Seek professional support if anxiety affects daily life.",
    "Would you like simple relaxation techniques?"
)

add(
    "stress", "Stress",
    "Stress is a response to demanding situations.",
    [
        "Take regular breaks.",
        "Maintain a comfortable sleep routine.",
        "Try relaxing activities.",
        "Talk to a trusted person."
    ],
    ["Avoid ignoring persistent stress."],
    "Seek support if stress becomes difficult to manage.",
    "Is your stress related to study, work or something else?"
)

add(
    "minor burn", "Minor Burn",
    "A minor superficial burn can cause skin discomfort.",
    [
        "Cool the area under cool running water for 20 minutes.",
        "Remove nearby jewellery if safe.",
        "Cover loosely with a clean non-stick dressing.",
        "Seek medical advice if unsure about severity."
    ],
    ["Do not apply ice, butter or toothpaste.",
     "Do not break blisters."],
    "Large, deep, chemical or electrical burns require urgent care.",
    "Where is the burn located?"
)

add(
    "minor cut", "Minor Cut",
    "A minor cut is a small break in the skin.",
    [
        "Wash your hands.",
        "Rinse the cut with clean running water.",
        "Cover with a clean dressing.",
        "Seek advice if tetanus protection may be needed."
    ],
    ["Avoid putting irritating substances into the wound."],
    "Uncontrolled bleeding or a deep wound needs urgent care.",
    "Is the bleeding controlled?"
)

add(
    "nosebleed", "Nosebleed",
    "A nosebleed means bleeding from the nose.",
    [
        "Sit upright and lean slightly forward.",
        "Pinch the soft part of your nose continuously for 10 to 15 minutes.",
        "Breathe through your mouth.",
        "Seek medical help if bleeding continues."
    ],
    ["Do not tilt your head backward.",
     "Avoid repeatedly checking before the pressure period ends."],
    "Heavy bleeding, faintness or bleeding after a serious injury "
    "requires urgent assessment.",
    "Has the bleeding stopped?"
)

add(
    "hiccups", "Hiccups",
    "Hiccups are repeated involuntary diaphragm contractions.",
    [
        "Eat slowly.",
        "Take a short break from eating.",
        "Avoid overeating.",
        "Notice possible triggers."
    ],
    ["Avoid forcing uncomfortable breathing techniques."],
    "Persistent hiccups affecting eating, sleeping or breathing "
    "need medical assessment.",
    "How long have the hiccups continued?"
)

add(
    "mouth dryness", "Dry Mouth",
    "Dry mouth occurs when the mouth does not produce enough saliva.",
    [
        "Sip water regularly.",
        "Maintain gentle oral hygiene.",
        "Discuss persistent symptoms with a dentist or clinician."
    ],
    ["Avoid tobacco.",
     "Avoid excessive caffeine if it worsens dryness."],
    followup="Is your mouth dry throughout the day?"
)

add(
    "leg cramps", "Leg Cramps",
    "Leg cramps cause sudden muscle tightness or discomfort.",
    [
        "Stop the activity causing discomfort.",
        "Try gentle comfortable stretching.",
        "Maintain normal hydration.",
        "Rest if needed."
    ],
    ["Avoid forcing painful stretches."],
    "Persistent cramps or cramps with swelling or weakness "
    "need medical assessment.",
    "Do cramps happen mainly at night?"
)

add(
    "eye strain", "Eye Strain",
    "Eye strain can happen after prolonged visual activity.",
    [
        "Take regular screen breaks.",
        "Adjust screen brightness comfortably.",
        "Blink normally.",
        "Maintain a comfortable viewing distance."
    ],
    ["Avoid prolonged screen use without breaks."],
    "Persistent pain or vision changes require assessment.",
    "Do symptoms worsen after using screens?"
)

add(
    "sleep apnea", "Sleep Apnea",
    "Sleep apnea causes repeated breathing interruptions during sleep.",
    [
        "Arrange medical assessment.",
        "Follow prescribed treatment.",
        "Maintain a consistent sleep schedule.",
        "Discuss symptoms with a sleep specialist."
    ],
    ["Do not rely on home remedies as a cure."],
    "Significant daytime sleepiness or breathing concerns "
    "need professional assessment.",
    "Has anyone noticed breathing pauses during your sleep?"
)

add(
    "vertigo", "Vertigo",
    "Vertigo causes a sensation of spinning or movement.",
    [
        "Sit or lie down safely.",
        "Avoid sudden head movements.",
        "Seek medical assessment if symptoms persist."
    ],
    ["Avoid driving while dizzy."],
    "Vertigo with new weakness, severe headache or difficulty "
    "speaking requires urgent assessment.",
    "Does the spinning sensation happen when moving your head?"
)

add(
    "low blood pressure", "Low Blood Pressure",
    "Low blood pressure can sometimes cause dizziness or faintness.",
    [
        "Sit or lie down if feeling faint.",
        "Stand up slowly.",
        "Discuss repeated low readings with a clinician.",
        "Maintain normal hydration unless medically restricted."
    ],
    ["Avoid changing prescribed medicines yourself."],
    "Fainting, chest pain or severe weakness requires urgent care.",
    "Do you have a recent blood pressure reading?"
)


# ==================================================
# ALTERNATIVE NAMES
# ==================================================

ALIASES = {
    "bukhar": "fever",
    "bukhaar": "fever",
    "sir dard": "headache",
    "sar dard": "headache",
    "head pain": "headache",
    "khansi": "cough",
    "khaansi": "cough",
    "sukhi khansi": "dry cough",
    "sukhi khaansi": "dry cough",
    "pet dard": "stomach pain",
    "pet mein dard": "stomach pain",
    "stomachache": "stomach pain",
    "kabz": "constipation",
    "kabj": "constipation",
    "ulti": "vomiting",
    "dast": "diarrhea",
    "loose motion": "diarrhea",
    "loose motions": "diarrhea",
    "neend nahi aa rahi": "insomnia",
    "neend nhi aa rhi": "insomnia",
    "high bp": "high blood pressure",
    "bp high": "high blood pressure",
    "low bp": "low blood pressure",
    "sugar disease": "diabetes",
    "flu": "influenza",
    "cold": "common cold",
    "covid": "covid 19",
    "covid 19": "covid 19",
    "uti": "urinary tract infection",
    "ibs": "irritable bowel syndrome",
    "tb": "tuberculosis",
    "pcod": "pcos",
    "thyroid low": "hypothyroidism",
    "thyroid high": "hyperthyroidism",
    "b12 deficiency": "vitamin b12 deficiency",
    "vitamin d low": "vitamin d deficiency",
    "acidity": "acid reflux",
    "gas": "bloating",
    "piles": "hemorrhoids",
    "dry mouth": "mouth dryness",
    "pink eye": "conjunctivitis",
    "period pain": "menstrual cramps",
    "period cramps": "menstrual cramps",
    "sun burn": "sunburn",
    "athlete's foot": "athletes foot",
    "food infection": "food poisoning"
}


# ==================================================
# LOOKUP FUNCTIONS
# ==================================================

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

    return (
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
        + "\n\n"
        + DISCLAIMER
    )


def find_homecare(message):
    """
    Find a health topic in a user message.

    This is a simple topic lookup, not a diagnosis engine.
    Negated mentions are excluded.
    """

    text = normalize(message)

    names = sorted(
        list(HOME_CARE.keys()) + list(ALIASES.keys()),
        key=len,
        reverse=True
    )

    for name in names:

        name = normalize(name)

        pattern = (
            r"(?<!\w)"
            + re.escape(name)
            + r"(?!\w)"
        )

        for match in re.finditer(pattern, text):

            before = text[max(0, match.start() - 35):match.start()]
            after = text[match.end():match.end() + 20]

            if re.search(
                r"(?:\bno|\bwithout|\bnot having|"
                r"\bdon't have|\bdo not have)\s*$",
                before
            ):
                continue

            if re.match(
                r"\s+(?:nahi|nhi)\s+(?:hai|h)\b",
                after
            ):
                continue

            condition = ALIASES.get(name, name)

            return format_homecare(condition)

    return None


def list_conditions():

    return sorted(HOME_CARE.keys())


def search_conditions(keyword):

    keyword = normalize(keyword)

    return [
        name
        for name in list_conditions()
        if keyword in name
    ]


# ==================================================
# LOCAL TEST
# ==================================================

if __name__ == "__main__":

    print("=" * 45)
    print("MediAssist AI - Home Care Knowledge Base")
    print("=" * 45)

    print("Available entries:", len(HOME_CARE))
    print("Alternative names:", len(ALIASES))

    print("\nExample: Fever\n")
    print(format_homecare("fever"))

    print("\n" + "=" * 45)
    print("Example: Malaria\n")
    print(format_homecare("malaria"))

    print("\n" + "=" * 45)
    print("Example: Dry Cough\n")
    print(format_homecare("dry cough"))

    print("\nKnowledge base loaded successfully.")
