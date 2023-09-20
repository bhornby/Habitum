from title_screen import title_screen
from launchpad import launchpad
import streamlit as st

host_location = None
if host_location == False:
    pass
    #will run on computer
elif host_location == True:
    pass
    #will run online

def main():
    data = title_screen()
    if data != None:
        launchpad(data[0], data[1])

#  end function
main()