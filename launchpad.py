import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
from title_screen import Userclass
from title_screen import load_account


def set_stage(i):
    st.session_state.stage = i

def update_save():
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
# end function

def calculate_streaks():
    habits = st.session_state.habits
    longest = 0
    habit_date_list = []
    longest_habit = None

    for key in habits:
        habit_date_list = habits[key]["dates_done"]
        count = 0
        temp = 0
        day = 0

        if habit_date_list == []:
            continue
        else:
            for date in habit_date_list:
                date_string = date
                date_string.replace("/","")
                date_num_list = list(date_string)
                # take the 3rd and 4th characters and append them into a string then convert to number then save as temp - mm/dd/yyyy
                
                if date_num_list[3] == "0":
                    day = date_num_list[4]
                else:
                    day = date_num_list[3] + date_num_list[4]
                # end if
                
                day = int(day)
                if (temp+1) == day:
                    temp = day
                    count += 1
                # end if
            # next day
            if count > longest:
                longest = temp
                # --- TO RETURN THE LONGEST HABIT ---
                longest_habit = habits[key]
            # end if
        # end if
    # next key
    return longest, longest_habit
# end function

def display_metrics():
    habits = st.session_state.habits
    
    # tells you the number of keys - therefore habits
    num_habits = len(habits) 
    habits_completed = 0
    now = datetime.now()
    today = now.strftime("%m/%d/%Y")
    for key in habits:
        if today in habits[key]["dates_done"]:
            habits_completed += 1
        # end if
    # next key
    habits_remaining = num_habits - habits_completed

    # --- Caluclate the longest streak ---
    longest_streak, longest_habit = calculate_streaks()

    col1, col2, col3 = st.columns(3)
    with col2:
        st.metric(label="Habits Completed", value=habits_completed, delta=habits_completed,delta_color="normal")
    with col3:
        st.metric(label="Habits Remaining", value=habits_remaining, delta=-habits_completed, delta_color="inverse")
    with col1:
        st.metric(label="Longest Streak",value=f"{longest_streak}🔥", delta=longest_streak,delta_color="normal")

    # area chart showing the running progress
    
    # also need to calculate the past number of habits done on that day
            
    date_list = []
    habits_completed_list = []
    index_list = []
    
    for key in habits:
        for date in habits[key]["dates_done"]:
            if date not in date_list and date != []:
                date_list.append(date)

    # should return a list which holds the number of habits done for each day
    habit_count = 0
    for date in date_list:
        for key in habits:
            if date in habits[key]["dates_done"]:
                habit_count += 1
            # end if
        # next key
        habits_completed_list.append(habit_count)
        habit_count = 0
    # next date
    
    count = 0
    for day in date_list:
        index_list.append(count)
        count += 1


    data = {
        "Habits Completed": habits_completed_list,
        "Dates":date_list
    }
    
    df = pd.DataFrame(data, index = index_list)
    # st.write(df)
    
    st.markdown("#")
    st.area_chart(
        data = df,
        x = "Dates",
        y = "Habits Completed",
    )
    

def display_habits(user):
    habits = st.session_state.habits
    # use a checkbox column
    fit_flag = 0
    fin_flag = 0
    rel_flag = 0
    acc_flag = 0

    fit_hab_list = []
    fin_hab_list = []
    rel_hab_list = []
    acc_hab_list = []

    for key in habits:
        if "fit" in key:
            fit_hab_list.append(habits[key]["desc"])
        # end if
    
    for key in habits:
        if "fin" in key:
            fin_hab_list.append(habits[key]["desc"])
        # end if
    
    for key in habits:
        if "rel" in key:
            rel_hab_list.append(habits[key]["desc"])
        # end if
    
    for key in habits:
        if "acc" in key:
            acc_hab_list.append(habits[key]["desc"])
        # end if


    for key in habits:
        if "fit_hab" in key:
            fit_flag += 1
        elif "fin_hab" in key:
            fin_flag += 1
        elif "rel_hab" in key:
            rel_flag += 1
        elif "acc_hab" in key:
            acc_flag += 1
    
    if fit_flag > 0:
        make_checkbox_col("fit",fit_hab_list, habits)
        update_checkbox_col("Fitness", habits, fit_hab_list,user)
    # end if
    if fin_flag > 0:
        make_checkbox_col("fin",fin_hab_list,habits)
        update_checkbox_col("Finances", habits, fin_hab_list,user)
    # end if
    if rel_flag > 0:
        make_checkbox_col("rel", rel_hab_list,habits)
        update_checkbox_col("Relationships", habits, rel_hab_list,user)
    # end if
    if acc_flag > 0:
        make_checkbox_col("acc", acc_hab_list,habits)
        update_checkbox_col("Accademic", habits, acc_hab_list,user)
    # end if
