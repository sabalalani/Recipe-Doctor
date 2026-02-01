🍳 Recipe Doctor - AI Chef Assistant
https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white
https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white

Transform your available ingredients into delicious recipes with AI-powered culinary creativity!

Recipe Doctor is an intelligent Streamlit web application that generates personalized recipes based on whatever ingredients you have on hand. Powered by Google's Gemini AI, it helps home cooks reduce food waste and discover new meal ideas effortlessly.

✨ Features
🤖 AI-Powered Recipe Generation
Ingredient-based creation: List what you have, get recipes instantly

Intelligent parsing: Extracts ingredients from natural language input

Detailed instructions: Step-by-step cooking guidance with specific times and temperatures

🎨 Smart Filtering & Personalization
Dietary preferences: Vegetarian, Vegan, Gluten-Free, Dairy-Free, Nut-Free, Low-Carb

Cuisine styles: Italian, Asian, Mexican, Indian, Mediterranean, American

Skill levels: Beginner, Intermediate, Expert

Meal types: Breakfast, Lunch, Dinner, Snack, Dessert

📱 User-Friendly Interface
Beautiful recipe cards with gradient designs

Visual ingredient chips for easy scanning

Interactive step-by-step instructions

Responsive layout for all devices

💾 Organizational Features
Save favorite recipes for future use

Shopping list builder from recipe ingredients

Clear all/Reset options for fresh starts

Session persistence across navigation

🚀 Quick Start
Prerequisites
Python 3.8+

Google Gemini API key (Get one here)

Streamlit

Installation
Clone the repository

bash
git clone https://github.com/yourusername/recipe-doctor.git
cd recipe-doctor
Install dependencies

bash
pip install streamlit google-genai
Set up API key

Option A: Create .streamlit/secrets.toml file:

toml
GEMINI_API_KEY = "your-api-key-here"
Option B: Enter API key directly in the app's Settings page

Run the application

bash
streamlit run app.py
📖 How to Use
1. Generate Recipes
Navigate to "🧑‍🍳 Generate Recipes"

Enter ingredients you have (comma-separated): eggs, milk, bread, cheese, tomatoes

Set your preferences (dietary, cuisine, skill level)

Click "🧠 Generate with AI"

View your custom recipe with detailed instructions

2. Save & Organize
Save recipes: Click "💾 Save" to add to your collection

Shopping list: Click "🛒 Add to List" to populate shopping list

View saved: Navigate to "💾 Saved Recipes"

Manage shopping: Go to "🛒 Shopping List"

3. Customize Experience
Adjust cooking difficulty in sidebar

Select dietary restrictions

Choose preferred cuisine styles

Toggle debug mode for technical details

🏗️ Architecture
Core Components
main(): Application entry point and navigation controller

generate_recipes_with_gemini(): AI recipe generation engine

parse_gemini_response(): Intelligent response parser

render_*() functions: Modular UI rendering components

Key Dependencies
Streamlit: Web application framework

Google Gemini AI: Recipe generation and natural language processing

Session State: User data persistence across interactions

🔧 Configuration
Environment Variables
bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
Customization Options
Modify CSS in the Custom CSS section for branding

Adjust AI parameters in generate_recipes_with_gemini():

temperature: Controls creativity (0.0-1.0)

max_output_tokens: Response length (100-1000)

Model selection: Choose between Gemini versions

🧪 Testing
Manual Testing
Test with various ingredient combinations

Verify dietary restriction filtering

Check shopping list functionality

Test recipe saving and retrieval

Common Test Cases
python
# Simple ingredients
"eggs, milk, bread"

# Complex ingredients
"chicken breast, bell peppers, onion, garlic, olive oil, paprika"

# Dietary-specific
"tofu, broccoli, soy sauce, ginger" (for vegan)
📊 Performance
Response Time: 2-5 seconds for recipe generation

Concurrent Users: Limited by Streamlit's free tier

API Limits: Subject to Google Gemini quota

🤝 Contributing
We welcome contributions! Here's how:

Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit changes: git commit -m 'Add amazing feature'

Push to branch: git push origin feature/amazing-feature

Open a Pull Request

Development Guidelines
Follow PEP 8 style guide

Add comments for complex logic

Update README.md for new features

Test changes before submitting

🐛 Troubleshooting
Common Issues
Issue: "Gemini API not available"

Solution: Verify API key in secrets.toml or Settings page

Issue: "No recipes generated"

Solution: Check internet connection and API quota

Issue: "Ingredients not parsed correctly"

Solution: Use comma-separated format or enable debug mode

Issue: "App crashes on reload"

Solution: Clear browser cache or restart Streamlit

Debug Mode
Enable debug mode in sidebar to:

View raw AI responses

See parsing details

Identify API errors

📈 Roadmap
Planned Features
Recipe scaling: Adjust servings automatically

Nutritional analysis: Detailed macro/micro nutrients

Meal planning: Weekly schedule generation

Image generation: AI-generated recipe photos

Voice input: Speak your ingredients

Multilingual support: Generate recipes in different languages

Integration: Connect with grocery delivery services

Current Limitations
Requires stable internet connection

Dependent on Google Gemini API availability

No offline functionality

Basic image support only