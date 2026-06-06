from datetime import datetime

def is_above_18(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%d/%m/%Y")
        age = (datetime.today() - dob).days // 365
        return age >= 18
    except:
        return False
