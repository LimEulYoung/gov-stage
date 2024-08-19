## 1. Overview
- This system supports enterprises in safely utilizing LLM by providing a personal data identification and re-identification system.
- It uses a dedicated Private LLM installed locally to perform identification and re-identification tasks, and queries an external LLM to ensure the personal data remains secure from external threats.

## 2. Package Installation
- To install the required packages, run the following command:
  ```
  pip install -r requirements.txt
  ```

## 3. How to Run
- Put your key value into the **.env** file.
- To start the application, navigate to the directory where the `main.py` file is located and run the following command:
  ```
  streamlit run main.py
  ```

## 4. Sample Screen (left: user interface, right: data sent to the external LLM)
![image](https://github.com/user-attachments/assets/761b08c5-6398-499a-9f01-e674a42fbaae)

## 5. Demo Webpage
- Please conduct a demo of **gov-stage** at [https://gov-stage.com](https://gov-stage.com).

## 6. Demo Video
- Please watch the demo video at [https://kr.object.gov-ncloudstorage.com/temp/Gov-STAGE_demo.mp4](https://kr.object.gov-ncloudstorage.com/temp/Gov-STAGE_demo.mp4).
