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
            gender = st.checkbox("Gender", value=True)
            phone_number = st.checkbox("Phone Number", value=True)
            birthdate = st.checkbox("Date of Birth", value=True)
            address = st.checkbox("Address", value=True)
            card_number = st.checkbox("Card Number", value=True)
            email = st.checkbox("Email", value=True)
            ip_address = st.checkbox("IP Address", value=True)
            password = st.checkbox("Password", value=True)
            date = st.checkbox("Date", value=True)
            birth_place = st.checkbox("Place of Birth")
            permanent_address = st.checkbox("Permanent Address")
            nationality = st.checkbox("Nationality")

        with st.expander("Unique Identifiable Information"):
            resident_registration_number = st.checkbox("Resident Registration Number", value=True)
            foreigner_registration_number = st.checkbox("Foreigner Registration Number", value=True)
            driver_license_number = st.checkbox("Driver's License Number", value=True)
            passport_number = st.checkbox("Passport Number", value=True)

    else:
        with st.expander("General Personal Information"):
            name = st.checkbox("Name", value=True, disabled=True)
            age = st.checkbox("Age", value=True, disabled=True)
            gender = st.checkbox("Gender", value=True, disabled=True)
            phone_number = st.checkbox("Phone Number", value=True, disabled=True)
            birthdate = st.checkbox("Date of Birth", value=True, disabled=True)
            address = st.checkbox("Address", value=True, disabled=True)
            card_number = st.checkbox("Card Number", value=True, disabled=True)
            email = st.checkbox("Email", value=True, disabled=True)
            ip_address = st.checkbox("IP Address", value=True, disabled=True)
            password = st.checkbox("Password", value=True, disabled=True)
            date = st.checkbox("Date", value=True, disabled=True)
            birth_place = st.checkbox("Place of Birth")
            permanent_address =st.checkbox("Permanent Address")
            nationality =st.checkbox("Nationality")
        with st.expander("Unique Identifiable Information"):
            resident_registration_number =  st.checkbox("Resident Registration Number", value=True, disabled=True)
            foreigner_registration_number =  st.checkbox("Foreigner Registration Number", value=True, disabled=True)
            driver_license_number =  st.checkbox("Driver's License Number", value=True, disabled=True)
            passport_number =  st.checkbox("Passport Number", value=True, disabled=True)
    st.divider()
    st.markdown("##### Role")
    system_prompt = st.text_area("system prompt",value="You are an office assistant at Jeju Special Self-Governing Province Development Co., responsible for promptly and accurately answering work-related questions from staff. Respond in a friendly and easy-to-understand language, while maintaining the professionalism and credibility of a public institution.")
    model_type = st.selectbox("model type",("gpt-4o", "llama3.1-405b", "solar-1-mini(fine_tuned)"),)
    st.divider()
    st.markdown("##### Jeju island🌊🌴")
    st.audio("music.mp3", format="audio/mpeg", loop=True)

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
    # The following code calls the Solar Mini API, which is used to determine the name of the chat session.
    load_dotenv(verbose=True)
    model = ChatUpstage()
    print("solar-1-mini-chat loaded...")
    return model

@st.cache_resource
def load_model2():
    # The following code is a function that calls a fine-tuned Solar Mini model. It detects personal information in the user prompt and performs decryption if necessary.
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

anonymization_prompt_template = """<|im_start|>system\n You are a personal data anonymization system. Anonymize the personal information in the sentences provided below as instructed. However, do not anonymize the personal information of public figures (e.g., celebrities, politicians, athletes).

Anonymization Rules:
1. Personal information to be anonymized: {List_of_PII}
2. Do not anonymize any information other than the personal information listed above.
3. Exceptions to anonymization:
   - Information about public figures (politicians, celebrities, athletes) and individuals who have been deceased for more than 5 years.
4. Examples of anonymization(Use placeholder):
   - Name: [NAME], [NAME2]
   - Age: [AGE]
   - Gender: [GENDER]
   - Date of Birth: [DOB], [DOB2]
5. Conversation format: Each turn of the anonymized conversation must be prefixed with 'Human:' and 'AI:'.

Original sentences: <|im_end|>\n<|im_start|>user\n 
{original_sentences}\n
Anonymized sentences (without additional comments or responses):<|im_end|>\n<|im_start|>assistant\n
"""

