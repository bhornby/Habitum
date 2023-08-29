from title_screen import title_screen
from launchpad import launchpad
import streamlit as st

def main():
    data = title_screen()
    if data != None:
        launchpad(data[0], data[1])

#  end function
st.set_page_config(layout="wide")
main()