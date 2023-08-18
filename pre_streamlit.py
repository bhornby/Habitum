# defining and instantiating
filename = "user-information.txt"
from art import logo 
from art import goal_art
from art import your_goals

import time
import json

# the user class
class Userclass:
    #constructor
    def __init__(self, user_name, user_surname, user_age, user_gender, user_birthday, user_goals, user_habits):
        #make a dictionary for this specific user and write it to the memory file
        self.user_dictionary = {
            "habits":  user_habits,
            "goals": user_goals,
            "age": user_age,
            "gender": user_gender,
            "birthday": user_birthday,
            "name": user_name,
            "surname": user_surname,    
        }
        
        # writes user data to the memory file
        # serialise to json
        # could use pandas for data handling - is a data science library
    def save(self): 
        filename = self.user_dictionary["name"] + self.user_dictionary["surname"] 
        with open(f"{filename}information.json", "w") as file:
            json.dump(self.user_dictionary, file)
    # end function

    # need a function to get data and to validate old users
    # will take the user information from the name information.json then add it to a new class
# end class 

# checks if the user has an account and if not prompts them to create one
def collect_user_information():
    has_account = False
    print("Welcome to the habit tracker! If you already have an account with us please type 'yes' Otherwise please type 'no'.")
    user_input = input()
    if user_input == "yes":
        has_account = True
        print("Now we will validate your identity.")
        name = input("Firstname: ")
        name = name.lower()
        surname = input("Surname: ") 
        surname = surname.lower()
        birthday = input("Birthday (dd/mm/yyyy): ")
        load_account(name, surname, birthday)

    elif user_input == "no":
        create_account(has_account)
    else:
        print("Oops! that was not what we expected. Please enter a valid response.")
        collect_user_information()
# end function

def print_goals(goals, fg_goal_list, rg_goal_list, mg_goal_list, ag_goal_list):
    # print goals to the creen
    print("\nFitness Goals:")
    for list in fg_goal_list:
        print(*list, sep="\n")
    print("")

    print("Relationship Goals:")
    for list in rg_goal_list:
        print(*list, sep="\n")
    print("")

    print("Financial Goals")
    for list in mg_goal_list:
        print(*list, sep="\n")
    print("")

    print("Academic Goals:")
    for list in ag_goal_list:
        print(*list, sep="\n")
    print("")
# end function

