# Gov-STAGE

## 1. Overview
Gov-STAGE is a powerful system designed to help enterprises and public institutions securely utilize Large Language Models (LLM) while ensuring personal data protection. Our solution integrates a Personal Data Identification and Re-identification system that prevents sensitive data from being exposed to external threats during the use of AI-powered services.

Key Features:
- **Private LLM Integration**: A dedicated, fine-tuned Private LLM, based on the Solar Mini model, is deployed locally to handle the detection and anonymization of personal information.
- **Secure Public LLM Queries**: Once the data is anonymized, it is safely transmitted to Public LLMs like ChatGPT or Claude, ensuring the sensitive information is never compromised.
- **Re-identification and Data Restoration**: If necessary, responses from Public LLMs can be re-identified using the internal Private LLM within the organization, making the process seamless and secure.

Gov-STAGE enables public institutions and enterprises to embrace advanced AI technologies without compromising on data privacy and compliance with global data protection regulations such as GDPR and local privacy laws.

## 2. Package Installation
To install the required packages, run the following command:

```
pip install -r requirements.txt
```

## 3. How to Run
1. Place your key value into the **.env** file.
2. Navigate to the directory where the `main.py` file is located.
3. Start the application with the following command:

```
streamlit run main.py
```

## 4. Sample Screen
Below is a sample screen of Gov-STAGE in action (left: user interface, right: data sent to the Public LLM):

![image](https://github.com/user-attachments/assets/cbfaa178-eeea-4817-8f06-a6032838cda9)

In this example:
- Personal information such as names, addresses, and dates are automatically anonymized before being sent to an Public LLM.
- The right-side menu shows the customizable list of personal data types that can be anonymized based on your requirements.
- Once the response is generated, re-identification is applied where needed, restoring the necessary information while keeping other data anonymized.

## 5. Demo Webpage
Experience a live demo of Gov-STAGE at [https://gov-stage.com](https://gov-stage.com).

## 6. Demo Video
Watch our demo video at [https://kr.object.gov-ncloudstorage.com/temp/Gov-STAGE_demo.mp4](https://kr.object.gov-ncloudstorage.com/temp/Gov-STAGE_demo.mp4).
[![Gov-STAGE Demo Video](https://img.youtube.com/vi/OlQq6_1hXUo/maxresdefault.jpg)](https://youtu.be/OlQq6_1hXUo)

## 7. Future Plan
Gov-STAGE is continuously evolving to meet the growing needs of public institutions and enterprises. Our upcoming features and improvements include:
- **Expanded Regulatory Compliance**: Supporting major global regulations like GDPR, CPRA, and Local Privacy laws with over 50 types of personal information for de-identification.
- **Multi-language Support**: Currently supporting 10+ languages with plans for continuous expansion.
- **AI Ethics Integration**: Embedding AI ethics principles tailored to the organization’s unique requirements, ensuring ethical and responsible AI usage.
- **Enterprise-grade Safety**: Built on proven chatbot technology, ensuring robust security and reliability for large-scale enterprise deployments.

By adopting Gov-STAGE, organizations can securely leverage LLM capabilities while staying compliant and protecting sensitive information.
