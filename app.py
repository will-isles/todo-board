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

                [data-testid="collapsedControl"] {{
                    display: none
                }}
            </style>
            ''',
            unsafe_allow_html=True,
        )


# Fetch all tasks
def fetch_tasks(filter="due:next week|overdue|no date"):
    try:
        tasks = api.get_tasks(filter=filter)
        tasks.sort(key=lambda x: x.priority, reverse=True)
        return tasks
    except Exception as error:
        print(error)
    

def write_task(task, col1, col2, col3):
    priorityEmoji = [ '🔵', '🟢', '🟡','🔴']
    labelEmoji = {"Home":"🏠", "Work": "🏢"}

    if task.labels == []:
        task.labels = ""
    else:
        for label in task.labels:
            task.labels = labelEmoji[label]
    with col1:
        st.markdown(f"**{task.content}**")
                    
    with col2:
        if task.due != None:
            st.caption(f"{task.due.string}")
    
    with col3:
        st.markdown(f"{priorityEmoji[task.priority-1]} {task.labels}")

def write_task_block(header, filter, limit):
    tasks = fetch_tasks(filter=filter)

    if len(tasks) == 0:
        return 0
    
    if limit <= 0:
        return 0

    tasks = tasks[:limit]
    
    # Display header
    st.subheader(header)    
    
    # Display tasks
    col1, col2, col3 = st.columns([8,2,2])
    for task in tasks:
        write_task(task, col1, col2, col3)
    return limit - len(tasks) - 1

def create_page():
    # Set page config  
    st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)
    set_page_container_style()

    # Display tasks
    limit = 8
    limit = write_task_block("Overdue", "overdue", limit)
    limit = write_task_block("Next Week", "next week", limit)
    limit = write_task_block("Sometime", "no date", limit)

create_page()