# 🎬 Movie Analytics & Recommendation System

A Netflix-style analytics and recommendation system built using the MovieLens dataset.  
This project was developed as part of a final assessment for a streaming technology company scenario, combining data analysis, machine learning, and deployment using Streamlit.

---

## 📌 Project Overview

This project analyses large-scale movie ratings and metadata to generate actionable insights and build recommendation systems. It demonstrates how machine learning can be applied to real-world streaming platforms for content discovery, personalization, and user engagement.

---

## 🎯 Objectives

- Analyse movie ratings and metadata at scale  
- Extract actionable business insights  
- Build and evaluate multiple recommendation models  
- Deploy an interactive Streamlit application  
- Demonstrate business value for content strategy and retention  

---

## 🤖 Recommendation Models

### 1. Baseline & Machine Learning Models
- Weighted popularity baseline  
- Ridge Regression  
- Logistic Regression  
- Lasso Regression  
- Decision Tree  
- Random Forest  
- K-Nearest Neighbours (KNN)  
- Gradient Boosting  

Used for trending content and general ranking recommendations.

### 2. Content-Based Filtering
- Uses genre and tag similarity  
- Recommends movies similar to those a user likes  
- Helps with discovery for new or inactive users  

### 3. Collaborative Filtering
- User–user similarity approach  
- Recommends movies based on similar user preferences  
- Enables personalised recommendations  

---

## 🖥️ Application Features

- Interactive analytics dashboard (Streamlit)  
- Movie similarity recommendations  
- User-based recommendations  
- Clean, fixed-size movie card UI  
- Handles missing movie posters gracefully  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Scikit-learn  
- Plotly  

---

## 🚀 How to Run

Clone the repository and run the Streamlit app:

```bash
streamlit run my_app.py