# end function

def update_checkbox_col(name, habits, habit_list, user):
    if name == "Fitness":
        dict = st.session_state.Fitness
    elif name == "Finances":
        dict = st.session_state.Finances
    elif name == "Relationships":
        dict = st.session_state.Relationships
    elif name == "Accademic":
        dict = st.session_state.Accademic

    true_pos = []
    edited_pos = []
    box_num = 0

    # loop that returns the true position of each checkbox
    for key in habit_list:
        true_pos.append(box_num)
        box_num += 1
    # next key
    

    for checkbox in dict["edited_rows"]:
        ed_num = checkbox
        for favourite in dict["edited_rows"][checkbox]:
            chosen = dict["edited_rows"][checkbox][favourite]
            if chosen == True:
                edited_pos.append(ed_num)
            # end if
            
        # next favourite
    # next checkbox

    # needs to compare the true pos and the edited pos to figuer out which habit it is
    for pos1 in true_pos:
        for pos2 in edited_pos:
            if habit_list[pos1] == habit_list[pos2]:
                hab = habit_list[pos1]
                now = datetime.now()
                today = now.strftime("%m/%d/%Y")
                for key in habits:
                    if habits[key]["desc"] == hab:
                        habits[key]["dates_done"].append(today)
                    # end if
                # next key
        # next pos
    st.session_state.habits = habits
     # update the save file
    user.user_dictionary["habits"] = st.session_state.habits
    st.session_state.user = user
    update_save() 
# end function - 

def make_checkbox_col(type, habit_list, habits):
    count = 0
    habit_name = f"{type}_hab"
    fav_list = []
    now = datetime.now()
    today = now.strftime("%m/%d/%Y")

    # search throught the user - habits - if today has been done mark it as true
    
    if habit_name == "fit_hab":
        habit_name = "Fitness"
    elif habit_name == "fin_hab":
        habit_name = "Finances"
    elif habit_name == "rel_hab":
        habit_name = "Relationships"
    elif habit_name == "acc_hab":
        habit_name = "Accademic"

    # this code actually work there is an issue in how the dates done is added to the json file becuase there is something up with it
    if count == 0:
        for hab in habit_list:
            for key in habits:
                if type in key and habits[key]["desc"] == hab:
                    temp_date_list = habits[key]["dates_done"]
                    date_bool = None
                    for date in temp_date_list:
                        if date == today:
                            date_bool = True
                        else:
                            date_bool = False
                    # next date
                    # just incase the habit has never been done 
                    if temp_date_list == []:
                        date_bool = False
                    
                    if date_bool == True:
                        fav_list.append(True)
                    elif date_bool == False:
                        fav_list.append(False)
        count += 1

    # st.write(len(habit_list), len(fav_list))

    data_df = pd.DataFrame(
        {
            habit_name:habit_list,
            "favourite":fav_list,
        }
    )   

    st.data_editor(
        data_df,
        column_config={
            "favourite": st.column_config.CheckboxColumn(
                "Completed",
                help="Check your habit when **completed**",
                width=None,
                required=True,
            )
        },
        disabled=["Habits"],
        hide_index=True,
        key=habit_name,
        use_container_width=True,
    )             
# end function 

def make_button(habit_list):
    string = ""
    count = 0
    button_list = []
    for habit in habit_list:
        string = habit["desc"]
        button = st.button(string, use_container_width=True, key=f"button{count}")
        button_list.append(button)
        count+=1
    # next habit

    pos = 0
    for button in button_list:
        if button == True:
            return pos
        pos += 1
    # next button
# end function
    
def change_habits(type):
            habit_list = []
            habits = st.session_state.habits
            # gives us a list of all the habits in area selected
            for key in habits:
                if type in key:
                    habit_list.append(habits[key])
                # end if
            # next key
            
            st.title("Edit Habits")
            st.divider()
            col1, col2 = st.columns(2, gap="large")
            with col1:
                # display the habits in a way the user can choose them
                st.write("Please select the habit you want to delete")
                pos = make_button(habit_list)
            with col2:
                st.write("You have chosen to delete this habit:")
                if pos != None:
                    st.write(habit_list[pos]["desc"])
                    #  need to return this information, but need to do an are you sure check before hand
                    st.checkbox("Are you sure", on_change=delete_habit, args=[habit_list[pos]["desc"]])
