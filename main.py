import os
import openai
import streamlit as st

# Retrieve OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    st.error("Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Set the API key in the environment
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Create OpenAI client
client = openai.OpenAI()

# الهوية المعينة للمساعد (تم تحديثها إلى الهوية الجديدة)
assistant_id = "asst_fIn3hgNSP1GjqQqp0sPAeMW4"

# اختيار رقم الثريد
thread_id = st.text_input("Enter Thread ID (default: thread_58QhEBPsgcZIXPQZlZgnhjc5)", "thread_58QhEBPsgcZIXPQZlZgnhjc5")

# إنشاء رسالة جديدة
user_input = st.text_input("User Input", "How many reps do I need to do to build lean muscles?")

# إدارة الأخطاء أثناء إنشاء الرسالة
try:
    message = client.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "user", "content": user_input, "thread_id": thread_id},
        ],
    )
except openai.error.OpenAIError as e:
    st.write(f"An error occurred while creating the message: {e}")
    st.stop()

# إدارة الأخطاء أثناء تشغيل المساعد
try:
    run = client.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "assistant", "content": "You are James Bond.", "thread_id": thread_id},
            {"role": "user", "content": user_input, "thread_id": thread_id},
        ],
    )
except openai.error.OpenAIError as e:
    st.write(f"An error occurred while running the assistant: {e}")
    st.stop()

# انتظار اكتمال التنفيذ
st.write("Waiting for run to complete...")
while not run["choices"][0]["message"]["content"]:
    try:
        run = client.ChatCompletion.retrieve(model="gpt-3.5-turbo-1106", run_id=run["id"])
    except openai.error.OpenAIError as e:
        st.write(f"An error occurred while retrieving the run: {e}")
        st.stop()

# عرض رد المساعد
st.write("Assistant Response:")
st.write(run["choices"][0]["message"]["content"])

# عرض الخطوات التي تم تسجيلها
st.write("Steps--->")
st.write(run)

