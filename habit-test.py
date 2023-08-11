import streamlit as st
import datetime

# called when the button is clicked to set the clicked state in the session state to true
def click_detect():
    st.session_state.clicked = True

# checks if the clicked key exists in the session state - if not if makes one and sets its value to false
if "clicked" not in st.session_state:
    st.session_state.clicked = False

# when the button it uses the on_click function and calls the click detect functio and sets the "clicked" key to true
# the buttons only job is to let us know if it has been clicked
st.button("yes", on_click = click_detect())

# whether the code is run of not is dependant on if the session state key "clicked" is set to true 
if st.session_state.clicked == True:
    st.write("Please enter your user information to access your data")
    name = st.text_input("Name")
    surname = st.text_input("Surname")
    birthday = st.date_input("Birthday", datetime.date(2023, 8, 11 ), max_value=datetime.date(2099,1 ,1), min_value=datetime.date(1955,1 ,1), format="DD/MM/YYYY")
            
st.write(st.session_state)
st.write(f"Thank you {name}, we will log you in shortly")