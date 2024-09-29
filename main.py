import streamlit as st
from predibase import Predibase
from langchain_upstage import ChatUpstage
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import uuid
import re
from langchain_openai import ChatOpenAI
import sqlite3
from datetime import datetime, timedelta
import os

st.set_page_config(
    page_title="Gov-STAGE",
    page_icon="🛡️",
    layout="wide"
    )


def save_conversation_to_db(dbname, question, response, question_anonymized, response_anonymized, subject):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO chatbot_conversations (question, response, question_anonymized, response_anonymized, subject, timestamp, session_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (question, response, question_anonymized, response_anonymized,  subject, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), st.session_state.session_id))
    conn.commit()
    conn.close()

styl = """
<style>
    @import url('https://unpkg.com/pretendard@1.3.9/dist/web/static/pretendard.css');
    header {visibility: hidden;}
    html, body, div, p, span, input, textarea, button, select {
        font-family: 'Pretendard', sans-serif !important;
    }
    div[data-testid="stChatInput"]{
    position: fixed;
    bottom: 3rem;
    }

    button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        text-align: left !important;
        padding-left: 0px !important;
        color: inherit !important;
        cursor: pointer;
    }
    
    button:hover {
        background-color: transparent !important;
        color: #FF4650 !important;
    }

    button:focus:hover, button:active:hover {
        background-color: transparent !important;
        color: #FF4650 !important;
    }
    
    button:focus, button:active {
    background-color: transparent !important;
    color: inherit !important;
    outline: none !important;
    }
    #text_area_1{
    height: 150px;
    }

    .st-emotion-cache-4uzi61{
    align-self: center;
    margin-top: 70px;
    width:80%;
    }

    #gov-stage{
    text-align: center;
    }

</style>
"""
st.markdown(styl, unsafe_allow_html=True)
col1, col2= st.columns([8,2])
col2.markdown("##### Personal Information Filter")

with col1:
    placeholder = st.empty()
    col1_1, col1_2 = st.columns(2)

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.session_state.anonymized_chat_history = []
    st.session_state.subject = ''
  

if len(st.session_state.chat_history) == 0:
    container = placeholder.container(border=True)
    container.subheader("Gov-STAGE")
    container.write("")
    container.markdown("##### A Secure AI Solution for Public Institutions")
    container.write("Gov-STAGE is a system designed to enable public institutions to safely leverage large-scale AI. Through filtering technology and specialized small language models, it detects and protects personal information, ensuring the safe use of large language models like Solar. With Gov-STAGE, prevent data breaches and experience innovation powered by LLMs.")
    container.write("")
    container.markdown("##### Related Link")
    container.markdown("[GitHub](https://github.com/LimEulYoung/govstage): Check out the source code and technical documentation for the Gov-STAGE project.")
    container.markdown("[YouTube](https://youtu.be/CQKreGpyPUw): Watch video tutorials and resources related to using Gov-STAGE.")
    container.markdown("[Blog](https://blog.example.com/): Read the latest updates and technical blog posts.")
    container.markdown("[Hugging Face](https://huggingface.co/ducut91): Explore models and data related to Gov-STAGE.")

    
    
else:
    col1_1.markdown("<h5 style='text-align: center; color: black;'>User Interface</h5>", unsafe_allow_html=True)
    col1_2.markdown("<h5 style='text-align: center; color: black;'>Internal Processing</h5>", unsafe_allow_html=True)
    for content in st.session_state.chat_history:
        with col1_1:
            with st.chat_message("AI" if content[0] == "AI" else "Human"):
                st.markdown(content[1])
    for content in st.session_state.anonymized_chat_history:
        with col1_2:
            with st.chat_message("AI" if content[0] == "AI" else "Human"):
                    st.markdown(content[1])