# end function
                    
                        
def delete_habit(habit_to_delete):
    habits = st.session_state.habits
    for key in habits:
        if habits[key]["desc"] == habit_to_delete:
            del habits[key]
            break
        # end if
    st.session_state.habits = habits
    update_save()
                

def make_sidebar():
    with st.sidebar:
        st.title("Navigation")
        st.markdown("#####")
        st.button("Launchpad", on_click=set_stage, args=["c"], use_container_width=True)
        st.button("View Streaks", on_click=set_stage, args=["n"], use_container_width=True)  
        st.button("Edit Habits", on_click=set_stage, args=["d"], use_container_width=True) 
        st.button("Add new Habit", on_click=set_stage, args=["i"], use_container_width=True)
# end function
    
def add_habit(type):
    habits = st.session_state.habits
    count = 0
    # find the number of habits for x type
    for key in habits:
        if type in key:
            count += 1
        # end if
    # next key
    key_name = f"{type}_hab{count}"
    st.write("Type your habit in the text box bellow and click SUBMIT to add it")
    habit = st.text_input("add habit",key = key_name, label_visibility="collapsed")
    if habit != "":
        habits[key_name] = {"desc": habit, "dates_done": []}
        st.button("Add another Habbit", on_click=set_stage, args=["d"])
    # end if
    st.session_state.habits = habits
    update_save()
# end function

# --- LAUNCHPAD ---
def launchpad(username, password):
    # --- HOME PAGE ---
    if st.session_state.stage == "c":
        st.set_page_config(layout="wide")
        load_account(st.session_state.username, st.session_state.password)
        user = st.session_state.user
        username = (st.session_state.username) 
        username = username.capitalize()
        st.title(f"{username}'s Launchpad")
        st.divider()

        if "habits" not in st.session_state:
            st.session_state.habits = user.user_dictionary["habits"]
        
        col2, col3 = st.columns(2, gap="large")
        with col2:
            display_habits(user)
        with col3:
            display_metrics()
        make_sidebar()
    # end if
    
    # --- DELETE HABITS ---
    if st.session_state.stage == "d":
        st.set_page_config(layout="centered")
        st.title("Edit Habits")
        st.divider()
        st.write("Please select type of habit you want to Delete")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("Fitness", on_click=set_stage, args=["e"], use_container_width=True)
        with col2:       
            st.button("Finance", on_click=set_stage, args=["f"], use_container_width=True)
        with col3:
            st.button("Relationships", on_click=set_stage, args=["g"], use_container_width=True)
        with col4:
            st.button("Accademic / Work", on_click=set_stage, args=["h"], use_container_width=True)
        make_sidebar()
    # end if

    if st.session_state.stage == "e":
        type = "fit"
        change_habits(type)
        make_sidebar()
    # end if
    if st.session_state.stage == "f":
        type = "fin"
        change_habits(type)
        make_sidebar()
    # end if
    if st.session_state.stage == "g":
        type = "rel"
        change_habits(type)
        make_sidebar()
    # end if
    if st.session_state.stage == "h":
        type = "acc"
        change_habits(type)
        make_sidebar()
    # end if

    # --- ADD NEW HABITS ---
    if st.session_state.stage == "i":
        st.set_page_config(layout="centered")
        st.title("Add Habits")
        st.divider()
        st.write("Please select the type of habit you want to Add")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("Fitness", on_click=set_stage, args=["j"], use_container_width=True)
        with col2:       
            st.button("Finance", on_click=set_stage, args=["k"], use_container_width=True)
        with col3:
            st.button("Relationships", on_click=set_stage, args=["l"], use_container_width=True)
        with col4:
            st.button("Accademic / Work", on_click=set_stage, args=["m"], use_container_width=True)
        make_sidebar()
    # end if

    if st.session_state.stage == "j":
        type = "fit"
        add_habit(type)
        make_sidebar()
    # end if
    if st.session_state.stage == "k":
        type = "fin"
        add_habit(type)
        make_sidebar()
    # end if
    if st.session_state.stage == "l":
        type = "rel"
        add_habit(type)
        make_sidebar()
    # end if
    if st.session_state.stage == "m":
        type = "acc"
        add_habit(type)
        make_sidebar()
    # end if

    # --- STREAKS VIEWING PAGE
    if st.session_state.stage == "n":
        st.set_page_config(layout='centered')
        longest, longest_habit = calculate_streaks()


    # st.write(st.session_state)
# end function

