# 🍳 Recipe Doctor - AI Chef Assistant

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Transform your available ingredients into delicious recipes with AI-powered culinary creativity!

**Recipe Doctor** is an intelligent Streamlit web application that generates personalized recipes based on whatever ingredients you have on hand. Powered by Google's Gemini AI, it helps home cooks reduce food waste and discover new meal ideas effortlessly.

---

## ✨ Features

### 🤖 AI-Powered Recipe Generation
* **Ingredient-based creation:** List what you have, get recipes instantly.
* **Intelligent parsing:** Extracts ingredients from natural language input.
* **Detailed instructions:** Step-by-step cooking guidance with specific times and temperatures.

### 🎨 Smart Filtering & Personalization
* **Dietary preferences:** Vegetarian, Vegan, Gluten-Free, Dairy-Free, Nut-Free, Low-Carb.
* **Cuisine styles:** Italian, Asian, Mexican, Indian, Mediterranean, American.
* **Skill levels:** Beginner, Intermediate, Expert.
* **Meal types:** Breakfast, Lunch, Dinner, Snack, Dessert.

### 📱 User-Friendly Interface
* Beautiful recipe cards with gradient designs.
* Visual ingredient chips for easy scanning.
* Interactive step-by-step instructions.
* Responsive layout for all devices.

### 💾 Organizational Features
* Save favorite recipes for future use.
* Shopping list builder from recipe ingredients.
* Clear all/Reset options for fresh starts.
* Session persistence across navigation.

---

## 🚀 Quick Start

### Prerequisites
* Python 3.8+
* Google Gemini API key ([Get one here](https://aistudio.google.com/))
* Streamlit

### Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/yourusername/recipe-doctor.git](https://github.com/yourusername/recipe-doctor.git)
   cd recipe-doctor

2. **Install dependencies**
    pip install streamlit google-genai

3. **Set up API key**
* **Option A:** Create `.streamlit/secrets.toml` file:
    ```toml
    GEMINI_API_KEY = "your-api-key-here"
* **Option B:** Enter API key directly in the app's Settings page.

4. **Run the application**
    streamlit run app.py