restoration_prompt_template  = """<|im_start|>system\nYou are a personal data restoration system.
Restore the placeholders such as [NAME], [NAME2], [DOB], [DOB2], [ADDRESS], [ADDRESS2] to their original form based on the reference conversation below.
The sentence to be restored may or may not be anonymized with placeholders. If it is anonymized, perform the restoration; if not, output the sentence to be restored as it is.
Ensure the restored sentence makes sense in context.<|im_end|>\n<|im_start|>user\n
Conversation history(reference conversation): 
{original_conversaion_sentence}

Anonymized Conversation history(reference conversation):
{anonymized_conversation_history}

Sentence to be restored: 
{sentence_to_be_restored}

Restored sentence(without any additional comments or responses):<|im_end|>\n<|im_start|>assistant\n"""

selected_fields = [
    var_name for var_name, value in zip(
        [
            'name', 'age', 'gender', 'phone_number', 'birthdate', 
            'address', 'card_number', 'email', 'ip_address', 'password', 
            'date', 'birth_place', 'permanent_address', 'nationality', 
            'resident_registration_number', 'foreigner_registration_number', 
            'driver_license_number', 'passport_number'
        ],
        [
            name, age, gender, phone_number, birthdate, 
            address, card_number, email, ip_address, password, 
            date, birth_place, permanent_address, nationality, 
            resident_registration_number, foreigner_registration_number, 
            driver_license_number, passport_number
        ]
    ) if value
]

with col1:
    if prompt := st.chat_input("Message Gov-STAGE"):
        if len(st.session_state.chat_history) == 0:
            placeholder.empty()
            col1_1.markdown("<h5 style='text-align: center; color: black;'>User Interface</h5>", unsafe_allow_html=True)
            col1_2.markdown("<h5 style='text-align: center; color: black;'>Internal Processing</h5>", unsafe_allow_html=True)
            st.session_state.subject = solar.invoke(f"'{prompt}'에 대한 3단어 이하의 간결한 제목을 제안해 주세요.").content.strip('"') # Determine the title of the chat session using the Solar Mini API
        with col1_1:
            with st.chat_message("Human"):
                st.markdown(prompt)
        st.session_state.chat_history.append(("Human", prompt))
        chat_history = "\n".join([f"{role}: {message}" for role, message in st.session_state.chat_history[-5:]])
        with col1_2: 
            with st.spinner("De-identification in progress...."): 
                # Detect personal information in the prompt and perform de-identification.
                if(mode_on):
                    anonymized_chat_history = lorax_client.generate(anonymization_prompt_template.format(**{"original_sentences": chat_history, "List_of_PII" : selected_fields}), adapter_id='solar anonymization/22', max_new_tokens=1000).generated_text
                else:
                    anonymized_chat_history = chat_history
            matches = re.findall(r'(?:Human:)(.*?)(?=AI:|$)|(?:AI:)(.*?)(?=Human:|$)', anonymized_chat_history, re.DOTALL | re.IGNORECASE)
            filtered_matches = [match[0] if match[0] else match[1] for match in matches if match[0] or match[1]]
            with st.chat_message("Human"):
                st.markdown(filtered_matches[-1])
                st.session_state.anonymized_chat_history.append(("Human", filtered_matches[-1]))
        
        with col1_1:
            with st.spinner("Generating response...."): 
                with col1_2:
                    with st.spinner("Generating response...."):
                        if model_type == "solar-1-mini(fine_tuned)":
                            # Query the Solar Mini, which has been trained on guidelines from a public institution (KDI School).
                            anonymized_response = lorax_client.generate(conversation_prompt_template.format(**{"system_prompt":system_prompt ,"anonymized_chat_history":anonymized_chat_history}), adapter_id='solar kdis/14', max_new_tokens=1000).generated_text
                        elif model_type == "gpt-4o-mini":
                            anonymized_response = gpt4o.invoke(conversation_prompt_template.format(**{"system_prompt":system_prompt ,"anonymized_chat_history":anonymized_chat_history})).content
                        else:
                            anonymized_response = llama3.invoke(conversation_prompt_template.format(**{"system_prompt":system_prompt ,"anonymized_chat_history":anonymized_chat_history})).content

        with col1_1:
            with st.spinner("Re-identification in progress...."): 
                with col1_2:
                    with st.spinner("Re-identification in progress...."):
                        # Restore personal information from the response of a public LLM.
                        if(mode_on):
                            restored_response = lorax_client.generate(restoration_prompt_template.format(**{"original_conversaion_sentence": chat_history, "anonymized_conversation_history": anonymized_chat_history, "sentence_to_be_restored": anonymized_response}), adapter_id='solar anonymization/22', max_new_tokens=1000).generated_text
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
