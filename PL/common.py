from datetime import date

def calculate_age(year_of_birth):
    today = date.today()
    age = today.year - year_of_birth
    if today.month < 1 or (today.month == 1 and today.day < 1):
        age -= 1
    return age
