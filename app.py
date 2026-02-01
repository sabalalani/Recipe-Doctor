import streamlit as st
from google import genai
import json
import time
import random
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Recipe Doctor - AI Chef Assistant",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0;
    }
    .recipe-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 5px solid #FF6B6B;
    }
    .ingredient-item {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 8px 0;
        border-left: 4px solid #4ECDC4;
    }
    .step-item {
        background: #fff9e6;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 8px 0;
        border-left: 4px solid #FFD166;
        counter-increment: step-counter;
    }
    .step-item:before {
        content: counter(step-counter) ".";
        font-weight: bold;
        color: #FF6B6B;
        margin-right: 10px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: bold;
        width: 100%;
    }
    .ingredient-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 10px;
        margin: 15px 0;
    }
    .ingredient-chip {
        background: #e3f2fd;
        padding: 8px 15px;
        border-radius: 20px;
        text-align: center;
        font-weight: 500;
    }
    .timer-alert {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'recipes': None,
        'ingredients': [],
        'saved_recipes': [],
        'shopping_list': [],
        'active_timer': None,
        'timer_start': None,
        'current_tab': "🧑‍🍳 Generate Recipes"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize Gemini
def init_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY", st.session_state.get("api_key", ""))
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            model_name = "gemini-3-flash-preview"
            
            try:
                # Test connection
                response = client.models.generate_content(
                    model=model_name,
                    contents="Test",
                    config={"max_output_tokens": 10}
                )
                st.sidebar.success(f"✅ Connected to {model_name}")
                return client, model_name
            except Exception as e:
                st.sidebar.warning(f"Gemini 3 not available: {str(e)[:100]}")
                
                try:
                    model_name = "gemini-2.5-flash"
                    return client, model_name
                except:
                    return client, "gemini-1.5-flash"
                    
        except Exception as e:
            st.sidebar.error(f"Configuration error: {str(e)[:100]}")
            return None, None
    else:
        st.sidebar.warning("⚠️ No API key found.")
        return None, None

# Simple ingredient detection
def detect_ingredients_from_text(ingredient_text):
    """Extract ingredients from user's text input"""
    ingredients = []
    raw_ingredients = [x.strip() for x in ingredient_text.split(',') if x.strip()]
    
    for ing in raw_ingredients:
        if ing:
            ingredients.append(ing)
    
    return ingredients

# Generate recipes with Gemini - UPDATED
def generate_recipes_with_gemini(ingredients_list, dietary_prefs, cuisine, meal_type, skill_level, client=None, model_name=None):
    """Generate recipes using Gemini text model - NO STATIC RECIPES"""
    if not client or not model_name:
        st.sidebar.error("Gemini API not available.")
        return None
    
    try:
        # STRONG, DIRECT prompt
        prompt = f"""CREATE A DETAILED RECIPE WITH SPECIFIC INSTRUCTIONS:
        
        Ingredients to use: {', '.join(ingredients_list)}
        
        CRITICAL RULES:
        1. Give EXACT cooking steps with specific times and temperatures
        2. NO generic steps like "prepare ingredients" or "cook as desired"
        3. Each step must be a specific action
        4. Include 5-7 detailed steps
        
        Example of GOOD steps:
        1. Heat 2 tbsp oil in a pan over medium heat
        2. Chop onions and sauté for 3 minutes until translucent
        3. Add minced garlic and cook for 30 seconds
        4. Crack eggs into bowl, whisk with milk and salt
        5. Pour egg mixture into pan, cook for 2-3 minutes while stirring
        
        Example of BAD steps:
        1. Prepare ingredients
        2. Cook as desired
        3. Serve and enjoy
        
        Now create a recipe with SPECIFIC steps:
        
        RECIPE NAME: [Name]
        DIFFICULTY: Easy/Medium/Hard
        PREP TIME: [exact time] minutes
        COOK TIME: [exact time] minutes
        SERVINGS: [number]
        CALORIES: [number]
        INGREDIENTS:
        - [Specific ingredient with quantity]
        - [Another ingredient with quantity]
        STEPS:
        1. [FIRST SPECIFIC ACTION with time/temperature]
        2. [SECOND SPECIFIC ACTION with details]
        3. [THIRD SPECIFIC ACTION with details]
        4. [FOURTH SPECIFIC ACTION with details]
        5. [FIFTH SPECIFIC ACTION with details]
        TIPS: [Practical tip]
        NUTRITION: [Nutrition info]"""
        
        # Generate response
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config={
                "temperature": 0.7,
                "top_p": 0.8,
                "max_output_tokens": 1000
            }
        )
        
        response_text = response.text.strip()
        
        # Show raw response for debugging
        if st.session_state.get('show_debug', False):
            st.sidebar.text_area("Gemini Raw Response", response_text, height=300, key="raw_response")
        
        # Parse the response
        return parse_gemini_response(response_text)
            
    except Exception as e:
        st.sidebar.error(f"Generation error: {str(e)}")
        return None

