from title_screen import title_screen
from launchpad import launchpad

def main():
    username, passoword = title_screen()
    launchpad(username, passoword)

#  end function
main()