with col2:
    mode_on = st.toggle("Protection Mode", value=True)
    if(mode_on):
        with st.expander("General Personal Information"):
            name = st.checkbox("Name", value=True)
            age = st.checkbox("Age", value=True)
            phone_number = st.checkbox("Phone Number", value=True)
            date_of_birth = st.checkbox("Date of Birth", value=True)
            email = st.checkbox("Email", value=True)
            nationality = st.checkbox("Nationality", value=True)
            state = st.checkbox("State", value=True)
            city = st.checkbox("City", value=True)
            district = st.checkbox("District", value=True)
            zip_code = st.checkbox("ZIP Code", value=True)
            detailed_address = st.checkbox("Detailed Address", value=True)
            road_name_address = st.checkbox("Road Name Address", value=True)
            gender = st.checkbox("Gender", value=True)
            job = st.checkbox("JOB", value=True)
            resident_registration_number = st.checkbox("Resident Registration Number", value=True)
            passport_number = st.checkbox("Passport Number", value=True)
            alien_registration_number = st.checkbox("Alien Resistration Number", value=True)
            driver_license = st.checkbox("Driver License", value=True)
        with st.expander("Health information"):
            condition = st.checkbox("Condition(To-Be)", value=False, disabled=True)
            physical_disability = st.checkbox("Physical Disablility(To-Be)", value=False, disabled=True)
            disability_level = st.checkbox("Disability Level(To-Be)", value=False, disabled=True)
            blood_type = st.checkbox("Blood Type", value=True)
            iq = st.checkbox("IQ", value=True)
            drug = st.checkbox("Drug(To-Be)", value=False, disabled=True)
        with st.expander("Credit Information"):
            account_number = st.checkbox("Account Number", value=True)
            money = st.checkbox("Money", value=True)
            order_number = st.checkbox("Order Number", value=True)
            credit_rating = st.checkbox("Credit Rating(To-Be)", value=False, disabled=True)
            cvv = st.checkbox("CVV(To-Be)", value=False, disabled=True)
            credit_card_expiration = st.checkbox("Credit Card Expiration(To-Be)", value=False, disabled=True)
            bank = st.checkbox("Bank", value=True)
        with st.expander("Social Information"):
            gpa = st.checkbox("GPA", value=True)
            technical_certification = st.checkbox("Technical Certification(To-Be)", value=False, disabled=True)
            student_number = st.checkbox("Student Number", value=True)
            school_name = st.checkbox("School Name", value=True)
            military_service_status = st.checkbox("Military Service Status(To-Be)", value=False, disabled=True)
            army_number = st.checkbox("Army Number", value=True)
            military_rank = st.checkbox("Military Rank(To-Be)", value=False, disabled=True)
            types_of_military_discharge = st.checkbox("Types of Military Discharge(To-Be)", value=False, disabled=True)
            organization = st.checkbox("Organization", value=True)
            employment_type = st.checkbox("Employment Type", value=True)
            work_experience = st.checkbox("Work Experience(To-Be)", value=False, disabled=True)
            employee_number = st.checkbox("Employee Number", value=True)
            criminal_record = st.checkbox("Criminal Record(To-Be)", value=False, disabled=True)
        with st.expander("Confidential Information"):
            source_code = st.checkbox("Source Code(To-Be)", value=False, disabled=True)
            statistics = st.checkbox("Statistics", value=True)
            crisis_alert_response = st.checkbox("Crisis Alert Response(To-Be)", value=False, disabled=True)
        with st.expander("Others"):
            password = st.checkbox("Password", value=True)
            ip_address = st.checkbox("IP Address", value=True)
            mac = st.checkbox("MAC", value=True)
            url = st.checkbox("URL", value=True)
            date = st.checkbox("Date", value=True)
            date_interval = st.checkbox("Date Interval", value=True)
            duration = st.checkbox("Duration", value=True)
            time = st.checkbox("Time", value=True)
    else:
        with st.expander("General Personal Information"):
            name = st.checkbox("Name", value=True, disabled=True)
            age = st.checkbox("Age", value=True, disabled=True)
            phone_number = st.checkbox("Phone Number", value=True, disabled=True)
            date_of_birth = st.checkbox("Date of Birth", value=True, disabled=True)
            email = st.checkbox("Email", value=True, disabled=True)
            nationality = st.checkbox("Nationality", value=True, disabled=True)
            state = st.checkbox("State", value=True, disabled=True)
            city = st.checkbox("City", value=True, disabled=True)
            district = st.checkbox("District", value=True, disabled=True)
            zip_code = st.checkbox("ZIP Code", value=True, disabled=True)
            detailed_address = st.checkbox("Detailed Address", value=True, disabled=True)
            road_name_address = st.checkbox("Road Name Address", value=True, disabled=True)
            gender = st.checkbox("Gender", value=True, disabled=True)
            job = st.checkbox("JOB", value=True, disabled=True)
            resident_registration_number = st.checkbox("Resident Registration Number", value=True, disabled=True)
            passport_number = st.checkbox("Passport Number", value=True, disabled=True)
            alien_registration_number = st.checkbox("Alien Resistration Number", value=True, disabled=True)
            driver_license = st.checkbox("Driver License", value=True, disabled=True)
        with st.expander("Health information"):
            condition = st.checkbox("Condition(To-Be)", value=False, disabled=True)
            physical_disability = st.checkbox("Physical Disablility(To-Be)", value=False, disabled=True)
            disability_level = st.checkbox("Disability Level(To-Be)", value=False, disabled=True)
            blood_type = st.checkbox("Blood Type", value=True, disabled=True)
            iq = st.checkbox("IQ", value=True, disabled=True)
            drug = st.checkbox("Drug(To-Be)", value=False, disabled=True)
        with st.expander("Credit Information"):
            account_number = st.checkbox("Account Number", value=True, disabled=True)
            money = st.checkbox("Money", value=True, disabled=True)
            order_number = st.checkbox("Order Number", value=True, disabled=True)
            credit_rating = st.checkbox("Credit Rating(To-Be)", value=False, disabled=True)
            cvv = st.checkbox("CVV(To-Be)", value=False, disabled=True)
            credit_card_expiration = st.checkbox("Credit Card Expiration(To-Be)", value=False, disabled=True)
            bank = st.checkbox("Bank", value=True, disabled=True)
        with st.expander("Social Information"):
            gpa = st.checkbox("GPA", value=True, disabled=True)
            technical_certification = st.checkbox("Technical Certification(To-Be)", value=False, disabled=True)
            student_number = st.checkbox("Student Number", value=True, disabled=True)
            school_name = st.checkbox("School Name", value=True, disabled=True)
            military_service_status = st.checkbox("Military Service Status(To-Be)", value=False, disabled=True)
            army_number = st.checkbox("Army Number", value=True, disabled=True)
            military_rank = st.checkbox("Military Rank(To-Be)", value=False, disabled=True)
            types_of_military_discharge = st.checkbox("Types of Military Discharge(To-Be)", value=False, disabled=True)
            organization = st.checkbox("Organization", value=True, disabled=True)
            employment_type = st.checkbox("Employment Type", value=True, disabled=True)
            work_experience = st.checkbox("Work Experience(To-Be)", value=False, disabled=True)
            employee_number = st.checkbox("Employee Number", value=True, disabled=True)
            criminal_record = st.checkbox("Criminal Record(To-Be)", value=False, disabled=True)
        with st.expander("Confidential Information"):
            source_code = st.checkbox("Source Code(To-Be)", value=False, disabled=True)
            statistics = st.checkbox("Statistics", value=True, disabled=True)
            crisis_alert_response = st.checkbox("Crisis Alert Response(To-Be)", value=False, disabled=True)
        with st.expander("Others"):
            password = st.checkbox("Password", value=True, disabled=True)
            ip_address = st.checkbox("IP Address", value=True, disabled=True)
            mac = st.checkbox("MAC", value=True, disabled=True)
            url = st.checkbox("URL", value=True, disabled=True)
            date = st.checkbox("Date", value=True, disabled=True)
            date_interval = st.checkbox("Date Interval", value=True, disabled=True)
            duration = st.checkbox("Duration", value=True, disabled=True)
            time = st.checkbox("Time", value=True, disabled=True)

    st.divider()
    st.markdown("##### Role")
    system_prompt = st.text_area("system prompt",value="You are an office assistant, responsible for promptly and accurately answering work-related questions from staff. Respond in a friendly and easy-to-understand language, while maintaining the professionalism and credibility of a public institution.")
    model_type = st.selectbox("model type",("gpt-4o", "llama3.1-405b", "solar-1-mini(fine_tuned)", "Grok-2", "Claude 3.5 Sonnet"),)

