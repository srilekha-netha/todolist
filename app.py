import streamlit as st
from src.task_manager import (
    load_tasks, save_tasks,
    add_task, toggle_task, delete_task, update_task,
    filter_tasks, load_deleted_tasks
)
from src.ui_components import show_task

st.set_page_config("TaskTrek", layout="centered")

# Load from storage
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "deleted_tasks" not in st.session_state:
    st.session_state.deleted_tasks = load_deleted_tasks()

st.title("🧠 TaskTrek")

# Sidebar: add and filter
st.sidebar.header("➕ Add Task")
new_task = st.sidebar.text_input("What do you want to do?")

if st.sidebar.button("Add"):
    if new_task.strip():
        st.session_state.tasks = add_task(st.session_state.tasks, new_task.strip())
        save_tasks(st.session_state.tasks)
        st.rerun()

st.sidebar.markdown("---")
filter_option = st.sidebar.radio("📂 Filter", ["All", "Pending", "Completed", "Deleted"])

# --- Callbacks ---
def handle_toggle(index):
    st.session_state.tasks = toggle_task(st.session_state.tasks, index)
    save_tasks(st.session_state.tasks)
    st.rerun()

def handle_delete(index):
    st.session_state.tasks = delete_task(st.session_state.tasks, index)
    save_tasks(st.session_state.tasks)
    st.session_state.deleted_tasks = load_deleted_tasks()
    st.rerun()

def handle_edit(index, new_text):
    st.session_state.tasks = update_task(st.session_state.tasks, index, new_text)
    save_tasks(st.session_state.tasks)

# --- Display Tasks ---
if filter_option == "Deleted":
    st.subheader(f"🗑️ Deleted Tasks ({len(st.session_state.deleted_tasks)})")
    if not st.session_state.deleted_tasks:
        st.info("No deleted tasks.")
    else:
        for task in st.session_state.deleted_tasks:
            st.markdown(f"~~{task['task']}~~")
else:
    filtered = filter_tasks(st.session_state.tasks, filter_option)
    st.subheader(f"📋 {filter_option} Tasks ({len(filtered)})")

    if not filtered:
        st.info("No tasks to display.")
    else:
        for i, task in enumerate(filtered):
            real_index = st.session_state.tasks.index(task)
            show_task(
                task,
                index=real_index,
                on_toggle=handle_toggle,
                on_delete=handle_delete,
                on_edit=handle_edit,
            )
