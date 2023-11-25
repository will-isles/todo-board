from pickle import LIST
import streamlit as st
from todoist_api_python.api import TodoistAPI
import os
from dotenv import load_dotenv

load_dotenv()

# Load Todoist List
TODOIST_API_KEY = os.getenv('TODOIST_API_KEY')
api = TodoistAPI(TODOIST_API_KEY)

LIST_LENGTH = os.getenv('LIST_LENGTH')  or 8


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

def write_task_block(header, filter, list_length):
    tasks = fetch_tasks(filter=filter)

    if len(tasks) == 0:
        return 0
    
    if list_length <= 0:
        return 0

    tasks = tasks[:list_length]
    
    # Display header
    st.subheader(header)    
    
    # Display tasks
    col1, col2, col3 = st.columns([8,2,2])
    for task in tasks:
        write_task(task, col1, col2, col3)
    return list_length - len(tasks) - 1

def create_page():
    # Set page config  
    st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)
    set_page_container_style()

    # Display tasks
    list_length = LIST_LENGTH
    list_length = write_task_block("Overdue", "overdue", list_length)
    list_length = write_task_block("Next Week", "next week", list_length)
    list_length = write_task_block("Sometime", "no date", list_length)

create_page()