def newChatButton():
    del st.session_state['session_id']

def history_button_clicked(dbname, subject):
    questions = []
    responses = []
    questions_anonymized = []
    responses_anonymized = []
    
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT question, response, question_anonymized, response_anonymized
        FROM chatbot_conversations
        WHERE subject = ?
    ''', (subject,))
    
    rows = cursor.fetchall()
    for row in rows:
        questions.append(row[0])
        responses.append(row[1])
        questions_anonymized.append(row[2])
        responses_anonymized.append(row[3])    
    conn.close() 
    conversation_history = []
    anonymized_conversation_history = []
    for q, r in zip(questions, responses):
        conversation_history.append(('Human', q))
        conversation_history.append(('AI', r))
    for q, r in zip(questions_anonymized, responses_anonymized):
        anonymized_conversation_history.append(('Human', q))
        anonymized_conversation_history.append(('AI', r))

    st.session_state.chat_history = conversation_history
    st.session_state.anonymized_chat_history = anonymized_conversation_history
    st.session_state.subject = subject


def fetch_and_sort_subject_dates(dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT subject, MAX(timestamp) as latest_timestamp
        FROM chatbot_conversations
        GROUP BY subject
    ''')
    subject_date_pairs = cursor.fetchall()
    conn.close()
    
    subject_date_pairs.sort(key=lambda x: x[1], reverse=True)
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    nine_days_ago = today - timedelta(days=9)

    today_shown = False
    yesterday_shown = False
    last_7_days_shown = False

    for i in subject_date_pairs:
        timestamp = datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S').date()
        
        if timestamp == today:
            if not today_shown:
                st.markdown("**today**")
                today_shown = True
            st.button(i[0], on_click=history_button_clicked, args=['govstage.db', i[0]])
        
        elif timestamp == yesterday:
            if not yesterday_shown:
                st.markdown("")
                st.markdown("**yesterday**")
                yesterday_shown = True
            st.button(i[0], on_click=history_button_clicked, args=['govstage.db', i[0]])
        
        elif nine_days_ago < timestamp < yesterday:
            if not last_7_days_shown:
                st.markdown("")
                st.markdown("**Previous 7 Days**")
                last_7_days_shown = True
            st.button(i[0], on_click=history_button_clicked, args=['govstage.db', i[0]])


