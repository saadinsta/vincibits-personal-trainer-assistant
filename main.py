import streamlit as st
import openai
import time

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

model = "gpt-3.5-turbo"

# Create a user message
user_input = st.text_input("Ask a question:")
if st.button("Submit"):
    st.write(f"User: {user_input}")

    # Send the user message directly to the model
    response = openai.Completion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]
    )

    # Get the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']
    st.write(f"Assistant Response: {assistant_reply}")
