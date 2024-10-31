import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
from gtts import gTTS
import os
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure( api_key = os.getenv( "GEMINI_API_KEY" ) )
model = genai.GenerativeModel( 'gemini-pro' )

def text_to_speech( text ):
    # Create gTTS object
    tts = gTTS( text = text, lang = 'en' )
    
    # Save to BytesIO buffer
    fp = BytesIO()
    tts.write_to_fp( fp )
    
    return fp

def generate_story_prompt( prompt ):
    response = model.generate_content( prompt )
    return response.text

def generate_prompt( age, length, theme, setting, addition ):
    prompt = " create a story for " + str( age ) + "s. The length is : " + str( length ) + ". The theme is : " + str( theme ) + \
      ". The setting is : " + str( setting ) + ". Some additional notes are : " + str( addition ) + \
        ". Just give a story dont say: ok let me provide you with a story  "
    return prompt

def generate_story_select( age, length, theme, setting, addition ):
    prompt = generate_prompt( age, length, theme, setting, addition )
    response = model.generate_content( prompt )
    return response.text

# UI Setup
option = option_menu(
    menu_title = None,
    options = [ "Prompt Generate", "Select Story" ],
    icons = [ "pencil", "list" ],
    orientation = "horizontal",
)

st.title( "StoryGenerator.ai" )

if option == "Prompt Generate":
    st.subheader( "Enter a prompt to generate your story!" )
    story_prompt = st.text_area( 
        "Enter your prompt", 
        value = "Write a story about a kid who finds out their pet cat can talk, but only at midnight. The cat has a big secret to share." 
    )
    if st.button( "Generate Story" ):
        generated_story = generate_story_prompt( story_prompt )
        st.write( generated_story )
        
        # Create audio file
        audio_fp = text_to_speech( generated_story )
        
        # Add audio player
        st.audio( audio_fp, format = 'audio/mp3' )

if option == "Select Story":
    age = st.selectbox( "Select Age Group", [ "5-8", "8-12", "12-18" ] )
    length = st.selectbox( "Select Length", [ "Short", "Medium", "Long" ] )
    theme = st.selectbox( 
        "Select Theme", 
        [ "Adventure", "Fantasy", "Mystery", "Sci-Fi", "Romance", "Drama", "Comedy", "Thriller", "Horror" ] 
    )
    setting = st.text_area( 
        "Describe the setting of the story", 
        value = "A magical forest" 
    )
    addition = st.text_area( 
        "Additional Notes", 
        value = "Add any additional notes or instructions for the story here." 
    )

    if st.button( "Generate Story" ):
        generated_story = generate_story_select( age, length, theme, setting, addition )
        st.write( generated_story )
        
        # Create audio file
        audio_fp = text_to_speech( generated_story )
        
        # Add audio player
        st.audio( audio_fp, format = 'audio/mp3' )

# Add voice options (optional enhancement)
with st.sidebar:
    st.subheader( "Voice Settings" )
    language = st.selectbox(
        "Select Language",
        [ "en", "es", "fr", "de", "it" ],
        index = 0
    )
    
    speed = st.slider(
        "Speech Speed",
        min_value = 0.5,
        max_value = 2.0,
        value = 1.0,
        step = 0.1
    )