def parse_gemini_response(text):
    """Parse Gemini's response with better step detection"""
    try:
        recipe = {
            'recipe_name': 'AI Recipe',
            'difficulty': 'Easy',
            'prep_time': '10 minutes',
            'cook_time': '15 minutes',
            'servings': 2,
            'calories': '300',
            'ingredients': [],
            'steps': [],
            'tips': 'Enjoy your meal!',
            'nutrition': 'Nutritional information'
        }
        
        lines = text.split('\n')
        current_section = None
        step_number = 1
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for headers (case insensitive)
            line_upper = line.upper()
            
            if 'RECIPE NAME:' in line_upper:
                recipe['recipe_name'] = line.split(':', 1)[1].strip()
            elif 'DIFFICULTY:' in line_upper:
                recipe['difficulty'] = line.split(':', 1)[1].strip()
            elif 'PREP TIME:' in line_upper:
                recipe['prep_time'] = line.split(':', 1)[1].strip()
            elif 'COOK TIME:' in line_upper:
                recipe['cook_time'] = line.split(':', 1)[1].strip()
            elif 'SERVINGS:' in line_upper:
                recipe['servings'] = line.split(':', 1)[1].strip()
            elif 'CALORIES:' in line_upper:
                recipe['calories'] = line.split(':', 1)[1].strip()
            elif 'TIPS:' in line_upper:
                recipe['tips'] = line.split(':', 1)[1].strip()
            elif 'NUTRITION:' in line_upper:
                recipe['nutrition'] = line.split(':', 1)[1].strip()
            
            # Section starts
            elif 'INGREDIENTS:' in line_upper:
                current_section = 'ingredients'
            elif 'STEPS:' in line_upper or 'INSTRUCTIONS:' in line_upper:
                current_section = 'steps'
                step_number = 1
            elif line_upper in ['TIPS:', 'NUTRITION:']:
                current_section = None
            
            # Parse ingredients
            elif current_section == 'ingredients':
                # Look for bullet points or numbered lists
                if line.startswith(('-', '*', '•')) or (line[0].isdigit() and line[1] in '. )'):
                    # Clean the line
                    if line.startswith(('-', '*', '•')):
                        ingredient = line[1:].strip()
                    elif line[0].isdigit():
                        if '.' in line:
                            ingredient = line.split('.', 1)[1].strip()
                        elif ')' in line:
                            ingredient = line.split(')', 1)[1].strip()
                        else:
                            ingredient = line[2:].strip()
                    else:
                        ingredient = line
                    
                    if ingredient and len(ingredient) > 2:
                        recipe['ingredients'].append(ingredient)
            
            # Parse steps - be more flexible
            elif current_section == 'steps':
                # Check for numbered steps
                if line and line[0].isdigit() and len(line) > 2:
                    # Extract step text
                    if '.' in line:
                        step_text = line.split('.', 1)[1].strip()
                    elif ')' in line:
                        step_text = line.split(')', 1)[1].strip()
                    else:
                        step_text = line[2:].strip()
                    
                    # Check if this is a real step (not a section header)
                    if step_text and len(step_text) > 10 and not any(
                        keyword in step_text.upper() for keyword in 
                        ['INGREDIENTS', 'STEPS', 'TIPS', 'NUTRITION', 'RECIPE']
                    ):
                        recipe['steps'].append(f"Step {step_number}: {step_text}")
                        step_number += 1
                
                # Also accept lines that look like steps but aren't numbered
                elif len(line) > 20 and current_section == 'steps':
                    # Check if it looks like a cooking instruction
                    cooking_keywords = ['heat', 'cook', 'chop', 'mix', 'add', 'stir', 'boil', 'fry', 'bake', 'whisk']
                    if any(keyword in line.lower() for keyword in cooking_keywords):
                        recipe['steps'].append(f"Step {step_number}: {line}")
                        step_number += 1
        
        # Check if steps are too generic
        generic_patterns = ['prepare ingredients', 'cook as desired', 'serve and enjoy', 'follow instructions']
        has_generic_steps = any(
            any(pattern in step.lower() for pattern in generic_patterns)
            for step in recipe['steps']
        )
        
        # If steps are generic or we have less than 3 steps, try to parse differently
        if has_generic_steps or len(recipe['steps']) < 3:
            # Try alternative parsing: look for paragraphs after STEPS:
            in_steps = False
            step_number = 1
            recipe['steps'] = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                if 'STEPS:' in line.upper() or 'INSTRUCTIONS:' in line.upper():
                    in_steps = True
                    continue
                elif 'TIPS:' in line.upper() or 'NUTRITION:' in line.upper():
                    in_steps = False
                    continue
                
                if in_steps and line:
                    # Skip empty lines and section headers
                    if len(line) > 15 and not any(
                        keyword in line.upper() for keyword in 
                        ['INGREDIENTS', 'STEPS', 'TIPS', 'NUTRITION', 'RECIPE']
                    ):
                        # Check if it's already numbered
                        if line[0].isdigit() and line[1] in '. )':
                            if '.' in line:
                                step_text = line.split('.', 1)[1].strip()
                            elif ')' in line:
                                step_text = line.split(')', 1)[1].strip()
                            else:
                                step_text = line[2:].strip()
                        else:
                            step_text = line
                        
                        if step_text:
                            recipe['steps'].append(f"Step {step_number}: {step_text}")
                            step_number += 1
        
        # If still no good steps, show the raw response in debug
        if len(recipe['steps']) < 3 and st.session_state.get('show_debug', False):
            st.sidebar.warning("⚠️ Could not parse detailed steps from Gemini response")
        
        return [recipe]
        
    except Exception as e:
        st.sidebar.error(f"Parsing error: {str(e)}")
        return None