with st.sidebar:
    st.markdown("## Gov-STAGE")
    st.button("\\+ New Chat", on_click=newChatButton)
    st.divider()
    fetch_and_sort_subject_dates('govstage.db')

@st.cache_resource
def load_model():
    load_dotenv(verbose=True)
    model = ChatUpstage()
    print("solar-1-mini-chat loaded...")
    return model

@st.cache_resource
def load_model2():
    pb= Predibase(api_token=os.environ['PREDIBASE_API_KEY'])
    print("Predibase loaded...")
    return pb.deployments.client("solar-1-mini-chat-240612")

@st.cache_resource
def load_model3():
    model = ChatOpenAI(temperature=0.1, model_name="gpt-4o")
    print("gpt-4o loaded...")
    return model

@st.cache_resource
def load_model4():
    model = ChatOpenAI(api_key = os.environ['LLAMA_API_KEY'], base_url = "https://api.llama-api.com", model= "llama3.1-405b", max_tokens=1000, temperature= 0.1)
    print("llama3.1-405b loaded...")
    return model

solar = load_model()
lorax_client = load_model2()
gpt4o = load_model3()
llama3 = load_model4()


output_parser = StrOutputParser()

conversation_prompt_template = """
<|im_start|>system\n{system_prompt}<|im_end|>
<|im_start|>Conversation\n {anonymized_chat_history}<|im_end|>
<|im_start|>AI:"""

