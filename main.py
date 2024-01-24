import streamlit as st
import openai
import time
import logging

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

model = "gpt-3.5-turbo"

# Create a Thread
thread = openai.Thread.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How do I get started working out to lose fat and build muscles?"},
    ]
)

thread_id = thread['id']

# Wait for Run Completion
def wait_for_run_completion(thread_id, run_id, sleep_interval=5):
    while True:
        run = openai.Thread.retrieve(thread_id=thread_id, run_id=run_id)
        if run['object'] == 'run' and run['data']['status'] == 'completed':
            elapsed_time = run['data']['created'] - run['data']['completed_at']
            formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            st.write(f"Run completed in {formatted_elapsed_time}")

            # Get messages here once Run is completed!
            messages = openai.Thread.list_messages(thread_id=thread_id)
            last_message = messages['data'][-1]
            response = last_message['content']['text']
            st.write(f"Assistant Response: {response}")
            break
        st.write("Waiting for run to complete...")
        time.sleep(sleep_interval)

# Streamlit App
st.title("OpenAI GPT-3.5 Turbo Assistant")

user_input = st.text_input("Ask a question:")
if st.button("Submit"):
    st.write(f"User: {user_input}")

    # Create a Message
    message = openai.Thread.create_message(
        thread_id=thread_id,
        model=model,
        role="user",
        content=user_input
    )

    # Run the Assistant
    run = openai.Completion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]
    )

    # Wait for Run Completion
    wait_for_run_completion(thread_id=thread_id, run_id=run['id'])
