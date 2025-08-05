import streamlit as st

def show_task(task, index, on_toggle, on_delete, on_edit):
    cols = st.columns([0.07, 0.55, 0.13, 0.13, 0.12])

    with cols[0]:
        toggle = st.checkbox("", value=task["done"], key=f"cb_{index}")
        if toggle != task["done"]:
            on_toggle(index)

    with cols[1]:
        st.markdown(task["task"])

    with cols[2]:
        if st.button("✏️", key=f"edit_{index}"):
            st.session_state.editing_index = index

    with cols[3]:
        if st.button("🗑️", key=f"del_{index}"):
            on_delete(index)

    if st.session_state.get("editing_index") == index:
        new_val = st.text_input("Edit task", value=task["task"], key=f"edit_input_{index}")
        if st.button("💾 Save", key=f"save_{index}"):
            on_edit(index, new_val)
            st.session_state.editing_index = None
            st.rerun()
