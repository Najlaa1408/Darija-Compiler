import streamlit as st
import pyttsx3
import speech_recognition as sr
from regles import lexer, parser
import re
from pydub import AudioSegment
from pydub.playback import play




# Text-to-Speech
def text_to_speech(text, lang='ar'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # You can adjust the speed if needed
    engine.setProperty('voice', 'arabic')
    engine.say(text)
    engine.runAndWait()

# Speech-to-Text
def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        st.write("Recognizing...")
        proverb = recognizer.recognize_google(audio, language="ar")
        return proverb
    except sr.UnknownValueError:
        st.write("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
        return None
translations = {
    "الفياق بكري بالذهب مشري": "Whoever gets up early has a golden chance.",
    "اللي بغا الزين يصبر للتقيب الوذنين": "He who wants the good should be patient for the difficulties.",
    "اللي تلف يشد الارض": "He who no longer knows what to do must attach himself to the earth.",
    "الاب يربي والام تخبي": "The father raises, and the mother conceals.",
    "مولى القلب الصافي ديما زهرو حافي": "He who has a pure heart is always be unlucky.",
    "شوف الجار قبل الدار": "Check the neighbor before the house.",
    "الحر بالغمزة والعبد بالدبزة": "The real person with a hint, and the servant with a whip.",
    "السلهام والعمامة وقلة الفهامة": "A turban, a cloak, and a lack of understanding.",
    "طلاب يطلب ومراته تصدق": "The beggar begs and his wife gives.",
    "نسا الهم ينساك": "If you forget your worries, they will forget you.",
    "لبس قدك يواتيك": "Wear your size; you will be respected.",
    "سول المجرب لا تسول طبيب": "Ask the experienced, not the doctor.",
    "الله ينجيك من المشتاق الى داق": "May God save you from a someone who had nothing, but now he has tasted something.",
}

translations2 = {
    "مولى القلب الصافي ديما زهرو حافي":"wadami isfa welns orda dars tili tezdayt ",
    "الله ينجيك من المشتاق الى داق":"aki nejja rebbi iwada ordarili yat illi dars ",
    "شوف الجار قبل الدار":"seqsa g wadjar orta tseqsat g tgemmi",
    "السلهام والعمامة وقلة الفهامة":"wada yzran tajelabit izar rezt walayni hat la'aql walout",
    "طلاب يطلب ومراته تصدق":"ama'ich ari tdalab artsdaq tamghartens",
    "نسا الهم ينساك":"tou lhem itouk",
    "لبس قدك يواتيك":"k aydamitghit thenat",
    "سول المجرب لا تسول طبيب":"seqsa wada f tka orta tkit dar otbib",
    "دخول الحمام ماشي بحال خروجو":"ord wanig tekchemt s lhemam  wan igskis  tefekht ",
    "اللي بغا الزين يصبر للتقيب الوذنين": "wan  iran zin  isber i toubiyin nimzguan.",
    "الفياق بكري بالذهب مشري":"wan iran ayqdo chgholns aynker zik",
    "عند رخصو تخلي نصو":"a torkhisin a toni'lin",
    "اللي تلف يشد الارض":"wan orisin mayskar iqim sakal ",
    "الاب يربي والام تخبي":"baba aritrebba ima artguero ",
    "الحر بالغمزه والعبد بالدبزه":"wada ychwan daytfham ghir s talin "
}

# Verify Proverb Function
def verify_proverb(proverb_input):
    # Set the input for the lexer
    lexer.input(proverb_input)
    
    # List to store tokens
    tokens = []
    
    # Get tokens until the end of the input
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append(token)

    valid_order = (
        ('ACTION', 'ENTITY', 'RELATION', 'MODIFIER', 'SPECIFIC', 'GROUP'),
        ('ACTION', 'ENTITY', 'RELATION', 'MODIFIER', 'SPECIFIC'),
        ('ACTION', 'ENTITY', 'RELATION', 'MODIFIER'),
        ('ACTION', 'ENTITY', 'RELATION'),
        ('ACTION', 'ENTITY'),
        ('ACTION',)
    )

    # Check for unknown token
    if any(token.type == 'IDENTIFIER' for token in tokens):
        st.write("<span style='color:red;font-weight:bold;'>Proverb error: Sentence contains unknown token.</span>", unsafe_allow_html=True)
    # Check for invalid token order
    elif tuple(token.type for token in tokens) not in valid_order:
        st.write("<span style='color:red; font-weight:bold;'>Syntax error: Invalid token order.</span>", unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('الفياق', 'بكري', 'بالذهب', 'مشري'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write(f"<span style='color:white;font-weight:bold;' >Equivalent English Proverb: {english_translations}</span>", unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write(f"<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb: {tamazight_translations}</span>", unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('عند', 'رخصو', 'تخلي', 'نصو'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('اللي', 'تلف', 'يشد', 'الارض'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('الاب', 'يربي', 'والام', 'تخبي'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('مولى', 'القلب', 'الصافي', 'ديما', 'زهرو', 'حافي'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('شوف', 'الجار', 'قبل', 'الدار'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('الحر', 'بالغمزه', 'والعبد', 'بالدبزه'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('السلهام', 'والعمامة', 'وقلة', 'الفهامة'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('طلاب', 'يطلب', 'ومراته', 'تصدق'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('نسا', 'الهم', 'ينساك'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('لبس', 'قدك', 'يواتيك'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('شوف', 'الجار', 'قبل', 'الدار'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('سول', 'المجرب', 'لا', 'تسول', 'طبيب'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    elif tuple(token.value for token in tokens) == ('الله', 'ينجيك', 'من', 'المشتاق', 'الى', 'داق'):
        darija_proverb = " ".join(token.value for token in tokens)
        english_translations = translations[darija_proverb]
        st.write("<span style='color:#00FF00;font-weight:bold;' >Verification Result: Valid phrase.</span>", unsafe_allow_html=True)
        st.write("<span style='color:white;font-weight:bold;' >Equivalent English Proverb:  </span>",english_translations, unsafe_allow_html=True)
        tamazight_translations = translations2[darija_proverb]
        st.write("<span style='color:white;font-weight:bold;' >Equivalent Tamazight Proverb:  </span>",tamazight_translations, unsafe_allow_html=True)
    else:
        st.write("<span style='color:red'>Verification Result: Invalid phrase in terms of meaning.</span>", unsafe_allow_html=True)          



# Définir quelques proverbes avec leurs indices
proverbes = [
    {
        "proverbe": "عند رخصو تخلي نصو",
        "indices": ["الحاجةالرخيصةديما ناقصة", "قيمة الحاجة في فلوسها"],
        "audio_path": "audios/3nd_rakhso.mp4",
        
    },
    {
        "proverbe": "اللي بغا الزين يصبر للتقيب الوذنين",
        "indices": ["بغيت ندير طوانق ولكن خفت من تقيب لودنين"],
        "audio_path": "audios/t9ib_lwdnin.mp4",
        
    },
    {
        "proverbe": "دخول الحمام ماشي بحال خروجو",
        "indices": ["واهد لبنت مع سنات عقد الزواج و هيا يتنادم معاهآ لحال"],
        "audio_path": "audios/dkhoul_lhemmam.mp4",
        
    },
    {
        "proverbe": "الفياق بكري بالذهب مشري",
        "indices": ["فقت مع 7 ودرت بزاف دلحوايج يلاه وصلات 10"],
        "audio_path": "audios/lefya9_bekri.mp4",
        
    },
    {
        "proverbe": "تبع الكذاب حتى لباب الدار",
        "indices": ["شي واحد انا عارفاه كايكدب و كانسول فيه و غادا معاه فلكدوب ديالو"],
        "audio_path": "audios/tbe3_lkedab.mp4",
    },
    {
        "proverbe": "اللي تلف يشد الارض",
        "indices": ["بغيت نمشي لمراكش و بغيت نمشي حتا لفاس"],
        "audio_path": "audios/li_tlef.mp4",
    },
    {
        "proverbe": "طلاب يطلب ومراته تصدق",
        "indices": ["راجل يخدم ويجمع لفلوس و مراتو كتخسرهم فلخوا لخاوي"],
        "audio_path": "audios/telab_itleb.mp4",
    },
]

# Fonction pour récupérer le proverbe basé sur les indices
# ...

def get_proverb_by_indices(indices_utilisateur):
    indices_utilisateur = re.split(r'[,/]+', indices_utilisateur)
    proverb_found = False
    for proverb_data in proverbes:
        if all(indice.lower() in map(str.lower, proverb_data["indices"]) for indice in indices_utilisateur):
            proverb_found = True
            proverbe = proverb_data["proverbe"]
            audio_path = proverb_data["audio_path"]
            st.audio(audio_path, format="audio/mp4")
            return proverbe

    return "Aucun proverbe correspondant trouvé."


def page_home():
    st.markdown("""
    <style>
    /* Import the font from Google Fonts */
   @import url('https://fonts.googleapis.com/css2?family=Ubuntu:ital@1&display=swap');

    /* Apply font-family to the specific element */
    h1 {
        font-family: 'Playfair Display', serif;
        color: #4F000B;
        text-align: center;
        margin-top: -60px;
        font-size : 140px;
    }
    p {
        font-family: 'Playfair Display', serif;
        color: #000000;
        text-align: justify;
        margin-bottom: 10px;
        line-height: 1.5;
    }
    /* Additional CSS styling */
    </style>
    
    <h1>Darija Compiler</h1>
    """,
    unsafe_allow_html=True)
    
# This will help center the container
    st.markdown(
    """
    <style>
        .st-d1 {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        
    </style>
    """,
    unsafe_allow_html=True,
)
        
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://i.pinimg.com/564x/e6/51/a1/e651a1525af0222c7bc7bdcffa312a44.jpg");
    background-size: 100%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    background-color: rgba(0, 0, 0, 0.5);
    margin-bottom:-100px;
    #opacity : 0.8 ;
    
    
    }}

    [data-testid="stSidebar"] > div:first-child {{

    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

    

    
    # Main Content
    # About Project Section
    

    # Create columns for image and text
    col1, col2 = st.columns(2)

    # Add image to the left column
    #with col1:
    #    st.image("https://cdn.shopify.com/s/files/1/0050/7478/0275/products/PlateauDuoRougeAngle1_400x.png?v=1621326677", width=200, use_column_width=False)  # Replace "images/about.png" with the actual path

    # Add text to the right column
    #with col2:
    #st.markdown("<h2 style='color: white; text-align:center; margin-bottom:5px;'>About our project</h2>", unsafe_allow_html=True)

    #st.write(
            
           # "**Our project is a Darija Proverb Verifier that empowers users to input Darija proverbs and meticulously assess their syntax. It's meticulously crafted to assist users in comprehending the intricate structure of Darija proverbs."
            #"This innovative project was meticulously developed by [Your Team Name] as an integral part of [Project Name]. It's geared towards providing a user-friendly platform for exploring and validating Darija proverbs.**"
    #)

    # App Overview Section
    
    # Create columns for image and text
    col1, col2 = st.columns(2)

    # Add image to the left column
    #with col1:
     #   st.image("images/henna.png", width=200, use_column_width=False)  # Replace "images/over.png" with the actual path

    # Add text to the right column
    #with col2:
    

def about_us() :
    
    st.markdown("<h1 style='color: #432818; text-align: center; margin-bottom: 5px; text-decoration: underline;'>About our project</h1>", unsafe_allow_html=True)

    # Introduction text
    st.write(
        "**Our project is a Darija Proverb Verifier that empowers users to input Darija proverbs and meticulously assess their syntax. It's meticulously crafted to assist users in comprehending the intricate structure of Darija proverbs."
        "This innovative project was meticulously developed by Our Team as an integral part of Our Darija Compiler Project. It's geared towards providing a user-friendly platform for exploring and validating Darija proverbs.**"
    )

    # Styling for the section header
    st.markdown("""
    <style>
    /* Import the font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&display=swap');

    /* Apply font-family to the specific element */
    h1 {
        font-family: 'Playfair Display', serif;
        color: #432818;
        text-align: center;
        margin-bottom: 5px;
        text-decoration: underline;
    }

    /* Additional CSS styling for the content */

    </style>

    <h1>App Overview</h1>
    """,
    unsafe_allow_html=True)

    # Detailed information about the app
    st.write(
        "**Welcome to our Darija Proverb Verifier app! This app allows you to enter Darija proverbs, verify their syntax, and also provides the option to input proverbs using your microphone. "
        "It's a handy tool to check if your Darija proverbs follow the correct structure. "
        "Feel free to input your proverbs or use the microphone button to speak and verify your proverb.**"
    )
def page_verify():

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://i.pinimg.com/564x/e6/51/a1/e651a1525af0222c7bc7bdcffa312a44.jpg");
    background-size: 100%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    
    margin-bottom:-100px;
    opacity : 0.8 ;
    
    }}

    [data-testid="stSidebar"] > div:first-child {{

    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Proverb Input Section
    st.markdown("""
    <style>
    /* Import the font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&display=swap');

    /* Apply font-family to the specific element */
    h1 {
        font-family: 'Playfair Display', serif;
        color: white;
        text-align: center;
        margin-bottom: 5px;
        background-color: rgba(139, 69, 19, 1);
        
    }
                
    h2 {
        font-family: 'Playfair Display', serif;
        color: white;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Additional CSS styling */
    </style>
    
    <h1>Darija Proverb Input</h1>
    """, unsafe_allow_html=True)

    # Option to input proverb using microphone
    if st.button("Input Proverb Using Microphone"):
        spoken_proverb = speech_to_text()
        if spoken_proverb:
            st.text_area("You said (Spoken):", spoken_proverb, key="spoken_proverb")
            verify_proverb(spoken_proverb)

    # Text input for entering the proverb
    st.markdown("<h2>Or Enter the Darija Proverb:</h2>", unsafe_allow_html=True)
    proverb_input = st.text_area("")



    # Combine the buttons in the same line
    col1, col2, col3 = st.columns(3)

    # Verify Proverb Button
    if col1.button("Verify Proverb", key="verify_button"):
        verify_proverb(proverb_input)

    # Listen to Proverb Button
    if col2.button("Listen to Proverb", key="listen_button"):
        text_to_speech(proverb_input, lang='ar')
    st.markdown(
        """
        <style>
            .button {
                margin-right:0;
                padding-right:0;
            }
        
        </style>
        """,
        unsafe_allow_html=True
    )

def page_find():

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://i.pinimg.com/564x/e6/51/a1/e651a1525af0222c7bc7bdcffa312a44.jpg");
    background-size: 100%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    
    margin-bottom:-100px;
    opacity : 0.8 ;
    
    }}

    [data-testid="stSidebar"] > div:first-child {{

    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)
    # Page Streamlit
    st.markdown("""
    <style>
    /* Import the font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&display=swap');

    /* Apply font-family to the specific element */
    h1 {
        font-family: 'Playfair Display', serif;
        color: white;
        text-align: center;
        margin-bottom: 5px;
        background-color: rgba(139, 69, 19, 1);
        
        
    }
                
    h2 {
        font-family: 'Playfair Display', serif;
        color: white;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Additional CSS styling */
    </style>
    
    <h1>Darija Proverb Finder</h1>
    """, unsafe_allow_html=True)

    # Zone pour entrer les indices
    st.markdown("<h2>Enter the Clues:</h2>", unsafe_allow_html=True)
    user_indices = st.text_input("")

    if st.button("Find the proverb"):
        # Obtenir le proverbe basé sur les indices
        result = get_proverb_by_indices(user_indices)

        # Afficher le proverbe trouvé
        st.write(f"<span style='color:white; font-weight:bold;'>Proverb Found : {result}</span>", unsafe_allow_html=True)

        # Lire et jouer l'audio

def main():

    # Set page configuration with background color
    st.set_page_config(
        page_title="Darija Proverb Verifier",
        page_icon=":sunny:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Define pages
    pages = {
        "Home": page_home,
        "Verify Proverb": page_verify,
        "Find Proverb": page_find,
        "About Our Project": about_us,
    }

    # Sidebar
    st.sidebar.image("images/logofinal.png", width=300, use_column_width=False)

    # Navigation
    selection = st.sidebar.selectbox("Go to", list(pages.keys()))
    page = pages[selection]
    page()


    # Sidebar with Team Members Information
    st.sidebar.header("Meet Our Team")

    # Contact Information
    st.sidebar.subheader("Contact Information")
    st.sidebar.write("Email: compilationdarija@gmail.com")
    st.sidebar.write("Phone: +212 645818519")
    st.sidebar.write("Ecole: ENSAK")

    # Team Members
    st.sidebar.subheader("Team Members")

    # Display team members using st.image
    # Create columns for team members
    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.write("**AIT IHY Soukaina**")
        st.write("**ALJIB Nawal**")

    with col2:
        st.write("**DINI Doha**\n")
        st.write("**BELMKADDEM Najlaa**")

    # Styling for the social media icons in the sidebar
    st.sidebar.subheader("Contact us")

    # Shorter images with clickable links in the same line
    col1, col2, col3, col4 = st.sidebar.columns(4)

    with col1:
        st.image("images/702300.png", width=60, caption="", use_column_width=False)

    with col2:
        st.image("images/Instagram.png", width=60, caption="", use_column_width=False)

    with col3:
        st.image("images/facebook.png", width=60, caption="", use_column_width=False)

    with col4:
        st.image("images/twii.png", width=60, caption="", use_column_width=False)

    # Apply additional styling to the main content
    st.markdown("""
    <style>
    body {
        background-color: #EDE9E4; /* Custom background color */
    }
    .sidebar .sidebar-content {
        border-radius: 10px; /* Rounded corners for the sidebar */
        padding: 20px; /* Add padding for a cleaner appearance */
    }
    </style>
    """, unsafe_allow_html=True)





if __name__ == "__main__":
    main()
