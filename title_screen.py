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

def finish_intro():
    user = st.session_state.user
    filename = user.user_dictionary["username"]

    # select habits and goals
    with open(f"{filename}information.json", 'r', encoding='utf-8') as json_file:
        user_dict = json.load(json_file)
    
    # updates habits and goals
    user_dict["habits"] = user.user_dictionary["habits"]
    user_dict["goals"] = user.user_dictionary["goals"]

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
    st.write("Congratulation on setting your goals! Remember, self-improvement is a gradual process, and it's important to be patient with yourself. Start with a few Goals that resonate with you and gradually incorporate more over time.")
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

    if st.session_state.stage == 0:
        st.title("Welcome to *Habitum*")

        st.write("Congratulations on taking the first step towards a brighter you. 🌟 ")
        st.write("Habitum is here to guide you on your journey of building positive habits and maintaining streaks that lead to lasting change.")
        st.write("Our app is designed to empower you, helping you unlock your full potential one day at a time. Whether you're striving for better health, increased productivity, enhanced mindfulness, or any other goal that resonates with you, habitum is your companion in this exciting endeavor. Tap 'Next' to learn how Habitum works and how you can make the most of its features. Remember, every small step adds up to a remarkable transformation. 🚀") 
        st.write("Here's to a radiant future filled with accomplishments and growth! The Habitum Team")
        
        account_status = st.radio("Do you have an account?", ("Yes", "No"),key="options")
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

        st.button("Habits", on_click=set_stage, args=[9])

        # st.button("Set my goals", on_click=set_stage, args=[3])
        # st.session_state.fg_count = 1
        # st.session_state.fng_count = 1
        # st.session_state.rg_count = 1
        # st.session_state.ag_count = 1
    # end if

    # --- SETTING GOALS --- Need to fix - do individual session stages for goals selection - use getter and setter methods for goals
    # if  st.session_state.stage == 3:
    #     st.title("Selection")
    #     st.write("Please select the area you would like to set a goal in")
    #     col1, col2, col3, col4 = st.columns(4)
        
    #     st.checkbox("Fitness", on_change=set_stage, args=[4])
    #     st.checkbox("Finances", on_change=set_stage, args=[5])
    #     st.checkbox("Relationships", on_change=set_stage, args=[6])
    #     st.checkbox("Academics / Work", on_change=set_stage, args=[7])

    #     st.button("Continue", on_click=set_stage, args=[8])

    # # -- FITNESS GOALS --
    # if st.session_state.stage == 4:
    #     st.title("Fitness")
    #     st.write("When setting fitness goals these can be holistic goals or very specific targets you set for yourself")
    #     st.write("For example, One of my goals is to run 10km")
    #     fit_goal = st.text_input("Set your fitness goals!", key="fitness_goal")
    #     fg_count = st.session_state.fg_count
    #     num = str(fg_count)
    #     user = st.session_state.user
    #     # being called before there is a goal to put it
    #     if fit_goal != "":
    #         user.user_dictionary["goals"][f"fitness goal {num}"] = [fit_goal]
    #         st.session_state.user = user
    #         st.button("Set another goal", on_click=set_stage, args=[3])
    #         st.session_state.fg_count += 1
    # # end if

    # # -- FINANCIAL GOALS ---
    # if st.session_state.stage == 5:
    #     st.title("Financial")
    #     st.write("When setting Financial goals holistic very specific targets you set for yourself or businesses")
    #     st.write("For example, One of my goals is save £10 every week")
    #     financial_goal = st.text_input("Set your Financial goals!", key="financial_goals")
    #     fng_count = st.session_state.fng_count
    #     num = str(fng_count)
    #     user = st.session_state.user
    #     # being called before there is a goal to put it
    #     if financial_goal != "":
    #         user.user_dictionary["goals"][f"financial goal {num}"] = [financial_goal]
    #         st.session_state.user = user
    #         st.button("Set another goal", on_click=set_stage, args=[3])
    #         st.session_state.fng_count += 1
    # # end if

    # # -- Relationship Goals --
    # if st.session_state.stage == 6:
    #     st.title("Relationship")
    #     st.write("When setting Relationship goals these could be as simple as going on more dates, or seeing your friends.")
    #     st.write("Life is made of relationships so take care of the one's you value the most")
    #     st.write("For example, One of my goals is to see my friends once a week!")
    #     rel_goal = st.text_input("Set your relationship goals!", key="relationship_goals")
    #     rg_count = st.session_state.rg_count
    #     num = str(rg_count)
    #     user = st.session_state.user
    #     # being called before there is a goal to put it
    #     if rel_goal != "":
    #         user.user_dictionary["goals"][f"relationship goal {num}"] = [rel_goal]
    #         st.session_state.user = user
    #         st.button("Set another goal", on_click=set_stage, args=[3])
    #         st.session_state.rg_count += 1
    # # end if

    # # --- ACADEMIC / WORKPLACE GOALS --
    # if st.session_state.stage == 7:
    #     st.title("Academic / Work")
    #     st.write("When setting Academic / Work goals these can be holistic or very specific targets you set for yourself")
    #     st.write("For example, One of my goals is have a 4.0 Gpa")
    #     ac_goal = st.text_input("Set your goals!", key="academic_goals")
    #     ag_count = st.session_state.ag_count
    #     num = str(ag_count)
    #     user = st.session_state.user
    #     # being called before there is a goal to put it
    #     if ac_goal != "":
    #         user.user_dictionary["goals"][f"academic goal {num}"] = [ac_goal]
    #         st.session_state.user = user
    #         st.button("Set another goal", on_click=set_stage, args=[3])
    #         st.session_state.ag_count += 1
    # # end if
    
    # # -- UPDATE USER INFORMATION AND CONTINUE --
    # if st.session_state.stage == 8:
    #     display_goals()
    #     st.subheader("The Next Step")
    #     st.write("If you are happy with your goals - click the button to set your habits")
    #     st.button("Habits", on_click=set_stage, args=[9])
    
    # --- HABIT SETTING !!---
    if st.session_state.stage == 9:
        st.title("Habits")
        st.subheader("What are Habits?")
        st.write("Habits are small bitesized activities the we aim to do everyday which help us make progress towards our goals.")
        st.write("When you look at a big goals e.g. 'run a marathon' is can seem daunting. So what we do is we break that down into smaller sub goals and set habits which help us achieve them")
        st.write("Hence we are always growing, always making progress!")
        st.button("Set my habits", on_click=set_stage, args=[10], use_container_width=True)
        st.session_state.fit_hab_count = 0
        st.session_state.fin_hab_count = 0
        st.session_state.rel_hab_count = 0
        st.session_state.acc_hab_count = 0
    
    if st.session_state.stage == 10:
        st.title("Habit selection")
        st.write("self-improvement is a gradual process, and it's important to be patient with yourself. Start with a few habits that resonate with you and gradually incorporate more over time. Additionally, consistency is key – it's better to start small and maintain these habits than to take on too much and become overwhelmed.")
        st.write("Please select the area you would like to set habits in")
        st.checkbox("Fitness", on_change=set_stage, args=[11])    
        st.checkbox("Finances", on_change=set_stage, args=[12])
        st.checkbox("Relationships", on_change=set_stage, args=[13])
        st.checkbox("Academics / Work", on_change=set_stage, args=[14])
        st.button("Continue", on_click=set_stage, args=[15])

    # --- FITNESS HABITS ---
    if st.session_state.stage == 11:
        user = st.session_state.user
        st.title("Fitness")
        st.write("Add your habits in the text box bellow, Or you can choose from the suggestions")
        fit_hab = st.text_input("add habit",key = "fit_hab", label_visibility="collapsed")
        if fit_hab != "":
            user.user_dictionary["habits"][f"fit_hab{st.session_state.fit_hab_count}"] = {"desc": fit_hab, "dates_done": []}
            st.session_state.user = user
            st.button("Add another Habbit", on_click=set_stage, args=[10])
            st.session_state.fit_hab_count += 1

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
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Regular Exercise - At least 30 minutes physical activity", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.fit_hab_count += 1
                st.session_state.user = user
            # end if

            if bal_nutrition == True:
                habits = user.user_dictionary["habits"]
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Balanced Nutrition - Consume a well-rounded diet", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if

            if sleep == True:
                habits = user.user_dictionary["habits"]
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Adequate Sleep - Sleep 7-9 hours each night", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if

            if mindful == True:
                habits = user.user_dictionary["habits"]
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Mindful Movement - Practice a mindful exercies like Taichi", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if

            if hydration == True:
                habits = user.user_dictionary["habits"]
                habits[f"fit_hab{st.session_state.fit_hab_count}"] = {"desc":"Hydration - Drink at least 2l of water a day", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if
            set_stage(10)
    # end if

    # --- Finance Habits ---
    if st.session_state.stage == 12:
        user = st.session_state.user
        st.title("Finances")
        st.write("Add your habits in the text box bellow, Or you can choose from the suggestions")
        fin_hab = st.text_input("add habit",key = "fin_hab", label_visibility="collapsed")
        if fin_hab != "":
            user.user_dictionary["habits"][f"fin_hab{st.session_state.fin_hab_count}"] = {"desc": fin_hab, "dates_done": []}
            st.session_state.user = user
            st.button("Add another Habbit", on_click=set_stage, args=[10])
            st.session_state.fin_hab_count += 1

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
                habits[f"fin_hab{st.session_state.fin_hab_count}"] = {"desc":"Budgeting - Spend some time each day to review you spending", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.fin_hab_count += 1
                st.session_state.user = user
            # end if

            if saving == True:
                habits = user.user_dictionary["habits"]
                habits[f"fin_hab{st.session_state.fin_hab_count}"] = {"desc":"Saving - Set aside a some money for rainy days","dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fin_hab_count += 1
            # end if

            if investing == True:
                habits = user.user_dictionary["habits"]
                habits[f"fin_hab{st.session_state.fin_hab_count}"] = {"desc":"Investing - Invest your money to make it work for you", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fit_hab_count += 1
            # end if

            if delay_grat == True:
                habits = user.user_dictionary["habits"]
                habits[f"fin_hab{st.session_state.fin_hab_count}"] = {"desc":"Spend No Money - Delay Gratification","dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.fin_hab_count += 1
            # end if
            set_stage(10)
    # end if
    
    # --- RELATIONSHIP HABITS ---
    if st.session_state.stage == 13:
        user = st.session_state.user
        st.title("Relationships")
        st.write("Add your habits in the text box bellow, Or you can choose from the suggestions")
        rel_hab = st.text_input("add habit",key = "rel_hab", label_visibility="collapsed")
        if rel_hab != "":
            user.user_dictionary["habits"][f"rel_hab{st.session_state.rel_hab_count}"] = {"desc": rel_hab, "dates_done": []}
            st.session_state.user = user
            st.button("Add another Habbit", on_click=set_stage, args=[10])
            st.session_state.rel_hab_count += 1

        st.divider()
        gratitude = st.checkbox("**Gratitude**: Express appreciation for the people in your life through words and actions.")
        qual_time = st.checkbox("**Quality Time**: Spend meaningful time with loved ones, nurturing connections and creating positive memories.")
        communication = st.checkbox("**Effective Communication**: Improve your interpersonal skills by actively listening and expressing yourself clearly and empathetically.")
        st.divider()

        clicked = st.button("Doublc click to continue", use_container_width=True)
        if clicked == True:
            if gratitude == True:
                habits = user.user_dictionary["habits"]
                habits[f"rel_hab{st.session_state.rel_hab_count}"] = {"desc":"Gratitude - Express appreciation for the people an things in your life","dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.rel_hab_count += 1

            if qual_time == True:
                habits = user.user_dictionary["habits"]
                habits[f"rel_hab{st.session_state.rel_hab_count}"] = {"desc":"Quality Time - Spend Time with those you Love","dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.rel_hab_count += 1
            
            if communication == True:
                habits = user.user_dictionary["habits"]
                habits[f"rel_hab{st.session_state.rel_hab_count}"] = {"desc":"Communication - Improve your social skills by speaking to a stranger everyday", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.rel_hab_count += 1
            # end if
            set_stage(10)
    # end if
        
    # --- ACADEMIC / WORK HABITS ---
    if st.session_state.stage == 14:
        user = st.session_state.user
        st.title("Academic / Work")
        st.write("Add your habits in the text box bellow, Or you can choose from the suggestions")
        acc_hab = st.text_input("add habit",key = "acc_hab", label_visibility="collapsed")
        if acc_hab != "":
            user.user_dictionary["habits"][f"acc_hab{st.session_state.acc_hab_count}"] = {"desc": acc_hab, "dates_done":[]}
            st.session_state.user = user
            st.button("Add another Habbit", on_click=set_stage, args=[10])
            st.session_state.acc_hab_count += 1
        
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
                habits[f"acc_hab{st.session_state.acc_hab_count}"] = {"desc":"Continuous Learning - Learn something new everyday", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.acc_hab_count += 1

            if time_management == True:
                habits = user.user_dictionary["habits"]
                habits[f"acc_hab{st.session_state.acc_hab_count}"] = {"desc":"Time Management - Plan the next day, focus your intent on a few critical tasks", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.acc_hab_count += 1
        
            if goal_setting == True:
                habits = user.user_dictionary["habits"]
                habits[f"acc_hab{st.session_state.acc_hab_count}"] = {"desc":"Goal Setting - Redefine and look over your goals everyday","dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.acc_hab_count += 1

            if networking == True:
                habits = user.user_dictionary["habits"]
                habits[f"acc_hab{st.session_state.acc_hab_count}"] = {"desc":"Networking - Build a strong professional network", "dates_done":[]}
                user.user_dictionary["habits"] = habits
                st.session_state.user = user
                st.session_state.acc_hab_count += 1
            # end if
            set_stage(10)
        # end if
    # end if

    # --- ALL HABITS SET ---
    if st.session_state.stage == 15:
        display_habits()
        st.button("Continue to Launchpad", on_click=finish_intro, use_container_width=True)

    # --- LOGIN TO EXISTING ACCOUNT ---
    if st.session_state.stage == "a":
        st.session_state.username = st.text_input("What is your username")
        st.session_state.password = st.text_input("What is your password")
        st.button("Login",on_click=set_stage, args=["b"])
    
    if st.session_state.stage == "b":
        st.button("Continue to Launchpad", on_click=finish_login,use_container_width=True)

    if st.session_state.login_finished == True:
        return [st.session_state.username, st.session_state.password]

    if st.session_state.intro_finished == True:
        user = st.session_state.user
        st.session_state.username = user.user_dictionary["username"]
        st.session_state.password = user.user_dictionary["password"]
        return [st.session_state.username, st.session_state.password]

    # TODO fix the create new account bug when accessing the launchpad
    st.write(st.session_state)
# end function
        


