import streamlit as st
from todoist_api_python.api import TodoistAPI
import os
from dotenv import load_dotenv

load_dotenv()

# Load Todoist List
TODOIST_API_KEY = os.getenv('TODOIST_API_KEY')
api = TodoistAPI(TODOIST_API_KEY)

def set_page_container_style(
        padding_top: int = 1
    ):
        st.markdown(
            f'''
            <style>
                .block-container {{
                    padding-top: {padding_top}rem;
                }}

                [data-testid="collapsedControl"] {
                    display: none
                }
            </style>
            ''',
            unsafe_allow_html=True,
        )


# Fetch all tasks
def fetch_tasks():
    try:
        projects = api.get_projects()
        inbox = next(
            (project for project in projects if project.is_inbox_project == True),
            None
        )

        tasks = api.get_tasks(project_id=inbox.id)
        tasks.sort(key=lambda x: x.priority, reverse=True)
    except Exception as error:
        print(error)
    return tasks

def write_task(task, col1, col2):
    priorityEmoji = [ '🟢', '🟡', '🟠','🔴']
    labelEmoji = {"Home":"🏠", "Work": "🏢"}

    if task.labels == []:
        task.labels = ""
    else:
        for label in task.labels:
            task.labels = labelEmoji[label]
    with col1:
        st.markdown(f"{task.content}")
                    
    with col2:
        st.markdown(f"{priorityEmoji[task.priority-1]} {task.labels}")
     

st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)
set_page_container_style()

# Display tasks
st.subheader('Todoist Tasks')
col1, col2 = st.columns([8,2])
tasks = fetch_tasks()[:6]
for task in tasks:
    write_task(task, col1, col2)