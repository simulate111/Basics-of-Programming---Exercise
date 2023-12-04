'''
The following text-based code try to make a event calendar by adding new event based on its name, date and time interval.
The program allows the user to save the calendar to the same path as the code directory.
User could allow th euser to remove any preiously inserted and saved data.
The code will be saved if ctrl+c is used to get out of the program.
User could see the previous saved calendar at the beginning of and during the program.
There is exit option to close the program and allow the user to save the code again.
The code checks any overlap among input to prevent any event overlap.
'''

#Import the required libraries into python environment.
import os
import json
import datetime

#Method to save calendar to the same path as the python.
def save_calendar(CalenderName, FileName):
    with open(FileName, 'w') as fs:
        json.dump(CalenderName, fs)

#Method to load the previously saved calendar.
def load_calendar(Name_of_Saved_Calender):
    try:
        with open(Name_of_Saved_Calender, 'r') as fl:
            return json.load(fl)
    except FileNotFoundError:
        return {}

#Method to check the entered date and time format to be in the correct format as YYYY-MM-DD HH:MM.
def DateTime(DT):
    while True:
        try:
            inputDT = input(DT)
            return datetime.datetime.strptime(inputDT, '%Y-%m-%d %H:%M')
        except ValueError:
            print("The correct time format is: YYYY-MM-DD HH:MM")

#method to add new event into the calendar by the given name, date and time.
def NewEvent(CalenderName1, name, Start, End):
    while End < Start:
        print("End time must be later than start time.")
        Start = DateTime("New start time (YYYY-MM-DD HH:MM):")
        End = DateTime("New end time (YYYY-MM-DD HH:MM):")

    new_event = {"name": name, "Start": Start.strftime('%Y-%m-%d %H:%M'), "End": End.strftime('%Y-%m-%d %H:%M')}

    # Check if there is any overlap between the new and previously saved events in the calendar.
    overlapping_events = [event for event in CalenderName1.values()
                          if "End" in event and datetime.datetime.strptime(event["End"], '%Y-%m-%d %H:%M') > Start and
                          datetime.datetime.strptime(event["Start"], '%Y-%m-%d %H:%M') < End]

    while overlapping_events:
        print("The new event overlaps with the existing events.")
        cancel_entry = input("Do you want to go back (yes/no)?")
        #User could cancel the event entry if they found any overlap in their schedule.
        if cancel_entry in ['yes', 'YES', 'Yes', 'y', 'Y', 'ok']:
            return 

        Start = DateTime("Enter a new start time (YYYY-MM-DD HH:MM):")
        End = DateTime("Enter a new end time (YYYY-MM-DD HH:MM):")
        #One primary timing check to prevent common mistake that start time should be sooner or equal to the end time of the event.
        while End < Start:
            print("End time must be later than start time.")
            Start = DateTime("New start time (YYYY-MM-DD HH:MM):")
            End = DateTime("New end time (YYYY-MM-DD HH:MM):")

        new_event["Start"] = Start.strftime('%Y-%m-%d %H:%M')
        new_event["End"] = End.strftime('%Y-%m-%d %H:%M')

        overlapping_events = [event for event in CalenderName1.values()
                              if datetime.datetime.strptime(event["End"], '%Y-%m-%d %H:%M') > Start and
                              datetime.datetime.strptime(event["Start"], '%Y-%m-%d %H:%M') < End]

    CalenderName1[name] = new_event
    print(f"Event '{name}' added successfully.")
    return CalenderName1
    

#Method to remove previously saved event in the calendar.
def RemoveEvent(CalenderName2):
    #First the previously saved events are shown to user to be able to have a correct selection for event removal.
    if CalenderName2:
        print("Existing Calendars:")
        for i, CalenderName2_name in enumerate(CalenderName2.keys(), start=1):
            print(f"{i}. {CalenderName2_name}")
        #To avoid any intruption due to the common input error, try and except are used to catch wrong indices and values, and notifying the user to enter the correct input.
        while True:
            try:
                CalenderName2_choice = int(input("Enter the number of the CalenderName2 to remove: "))
                CalenderName2_name = list(CalenderName2.keys())[CalenderName2_choice - 1]

                if CalenderName2_name in CalenderName2:
                    event = CalenderName2[CalenderName2_name]
                    print(f"\nEvent Details:")
                    print(f"Name: {event['name']}")
                    print(f"Start Time: {event['Start']}")
                    print(f"End Time: {event['End']}\n")
                    #Asking for removal confiramtion.
                    confirm = input("Do you want to remove this event? (yes/no): ").lower()
                    if confirm in ['yes', 'YES', 'Yes', 'y', 'Y', 'ok']:
                        del CalenderName2[CalenderName2_name]
                        print(f"Event '{CalenderName2_name}' removed successfully.")
                    else:
                        print("Event removal canceled.")
                    break
                #The user may select the wrong input and this line avoid the simple interuption in program and ask again for the correct input by user.
                else:
                    print(f"Calendar '{CalenderName2_name}'Enter a valid number.")
            except (ValueError, IndexError):
                print("Please enter a valid number.")
    else:
        print("Calendar is empty.")

