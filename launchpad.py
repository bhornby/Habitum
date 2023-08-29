import streamlit as st
import pandas as pd
from datetime import datetime
import json
from title_screen import Userclass
from title_screen import load_account

def set_stage(i):
    st.session_state.stage = i

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

def display_habits():
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
        make_checkbox_col(habits, "fit",fit_hab_list)
    # end if
    if fin_flag > 0:
        make_checkbox_col(habits, "fin",fin_hab_list)
    # end if
    if rel_flag > 0:
        make_checkbox_col(habits, "rel", rel_hab_list)
    # end if
    if acc_flag > 0:
        make_checkbox_col(habits, "acc", acc_hab_list)
    # end if

    update_checkbox_col("Fitness", habits, fit_hab_list)
    update_checkbox_col("Finances", habits, fin_hab_list)
    update_checkbox_col("Relationships", habits, rel_hab_list)
    update_checkbox_col("Accademic", habits, acc_hab_list)

def update_checkbox_col(name, habits, habit_list):
    if name == "Fitness":
        dict = st.session_state.Fitness
    elif name == "Finances":
        dict = st.session_state.Finances
    elif name == "Relationships":
        dict = st.session_state.Relationships
    elif name == "Accademic":
        dict = st.session_state.Accademic

    true_pos = []
    box_num = 0
    for checkbox in dict["edited_rows"]:
        for favourite in dict["edited_rows"][checkbox]:
            chosen = dict["edited_rows"][checkbox][favourite]
            # if the box is checked - add its position to the fit true pos
            if chosen == True:
                true_pos.append(box_num)
            # end if
            box_num += 1
        # next favourite
    # next checkbox

    # now to find which habit it corresponds to and set the date done - need to add the constant
    for pos in true_pos:
        hab = habit_list[pos]
        now = datetime.now()
        today = now.strftime("%m/%d/%Y")
        for key in habits:
            if habits[key]["desc"] == hab:
                habits[key]["dates_done"] = today
            # end if
        # next key
    # next pos
    st.session_state.habits = habits
# end if

def make_checkbox_col(habits, type, habit_list):
    count = 0
    habit_name = f"{type}_hab"
    fav_list = []

    if count == 0:
        for hab in habit_list:
            fav_list.append(False)
        count += 1
    
    if habit_name == "fit_hab":
        habit_name = "Fitness"
    elif habit_name == "fin_hab":
        habit_name = "Finances"
    elif habit_name == "rel_hab":
        habit_name = "Relationships"
    elif habit_name == "acc_hab":
        habit_name = "Accademic"
        
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
            display_habits()
        with col3:
            display_metrics()
# end function





# TODO - daily tracker - first display the habits
# then allow the user to tick a checkbox if they have completed it, if completed that habit is removed from the stack,
# and they all shuffle up
# TODO use the metrics feature for indicating how well the day has gone