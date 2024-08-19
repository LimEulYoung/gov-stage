## 0. Overview
- This system supports enterprises in safely utilizing LLM by providing a personal data identification and re-identification system.
- It uses a dedicated Private LLM installed locally to perform identification and re-identification tasks, and queries an external LLM to ensure the personal data remains secure from external threats.

## 1. Package Installation
- To install the required packages, run the following command:
  ```
  pip install -r requirements.txt
  ```

## 2. How to Run
- To start the application, navigate to the directory where the `main.py` file is located and run the following command:
  ```
  streamlit run main.py
  ```

## 3. Sample Screen (left: user interface, right: data sent to the external LLM)
![image](https://github.com/user-attachments/assets/761b08c5-6398-499a-9f01-e674a42fbaae)
