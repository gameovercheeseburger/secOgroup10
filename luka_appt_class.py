class Appointment:
    def __init__(self, day_of_week, start_time_hour):
        self.client_name = ""
        self.client_phone = ""
        self.appt_type = 0
        self.day_of_week = day_of_week
        self.start_time_hour = start_time_hour

    def get_client_name(self):
        return self.client_name

    def get_client_phone(self):
        return self.client_phone

    def get_day_of_week(self):
        return self.day_of_week
    
    def get_start_time_hour(self):
        return self.start_time_hour
    
    def get_appt_type(self):
        return self.appt_type

    def get_appt_type_description(self):
        if self.appt_type == 0:
            return "Available"
        elif self.appt_type == 1:
            return "Mens Cut"
        elif self.appt_type == 2:
            return "Ladies Cut"
        elif self.appt_type == 3:
            return "Mens Colouring"
        elif self.appt_type == 4:
            return "Ladies Colouring"
        else:
            return "Invalid appt_type"
        
    def get_end_time_hour(self):
        return self.start_time_hour + 1
    
    def set_client_name(self, client_name):
        self.client_name = client_name

    def set_client_phone(self, client_phone):
        self.client_phone = client_phone

    def set_appt_type(self, appt_type):
        self.appt_type = appt_type

    def schedule(self, client_name, client_phone, appt_type):
        self.client_name = client_name
        self.client_phone = client_phone
        self.appt_type = appt_type

    def cancel(self):
        self.client_name = ""
        self.client_phone = ""
        self.appt_type = 0

    def format_record(self):
        return f"{self.client_name},{self.client_phone},{self.appt_type},{self.day_of_week},{self.start_time_hour}"

    def __str__(self):
        return f"{self.client_name:<15} {self.client_phone:>16} {self.day_of_week:>10} {'{:02d}'.format(self.start_time_hour):>3}:00 {'-':>2} {self.get_end_time_hour():>3}:00 {'':>3} {self.get_appt_type_description()}"


def create_weekly_calendar():
    calendar = []
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for day in days_of_week:
        for hour in range(9, 17):
            calendar.append(Appointment(day, hour))
    return calendar


      
    





  

