from title_screen import title_screen
from launchpad import launchpad

def main():
    finished = title_screen()
    if finished == True:
        launchpad()
#  end function
main()