def make_goals(goals):
    # goal creation
        print(goal_art)
        print("We are now going to set goals, goals can be set for all areas of your life and are extreemly benificial. \nThey can provide you with the motivation when you need it the most giving you that extra drive. \nJust the fact that you downloaded this app shows you've got what it takes to succeed!\n")

        area_count = 0
        while area_count < 4:
            print("Select which area you wish to add a goal to. Enter: 'a' for fitness goals, 'b' for relationship goals, 'c' for finance goals, or 'd' for academic goals")
            area = input()
            if area == "a":
                more = True
                count = 0
                # fitness goal
                goal_type = "fg"
                while more == True :
                    goal = input("Please enter your fitness goals, Type 'next' when you are ready for the next section, Or type 'done' to finish goal selection\n")
                    if goal == "next":
                        more = False
                    elif goal == "done":
                        more = False
                        area_count = 4
                    else: 
                        key_name = goal_type + str(count)
                        goals[key_name] = [goal]
                        #check if they have more than one fitness goal
                        count += 1
                    #end if
                #end while
                area_count += 1
            #end if
            if area == "b":
                more = True
                count = 0
                # relationship goal
                goal_name = "rg"
                while more == True:
                    goal = input("Please enter your relationship goals, Type 'next' when you are ready for the next section, Or type 'done' to finish goal selection\n")
                    if goal == "next":
                        more = False
                    elif goal == "done":
                        more = False
                        area_count = 4
                    else: 
                        key_name = goal_name + str(count)
                        goals[key_name] = [goal]
                        #check if they have more than one relationship goal
                        count += 1
                    #end if
                #end while
                area_count += 1
            #end if
            if area == "c":
                more = True
                count = 0
                # finance (money) goal
                goal_name = "mg"
                while more == True:
                    goal = input("Please enter your fitness goals, Type 'next' when you are ready for the next section, Or type 'done' to finish goal selection\n")
                    if goal == "next":
                        more = False
                    elif goal == "done":
                        more = False
                        area_count = 4
                    else: 
                        key_name = goal_name + str(count)
                        goals[key_name] = [goal]
                        #check if they have more than one finance goal
                        count += 1
                    #end if
                #end while
                area_count += 1
            #end if
            if area == "d":
                more = True
                count = 0
                # academic goals
                goal_name = "ag"
                while more == True:
                    goal = input("Please enter your fitness goals, Type 'next' when you are ready for the next section, Or type 'done' to finish goal selection\n")
                    if goal == "next":
                        more = False
                    elif goal == "done":
                        more = False
                        area_count = 4
                    else: 
                        key_name = goal_name + str(count)
                        goals[key_name] = [goal]
                        #check if they have more than one academic goal
                        count += 1
                    #end if
                #end while
                area_count += 1
            # end if
        # end while  
        print("Thank you for entering you goals")
        # now we want to display the users current goals
        time.sleep(1)
        print(your_goals)
        # search through the dictionary and where it has tno
        # he identifyer for each type add a sub heading then print it out
        # only want to print the title "fitness goals" once and same for other goal types
        fg_goal_list = []
        rg_goal_list = []
        mg_goal_list = []
        ag_goal_list = []

        #is actually creating lists within lists
        for key in goals:
            if "fg" in key:
                fg_goal_list.append(goals[key])    
            elif "rg" in key:
                rg_goal_list.append(goals[key])
            elif "mg" in key:
                mg_goal_list.append(goals[key])
            elif "ag" in key:
                ag_goal_list.append(goals[key])
            # end if    
        #next key

        # output goals to screen for user to see
        # as printing from a list within a list
        print_goals(goals, fg_goal_list, rg_goal_list, mg_goal_list, ag_goal_list)

        return goals

    # end if
# end function

def change_goals(goals):
    fg_goal_list = []
    rg_goal_list = []
    mg_goal_list = []
    ag_goal_list = []

    #is actually creating lists within lists
    for key in goals:
        if "fg" in key:
            fg_goal_list.append(goals[key])    
        elif "rg" in key:
            rg_goal_list.append(goals[key])
        elif "mg" in key:
            mg_goal_list.append(goals[key])
        elif "ag" in key:
            ag_goal_list.append(goals[key])
        # end if    
    #next key

    goal_area = input("Select which area you need to change. Enter: 'a' for fitness goals, 'b' for relationship goals, 'c' for finance goals, or 'd' for academic goals\n")
    if goal_area == 'a': 
        print("Fitness Goals:")
        for list in fg_goal_list:
            print(*list, sep="\n")
        # next list
        goal_to_change = input("\nCopy and paste in the goal you want to change\n")
        new_goal = input("Enter your new goal: ")
        temp = []
        temp.append(goal_to_change)
        for key in goals:
            if goals[key] == temp:
                temp[0] = new_goal
                goals[key] = temp   
                # end if
            # end if
        # next key

    elif goal_area == 'b':
        print("Relationship Goals:")
        for list in rg_goal_list:
            print(*list, sep="\n")
        # next list
        goal_to_change = input("\nCopy and paste in the goal you want to change\n")
        new_goal = input("Enter your new goal: ")
        temp = []
        temp.append(goal_to_change)
        for key in goals:
            if goals[key] == temp:
                temp[0] = new_goal
                goals[key] = temp   
                # end if
            # end if
        # next key

    elif goal_area == 'c':
        print("Financial Goals")
        for list in mg_goal_list:
            print(*list, sep="\n")
        # next list
        goal_to_change = input("\nCopy and paste in the goal you want to change\n")
        new_goal = input("Enter your new goal: ")
        temp = []
        temp.append(goal_to_change)
        for key in goals:
            if goals[key] == temp:
                temp[0] = new_goal
                goals[key] = temp   
                # end if
            # end if
        # next key

    elif goal_area == 'd':
        print("Academic Goals:")
        for list in ag_goal_list:
            print(*list, sep="\n")
        # next list
        goal_to_change = input("\nCopy and paste in the goal you want to change\n")
        new_goal = input("Enter your new goal: ")
        temp = []
        temp.append(goal_to_change)
        for key in goals:
            if goals[key] == temp:
                temp[0] = new_goal
                goals[key] = temp   
                # end if
            # end if
        # next key
    
    # new goal lists
    fg_goal_list = []
    rg_goal_list = []
    mg_goal_list = []
    ag_goal_list = []

    #is actually creating lists within lists
    for key in goals:
        if "fg" in key:
            fg_goal_list.append(goals[key])    
        elif "rg" in key:
            rg_goal_list.append(goals[key])
        elif "mg" in key:
            mg_goal_list.append(goals[key])
        elif "ag" in key:
            ag_goal_list.append(goals[key])
        # end if    
    #next key

    print_goals(goals, fg_goal_list, rg_goal_list, mg_goal_list, ag_goal_list)
    return goals
