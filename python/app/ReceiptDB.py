from datetime import datetime

from . import db


class Category(db.Model):  # creates a category
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class AddReceipt(db.Model): # creates a receipt
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    merchant = db.Column(db.String(80), nullable=False)
    dateOfPurchase = db.Column(db.String(80), nullable=False)
    returnDate = db.Column(db.String(80), nullable=False)
    totalPrice = db.Column(db.Numeric(10, 2), nullable=False)
    numberOfItems = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')


    def __repr__(self):
        return '<AddReceipt %r>' % self.title


db.create_all()