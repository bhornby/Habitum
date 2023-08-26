import streamlit as st
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


def launchpad(username, password):
    # --- HOME PAGE ---
    if st.session_state.stage == "c":
        load_account(st.session_state.username, st.session_state.password)
        user = st.session_state.user
        username = (st.session_state.username) 
        username = username.capitalize()
        st.title(f"{username}'s Launchpad")
        # st.write(user.user_dictionary["habits"])
    
        display_metrics(user)

    
# end function
# end function





# TODO - daily tracker
# TODO use the metrics feature for indicating how well the day has gone