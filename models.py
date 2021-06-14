def create_beer(db):
    class Beer(db.Model):
        __tablename__ = 'beer'

        id = db.Column(db.Integer, primary_key=True)
        timestamp = db.Column(db.DateTime)
        month = db.Column(db.String(32))
        category = db.Column(db.String(64))
        brand = db.Column(db.String(64))
        product = db.Column(db.String(64))
        volAmt = db.Column(db.Float)
        volUnit = db.Column(db.String(32))
        xpack = db.Column(db.Integer)
        container = db.Column(db.String(64))
        price = db.Column(db.Float)

        def __repr__(self):
            return f'<Beer {self.brand} {self.product}>'
    return Beer

def create_wine(db):
    class Wine(db.Model):
        __tablename__ = 'wine'

        id = db.Column(db.Integer, primary_key=True)
        timestamp = db.Column(db.DateTime)
        month = db.Column(db.String(32))
        category = db.Column(db.String(64))
        brand = db.Column(db.String(64))
        product = db.Column(db.String(64))
        volAmt = db.Column(db.Float)
        volUnit = db.Column(db.String(32))
        container = db.Column(db.String(64))
        varietals = db.Column(db.String(64))
        price = db.Column(db.Float)

        def __repr__(self):
            return f'<Wine {self.brand} {self.product}>'
    return Wine

def create_spirit(db):
    class Spirit(db.Model):
        __tablename__ = 'spirits'

        id = db.Column(db.Integer, primary_key=True)
        timestamp = db.Column(db.DateTime)
        month = db.Column(db.String(32))
        category = db.Column(db.String(64))
        brand = db.Column(db.String(64))
        product = db.Column(db.String(64))
        volAmt = db.Column(db.Float)
        volUnit = db.Column(db.String(32))
        price = db.Column(db.Float)

        def __repr__(self):
            return f'<Spirit {self.brand} {self.product}>'
    return Spirit

def create_staff(db):
    class Staff(db.Model):
        __tablename__ = 'staff'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(32))
        pos = db.Column(db.String(32))
        specialties = db.Column(db.String(64))
        hobbies = db.Column(db.String(64))
        goals = db.Column(db.String(64))

        def __repr__(self):
            return f'<Staff {self.name}>'
    return Staff