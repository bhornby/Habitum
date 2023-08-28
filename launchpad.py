import streamlit as st
import pandas as pd
import json
from title_screen import Userclass
from title_screen import load_account

def set_stage(i):
    st.session_state.stage = i

def display_metrics(user):
    habits = user.user_dictionary["habits"]
    # tells you the number of keys - therefore habits
    num_habits = len(habits) 
    st.metric(label="Habits Completed", value=num_habits, delta=2.0,delta_color="normal")

def display_habits(user):
    habits = user.user_dictionary["habits"]
    # use a checkbox column
    
    make_checkbox_col(habits, "fit")
    make_checkbox_col(habits, "fin")
    make_checkbox_col(habits, "rel")
    make_checkbox_col(habits, "acc")

def make_checkbox_col(habits, type):
    habit_name = f"{type}_hab"
    widget_list = []
    fav_list = []
    for key in habits:
        if habit_name in key:
            widget_list.append(habits[key]["desc"])
        # end if

    for hab in widget_list:
        fav_list.append(False)
    
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
                "Completed?",
                help="Check your habit when **completed**",
                width="large"
            )
        },
        disabled=["Habits"],
        hide_index=True,
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
    
        display_metrics(user)
        st.divider()
        display_habits(user)
# end function





# TODO - daily tracker - first display the habits
# then allow the user to tick a checkbox if they have completed it, if completed that habit is removed from the stack,
# and they all shuffle up
# TODO use the metrics feature for indicating how well the day has gone