#This method is defined to show the saved events in the calendar.
def Display(CalenderName3, Start=None, End=None):
    if CalenderName3:
        print("\nEvents in the Calendar:")
        for event in CalenderName3.values():
            event_start = datetime.datetime.strptime(event["Start"], '%Y-%m-%d %H:%M')
            event_end = datetime.datetime.strptime(event["End"], '%Y-%m-%d %H:%M')

            if Start is None or (Start <= event_end and End >= event_start):
                print(f"Name: {event['name']}")
                print(f"Start Time: {event['Start']}")
                print(f"End Time: {event['End']}\n")
    else:
        print("No events to display. Calendar is empty.")

#This method shows the previously saved calendar to be loaded by user or the user could start to make a new calendar.
def Load_or_Make_Calendar():
    print("\nWelcome to thre Calendar.\n")
    SavedCalendars = os.listdir()
    SavedCalendars = [calendar for calendar in SavedCalendars if calendar.endswith('.json')]
    if SavedCalendars:
        print("Previously saved calendars that you could load:")
        for idx, Namee in enumerate(SavedCalendars, start=1):
            print(f"{idx}- {Namee}")

        Load = input("Do you want to load any previous saved calendar? (yes/no)")
        if Load in ['yes', 'YES', 'Yes', 'y', 'Y', 'ok']:
            CalendarLoad = int(input("Which calendar do you want to load: (Choose one of the calendar's numbers)"))
            SelectedCalendar = SavedCalendars[CalendarLoad - 1]
            calendar = load_calendar(SelectedCalendar)
            print(f"Loaded calendar '{SelectedCalendar}' successfully.")
            CalendarName = SelectedCalendar
            today_date = datetime.datetime.now().date()
            start_time = datetime.datetime.combine(today_date, datetime.datetime.min.time())
            end_time = datetime.datetime.combine(today_date, datetime.datetime.max.time())
            format_date = today_date.strftime("%Y-%m-%d")
            display(calendar, start=start_time.strftime("%Y-%m-%d %H:%M"), end=end_time.strftime("%Y-%m-%d %H:%M"))
            return calendar, CalendarName
        else:
            calendar = {}
            #The extension of .json is used to be able to read and identify the already saved calenders.
            CalendarName = input("Select a name for your new calendar:") + '.json'
            return calendar, CalendarName
    else:
        calendar = {}
        CalendarName = input("Enter a name for the new calendar:") + '.json'
        return calendar, CalendarName
        
    return calendar, CalendarName
#The method shows the available options to the user to apply the possible modification on the calendar.
def Option_List(calendar, CalendarName):
    while True:
                print("\nSelection Menu:\n")
                print("0. Show and load previously saved calendars (0)")
                print("1. Add a new event to the calendar (1)")
                print("2. Remove event from calender (2)")
                print("3. Show all events in the calender (3)")
                print("4. Show events in the specific interval (4)")
                print("5. Save the calendar(5)")
                print("6. Exit and save the calandar (6)")
                selection = input("\nWhat do you want to do?")
                if selection == '0':
                    Load_or_Make_Calendar()
                        
                elif selection == '1':
                    Name = input("Select the name for your event:")
                    Start = DateTime(f"What is the start time of {Name} (YYYY-MM-DD HH:MM)?")
                    End = DateTime(f"What is the end time of {Name} (YYYY-MM-DD HH:MM)?")
                    calendar=NewEvent(calendar, Name, Start, End)
                elif selection == '2':
                    RemoveEvent(calendar)
                elif selection == '3':
                    try:
                        Display(calendar, Start=None, End=None)
                    except KeyError:
                        print('\nThere is no scheduled event in the calendar.')
                elif selection == '4':
                    StartTime = DateTime("What is the start time (YYYY-MM-DD HH:MM)?")
                    EndTime = DateTime("What is the end time (YYYY-MM-DD HH:MM)?")
                    Display(calendar, StartTime, EndTime)
                elif selection == '5':
                    save_calendar(calendar, CalendarName)
                    print(f"'{CalendarName}' saved successfully.")
                elif selection == '6':
                    save_selection = input("Do you want to save the data? (yes/no):")
                    if save_selection in ['yes', 'YES', 'Yes', 'y', 'Y', 'ok']:
                        save_calendar(calendar, CalendarName)
                        print(f"'{CalendarName}' saved successfully.")
                    print("\nHave a nice day.")
                    break
                else:
                    print("Selection should be a number between 1 and 6.")
#This mehtod is used to show simple steps meaning that the program first try to load previously data or create a new calendar and then using available options to modify the calendar.
def main():
#Using try and except to safely save the data if there is any intruption by ctrl+c.
    try:
        #Show the previously saved calendar or start new calendar.
        Calendar, CalendarName = Load_or_Make_Calendar()
        #Show the menu options and the possible available or defined modifications.
        Option_List(Calendar, CalendarName)
    except KeyboardInterrupt:
        save_calendar(Calendar, CalendarName)
        print(f"\n'{CalendarName}' is now saved safely.")
        print("\nHave a nice day.")
#This method is defined to run the code as soon as it is read by python.       
if __name__ == "__main__":
    main()
