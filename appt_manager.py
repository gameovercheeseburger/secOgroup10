from appointment import Appointment

def create_weekly_calendar():
    calendar = []
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for day in days_of_week:
        for hour in range(9, 17):
            calendar.append(Appointment(day, hour))
    return calendar

class AppointmentManagementModule:
    def __init__(self):
        self.calendar = create_weekly_calendar()
        self.scheduled_appointments = []

    def load_scheduled_appointments(self):
        file_name = input("Enter the file name to load appointments from (or press Enter to skip): ")
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        data = line.strip().split(',')
                        appointment = Appointment(data[3], int(data[4]))
                        appointment.client_name = data[0]
                        appointment.client_phone = data[1]
                        appointment.appt_type = int(data[2])
                        self.scheduled_appointments.append(appointment)
                        # Mark the slot as unavailable
                        self.calendar[(int(data[3]) - 1) * 6 + int(data[4]) - 9].client_name = data[0]
            except FileNotFoundError:
                print("File not found. No appointments loaded.")

    def print_menu(self):
        print("\nMenu:")
        print("1. Schedule an appointment")
        print("2. Find appointment by name")
        print("3. Print calendar for a specific day")
        print("4. Cancel an appointment")
        print("5. Save all scheduled appointments to a file")
        print("6. Exit the system")

    def find_appointment_by_time(self):
        day = input("Enter the day of the week (e.g., Monday): ")
        hour = int(input("Enter the start time of the appointment (9-16): "))
        for appointment in self.scheduled_appointments:
            if appointment.day_of_week.lower() == day.lower() and appointment.start_time_hour == hour:
                print(appointment)
                return
        print("No appointment found for the specified time.")

    def show_appointments_by_name(self):
        name = input("Enter the client name: ")
        found_appointments = [appointment for appointment in self.scheduled_appointments if
                              appointment.client_name.lower() == name.lower()]
        if found_appointments:
            for appointment in found_appointments:
                print(appointment)
        else:
            print("No appointments found for the specified client name.")

    def show_appointments_by_day(self):
        day = input("Enter the day of the week (e.g., Monday): ")
        found_appointments = [appointment for appointment in self.scheduled_appointments if
                              appointment.day_of_week.lower() == day.lower()]
        if found_appointments:
            for appointment in found_appointments:
                print(appointment)
        else:
            print("No appointments found for the specified day.")

    def save_scheduled_appointments(self):
        file_name = input("Enter the file name to save appointments to: ")
        with open(file_name, 'w') as file:
            for appointment in self.scheduled_appointments:
                file.write(appointment.format_record() + '\n')

def main():
    appointment_module = AppointmentManagementModule()
    appointment_module.load_scheduled_appointments()

    while True:
        appointment_module.print_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            # Schedule an appointment
            day = input("Enter the day of the week (e.g., Monday): ")
            hour = int(input("Enter the start time of the appointment (9-16): "))
            appt_type = int(input("Enter the type of appointment (0-4): "))
            name = input("Enter the client name: ")
            phone = input("Enter the client phone number: ")

            if appt_type == 0 and appointment_module.calendar[(int(day) - 1) * 6 + hour - 9].client_name:
                print("Slot is not available.")
            else:
                appointment_module.calendar[(int(day) - 1) * 6 + hour - 9].schedule(name, phone, appt_type)
                appointment_module.scheduled_appointments.append(
                    appointment_module.calendar[(int(day) - 1) * 6 + hour - 9])
                print("Appointment scheduled successfully.")

        elif choice == "2":
            # Find appointment by name
            appointment_module.show_appointments_by_name()

        elif choice == "3":
            # Print calendar for a specific day
            appointment_module.show_appointments_by_day()

        elif choice == "4":
            # Cancel an appointment
            appointment_module.find_appointment_by_time()
            cancel_choice = input("Do you want to cancel this appointment? (yes/no): ")
            if cancel_choice.lower() == "yes":
                appointment_module.calendar[(int(day) - 1) * 6 + hour - 9].cancel()
                print("Appointment canceled successfully.")

        elif choice == "5":
            # Save all scheduled appointments to a file
            appointment_module.save_scheduled_appointments()
            print("Appointments saved to file successfully.")

        elif choice == "6":
            # Exit the system
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
