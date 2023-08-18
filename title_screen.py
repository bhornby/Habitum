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

def display_goals():
    fg_list = []
    fng_list = []
    rg_list = []
    ag_list = []

    user = st.session_state.user
    goals = user.user_dictionary["goals"]
    for key in goals:
        if "fitness goal" in key:
            fg_list.append(goals[key])
        elif "financial goal" in key:
            fng_list.append(goals[key])
        elif "relationship goal " in key:
            rg_list.append(goals[key])
        elif "academic goal" in key:
            ag_list.append(goals[key])
        # end if
    # next key

    # col1, col2, col3, col4 = st.columns(4)
    # with col1:
    st.title("Your Goals")
    st.subheader("Fitness Goals")
    for list in fg_list:
        st.write(*list)
    # with col2:
    st.subheader("Financial Goals")
    for list in fng_list:
        st.write(*list)    
    # with col3:
    st.subheader("Relationship Goals")
    for list in rg_list:
        st.write(*list)
    # with col4:
    st.subheader("Academic Goals")
    for list in ag_list:
        st.write(*list)
# end function


def increment(count):
    count += 1

def set_stage(i):
    st.session_state.stage = i

def goal_button_clicked():
    st.session_state.clicked = True

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
        account_status = st.radio("Do you have an account?", ("Yes", "No"), key="option")
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

    # -- COLLECTING INFORMATION --
    if  st.session_state.stage == 2:
        st.session_state.birthday = str(st.session_state.birthday)
        # instance of user class
        user = Userclass(user_habits={}, user_goals={},username=(st.session_state.username), password=(st.session_state.password), birthday=(st.session_state.birthday))
        user.save()
        st.session_state.user = user
        st.title("Goals")
        st.write("The next step is to set your goals")
        st.write("Goals can be set for all areas of your life and are extreemly benificial.") 
        st.write("They can provide you with the motivation when you need it the most giving you that extra drive. Just the fact that your using this web app shows you've got what it takes to succeed!")
        st.write("If you've got what it takes click the button below to begin")
        st.button("Set my goals", on_click=set_stage, args=[3])
        st.session_state.fg_count = 1
        st.session_state.fng_count = 1
        st.session_state.rg_count = 1
        st.session_state.ag_count = 1
    # end if

    # --- SETTING GOALS --- Need to fix - do individual session stages for goals selection - use getter and setter methods for goals
    if  st.session_state.stage == 3:
        st.title("Selection")
        st.write("Please select the area you would like to set a goal in")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("Fitness", on_click=set_stage, args=[4])
        with col2:
            st.button("Finances", on_click=set_stage, args=[5])
        with col3:
            st.button("Relationships", on_click=set_stage, args=[6])
        with col4:
            st.button("Academics", on_click=set_stage, args=[7])

        st.button("Continue", on_click=set_stage, args=[8])

    # -- FITNESS GOALS --
    if st.session_state.stage == 4:
        st.title("Fitness")
        st.write("When setting fitness goals these can be holistic goals or very specific targets you set for yourself")
        st.write("For example, One of my goals is to run 10km")
        fit_goal = st.text_input("Set your fitness goals!", key="fitness_goal")
        fg_count = st.session_state.fg_count
        num = str(fg_count)
        user = st.session_state.user
        # being called before there is a goal to put it
        if fit_goal != "":
            user.user_dictionary["goals"][f"fitness goal {num}"] = [fit_goal]
            st.session_state.user = user
            st.button("Set another goal", on_click=set_stage, args=[3])
            st.session_state.fg_count += 1
    # end if

    # -- FINANCIAL GOALS ---
    if st.session_state.stage == 5:
        st.title("Financial")
        st.write("When setting Financial goals holistic very specific targets you set for yourself or businesses")
        st.write("For example, One of my goals is save £10 every week")
        financial_goal = st.text_input("Set your Financial goals!", key="financial_goals")
        fng_count = st.session_state.fng_count
        num = str(fng_count)
        user = st.session_state.user
        # being called before there is a goal to put it
        if financial_goal != "":
            user.user_dictionary["goals"][f"financial goal {num}"] = [financial_goal]
            st.session_state.user = user
            st.button("Set another goal", on_click=set_stage, args=[3])
            st.session_state.fng_count += 1
    # end if

    # -- Relationship Goals --
    if st.session_state.stage == 6:
        st.title("Relationship")
        st.write("When setting Relationship goals these could be as simple as going on more dates, or seeing your friends.")
        st.write("Life is made of relationships so take care of the one's you value the most")
        st.write("For example, One of my goals is to see my friends once a week!")
        rel_goal = st.text_input("Set your relationship goals!", key="relationship_goals")
        rg_count = st.session_state.rg_count
        num = str(rg_count)
        user = st.session_state.user
        # being called before there is a goal to put it
        if rel_goal != "":
            user.user_dictionary["goals"][f"relationship goal {num}"] = [rel_goal]
            st.session_state.user = user
            st.button("Set another goal", on_click=set_stage, args=[3])
            st.session_state.rg_count += 1
    # end if

    if st.session_state.stage == 7:
        st.title("Academic")
        st.write("When setting Academic goals these can be holistic or very specific targets you set for yourself")
        st.write("For example, One of my goals is have a 4.0 Gpa")
        ac_goal = st.text_input("Set your Academic goals!", key="academic_goals")
        ag_count = st.session_state.ag_count
        num = str(ag_count)
        user = st.session_state.user
        # being called before there is a goal to put it
        if ac_goal != "":
            user.user_dictionary["goals"][f"academic goal {num}"] = [ac_goal]
            st.session_state.user = user
            st.button("Set another goal", on_click=set_stage, args=[3])
            st.session_state.ag_count += 1
    # end if
    
    # -- UPDATE USER INFORMATION AND CONTINUE --
    if st.session_state.stage == 8:
        display_goals()
        

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

# TODO display the users goals nicely - then ask perform habit analysis - chat gpt input??? - make sure to have space for personal input
# learn how to display the data from the dictionary nicely
# TODO save the user data to the json file as well - update it
# TODO use the metrics feature for indicating how well the day has gone
