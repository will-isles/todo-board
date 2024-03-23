import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime as dt
from todoist_api_python.api import TodoistAPI

load_dotenv()

# Load Todoist List
TODOIST_API_KEY = os.getenv('TODOIST_API_KEY')
if TODOIST_API_KEY == None:
    raise Exception("TODOIST_API_KEY not found in .env file")

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
    

def write_task(task):
    priorityEmoji = [ '🔵', '🟢', '🟡','🔴']
    labelEmoji = {"Home":"🏠", "Work": "🏢", "2 minutes": "⏰"}

    if task.labels == []:
        task.labels = ""
    else:
        for label in task.labels:
            task.labels = labelEmoji[label]

    st.container()
    with st.container():
        col1, col2, col3 = st.columns([8,2,2])

    with col1:
        st.markdown(f"**{task.content}**")
                    
    with col2:
        formatted = None
        if task.due.datetime != None:
            formatted = dt.fromisoformat(task.due.datetime).strftime("%d %b")
        if task.due.date != None:
            formatted = dt.strptime(task.due.date, '%Y-%m-%d').strftime("%d %b")
        st.markdown(f"{formatted}")
    
    with col3:
        st.markdown(f"{priorityEmoji[task.priority-1]} {task.labels}")

def write_task_block(header, filter, list_length):
    tasks = fetch_tasks(filter=filter)
    if not (tasks is None) or len(tasks) == 0:
        print("No tasks")
        return list_length
    
    if list_length <= 0:
        print("No free space for tasks")
        return list_length

    tasks = tasks[:list_length]
    
    # Display header
    st.subheader(header)    
    
    # Display tasks
    for task in tasks:
        write_task(task)
    return list_length - len(tasks) - 1

def create_page():
    print("Creating page")
    # Set page config  
    st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)
    set_page_container_style()

    # Display tasks
    list_length = 7
    list_length = write_task_block("Overdue", "od" , list_length)
    list_length = write_task_block("Today", "due:today", list_length)
    list_length = write_task_block("This Week", "due before:+7 days & !today", list_length)
    list_length = write_task_block("Sometime", "no date", list_length)

create_page()
