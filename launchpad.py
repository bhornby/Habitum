import streamlit as st
import json
from title_screen import Userclass
from title_screen import load_account

def set_stage(i):
    st.session_state.stage = i

def launchpad(username, password):
    load_account(st.session_state.username, st.session_state.password)
    user = st.session_state.user
    st.write(user.user_dictionary["habits"])

    
# end function
# end function




# TODO - load the user data 
# TODO - daily tracker
# TODO - makes ure its is a new page
# TODO use the metrics feature for indicating how well the day has gone