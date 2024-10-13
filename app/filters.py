from app.models import PhoneNumber, Blacklist

def filter_blacklist() -> int:
    """
    Фильтрует номера, которые присутствуют в черном списке.
    Удаляет их из базы данных телефонных номеров.
    Возвращает количество удаленных записей.
    """
    blacklist_numbers = Blacklist.query.with_entities(Blacklist.number).all()
    blacklist_set = {num[0] for num in blacklist_numbers}
    
    deleted_count = 0
    for phone in PhoneNumber.query.all():
        if phone.number in blacklist_set:
            db.session.delete(phone)
            deleted_count += 1

    db.session.commit()
    return deleted_count

def filter_partial_match(pattern: str) -> int:
    """
    Фильтрует номера, частично совпадающие с переданным паттерном.
    Возвращает количество удаленных записей.
    """
    deleted_count = 0
    for phone in PhoneNumber.query.all():
        if pattern in phone.number:
            db.session.delete(phone)
            deleted_count += 1
    
    db.session.commit()
    return deleted_count