# anonymization_prompt_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# You are a personal data anonymization system. Your task is to anonymize personal information in the sentences provided, following the instructions below. However, do not anonymize the personal information of public figures (e.g., celebrities, politicians, athletes).

# Anonymization Rules:
# 1. Use the following placeholders for anonymization: {List_of_PII}.
# 2. If a placeholder is not applicable or relevant, retain the original information.
# 3. Exceptions to anonymization: Do not anonymize information about public figures (politicians, celebrities, athletes) or individuals who have been deceased for more than 5 years.
# 4. Format: Each exchange in the anonymized conversation should begin with 'Human:' or 'AI:' to indicate the speaker.

# Original sentences: <|eot_id|><|start_header_id|>user<|end_header_id|>

# {original_sentences}

# Anonymized sentences (without additional comments or responses):<|eot_id|><|start_header_id|>assistant<|end_header_id|>

# """

anonymization_prompt_template = """<|im_start|>system
You are a personal data anonymization system. Your task is to anonymize personal information in the sentences provided, following the instructions below. However, do not anonymize the personal information of public figures (e.g., celebrities, politicians, athletes).

Anonymization Rules:
1. Use the following placeholders for anonymization: {List_of_PII}.
2. If a placeholder is not applicable or relevant, retain the original information.
3. Exceptions to anonymization: Do not anonymize information about public figures (politicians, celebrities, athletes) or individuals who have been deceased for more than 5 years.
4. Format: Each exchange in the anonymized conversation should begin with 'Human:' or 'AI:' to indicate the speaker.

Original sentences: <|im_end|>
<|im_start|>user

{original_sentences}

Anonymized sentences (without additional comments or responses):<|im_end|>
<|im_start|>assistant

"""

# restoration_prompt_template  = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# You are a personal data restoration system.
# Restore the placeholders such as [NAME], [NAME2], [DOB], [DOB2], [ADDRESS], [ADDRESS2] to their original form based on the reference conversation below.
# The sentence to be restored may or may not be anonymized with placeholders. If it is anonymized, perform the restoration; if not, output the sentence to be restored as it is.
# Ensure the restored sentence makes sense in context.<|eot_id|><|start_header_id|>user<|end_header_id|>

# Conversation history(reference conversation): 
# {original_conversaion_sentence}

# Anonymized Conversation history(reference conversation):
# {anonymized_conversation_history}

# Sentence to be restored: 
# {sentence_to_be_restored}

# Restored sentence(without any additional comments or responses):<|eot_id|><|start_header_id|>assistant<|end_header_id|>

# """

restoration_prompt_template  = """<|im_start|>system

You are a personal data restoration system.
Restore the placeholders such as [NAME], [NAME2], [DOB], [DOB2], [ADDRESS], [ADDRESS2] to their original form based on the reference conversation below.
The sentence to be restored may or may not be anonymized with placeholders. If it is anonymized, perform the restoration; if not, output the sentence to be restored as it is.
Ensure the restored sentence makes sense in context.<|im_end|>
<|im_start|>user

Conversation history(reference conversation): 
{original_conversaion_sentence}

Anonymized Conversation history(reference conversation):
{anonymized_conversation_history}

Sentence to be restored: 
{sentence_to_be_restored}

Restored sentence(without any additional comments or responses):<|im_end|>
<|im_start|>assistant

"""


first_selected_fields = true_list = [var_name for var_name, var_value in [('[ACCOUNT_NUMBER]', account_number), ('[EMAIL]', email), ('[RESIDENT_REGISTRATION_NUMBER]', resident_registration_number), ('[PASSPORT_NUMBER]', passport_number), ('[ALIEN_REGISTRATION_NUMBER]', alien_registration_number), ('[DRIVER_LICENSE]', driver_license), ('[ARMY_NUMBER]', army_number), ('[IP_ADDRESS]', ip_address), ('[MAC]', mac), ('[URL]', url), ('[PHONE_NUMBER]', phone_number)] if var_value]


