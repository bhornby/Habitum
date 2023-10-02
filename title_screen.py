# --- USER LOG IN ---
import streamlit as st
import datetime
import json
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import time

online = False

class Userclass:
    #constructor
    def __init__(self, user_habits, username, password, birthday):
        #make a dictionary for this specific user and write it to the memory file
        self.user_dictionary = {
            "habits":  user_habits,
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

def finish_intro():
    user = st.session_state.user
    filename = user.user_dictionary["username"]

    # select habits
    with open(f"{filename}information.json", 'r', encoding='utf-8') as json_file:
        user_dict = json.load(json_file)
    
    # updates habits
    user_dict["habits"] = user.user_dictionary["habits"]

    # need to replace the old with the new
    with open(f"{filename}information.json", 'w', encoding='utf-8') as json_file:
        json.dump(user_dict, json_file)

    set_stage("c")
    st.session_state.intro_finished = True
    # hello

def finish_login():
    # no need to update as the file already exitst
    set_stage("c")
    st.session_state.login_finished = True
    
def display_habits():
    
    user = st.session_state.user
    habits = user.user_dictionary["habits"]
    st.title("Your habits")

    st.subheader("Fitness Habits:")
    for key in habits:
        if "fit_hab" in key:
            st.write(habits[key]["desc"])
    
    st.subheader("Finance Habits:")
    for key in habits:
        if "fin_hab" in key:
            st.write(habits[key]["desc"])

    st.subheader("Relationship Habits:")
    for key in habits:  
        if "rel_hab" in key:
            st.write(habits[key]["desc"])

    st.subheader("Academic / Work Habits:")
    for key in habits:
        if "acc_hab" in key:
            st.write(habits[key]["desc"])
# end function

def make_intro_finished():
    st.session_state.intro_finished = False

def make_login_finished():
    st.session_state.login_finished = False

def increment(count):
    count += 1

def set_stage(i):
    st.session_state.clicked = True
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
        birthday = ""
        username = ""

        for key in user_information:
            if key == "habits":
                habits = user_information[key]
            elif key == "birthday":
                birthday = user_information[key]
            elif key == "username":
                username = user_information[key]
            elif key == "password":
                password = user_information[key]
            
        user = Userclass(habits, username, password, birthday)
        st.session_state.user = user
    # end if
# end function 

# key numbers (1, 2, 3) etc for creation of account, and letters (a, b, c) for loggin in
def title_screen():
    if "stage" not in st.session_state:
        st.session_state.stage = 0
    # end if
    if "intro_finished" not in st.session_state:
        make_intro_finished()

    if "login_finished" not in st.session_state:
            make_login_finished()

# --- MAIN LANDING PAGE ---
    if st.session_state.stage == 0:
        st.set_page_config(layout="centered")
        st.title("*Habitum*")
        st.divider()
        
        
        st.subheader("Habitum is the to do list that makes it easy for you to visualise, analyse, and share you habits.")
        st.markdown("#")
        col3, col4, col5 = st.columns(3)
        with col4:
            st.metric(label="Habits Completed", value="5", delta="1")
        with col5:
            st.metric(label="Habits Remaining", value="9", delta="-5", delta_color="inverse")
        with col3:
            st.metric(label="Longest Streak", value="3🔥", delta="1")

        st.markdown("#")
        st.markdown("#")
        st.subheader("View your progress at a glance with the metrics system, or delve deeper with our graphical analysis")
        st.markdown("#")

        chart_data = pd.DataFrame(
        np.random.randn(40, 2),
        columns = ['Go for a run', 'Walk the dog'])

        st.area_chart(chart_data)

        st.markdown("######")
        st.subheader("Choose or Create as many habits as you want, such as:")
        st.markdown("#####")
        col1, col2, col3 = st.columns(3)
        with col2:
            st.write("- Brush your teeth\n- Go to the gym\n- Practice Piano\n- Sleep 8 hours")
        st.markdown("#")

        st.subheader("Everyday you complete a task, your streak is extened! So don't break the chain, or your streak will fall to zero.")

        st.markdown("#")

        col3, col4, col5 = st.columns(3)
        with col4:
            st.metric(label="Longest Streak", value="0💀", delta="-3", delta_color="normal")

        st.subheader("Compete with you friends to maintain the longest streak unlocking medals and rewards along the way.")

        col3, col4, col5 = st.columns(3)
        with col4:
            st.title("🏅🏅🏅🏅")
        
        st.markdown("##")

        st.subheader("Sign up to our weekly newsletter to be notified when Beta Access goes live!")

        # st.subheader("Working on someting everyday helps you form new habits.")

        st.markdown("#")

        # st.subheader("Live the life you deserve, go build those habits")
        
        # st.markdown("#")
        
        if online == True:
            st.button("Sign up for pre-release", on_click=set_stage,args=["email"], use_container_width=True)
        elif online == False:
            col1 , col2 = st.columns(2)
            with col1:
                st.button("Login", on_click=set_stage, args=["a"], key="login", use_container_width=True)
            with col2:
                st.button("Create Account", on_click=set_stage, args=[1], key="new account", use_container_width=True)    
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
        user = Userclass(user_habits={},username=(st.session_state.username), password=(st.session_state.password), birthday=(st.session_state.birthday))
        user.save()
        st.session_state.user = user
        st.button("Set my Habits", on_click=set_stage, args=[3])

    # end if

    # --- HABIT SETTING !!---
    if st.session_state.stage == 3:
        st.title("Habits")
        st.subheader("What are Habits?")
        st.write("Habits are small bitesized activities the we aim to do everyday which help us make progress towards our goals.")
        st.write("When you look at a big goals e.g. 'run a marathon' is can seem daunting. So what we do is we break that down into smaller sub goals and set habits which help us achieve them")
        st.write("Hence we are always growing, always making progress!")
        st.button("Set my habits", on_click=set_stage, args=[4], use_container_width=True)
        st.session_state.fit_hab_count = 0
        st.session_state.fin_hab_count = 0
        st.session_state.rel_hab_count = 0
        st.session_state.acc_hab_count = 0
    
    if st.session_state.stage == 4:
        st.title("Habit selection")
        st.write("self-improvement is a gradual process, and it's important to be patient with yourself. Start with a few habits that resonate with you and gradually incorporate more over time. Additionally, consistency is key – it's better to start small and maintain these habits than to take on too much and become overwhelmed.")
        st.write("Please select the area you would like to set habits in")
        st.checkbox("Fitness", on_change=set_stage, args=[5])    
        st.checkbox("Finances", on_change=set_stage, args=[6])
        st.checkbox("Relationships", on_change=set_stage, args=[7])
        st.checkbox("Academics / Work", on_change=set_stage, args=[8])
        st.button("Continue", on_click=set_stage, args=[9])

    # --- FITNESS HABITS ---
    if st.session_state.stage == 5:
        user = st.session_state.user
        st.title("Fitness")
        st.write("Select your habits from the options below, you can add your own custom habits on the launchpad")

        st.divider()
        # use the checkbox
        reg_exercise = st.checkbox("**Regular Exercise:** Engage in physical activity for at least 30 minutes most days of the week to improve cardiovascular health, strength, and overall well-being.")
        bal_nutrition = st.checkbox("**Balanced Nutrition:** Consume a well-rounded diet that includes a variety of fruits, vegetables, lean proteins, whole grains, and healthy fats.")
        sleep = st.checkbox("**Adequate Sleep**: Prioritize getting 7-9 hours of quality sleep each night to support physical and mental recovery.")
        mindful = st.checkbox("**Mindful Movement**: Incorporate mindfulness practices like yoga, tai chi, or meditation to promote relaxation and flexibility.")
        hydration = st.checkbox("**Hydration:** Drink enough water throughout the day to stay hydrated and support bodily functions.")
        st.divider()
        # clicked = st.checkbox("**Continue**")
        clicked = st.button("Doublc click to continue", use_container_width=True)
        if clicked == True:
            if reg_exercise == True:
                habits = user.user_dictionary["habits"]
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Regular Exercise - At least 30 minutes physical activity", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.fit_hab_count += 1
                st.session_state.user = user
            # end if

            if bal_nutrition == True:
                habits = user.user_dictionary["habits"]
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Balanced Nutrition - Consume a well-rounded diet", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if

            if sleep == True:
                habits = user.user_dictionary["habits"]
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Adequate Sleep - Sleep 7-9 hours each night", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if

            if mindful == True:
                habits = user.user_dictionary["habits"]
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Mindful Movement - Practice a mindful exercies like Taichi", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if

            if hydration == True:
                habits = user.user_dictionary["habits"]
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Hydration - Drink at least 2l of water a day", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if
            set_stage(4)
    # end if

    # --- Finance Habits ---
    if st.session_state.stage == 6:
        user = st.session_state.user
        st.title("Finances")
        st.write("Select your habits from the options below, you can add your own custom habits on the launchpad")

        st.divider()

        budgeting = st.checkbox("**Budgeting**: Create a detailed budget to track income, expenses, and savings goals.")
        saving = st.checkbox("**Savings**: Regularly set aside a portion of your income for savings and emergency funds.")
        investing = st.checkbox("**Investing**: Educate yourself about investing to grow your wealth over time.")
        delay_grat = st.checkbox("**Spend No Money**: Practice self-discipline by avoiding unnecessary purchases and focusing on long-term financial goals.")

        st.divider()

        clicked = st.button("Doublc click to continue", use_container_width=True)
        if clicked == True:
            if budgeting == True:
                habits = user.user_dictionary["habits"]
                habits[f"fin_hab{st.session_state.fin_hab_count}"] = {"desc":"Budgeting - Spend some time each day to review you spending", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.fin_hab_count += 1
                st.session_state.user = user
            # end if

            if saving == True:
                habits = user.user_dictionary["habits"]
                habits[f"fin_hab{st.session_state.fin_hab_count}"] = {"desc":"Saving - Set aside a some money for rainy days","dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fin_hab_count += 1
            # end if

            if investing == True:
                habits = user.user_dictionary["habits"]
                habits[f"fin_hab{st.session_state.fin_hab_count}"] = {"desc":"Investing - Invest your money to make it work for you", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if

            if delay_grat == True:
                habits = user.user_dictionary["habits"]
                habits[f"fin_hab{st.session_state.fin_hab_count}"] = {"desc":"Spend No Money - Delay Gratification","dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fin_hab_count += 1
            # end if
            set_stage(4)
    # end if
    
    # --- RELATIONSHIP HABITS ---
    if st.session_state.stage == 7:
        user = st.session_state.user
        st.title("Relationships")
        st.write("Select your habits from the options below, you can add your own custom habits on the launchpad")

        st.divider()
        gratitude = st.checkbox("**Gratitude**: Express appreciation for the people in your life through words and actions.")
        qual_time = st.checkbox("**Quality Time**: Spend meaningful time with loved ones, nurturing connections and creating positive memories.")
        communication = st.checkbox("**Effective Communication**: Improve your interpersonal skills by actively listening and expressing yourself clearly and empathetically.")
        st.divider()

        clicked = st.button("Doublc click to continue", use_container_width=True)
        if clicked == True:
            if gratitude == True:
                habits = user.user_dictionary["habits"]
                habits[f"rel_hab{st.session_state.rel_hab_count}"] = {"desc":"Gratitude - Express appreciation for the people an things in your life","dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.rel_hab_count += 1

            if qual_time == True:
                habits = user.user_dictionary["habits"]
                habits[f"rel_hab{st.session_state.rel_hab_count}"] = {"desc":"Quality Time - Spend Time with those you Love","dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.rel_hab_count += 1
            
            if communication == True:
                habits = user.user_dictionary["habits"]
                habits[f"rel_hab{st.session_state.rel_hab_count}"] = {"desc":"Communication - Improve your social skills by speaking to a stranger everyday", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.rel_hab_count += 1
            # end if
            set_stage(4)
    # end if
        
    # --- ACADEMIC / WORK HABITS ---
    if st.session_state.stage == 8:
        user = st.session_state.user
        st.title("Academic / Work")
        st.write("Select your habits from the options below, you can add your own custom habits on the launchpad")
        
        st.divider()
        cont_learn = st.checkbox("**Continuous Learning**: Cultivate a habit of learning by reading books, taking courses, or attending workshops relevant to your field.")
        time_management = st.checkbox("**Time Management**: Plan the next day, focus your intent on a set few critical tasks")
        goal_setting = st.checkbox("**Goal Setting**: Redefine and look over your goals everyday, set meaningful and personal goals that resonate with you.")
        networking = st.checkbox("**Networking**: Build a strong professional network by attending events and maintaining connections with peers and mentors.")
        st.divider()

        clicked = st.button("Doublc click to continue", use_container_width=True)
        if clicked == True:
            if cont_learn == True:
                habits = user.user_dictionary["habits"]
                habits[f"acc_hab{st.session_state.acc_hab_count}"] = {"desc":"Continuous Learning - Learn something new everyday", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.acc_hab_count += 1

            if time_management == True:
                habits = user.user_dictionary["habits"]
                habits[f"acc_hab{st.session_state.acc_hab_count}"] = {"desc":"Time Management - Plan the next day, focus your intent on a few critical tasks", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.acc_hab_count += 1
        
            if goal_setting == True:
                habits = user.user_dictionary["habits"]
                habits[f"acc_hab{st.session_state.acc_hab_count}"] = {"desc":"Goal Setting - Redefine and look over your goals everyday","dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.acc_hab_count += 1

            if networking == True:
                habits = user.user_dictionary["habits"]
                habits[f"acc_hab{st.session_state.acc_hab_count}"] = {"desc":"Networking - Build a strong professional network", "dates_done":[], "streak": 0}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.acc_hab_count += 1
            # end if
            set_stage(4)
        # end if
    # end if

    # --- ALL HABITS SET ---
    if st.session_state.stage == 9:
        display_habits()
        st.button("Continue to Launchpad", on_click=finish_intro, use_container_width=True)

    # --- LOGIN TO EXISTING ACCOUNT ---
    if st.session_state.stage == "a":
        st.session_state.username = st.text_input("What is your username")
        st.session_state.password = st.text_input("What is your password")
        st.button("Continue to Launchpad", on_click=finish_login,use_container_width=True)
    
    if st.session_state.login_finished == True:
        return [st.session_state.username, st.session_state.password]

    if st.session_state.intro_finished == True:
        user = st.session_state.user
        st.session_state.username = user.user_dictionary["username"]
        st.session_state.password = user.user_dictionary["password"]
        return [st.session_state.username, st.session_state.password]
    
    # --- COLLECT USER EMAILS IF INTERESTED --- 
    if st.session_state.stage == "email":
        st.title("Registration")
        

    
    # st.write(st.session_state)
# end function
        


