# Updated app.py

import streamlit as st
import requests

# Fetching sensitive tokens from input fields
api_key = st.text_input('Enter your API Key')

# API endpoint
api_url = 'https://api.runpod.io'

# Function to make API calls
def get_data(endpoint):
    try:
        response = requests.get(f'{api_url}/{endpoint}', headers={'Authorization': f'Bearer {api_key}'})
        response.raise_for_status()  # Raises an error for bad responses
        return response.json()  # Return JSON data if the request is successful
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            st.error('Error 404: Resource not found.')
        elif err.response.status_code == 401:
            st.error('Error 401: Unauthorized access. Please check your API key.')
        else:
            st.error('An error occurred: {}'.format(err))
    except Exception as e:
        st.error('An unexpected error occurred: {}'.format(str(e)))

# Main Streamlit app structure
st.title('RunPod API Streamlit App')
# Implement other functionalities of the app here...
