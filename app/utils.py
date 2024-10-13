import pandas as pd
from app.models import PhoneNumber, Blacklist, db

def import_phone_numbers(file_path: str) -> dict:
    data = pd.read_csv(file_path, header=None, names=['number'])
    added, duplicates = 0, 0

    for index, row in data.iterrows():
        number = row['number']
        if not PhoneNumber.query.filter_by(number=number).first():
            new_number = PhoneNumber(number=number, source='imported')
            db.session.add(new_number)
            added += 1
        else:
            duplicates += 1

    db.session.commit()
    return {'added': added, 'duplicates': duplicates}

def import_blacklist(file_path: str) -> dict:
    data = pd.read_csv(file_path, header=None, names=['number'])
    added, duplicates = 0, 0

    for index, row in data.iterrows():
        number = row['number']
        if not Blacklist.query.filter_by(number=number).first():
            new_number = Blacklist(number=number)
            db.session.add(new_number)
            added += 1
        else:
            duplicates += 1

    db.session.commit()
    return {'added': added, 'duplicates': duplicates}

def filter_blacklist() -> int:
    blacklist_numbers = Blacklist.query.with_entities(Blacklist.number).all()
    blacklist_set = {num[0] for num in blacklist_numbers}
    
    deleted_count = 0
    for phone in PhoneNumber.query.all():
        if phone.number in blacklist_set:
            db.session.delete(phone)
            deleted_count += 1

    db.session.commit()
    return deleted_count

def export_cleaned_data() -> str:
    file_path = '/tmp/cleaned_data.csv'
    numbers = PhoneNumber.query.all()

    with open(file_path, 'w') as f:
        for number in numbers:
            f.write(f"{number.number}\n")

    return file_path

def export_global_database() -> str:
    file_path = '/tmp/global_database.csv'
    numbers = PhoneNumber.query.all()

    with open(file_path, 'w') as f:
        for number in numbers:
            f.write(f"{number.number}\n")

    return file_path
