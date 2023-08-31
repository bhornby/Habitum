import streamlit as st
import pandas as pd
from datetime import datetime
import json
from title_screen import Userclass
from title_screen import load_account


def set_stage(i):
    st.session_state.stage = i

def update_save():
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

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Habits Completed", value=habits_completed, delta=habits_completed,delta_color="normal")
    with col2:
        st.metric(label="Habits Remaining", value=habits_remaining, delta=-habits_completed, delta_color="inverse")

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
                        habits[key]["dates_done"] = today
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

    if count == 0:
        for habit in habits:
            if type in habit:
                if habits[habit]["dates_done"] == today:
                    fav_list.append(True)
                else:
                    fav_list.append(False)
        count += 1
        
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
                width="large",
                required=True,
            )
        },
        disabled=["Habits"],
        hide_index=True,
        key=habit_name,
        use_container_width=True,
    )             
# end function    

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

        # st.write(st.session_state)
# end function

