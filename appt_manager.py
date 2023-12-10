from appointment import Appointment

def create_weekly_calendar():
    calendar = []
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for day in days_of_week:
        for hour in range(9, 17):
            calendar.append(Appointment(day, hour, "", "", 0))
    return calendar

def print_menu():
    print("\nMenu:")
    print("=" * 35)
    print("1. Schedule an appointment")
    print("2. Find appointment by name")
    print("3. Print calendar for a specific day")
    print("4. Cancel an appointment")
    print("9. Exit the system")

def find_appointment_by_time(calendar, scheduled_appointments, days_mapping, day_index, start_hour):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    search_day = days_of_week[day_index - 1].lower()
    appointments_at_time = [
        appointment for appointment in scheduled_appointments
        if appointment.day_of_week.lower() == search_day
        and appointment.start_time_hour == start_hour
    ]

    if appointments_at_time:
        print(f"Appointments at {start_hour}:00 on {search_day.capitalize()}:")
        for i, appointment in enumerate(appointments_at_time, start=1):
            print(f"{i}. {appointment}")

        choice = input("Enter 'yes' to cancel an appointment (or 'no' to cancel nothing): ").lower()

        if choice == 'yes':
            # Cancel the first appointment found at this time
            appointment_to_cancel = appointments_at_time[0]
            appointment_to_cancel.cancel(calendar, days_mapping, scheduled_appointments)
            print("Appointment canceled successfully.")
        elif choice == 'no':
            print("No appointment canceled.")
        else:
            print("Invalid input. No appointment canceled.")
    else:
        print("No appointment found for the specified time.")


def load_scheduled_appointments(calendar, scheduled_appointments):
    print("Starting the Appointment Manager System")
    print("Weekly calendar created")
    days_mapping = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}

    while True:
        load_option = input("Would you like to load previously scheduled appointments from a file? (y/n): ").lower()
        if load_option == 'y':
            file_name = input("Enter appointment filename: ")
            #import os is prohibited to use in this activity. Change this file path for CSV
            file_path = r"C:\OOP\New folder" + "\\" + file_name 
            #W3School added this because if the file is not found everythings is broken.
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        data = line.strip().split(',')
                        day_string = data[3].capitalize()
                        day_index = days_mapping.get(day_string)
                        if day_index is not None:
                            appointment = Appointment(day_string, int(data[4]), "", "", 0)
                            appointment.client_name = data[0]
                            appointment.client_phone = data[1]
                            appointment.appt_type = int(data[2])
                            scheduled_appointments.append(appointment)
                            # Mark the slot as unavailable
                            calendar[(day_index - 1) * 6 + int(data[4]) - 9].client_name = data[0]
                    print(len(scheduled_appointments), "previously scheduled appointments have been loaded")
                    break
            except FileNotFoundError:
                print("File not found or is a directory. Re-enter appointment filename.")
        elif load_option == 'n':
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def show_appointments_by_day(scheduled_appointments, days_of_week):
    # w3school for capitalize
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    if any(not appointment.day_of_week for appointment in scheduled_appointments):
        day = input("Enter the day of the week (e.g., Monday): ").capitalize()
    else:
        day = days_of_week

    if day.capitalize() in valid_days:
        # Print header
        print(f"\n{'Client Name':<20} {'Phone':<15} {'Day':<15} {'Start - End':<20} {'Type'}")
        print("=" * 85)

        for hour in range(9, 17):
            appointment_found = False
            for appointment in scheduled_appointments:
                if (
                    appointment.day_of_week.lower() == day.lower()
                    and appointment.start_time_hour == hour
                ):
                    print(appointment)
                    appointment_found = True
                    break

            if not appointment_found:
                print(f"{'':<20} {'':<15} {day:<15} {hour:02}:00 - {hour + 1:02}:00 {'Available'}")

        print("=" * 85)
    else:
        print("Invalid day entered. Please enter a valid day of the week.")

def show_appointments_by_name(scheduled_appointments):
    name = input("Enter the client name: ").lower()
    found_appointments = [appointment for appointment in scheduled_appointments if
                          name in appointment.client_name.lower()]
    
    if found_appointments:
        print(f"\n{'Client Name':<20} {'Phone':<15} {'Day':<15} {'Start - End':<20} {'Type'}")
        print("=" * 85)
        for appointment in found_appointments:
            print(appointment)
    else:
        print(f"No appointments found for names containing '{name}'.")

# Rest of the code remains the same