# Main function
def main():
    # Initialize session state
    init_session_state()
    
    # Initialize Gemini
    gemini_info = init_gemini()
    gemini_client = None
    gemini_model_name = None
    
    if gemini_info:
        gemini_client, gemini_model_name = gemini_info
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/chef-hat.png", width=80)
        st.title("Recipe Doctor")
        st.markdown("### AI Chef Assistant")
        st.markdown("---")
        
        # Navigation
        st.subheader("📱 Navigation")
        nav_option = st.radio(
            "Go to:",
            ["🧑‍🍳 Generate Recipes", "💾 Saved Recipes", "🛒 Shopping List", "⚙️ Settings"],
            key="nav_radio"
        )
        
        st.session_state.current_tab = nav_option
        
        st.markdown("---")
        
        # Preferences
        st.subheader("📝 Your Preferences")
        dietary_prefs = st.multiselect(
            "Dietary Restrictions",
            ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free", "Low-Carb"],
            key="dietary_prefs"
        )
        
        cuisine = st.selectbox(
            "Cuisine Style",
            ["Any", "Italian", "Asian", "Mexican", "Indian", "Mediterranean", "American"],
            key="cuisine_select"
        )
        
        meal_type = st.selectbox(
            "Meal Type",
            ["Any", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],
            key="meal_type_select"
        )
        
        skill_level = st.select_slider(
            "👨‍🍳 Cooking Level",
            options=["Beginner", "Intermediate", "Expert"],
            key="skill_level_slider"
        )
        
        st.markdown("---")
        
        # Debug
        show_debug = st.checkbox("🔧 Show Debug", key="show_debug")
        with st.sidebar:
            if show_debug and st.session_state.get('raw_response'):
                st.markdown("### 🔍 Last Gemini Response")
                st.text_area("", st.session_state.raw_response, height=200)
        
        # Clear buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Clear", key="clear_btn"):
                st.session_state.recipes = None
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", key="reset_btn"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        st.caption("Built with Gemini AI")
    
    # Render based on tab
    if st.session_state.current_tab == "🧑‍🍳 Generate Recipes":
        render_generate_recipes(gemini_client, gemini_model_name, dietary_prefs, cuisine, meal_type, skill_level, show_debug)
    elif st.session_state.current_tab == "💾 Saved Recipes":
        render_saved_recipes()
    elif st.session_state.current_tab == "🛒 Shopping List":
        render_shopping_list()
    elif st.session_state.current_tab == "⚙️ Settings":
        render_settings()

