import streamlit as st
import pandas as pd
import models
from datetime import datetime

def home():
    page = st.sidebar.radio("Go to", ["Home"])


    database_name = '123456789.csv'  # Set a fixed database name
    database = pd.read_csv(f'Database/{database_name}')

    if page == "Home":
        st.title("Welcome to the Mental Health Analyzer!")

        st.write("Select the language and speak into the microphone.")
        language = st.radio("Select language:", ("English", "Kannada"))
        
        if st.button("Recognize and Analyze"):
            recognized_text, translated_text = models.recognize_and_translate(language)
            if recognized_text and translated_text:
                st.write(f"**Recognized {language} text:** {recognized_text}")
                st.write(f"**Translated text:** {translated_text}")
                
                # Sentiment analysis
                sentiment_score = models.sentiment_analysis(translated_text)
                st.write(f"Sentiment Score: {sentiment_score}")
                
                # Check for signs of depression
                if sentiment_score in [1, 2, 3]:  # Scores 1, 2, 3 indicate negative sentiment
                    st.warning("Signs of Depression found")
                    depression = 'Depression'
                else:
                    st.success("No signs of depression")
                    depression = 'No Depression'
                
                # Emotion analysis
                detected_emotions = models.emotion_analysis(translated_text)
                st.write("**Detected Emotions :**")
                for emotion, score in detected_emotions.items():
                    st.write(f"{emotion.capitalize()}: {score:.2f}%")
                
                # Save results into the database
                new_row = pd.DataFrame({
                    'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                    'depression': [depression],
                    'happy': [detected_emotions['happy']],
                    'angry': [detected_emotions['angry']],
                    'sad': [detected_emotions['sad']]
                })
                
                # Append the new row to the database
                database = pd.concat([new_row, database], ignore_index=True)
                database.to_csv(f'Database/{database_name}', index=False)

if __name__ == "__main__":
    home()
