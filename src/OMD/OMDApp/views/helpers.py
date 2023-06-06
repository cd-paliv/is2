from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from OMDApp.models import Turno
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
        'D': 'Desparasitacion',
        'VA': 'Vacunación - Tipo A',
        'VB': 'Vacunacion - Tipo B',
    }
    return map

def turn_type_mapping_with_urgency():
    map = {
        'T': 'Turno normal',
        'C': 'Castración',
        'VA': 'Vacunación - Tipo A',
        'VB': 'Vacunacion - Tipo B',
        'U': 'Urgencia',
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

    morning_start = time(8, 0)
    morning_end = time(13, 0)
    afternoon_start = time(15, 0)  # 15:00
    afternoon_end = time(20, 0)  # 20:00
    
    if afternoon_start <= current_time <= afternoon_end:
        return 'Afternoon'
    #elif morning_start <= current_time <= morning_end:
    #    return 'Morning'
    else:
    #    return 'None'
        return 'Morning'

def generate_date(birthdate, type):
    today = date.today()

    if type != 'D':
        if type == 'VA':
            months_diff = (today.year - birthdate.year) * 12 + (today.month - birthdate.month)
        else:
            months_diff = 4 # default 365 days for type B

        if months_diff < 4:
            future_date = today + timedelta(days=21)
        else:
            future_date = today + timedelta(days=365)

        return future_date
    return today + timedelta(days=1)

def append_data(model_instance, new_data):
    existing_data = json.loads(model_instance.urgency_turns)

    existing_data.append(new_data)

    model_instance.urgency_turns = json.dumps(existing_data)
    model_instance.save()

def delete_unwanted_next_turns(dog, turn_type):
    next_allowed_date = generate_date(dog.birthdate, turn_type)

    start_date = date.today() + timedelta(days=1)
    end_date = next_allowed_date - timedelta(days=1)

    turns =  Turno.objects.filter(solicited_by=dog, type=turn_type, date__range=(start_date, end_date))

    if turns is not None:
        for turn in turns:
            turn.delete()

def get_filtered_interventions(dog):
    today = date.today()

    choices = (('D', 'Desparasitacion'), ('C', 'Castración'), ('VA', 'Vacunacion - Tipo A'), ('VB', 'Vacunacion - Tipo B'))
    filtered_choices = {}
    for choice_label, choice_value in choices:
        if choice_label == 'C' and dog.castrated:
            continue
        if choice_label == 'D':
            dog_age = calculate_age(dog.birthdate)
            if "Menos de" not in dog_age:
                continue
            has_desp_turn = lambda: True if Turno.objects.filter(date=date.today(), type='D').exists() else False
            if has_desp_turn:
                continue
        most_recent_turn = Turno.objects.filter(solicited_by=dog, type=choice_label, state='F').order_by('-date').first()
        if most_recent_turn is not None:
            days_difference = (today - most_recent_turn.date).days # Days from the las intervention
            max_days = (generate_date(dog.birthdate, choice_label) - today).days # Necessary days to implement that intervention again
            if days_difference >= max_days:
                filtered_choices[choice_label] = choice_value
        else:
            filtered_choices[choice_label] = choice_value
            
    return filtered_choices

    