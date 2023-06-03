from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
import json



# Accounts


# Dogs
def calculate_age(birthDate):
    today = date.today()
    age = relativedelta(today, birthDate)
    if age.years > 0:
        return f"{age.years} años"
    elif age.months > 0:
        return f"Menos de un año"
    else:
        return f"Menos de un mes"
    

# Turns
def turn_type_mapping():
    map = {
        'T': 'Turno normal',
        'C': 'Castración',
        'VA': 'Vacunación - Tipo A',
        'VB': 'Vacunacion - Tipo B',
    }
    return map

def turn_hour_mapping():
    map = {
        'Morning': 'Tanda mañana: 08:00 a 13:00hs',
        'Afternoon': 'Tanda tarde: 15:00 a 20:00hs',
    }
    return map

def actual_turn_hour_check():
    current_time = datetime.now().time()

    afternoon_start = time(15, 0)  # 15:00
    afternoon_end = time(20, 0)  # 20:00
    
    if afternoon_start <= current_time <= afternoon_end:
        return 'Afternoon'
    else:
        return 'Morning'

def generate_date(today, birthdate, type):
    if type == 'VA':
        months_diff = (today.year - birthdate.year) * 12 + (today.month - birthdate.month)
    else:
        months_diff = 4 # default 365 days for type B

    if months_diff < 4:
        future_date = today + timedelta(days=21)
    else:
        future_date = today + timedelta(days=365)

    return future_date

def append_data(model_instance, new_data):
    # Retrieve the existing data
    existing_data = json.loads(model_instance.urgency_turns)

    # Append the new data
    existing_data.append(new_data)

    # Save the updated data
    model_instance.urgency_turns = json.dumps(existing_data)
    model_instance.save()