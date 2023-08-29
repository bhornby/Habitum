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
        make_checkbox_col(habits, "fit")
    # if fin_flag > 0:
    #     make_checkbox_col(habits, "fin")
    # if rel_flag > 0:
    #     make_checkbox_col(habits, "rel")
    # if acc_flag > 0:
    #     make_checkbox_col(habits, "acc")

def make_checkbox_col(habits, type):
    count = 0
    habit_name = f"{type}_hab"
    widget_list = []
    fav_list = []
    for key in habits:
        if habit_name in key:
            widget_list.append(habits[key]["desc"])
        # end if

    if count == 0:
        for hab in widget_list:
            fav_list.append(False)
        count += 1
    
    if habit_name == "fit_hab":
        habit_name = "Fitness"
    elif habit_name == "fin_hab":
        habit_name = "Finances"
    elif habit_name == "rel_hab":
        habit_name = "Relationships"
    elif habit_name == "acc_hab":
        habit_name = "Accademic and Work"
        
    data_df = pd.DataFrame(
        {
            habit_name:widget_list,
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
    )  
    
    if "Fitness" in st.session_state:
        fit_dict = st.session_state.Fitness
        fit_true_pos = []
        box_num = 0
        for checkbox in fit_dict["edited_rows"]:
            for favourite in fit_dict["edited_rows"][checkbox]:
                chosen = fit_dict["edited_rows"][checkbox][favourite]
                st.write(box_num)
                # if the box is checked - add its position to the fit true pos
                if chosen == True:
                    fit_true_pos.append(box_num)
                # end if
                box_num += 1
            # next favourite
        # next checkbox

        # now to find which habit it corresponds to and set the date done
        for pos in fit_true_pos:
            hab = widget_list[pos]
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
                
# end function    

def launchpad(username, password):
    # --- HOME PAGE ---
    if st.session_state.stage == "c":
        load_account(st.session_state.username, st.session_state.password)
        user = st.session_state.user
        username = (st.session_state.username) 
        username = username.capitalize()
        st.title(f"{username}'s Launchpad")

        if "habits" not in st.session_state:
            st.session_state.habits = user.user_dictionary["habits"]
    
        display_metrics()
        st.divider()
        display_habits()

        st.write(st.session_state)
# end function





# TODO - daily tracker - first display the habits
# then allow the user to tick a checkbox if they have completed it, if completed that habit is removed from the stack,
# and they all shuffle up
# TODO use the metrics feature for indicating how well the day has gone