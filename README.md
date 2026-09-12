\# 🌱 Crop Disease AI



An AI-powered tomato crop disease detection and agricultural assistance system that uses deep learning for disease classification and a real-time AI agent for treatment and management guidance.



\## 🚀 Project Overview



Crop Disease AI is a Flask-based web application designed to help identify tomato leaf diseases from images.



The system uses a trained YOLO11 classification model to predict the disease class and confidence score. After prediction, a real-time agricultural AI agent searches the web for relevant agricultural information and uses Llama 3.2 through Ollama to generate practical disease-management guidance.



\### Complete Workflow



User Upload

↓

Tomato Leaf Image

↓

YOLO11 Disease Classification

↓

Disease Prediction + Confidence

↓

Real-Time Agricultural Web Search

↓

Ollama / Llama 3.2

↓

AI-Generated Disease Information

↓

Treatment \& Prevention Recommendations



\---



\## 🎯 Objectives



\- Detect tomato leaf diseases using deep learning.

\- Provide disease prediction with confidence.

\- Provide information about symptoms and causes.

\- Retrieve current agricultural information from the web.

\- Generate practical treatment and prevention guidance.

\- Provide an easy-to-use web interface for farmers and users.



\---



\## 🤖 Machine Learning Model



The project uses a YOLO11 classification model trained specifically for tomato leaf disease classification.



\### Model



\- Architecture: YOLO11

\- Model: YOLO11n Classification

\- Training epochs: 30

\- Training images: 10,000

\- Validation images: 1,000

\- Number of classes: 10



\### Validation Performance



| Metric | Result |

|---|---:|

| Top-1 Accuracy | 99.6% |

| Top-5 Accuracy | 100% |



\---



\## 🦠 Supported Diseases



The model supports the following 10 tomato classes:



1\. Bacterial Spot

2\. Early Blight

3\. Healthy

4\. Late Blight

5\. Leaf Mold

6\. Septoria Leaf Spot

7\. Spider Mites / Two-Spotted Spider Mite

8\. Target Spot

9\. Tomato Mosaic Virus

10\. Tomato Yellow Leaf Curl Virus



\---



\## 🧠 Real-Time Agricultural AI Agent



A major feature of this project is the agricultural AI agent.



Instead of displaying only predefined disease information, the system performs real-time web searches based on the detected disease.



The retrieved information is then provided to Llama 3.2 through Ollama.



\### Agent Workflow



Disease Prediction

→

Web Search

→

Agricultural Information Retrieval

→

Llama 3.2

→

Structured Agricultural Guidance



The agent can provide:



\- Disease overview

\- Possible causes

\- Common symptoms

\- Severity information

\- Immediate actions

\- Treatment / management

\- Prevention

\- When expert confirmation may be required

\- Reference sources



The agent is designed to distinguish between the model's prediction and a confirmed agricultural diagnosis.



\---



\## 🌐 Web Application



The application is developed using Flask.



\### Main Features



\- Image upload

\- Tomato disease prediction

\- Confidence score

\- Disease information

\- AI-generated agricultural guidance

\- Real-time web search

\- Treatment recommendations

\- Prevention recommendations

\- Disease information pages

\- Dashboard interface



\---



\## 🏗️ System Architecture



```text

&#x20;                   ┌──────────────────────┐

&#x20;                   │       User           │

&#x20;                   │ Upload Leaf Image    │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │    Flask Web App     │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   YOLO11 Classifier  │

&#x20;                   │   Tomato Disease ML  │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                     Prediction + Confidence

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   Crop AI Agent      │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;               ┌──────────────┴──────────────┐

&#x20;               ▼                             ▼

&#x20;      ┌────────────────┐            ┌────────────────┐

&#x20;      │ Real-Time Web  │            │ Ollama         │

&#x20;      │ Search         │            │ Llama 3.2      │

&#x20;      └───────┬────────┘            └───────┬────────┘

&#x20;              │                             │

&#x20;              └──────────────┬──────────────┘

&#x20;                             ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Agricultural Advice  │

&#x20;                   │ Treatment \&          │

&#x20;                   │ Prevention           │

&#x20;                   └──────────────────────