# end function

# need a function to get data and to validate old users
# will take the user information from the name information.json then add it to a new class
# as the old one from when the user last accessed the app will not exist

def load_account(user_name, user_surname, user_birthday):
    filename = user_name + user_surname + "information.json" 
    user_information = None
    with open(filename, "r") as openfile:
        json_object = json.load(openfile)
        # this is the data stored not just the dictionary
    correct_account = False
    for key in json_object:
        if json_object[key] == user_birthday:
            correct_account = True
            user_information = json_object
        # end if
    # next key

    if correct_account == False:
        print("You entered the wrong infomration, please try again.")
        collect_user_information()
    else:
        # fill out the user class with data from the json file
        # add in loading user information bar with streamlit TODO5
        habits = {}
        goals = {}
        age = int
        gender = ""
        birthday = "" 
        name = ""
        surname = "" 

        for key in user_information:
            if key == "habits":
                habits = user_information[key]
            elif key == "goals":
                goals = user_information[key]
            elif key == "age":
                age = user_information[key]
            elif key == "gender":
                gender = user_information[key]
            elif key == "birthday":
                birthday = user_information[key]
            elif key == "name":
                name = user_information[key]
            elif key == "surname":
                name = user_information[key]
            # end if

        user = Userclass(name, surname, age, gender, birthday, goals, habits)
    # end if
# end function 

def create_account(has_account):
    if has_account == False:
        input("Hit enter if you want to create an account. \n")
        print("Thank you for creating an account, please fill out all the information requested.")
        time.sleep(1.5)

        # make instance of the user class with all of these values stored within it

        habits = {}
        goals = {}

        age = int(input("How old are you? \n"))
        gender = input("Are you male or female? \n")
        birthday = input("when is your birthday dd/mm/yyyy? \n")
        name = input("What is your first name? \n")
        surname = input("What is your surname? \n")
        print("Thank you.")

        gender = gender.lower()
        birthday = birthday.lower()
        name = name.lower()
        surname = surname.lower()
        time.sleep(1.2)

        # goal creation
        goals = make_goals(goals)

        # allow user to change or add new goals if they wish
        cont = True
        while cont == True:
            choice = input("Are you happy with you goals? If you would like to make changes or add more enter 'n'. Otherwise hit any other key to continue\n")

            if choice == "n":
                print("type 'a' to add a new goal, type 'b' to change an existing goal, type 'c' if you are happy with your current goals")
                choice = input()
                if choice == 'a':
                    goals = make_goals(goals)
                elif choice == 'b':
                    goals = change_goals(goals)
                #end if
            #end if
            else:
                cont = False
            # end if
        # end while

        # habit creation

        # class instanciation
        user = Userclass(name, surname, age, gender, birthday, goals, habits)
        user.save()

# end function 
       


# TODO1 make the goals:
# 1. finish the change goals function - DONe
# 2. test the function - DONE
# 3. make sure you can write it to the text file - json loads and json dumps - DONE but is in the class so need to make a class first

# TODO2 write the user dictionary to the text file - DONE


# TODO3 be able to access the data in the user information text file when logging back into an account - DONE

# TODO4 port over to streamlit
# get habits working
# get graphs and analysis tracking working using streamlit

# add in loading user information bar with streamlit TODO5

# main loop 
def main_loop():
    print(logo)
    collect_user_information()

main_loop()