from title_screen import title_screen
from launchpad import launchpad

def main():
    data = title_screen()
    if data != None:
        launchpad(data[0], data[1])

#  end function
main()