import streamlit as st
import openai
import time

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

model = "gpt-3.5-turbo-1106"  # استخدم نموذج GPT-3.5 Turbo برقم الإصدار 1106

# Create a user message
user_input = st.text_input("Ask a question:")
if st.button("Submit"):
    st.write(f"User: {user_input}")

    # Send the user message directly to the model
    response = openai.Completion.create(
        engine=model,
        prompt=f"User: {user_input}\nAssistant:",
        temperature=0.7,
        max_tokens=150,
    )

    # Get the assistant's reply
    assistant_reply = response['choices'][0]['text']
    st.write(f"Assistant Response: {assistant_reply}")
