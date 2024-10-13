from app import db

class PhoneNumber(db.Model):
    __tablename__ = 'phone_numbers'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False, unique=True)
    source = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<PhoneNumber {self.number}>'


class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'<Blacklist {self.number}>'


class GlobalDatabase(db.Model):
    __tablename__ = 'global_database'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'<GlobalDatabase {self.number}>'
