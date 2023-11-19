import streamlit as st
from todoist_api_python.api import TodoistAPI
import os
from dotenv import load_dotenv

load_dotenv()

# Load Todoist List
TODOIST_API_KEY = os.getenv('TODOIST_API_KEY')
api = TodoistAPI(TODOIST_API_KEY)

BACKGROUND_COLOR = 'white'
COLOR = 'black'

def set_page_container_style(
        padding_top: int = 1
    ):
        st.markdown(
            f'''
            <style>
                .block-container {{
                    padding-top: {padding_top}rem;
                }}
            </style>
            ''',
            unsafe_allow_html=True,
        )


# Fetch all tasks
def fetch_tasks():
    try:
        tasks = api.get_tasks()
    except Exception as error:
        print(error)
    return tasks

st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)
set_page_container_style()

# Display tasks
st.header('Todoist Tasks')
tasks = fetch_tasks()
for task in tasks:
    st.write(f"Task: {task.content}, Label: {task.labels}, Priority: {task.priority}")