def save_scheduled_appointments(scheduled_appointments, file_path):
    #this is from w3 school. so that the application would not error out. since I am not allowed to use import os
    try:
        with open(file_path, 'r'):
            overwrite = input("The file already exists. Do you want to overwrite it? (Y/N): ").lower()
            if overwrite != 'y':
                file_name = input("Enter a different file name: ")
                file_path = r"C:\OOP\New folder" + "\\" + file_name + ".csv"
    except FileNotFoundError:
        pass  # The file doesn't exist, continue with saving

    with open(file_path, 'w') as file:
        for appointment in scheduled_appointments:
            file.write(appointment.format_record() + '\n')

    print(len(scheduled_appointments), "appointments have been successfully saved to:", file_path)


def main():
    days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
    calendar = create_weekly_calendar()
    scheduled_appointments = []
    days_mapping = {day.lower(): index + 1 for index, day in enumerate(days)}
    load_scheduled_appointments(calendar, scheduled_appointments)

    while True:
        print_menu()
        choice = input("Enter your choice (1-4 and 9): ")

        if choice == "1":
            # Schedule an appointment
            day = input("What Day: ").lower()
            hour = int(input("Enter Start hour (24-hour clock): "))
            client_name = input("Client Name: ")
            client_phone = input("Client Phone:")
            print("Appointment types")
            print("1: Mens cut $50, 2: Ladies Cut $80, 3: Men coloring $50, 4: Ladies coloring $120")
            appt_type = int(input("Enter the type of appointment (1-4): "))
            if appt_type == 0 and calendar[(days_mapping[day] - 1) * 7 + hour - 9].client_name:
                existing_appointment = calendar[(days_mapping[day] - 1) * 7 + hour - 9]
                print(f"Slot not available. Existing appointment: {existing_appointment.get_client_name()}")
   
            elif appt_type == 1 and calendar[(days_mapping[day] - 1) * 7 + hour - 9].client_name:
                existing_appointment = calendar[(days_mapping[day] - 1) * 7 + hour - 9]
                print(f"Slot not available. Existing appointment: {existing_appointment.get_client_name()}")
                print(f"\n{show_appointments_by_day(scheduled_appointments, day)}")
            elif appt_type == 2 and calendar[(days_mapping[day] - 1) * 7 + hour - 9].client_name:
                existing_appointment = calendar[(days_mapping[day] - 1) * 7 + hour - 9]
                print(f"Slot not available. Existing appointment: {existing_appointment.get_client_name()}")
                print(f"\n{show_appointments_by_day(scheduled_appointments, day)}")
            elif appt_type == 3 and calendar[(days_mapping[day] - 1) * 7 + hour - 9].client_name:
                existing_appointment = calendar[(days_mapping[day] - 1) * 7 + hour - 9]
                print(f"Slot not available. Existing appointment: {existing_appointment.get_client_name()}")
                print(f"\n{show_appointments_by_day(scheduled_appointments, day)}")
            elif appt_type == 4 and calendar[(days_mapping[day] - 1) * 7 + hour - 9].client_name:
                existing_appointment = calendar[(days_mapping[day] - 1) * 7 + hour - 9]
                print(f"Slot not available. Existing appointment: {existing_appointment.get_client_name()}")
                print(f"\n{show_appointments_by_day(scheduled_appointments, day)}")
            else:
                calendar[(days_mapping[day] - 1) * 7 + hour - 9].schedule(client_name, client_phone, appt_type)
                scheduled_appointments.append(Appointment(day, hour, client_name, client_phone, appt_type))
                print(f"Ok, {client_name} appointment has been scheduled")

        elif choice == "2":
            # Find appointment by name
            show_appointments_by_name(scheduled_appointments)

        elif choice == "3":
            # Print calendar for a specific day
            day = input("What Days of the week do you like to check?: ")
            show_appointments_by_day(scheduled_appointments, day)

        # Inside main function
        elif choice == "4":
            # Cancel an appointment
            day = input("Enter the day of the week to cancel the appointment: ").capitalize()
            hour = int(input("Enter the hour to cancel the appointment (24-hour clock): "))
            find_appointment_by_time(calendar, scheduled_appointments, days_mapping, days_mapping[day.lower()], hour)


        elif choice == "9":
            # Exit the system
            save_option = input("Would you like to save all scheduled appointments to a file (Y/N)? ").lower()
            if save_option == 'y':
                file_name = input("Enter the file name to save appointments to: ")
                file_path = r"C:\OOP\New folder" + "\\" + file_name + ".csv"
                save_scheduled_appointments(scheduled_appointments, file_path)
                print("Good Bye!")
                break

        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