def pattern_matching_filter(label, target_sentense):
    if label == '[PHONE_NUMBER]':
        regex = r'(?<![1-9])(?:02|031|032|033|041|042|043|044|051|052|053|054|055|061|062|063|067)\d{7,8}(?![1-9])|(?<![1-9])010\d{8}(?![1-9])|(?<![1-9])(?:02|031|032|033|041|042|043|044|051|052|053|054|055|061|062|063|067)[\s-]\d{3,4}[\s-]\d{4}(?![1-9])|(?<![1-9])010[\s-]\d{4}[\s-]\d{4}(?![1-9])'
    elif label == '[EMAIL]':
        regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    elif label == '[RESIDENT_REGISTRATION_NUMBER]':
        regex = r'(?<![1-9])\d\d[01][0-9][0-3][0-9]-[1234]\d{6}(?![1-9])'
    elif label == '[PASSPORT_NUMBER]':
        regex = r'[MmSsOoRrDdTt]\s?\d{8}|[Tt][Cc]\s?\d{7}(?![1-9])'
    elif label == '[ALIEN_REGISTRATION_NUMBER]':
        regex = r'(?<![1-9])\d\d[01][0-9][0-3][0-9]-[5678]\d{6}(?![1-9])'
    elif label == '[DRIVER_LICENSE]':
        regex = r'(?<![1-9])[12][0-9]-[0-9][0-9]-[0-5]\d{5}-[0-9][0-9](?![1-9])|(?<![1-9])[12][0-9][0-9][0-9][0-5]\d{5}[0-9][0-9](?![1-9])'
    elif label == '[ACCOUNT_NUMBER]':
        regex = r'\d{3}-(?:13|20|19|11|22)-\d{6}|\d{3}-(?:01|02|03|13|07|09|04)|\d{3}-\d{6}-(?:01|02|03|13|07|06|04)-\d{3}|\d{4}(?:01|02|21|24|05|04|25|26|07)-\d{2}-\d{6}|\d{3}-\d{6}-\d{3}(?:05|07|08|02|01|04|94|37|32|60)|(?:101|201|102|202|209|103|208|106|108|113|114|206)\d-\d{4}-\d{4}|\d{3}-(?:01|02|06|08|40)-\d{8}-\d|\d{3}-(?:01|02|12|06|05|17)-\d{6}|\d{4}-(?:01|02|12|06|05|17)-\d{6}|(?:351|352|356|355|354|360|384|394|398|028)-\d{4}-\d{4}-\d{2}|(?:351|352|356|355|354|360|384|394|398|028)-\d{4}-\d{4}-\d{3}|1(?:006|007|002|004|003|005)-\d{3}-\d{6}|\d{3}-\d{6}-(?:18|92)-\d{3}|\d{3}-(?:10|20|30|85)-\d{6}|\d-(?:15|16)-\d{9}|10\d-\d{3}-\d{6}|1[12345][0-9]-\d{3}-\d{6}|(?:160|161)-\d{3}-\d{6,7}|\d{3}-\d{5}-(?:01|11|21|25|31|42|51|71|81|23|05|06|15|26|29|07|27|55|99|03|13|33|41|43|53|63|24)\d-\d{2}|\d-\d{6}-\d(?:25,41,24,18)-\d{2}|(?:505|508|502|501|504|519|520|521|524|525|527|528|937)-\d{2}-\d{6}-\d|9(?:002|003|004|072|090|091|092|093|200|202|205|207|208|209|210|212|005)-\d{4}-\d{4}-\d|(?:100-2|100-5)\d{2}-\d{6}|3(?:333|388|355|310)-\d{2}-\d{7}|7(?:777|979)-\d{2}-\d{7}|9101-\d{2}-\d{7}|(?:100|106|300|150|700)\d-\d{4}-\d{4}|(?:17|19)\d{2}-\d{4}-\d{4}'
    elif label == '[ARMY_NUMBER]':
        regex = r'(?<![1-9])\d\d-(?:1|2|3)\d{4}(?![1-9])|(?<![1-9])\d\d-5\d{5}(?![1-9])|(?<![1-9])\d\d-7(?:0|1|2|3|6|7|)\d{6}(?![1-9])|(?<![1-9])\d\d-9(?:1|2|3|4|6|7|8)\d{5}(?![1-9])'
    elif label == '[IP_ADDRESS]':
        regex = r'(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)'
    elif label == '[MAC]':
        regex = r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b'
    elif label == '[URL]':
        regex = r'https?:\/\/(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+\/?[a-zA-Z0-9@:%_\+.~#?&//=]*|www\.[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+\/?[a-zA-Z0-9@:%_\+.~#?&//=]*|\b(?<!@)(?:[a-zA-Z0-9-]+\.)+(?:com|co\.kr|go\.kr|ac\.kr|re\.kr)\b(?![a-zA-Z])'
    matched_list = list(dict.fromkeys(re.findall(regex, target_sentense)))
    for index, value in enumerate(matched_list):
        if index == 0:
            target_sentense = target_sentense.replace(value, label)
        else:
            target_sentense = target_sentense.replace(value, label[:-1] + '_' + str(index+1) +']')
    return target_sentense

