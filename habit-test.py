# --- USER LOG IN ---
import streamlit as st
import datetime
import json

class Userclass:
    #constructor
    def __init__(self, user_habits, user_goals, username, password, birthday):
        #make a dictionary for this specific user and write it to the memory file
        self.user_dictionary = {
            "habits":  user_habits,
            "goals": user_goals,
            "username": username,
            "password": password,
            "birthday": birthday,
        }

    def save(self): 
        filename = self.user_dictionary["username"]
        with open(f"{filename}information.json", "w") as file:
            json.dump(self.user_dictionary, file)
    # end function
# end class



def set_stage(i):
    st.session_state.stage = i

# --- PASSWORD CHECK AND ACCOUNT LOAD ---
def load_account(username, password):
    filename = username + "information.json" 
    user_information = None

    with open(filename, "r") as openfile:
        json_object = json.load(openfile)
    
    correct_account = False

    if json_object["password"] == password:
        correct_account = True
        user_information = json_object
        # end if
    # next key

    if correct_account == False:
        st.write("You entered the wrong infomration, please try again.")
        st.session_state.stage = 0
    else:
        # fill out the user class with data from the json file
        habits = {}
        goals = {}
        birthday = ""
        username = ""

        for key in user_information:
            if key == "habits":
                habits = user_information[key]
            elif key == "goals":
                goals = user_information[key]
            elif key == "birthday":
                birthday = user_information[key]
            elif key == "username":
                username = user_information[key]
            elif key == "password":
                password = user_information[key]
            
        user = Userclass(habits, goals, username, password, birthday)
    # end if
# end function 

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
        # instance of user class
        user = Userclass(user_habits=None, user_goals=None,username=(st.session_state.username), password=(st.session_state.password), birthday=(st.session_state.birthday))
        user.save()
        st.write("The next step is to set your goals")
        
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

    # --- LOAD DATA ---
    if st.session_state.stage == "b":
        load_account(st.session_state.username, st.session_state.password)
# end function
title_screen()
# st.write(st.session_state)


