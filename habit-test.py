# --- USER LOG IN ---
import streamlit as st
import datetime
import json

def set_stage(i):
    st.session_state.stage = i

def store_data(dict):
    filename = dict["username"]

    with open(f"{filename}information.json", "w") as file:
        json.dump(dict, file)

def load_account():
    st.write("Loading...")

# key numbers (1, 2, 3) etc for creation of account, and letters (a, b, c) for loggin in
def title_screen():
    if "stage" not in st.session_state:
        st.session_state.stage = 0
    # end if

    if st.session_state.stage == 0:
        st.title("Welcome to Habitum")
        account_status = st.radio("Do you have an account?", ("Yes", "No"))
        if account_status == "Yes":
            st.button("Login", on_click=set_stage, args=["a"], key="login")
        elif account_status == "No":
            st.button("Create Account", on_click=set_stage, args=[1], key="new account")    
    # end if

    # --- NEW ACCOUNT CODE ---
    if  st.session_state.stage == 1:
        st.text_input("Please make a username", key="username")
        st.text_input("Please enter a memorable password", key="password")
        st.date_input("Please enter your birthday?", key="birthday", format="DD/MM/YYYY")
        col1, col2 = st.columns(2, gap="large")
        
        st.button("Submit ", on_click=set_stage, args=[2], use_container_width=True)
        
        st.button("Restart", on_click=set_stage, args=[0], use_container_width=True)
    # end if

    if  st.session_state.stage == 2:
        st.session_state.birthday = str(st.session_state.birthday)
        user_dict = {}
        user_dict["username"] = st.session_state.username
        user_dict["password"] = st.session_state.password
        user_dict["birthday"] = st.session_state.birthday
        # don't save the user password in the user dict 
        # but for now the key is the username and the password is the data stored
        
        store_data(user_dict)
    # end if

    # --- LOGIN TO EXISTING ACCOUNT ---
    if st.session_state.stage == "a":
        st.text_input("What is your username", key="username")
        st.text_input("What is your password", key="password")
        col1, col2 = st.columns(2, gap="large")
        # with col1:
        st.button("Continue", on_click=set_stage, args= "b",use_container_width=True)
        # with col2:
        st.button("Restart", on_click=set_stage, args=[0], use_container_width=True)
    # end if

    if st.session_state.stage == "b":
        load_account()
# end function
title_screen()
# st.write(st.session_state)


