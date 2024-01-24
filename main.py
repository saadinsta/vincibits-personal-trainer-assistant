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

# الهوية المعينة للموضوع
thread_id = "thread_58QhEBPsgcZIXPQZlZgnhjc5"

# إنشاء رسالة جديدة
user_input = st.text_input("User Input", "How many reps do I need to do to build lean muscles?")
message = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-1106",  # تم تحديث الموديل
    messages=[
        {"role": "user", "content": user_input, "thread_id": thread_id},
    ],
)

# تشغيل المساعد
run = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-1106",  # تم تحديث الموديل
    messages=[
        {"role": "assistant", "content": "You are James Bond.", "thread_id": thread_id},
        {"role": "user", "content": user_input, "thread_id": thread_id},
    ],
)

# انتظار اكتمال التنفيذ
st.write("Waiting for run to complete...")
while not run["choices"][0]["message"]["content"]:
    run = openai.ChatCompletion.retrieve(model="gpt-3.5-turbo-1106", run_id=run["id"])

# عرض رد المساعد
st.write("Assistant Response:")
st.write(run["choices"][0]["message"]["content"])

# عرض الخطوات التي تم تسجيلها
st.write("Steps--->")
st.write(run)
