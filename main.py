import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging

load_dotenv()

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

model = "gpt-3.5-turbo"

# === Create a Thread ===
thread = openai.Thread.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How do I get started working out to lose fat and build muscles?"},
    ]
)

thread_id = thread['id']

# === Create a Message ===
message = openai.Thread.create_message(
    thread_id=thread_id,
    model=model,
    role="user",
    content="How many reps do I need to do to build lean muscles?"
)

# === Run the Assistant ===
run = openai.Completion.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How do I get started working out to lose fat and build muscles?"},
        {"role": "assistant", "content": "You should aim for 3 sets of 10-12 reps for each exercise."},
    ]
)

# === Wait for Run Completion ===
def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    while True:
        run = client.Thread.retrieve(thread_id=thread_id, run_id=run_id)
        if run['object'] == 'run' and run['data']['status'] == 'completed':
            elapsed_time = run['data']['created'] - run['data']['completed_at']
            formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            print(f"Run completed in {formatted_elapsed_time}")
            logging.info(f"Run completed in {formatted_elapsed_time}")

            # Get messages here once Run is completed!
            messages = client.Thread.list_messages(thread_id=thread_id)
            last_message = messages['data'][-1]
            response = last_message['content']['text']
            print(f"Assistant Response: {response}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# === Run ===
wait_for_run_completion(client=openai, thread_id=thread_id, run_id=run['id'])

# ==== Steps --- Logs ==
run_steps = openai.Thread.list_steps(thread_id=thread_id, run_id=run['id'])
print(f"Steps---> {run_steps['data'][0]}")
