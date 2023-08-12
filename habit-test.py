# --- USER LOG IN ---
import streamlit as st

def set_stage(i):
    st.session_state.stage = i

def log_in():

    if "stage" not in st.session_state:
        st.session_state.stage = 0
    # end if

    if st.session_state.stage == 0:
       st.title("Welcome to Habitum")
       st.button("Begin", on_click=set_stage, args=[1], key="begin")
    # end if

    if  st.session_state.stage == 1:
        st.text_input("What is your name", on_change=set_stage, args=[2], key="name")
    # end if

    if  st.session_state.stage == 2:
        return st.session_state.name
    
# end function
username = log_in()

st.write(username)
st.write(st.session_state)
