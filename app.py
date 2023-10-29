import os
import streamlit as st
from todoist_api_python.api import TodoistAPI

from dotenv import load_dotenv
load_dotenv()

# Load Todoist List
TODOIST_API_KEY = os.getenv('TODOIST_API_KEY')
api = TodoistAPI(TODOIST_API_KEY)

def load_tasks():
    try:
        st.session_state['tasks'] = api.get_tasks()
    except Exception as error:
        print(error)

st.set_page_config(page_title="Streamlit App", page_icon=":smiley:", layout="wide")


# Task Layout
def layoutTask(task):
    with st.container():
        st.header(f"ContentA: {task.content}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Labels: {task.labels}")
        with col2:
            st.write(f"Priority: {task.priority}")
        with col3:
            if task.due is not None:
                st.write(f"Due: {task.due}")

# Page Layout
if 'tasks' not in st.session_state:
    load_tasks()

with st.container():
    st.subheader("Todo List")
    st.title("Today's Items")

    for task in st.session_state['tasks']:
        layoutTask(task)