second_selected_fields = sorted([
    var_name for var_name, value in zip(
        [
            '[AGE]', '[BANK]', '[BLOOD_TYPE]', '[CITY]', '[DATE]', '[DATE_INTERVAL]', '[DATE_OF_BIRTH]', '[DETAILED_ADDRESS]', '[DISTRICT]', '[DURATION]', '[EMPLOYEE_NUMBER]', '[EMPLOYMENT_TYPE]', '[GENDER]', '[GPA]', '[IQ]', '[JOB]', '[MONEY]', '[NAME]','[NATIONALITY]', '[ORDER_NUMBER]', '[ORGANIZATION]', '[PASSWORD]', '[ROAD_NAME_ADDRESS]', '[SCHOOL_NAME]', '[STATE]', '[STATISTICS]', '[STUDENT_NUMBER]', '[TIME]', '[ZIP_CODE]'
        ],
        [
            age, bank, blood_type, city, date, date_interval, date_of_birth, detailed_address, district, duration, employee_number, employment_type, gender, gpa, iq, job, money, name, nationality, order_number, organization, password, road_name_address, school_name, state, statistics, student_number, time, zip_code
        ]
    ) if value
])

ai_act_template = '''
너는 LLM을 윤리에 맞게 안전하게 사용하는지 감시하는 챗봇이야.
아래의 비윤리적인 시스템 예시에 해당하는 경우 1을 출력하고, 그렇지 않은 경우 0을 출력해.

비윤적인 시스템 예시: 공공 당국이 또는 공공 당국을 대신하여 자연인의 공공지원서비스를 지원하는 시스템(예: 긴급복지제도, 긴급사회복지제도, 의료복지대상자선정 등)

출력 예시1:
사용자 입력: 안녕, 내 이름은 임을영이야.
출력: 0

출력 예시2:
사용자 입력: 민원인은 30살이고, 소득이 201만원이야. 가족은 없고, 재산은 2천만원이 있는데, 부채가 4천만원이 있어. 서울에 거주하고 있는데, 4개월전에 교정시설에서 출소한 이력이 있어. 긴급사회복지를 신청했는데 대상자가 맞는지 확인해줘.
출력: 1

출력 예시3: 
사용자 입력: 아래의 공문을 요약해줘. 
공무로 인한 공가를 신청하오니 결재하여 주시기 바랍니다.
이름: 임을영
소속: 전산1팀
날짜: 4월 2일~10일
출력: 0

출력 예시4:
사용자 입력: 아래 내용을 이메일 형태로 변경해줘.
서울시에 공공주택 20만호 공급예정.
인천광역시 oo구 9월 중 재개발 승인 예정
출력: 0

! 아래의 사용자 입력을 판단하시오.
사용자 입력: {PROMPT}
출력: 
'''

