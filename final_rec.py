import streamlit as st
import pandas as pd
import pickle
from PIL import Image
import requests
import io

# Load your CSV file into a DataFrame
drama_data = pickle.load(open("C:/Users/pcc/Desktop/drama.pkl", "rb"))

# Load the cosine similarity data
cosine_similarity = pickle.load(open("C:/Users/pcc/Desktop/cosine_sim.pkl", "rb"))

# Streamlit app with custom frontend
st.set_page_config(
    page_title="K-Drama Recommendation System",
    page_icon="✨",
    layout="wide"  # Use wide layout to center-align content
)

# Set background color and custom styles
st.markdown(
    """
    <style>
    body {
        background-color: #1E1E1E; /* Background color: Black */
        font-family: Arial, sans-serif; /* Font family */
        color: #D4AF37; /* Text color: Gold */
    }
    .stApp { 
        max-width: 800px; /* Max width for the content */
        margin: auto; /* Center the content */
        padding: 20px; /* Add padding for spacing */
        background-color: #1E1E1E; /* Background color for the content */
    }
    .stTextInput {
        width: 100%;
        margin-bottom: 20px; /* Add margin for spacing */
        background-color: #1E1E1E; /* Input box background color */
        border: 1px solid #1E1E1E; /* Input box border color: Gold */
    }
    .stTextInput input {
        color: #D4AF37 !important; /* Input text color: Gold */
    }
    .stButton {
        background-color: transparent; /* Transparent button background */
        color: #D4AF37 !important; /* Button text color: Gold */
        border: none; /* Remove button border */
        border-radius: 8px; /* Round button corners */
        display: block;
        margin: 0 auto; /* Center the button */
        padding: 10px 20px; /* Add padding to the button */
        cursor: pointer; /* Add pointer cursor */
    }
    .stButton:hover {
        background-color: transparent; /* Transparent button background on hover */
    }
    .stMarkdown {
        color: #4169E1; /* Title color: Royal Blue */
        text-align: center; /* Center-align Markdown text */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Center-align the title with gold color
st.markdown("## <span style='color: #D4AF37;'>K-Drama Recommendation System</span>", unsafe_allow_html=True)

# Text input for entering a K-Drama name with gold color
selected_drama_name = st.text_input("Enter the name of the K-Drama to get recommendations", key="drama_input")

# Add an attractive K-Drama related sentence with royal blue color
st.markdown("Discover your next favorite K-Drama and uncover hidden gems!", unsafe_allow_html=True)

# Function to recommend similar K-Dramas
def recommend(selected_drama_name):
    index = drama_data[drama_data["Name"] == selected_drama_name].index[0]
    similar_dramas = sorted(enumerate(cosine_similarity[index]), key=lambda x: x[1], reverse=True)[1:5]  # Display 4 recommendations
    recommended_dramas = []
    recommended_posters = []
    
    for i in similar_dramas:
        similar_drama_name = drama_data.iloc[i[0]]["Name"]
        recommended_dramas.append(similar_drama_name)
        # Use the poster image URL from your drama_data DataFrame
        poster_url = drama_data.iloc[i[0]]["URL"]
        recommended_posters.append(poster_url)
    
    return recommended_dramas, recommended_posters

# Function to resize an image to 100x100 pixels
def resize_image(image_url, size=(100, 100)):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check for HTTP errors
        image = Image.open(io.BytesIO(response.content))
        image = image.resize(size)
        return image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Center-align the "Recommend" button container
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
if st.button("Recommend", key="recommend_button"):
    # Calculate cosine similarity and get the recommendations
    similar_drama = recommend(selected_drama_name)
    
    # Unpack the recommendations into separate lists
    recommended_dramas, recommended_posters = similar_drama
    
    # Display the recommendations in a single column
    for i in range(len(recommended_dramas)):
        similar_drama_name = recommended_dramas[i]
        poster_url = recommended_posters[i]
            
        # Convert the text URL to a hyperlink
        st.markdown(f"[{similar_drama_name}]({poster_url})", unsafe_allow_html=True)
            
        # Resize the image to 100x100 pixels and display as a hyperlink
        resized_image = resize_image(poster_url)
        if resized_image:
            st.image(resized_image, caption=similar_drama_name, width=100, use_column_width=False)
st.markdown("</div>", unsafe_allow_html=True)  # Close the centered div
