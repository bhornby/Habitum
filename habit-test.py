# --- USER LOG IN ---
import streamlit as st
import datetime
import json

def set_stage(i):
    st.session_state.stage = i

def store_data(dict):
    filename = dict["name"] + dict["surname"] 

    with open(f"{filename}information.json", "w") as file:
        json.dump(dict, file)

# key numbers (1, 2, 3) etc for creation of account, and letters (a, b, c) for loggin in

def title_screen():

    if "stage" not in st.session_state:
        st.session_state.stage = 0
    # end if

    if st.session_state.stage == 0:
       st.title("Welcome to Habitum")
       st.button("Create Account", on_click=set_stage, args=[1], key="begin")
    # end if

    if  st.session_state.stage == 1:
        st.text_input("What is your name", key="name")
        st.text_input("What is your surname", key="surname")
        st.date_input("When is your birthday?", key="birthday")
        st.button("done", on_click=set_stage, args=[2])
    # end if

    if  st.session_state.stage == 2:
        st.session_state.birthday = str(st.session_state.birthday)
        user_dict = {}
        user_dict["name"] = st.session_state.name
        user_dict["surname"] = st.session_state.surname
        user_dict["birthday"] = st.session_state.birthday
        store_data(user_dict)
    # end if
# end function
title_screen()