with col1:
    if prompt := st.chat_input("Message Gov-STAGE"):
        #ai_act_status = solar.invoke(ai_act_template.format(**{"PROMPT" : prompt})).content.strip('"')
        if len(st.session_state.chat_history) == 0:
            placeholder.empty()
            col1_1.markdown("<h5 style='text-align: center; color: black;'>User Interface</h5>", unsafe_allow_html=True)
            col1_2.markdown("<h5 style='text-align: center; color: black;'>Internal Processing</h5>", unsafe_allow_html=True)
            st.session_state.subject = solar.invoke(f"'{prompt}'에 대한 3단어 이하의 간결한 제목을 제안해 주세요.").content.strip('"')
        with col1_1:
            with st.chat_message("Human"):
                st.markdown(prompt)
        st.session_state.chat_history.append(("Human", prompt))
        chat_history = "\n".join([f"{role}: {message}" for role, message in st.session_state.chat_history[-5:]])
        chat_history2 = chat_history
        with col1_2: 
            with st.spinner("De-identification in progress...."): 
                if(mode_on):
                    for label in first_selected_fields:
                        chat_history = pattern_matching_filter(label, chat_history)
                    anonymized_chat_history = lorax_client.generate(anonymization_prompt_template.format(**{"original_sentences": chat_history, "List_of_PII" : second_selected_fields}), adapter_id='solarism_v1/5', max_new_tokens=1000).generated_text
                else:
                    anonymized_chat_history = chat_history
            matches = re.findall(r'(?:Human: )(.*?)(?=AI: |$)|(?:AI: )(.*?)(?=Human: |$)', anonymized_chat_history, re.DOTALL)
            filtered_matches = [match[0] if match[0] else match[1] for match in matches if match[0] or match[1]]
            with st.chat_message("Human"):
                st.markdown(filtered_matches[len(st.session_state.anonymized_chat_history)])
                st.session_state.anonymized_chat_history.append(("Human", filtered_matches[len(st.session_state.anonymized_chat_history)]))
        
        with col1_1:
            with st.spinner("Generating response...."): 
                with col1_2:
                    with st.spinner("Generating response...."):
                        if model_type == "solar-1-mini(fine_tuned)":
                            anonymized_response = lorax_client.generate(conversation_prompt_template.format(**{"system_prompt":system_prompt ,"anonymized_chat_history":anonymized_chat_history}), adapter_id='solar kdis/14', max_new_tokens=1000).generated_text
                        elif model_type == "gpt-4o":
                            anonymized_response = gpt4o.invoke(conversation_prompt_template.format(**{"system_prompt":system_prompt ,"anonymized_chat_history":anonymized_chat_history})).content
                        else:
                            anonymized_response = llama3.invoke(conversation_prompt_template.format(**{"system_prompt":system_prompt ,"anonymized_chat_history":anonymized_chat_history})).content

        with col1_1:
            with st.spinner("Re-identification in progress...."): 
                with col1_2:
                    with st.spinner("Re-identification in progress...."):
                        if(mode_on):
                            restored_response = lorax_client.generate(restoration_prompt_template.format(**{"original_conversaion_sentence": chat_history2, "anonymized_conversation_history": anonymized_chat_history, "sentence_to_be_restored": anonymized_response}), adapter_id='solarism_v1/5', max_new_tokens=1000).generated_text
                            #if(ai_act_status == "1"):
                            #    restored_response = "**⛔Alert** \n\n**필수 민간 및 공공 서비스 용도로 AI를 활용하는 것은 금지입니다.**\n\n*근거조항: EU AI Act 제6조 제2항, 부속서3 5호 (a)*\n\n" + restored_response
                        else:
                            restored_response = anonymized_response
        with col1_1:
            with st.chat_message("AI"):
                st.markdown(restored_response)
                st.session_state.chat_history.append(("AI", restored_response))
        with col1_2:
            with st.chat_message("AI"):
                st.markdown(anonymized_response)
                st.session_state.anonymized_chat_history.append(("AI", anonymized_response))
        save_conversation_to_db('govstage.db', prompt, restored_response, filtered_matches[-1], anonymized_response, st.session_state.subject)
        if len(st.session_state.chat_history) <= 2:
            st.rerun()
