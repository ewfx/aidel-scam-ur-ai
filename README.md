# 🚀 Ganda hai par Dhandha hai

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
This project helps analysing risk from transaction in real-time and gives a comprehensive Risk Report💥.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
Real-time risk analysis is much required for analysing transactions involving new entities for which banks may not have any history. Latest news articles, sanction lists or information about the entities involved along with reviewing key transaction details can help in analysing risk in realtime and blocking such transactions.

## ⚙️ What It Does
This solution extracts entities from the transaction, searches from them in the open-source databases and news and fetches data from them to finally generates a risk analysis report.

## 🛠️ How We Built It
We have used ReactJS, Tailwind CSS and Radix UI on frontend and FastAPI on the backend. For our external data sources where we look for entities we are using OFAC API, Wikidata, NewsAPI, ICIJ Leaks API and locally downloaded files containing list of sanctioned entities and PEPs. For Entity Recognition, sentiment analysis from News Articles and overall risk scoring and risk analysis we are using Gemini API Free Tier with the Gemini 2.0 Flash model.

## 🚧 Challenges We Faced
- Handling Entities not found in any data sources like Wikidata, sanctions, news etc.
- Assigning a Risk score, Confidence Score based on whatever data we collected from our external data sources
- Handling rate limitations and quotas on certain APIs like OFAC API and News API which could result in less data available for Risk Analysis.

## 🏃 How to Run
1. Clone the repository  
   ```
   git clone https://github.com/ewfx/aidel-scam-ur-ai.git
   ```
2. Install dependencies  
   ```
   cd code/src
   pip install -r requirements.txt
   ```
3. Run the project  
   ```
   uvicorn app:app --reload
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: ReactJS, TailwindCSS, RadixUI
- 🔹 Backend:  FastAPI
- 🔹 Database: None
- 🔹 Other: Gemini API, OFAC API, News api, WikiData, Sanctions Lists, ICIJ Leaks API

## 👥 Team
- **Mayank Panda** - [GitHub](#) | [LinkedIn](#)
- **Harshit Bhalla** - [GitHub](#) | [LinkedIn](#)
- **Keerthana S** - [GitHub](#) | [LinkedIn](#)
- **Himanshu Wadhwa** - [GitHub](https://github.com/ninjacode01) | [LinkedIn](#)
