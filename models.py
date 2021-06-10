def create_beer(db):
    class Beer(db.Model):
        __tablename__ = 'beer'

        id = db.Column(db.Integer, primary_key=True)
        category = db.Column(db.String(64))
        brand = db.Column(db.String(64))
        product = db.Column(db.String(64))
        volAmt = db.Column(db.Float)
        volUnit = db.Column(db.String(32))
        xpack = db.Column(db.Integer)
        bottles = db.Column(db.Boolean)
        cans = db.Column(db.Boolean)
        price = db.Column(db.Float)
        image = db.Column(db.String(32))

        def __repr__(self):
            return '<Beer %r>' % (self.name)
    return Beer

def create_wine(db):
    class Wine(db.Model):
        __tablename__ = 'wine'

        id = db.Column(db.Integer, primary_key=True)
        category = db.Column(db.String(64))
        brand = db.Column(db.String(64))
        product = db.Column(db.String(64))
        volAmt = db.Column(db.Float)
        volUnit = db.Column(db.String(32))
        varietals = db.Column(db.String(64))
        price = db.Column(db.Float)
        image = db.Column(db.String(32))

        def __repr__(self):
            return '<Wine %r>' % (self.name)
    return Wine

def create_spirit(db):
    class Spirit(db.Model):
        __tablename__ = 'spirits'

        id = db.Column(db.Integer, primary_key=True)
        category = db.Column(db.String(64))
        brand = db.Column(db.String(64))
        product = db.Column(db.String(64))
        volAmt = db.Column(db.Float)
        volUnit = db.Column(db.String(32))
        price = db.Column(db.Float)
        image = db.Column(db.String(32))

        def __repr__(self):
            return '<Spirit %r>' % (self.name)
    return Spirit