def render_generate_recipes(client, model_name, dietary_prefs, cuisine, meal_type, skill_level, show_debug):
    """Render the recipe generation page"""
    st.markdown('<h1 class="main-header">🍳 Recipe Doctor</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI Chef that creates recipes from your available ingredients</p>', unsafe_allow_html=True)
    
    # Ingredient Input
    st.markdown("---")
    st.subheader("📝 What ingredients do you have?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ingredient_text = st.text_area(
            "List ingredients (separate with commas)",
            placeholder="eggs, milk, bread, cheese...",
            height=100,
            key="ingredient_input"
        )
    
    with col2:
        if ingredient_text:
            ingredients = [x.strip() for x in ingredient_text.split(',') if x.strip()]
            st.session_state.ingredients = ingredients
            
            st.write("### Your Ingredients")
            for ing in ingredients[:8]:
                st.markdown(f'<div class="ingredient-chip">{ing}</div>', unsafe_allow_html=True)
        else:
            st.info("Enter ingredients")
    
    # Generate Recipes
    if ingredient_text and st.session_state.ingredients:
        st.markdown("---")
        st.subheader("🚀 Generate Recipe")
        
        if st.button("🧠 Generate with AI", type="primary", use_container_width=True, key="generate_btn"):
            with st.spinner("Creating recipe..."):
                detected = detect_ingredients_from_text(ingredient_text)
                
                if client:
                    recipes = generate_recipes_with_gemini(
                        detected,
                        dietary_prefs,
                        cuisine,
                        meal_type,
                        skill_level,
                        client,
                        model_name
                    )
                    
                    if recipes:
                        st.session_state.recipes = recipes
                        st.success("✅ Recipe generated!")
                    else:
                        st.error("Failed to generate. Try again.")
                else:
                    st.error("API not available. Check settings.")
    
    # Display Recipes
    if st.session_state.recipes:
        st.markdown("---")
        st.subheader("🍽️ Your Recipe")
        
        for idx, recipe in enumerate(st.session_state.recipes):
            # Recipe card
            st.markdown(f"""
            <div class="recipe-card">
                <h3>📋 {recipe.get('recipe_name', 'Recipe')}</h3>
                <div style="display: flex; gap: 15px; margin: 10px 0; flex-wrap: wrap;">
                    <span>⚡ <b>{recipe.get('difficulty', 'Easy')}</b></span>
                    <span>⏱️ <b>Prep:</b> {recipe.get('prep_time', '10 min')}</span>
                    <span>🔥 <b>Cook:</b> {recipe.get('cook_time', '15 min')}</span>
                    <span>👥 <b>Serves:</b> {recipe.get('servings', 2)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Ingredients
            st.markdown("#### 🥗 Ingredients")
            for ing in recipe.get('ingredients', []):
                st.markdown(f'<div class="ingredient-item">{ing}</div>', unsafe_allow_html=True)
            
            # Steps
            st.markdown("#### 👨‍🍳 Instructions")
            st.markdown('<div style="counter-reset: step-counter;">', unsafe_allow_html=True)
            for step in recipe.get('steps', []):
                st.markdown(f'<div class="step-item">{step}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Tips & Nutrition
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"💡 **Tip:** {recipe.get('tips', '')}")
            with col2:
                st.info(f"📊 **Nutrition:** {recipe.get('nutrition', '')}")
            
            # Action buttons - FIXED
            st.markdown("#### 🛠️ Actions")
            col_save, col_shop, col_new = st.columns(3)
            
            with col_save:
                if st.button(f"💾 Save", key=f"save_{idx}", use_container_width=True):
                    if 'saved_recipes' not in st.session_state:
                        st.session_state.saved_recipes = []
                    
                    # Check if already saved
                    existing = [r.get('recipe_name', '') for r in st.session_state.saved_recipes]
                    if recipe.get('recipe_name', '') not in existing:
                        import copy
                        st.session_state.saved_recipes.append(copy.deepcopy(recipe))
                        st.success("Saved!")
                        st.balloons()
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.info("Already saved")
            
            with col_shop:
                if st.button(f"🛒 Add to List", key=f"shop_{idx}", use_container_width=True):
                    if 'shopping_list' not in st.session_state:
                        st.session_state.shopping_list = []
                    
                    added = 0
                    for ing in recipe.get('ingredients', []):
                        if ing not in st.session_state.shopping_list:
                            st.session_state.shopping_list.append(ing)
                            added += 1
                    
                    if added > 0:
                        st.success(f"Added {added} items")
                    else:
                        st.info("No new items")
                    
                    time.sleep(0.5)
                    st.rerun()
            
            with col_new:
                if st.button(f"🔄 New", key=f"new_{idx}", use_container_width=True):
                    st.session_state.recipes = None
                    st.rerun()
            
            st.markdown("---")

def render_saved_recipes():
    """Render saved recipes page"""
    st.markdown('<h1 class="main-header">💾 Saved Recipes</h1>', unsafe_allow_html=True)
    
    if 'saved_recipes' not in st.session_state:
        st.session_state.saved_recipes = []
    
    if st.session_state.saved_recipes:
        st.write(f"### You have {len(st.session_state.saved_recipes)} saved recipes")
        
        for i, recipe in enumerate(st.session_state.saved_recipes):
            with st.expander(f"{i+1}. {recipe.get('recipe_name', 'Recipe')}"):
                st.write(f"**Difficulty:** {recipe.get('difficulty', 'Easy')}")
                st.write(f"**Time:** {recipe.get('prep_time', '')} + {recipe.get('cook_time', '')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("View", key=f"view_{i}"):
                        st.session_state.recipes = [recipe]
                        st.session_state.current_tab = "🧑‍🍳 Generate Recipes"
                        st.rerun()
                with col2:
                    if st.button("Delete", key=f"delete_{i}"):
                        st.session_state.saved_recipes.pop(i)
                        st.rerun()
        
        if st.button("Clear All", type="secondary"):
            st.session_state.saved_recipes = []
            st.rerun()
    else:
        st.info("No saved recipes")
        if st.button("Go Generate Recipes"):
            st.session_state.current_tab = "🧑‍🍳 Generate Recipes"
            st.rerun()

def render_shopping_list():
    """Render shopping list page"""
    st.markdown('<h1 class="main-header">🛒 Shopping List</h1>', unsafe_allow_html=True)
    
    if 'shopping_list' not in st.session_state:
        st.session_state.shopping_list = []
    
    if st.session_state.shopping_list:
        st.write(f"### {len(st.session_state.shopping_list)} items")
        
        checked = []
        for i, item in enumerate(st.session_state.shopping_list):
            col1, col2 = st.columns([8, 1])
            with col1:
                if st.checkbox(f"• {item}", key=f"check_{i}"):
                    checked.append(i)
            with col2:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.session_state.shopping_list.pop(i)
                    st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if checked and st.button("Remove Checked"):
                for i in sorted(checked, reverse=True):
                    st.session_state.shopping_list.pop(i)
                st.rerun()
        
        with col2:
            if st.button("Clear All"):
                st.session_state.shopping_list = []
                st.rerun()
    else:
        st.info("Shopping list is empty")
        if st.button("Go Generate Recipes"):
            st.session_state.current_tab = "🧑‍🍳 Generate Recipes"
            st.rerun()

def render_settings():
    """Render settings page"""
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    st.write("### API Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    
    if api_key:
        st.session_state.api_key = api_key
        st.success("Saved")
    
    st.write("### Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Saved Recipes", len(st.session_state.get('saved_recipes', [])))
    with col2:
        st.metric("Shopping List", len(st.session_state.get('shopping_list', [])))

if __name__ == "__main__":
    main()