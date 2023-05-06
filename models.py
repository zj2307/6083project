from extensions import db
from flask_login import UserMixin
from sqlalchemy import ForeignKey, CheckConstraint


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    cell_number = db.Column(db.BigInteger, nullable=False)
    email_address = db.Column(db.String(30), nullable=False)
    permission = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Visitor(db.Model):
    visitor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    email_address = db.Column(db.String(30), nullable=False)
    cell_number = db.Column(db.BigInteger, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    visitor_type = db.Column(db.String(10), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)

    # Relationships
    payments = db.relationship('Payment', backref='visitor', lazy=True)
    visitor_attractions = db.relationship('VisitorAttraction', backref='visitor', lazy=True)
    visitor_shows = db.relationship('VisitorShow', backref='visitor', lazy=True)

    # Check constraints
    __table_args__ = (
        CheckConstraint("visitor_type IN ('Individual', 'Group', 'Member', 'Student')"),
    )


class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.String(10), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_amount = db.Column(db.Numeric(10, 2), nullable=False)
    name_on_card = db.Column(db.String(50))
    card_number = db.Column(db.BigInteger)
    exp_date = db.Column(db.Date, nullable=False)
    cvv_number = db.Column(db.Integer)
    visitor_id = db.Column(db.Integer, ForeignKey('visitor.visitor_id'), nullable=False)

    # Relationships
    tickets = db.relationship('Ticket', backref='payment', lazy=True)
    parkings = db.relationship('Parking', backref='payment', lazy=True)
    orders = db.relationship('Order', backref='payment', lazy=True)

    # Check constraints
    __table_args__ = (
        CheckConstraint("payment_method IN ('Cash', 'Credit', 'Debit Card')"),
    )


class Attraction(db.Model):
    attraction_id = db.Column(db.Integer, primary_key=True)
    attraction_name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    minimum_height = db.Column(db.Integer, nullable=False)
    duration_in_minutes = db.Column(db.Integer, nullable=False)
    location_section = db.Column(db.String(10), nullable=False)

    # Relationships
    visitor_attractions = db.relationship('VisitorAttraction', backref='attraction', lazy=True)

    # Check constraints
    __table_args__ = (
        CheckConstraint("type IN ('roller coaster', 'water ride', 'dark ride', 'kid ride')"),
        CheckConstraint("status IN ('open', 'closed', 'under maintenance')"),
        CheckConstraint("location_section IN ('Lot A', 'Lot B', 'Lot C', 'Lot D')"),
    )


class Show(db.Model):
    show_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    wheelchair_accessible = db.Column(db.String(3), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    # Relationships
    visitor_shows = db.relationship('VisitorShow', backref='show', lazy=True)

    # Check constraints
    __table_args__ = (
        CheckConstraint("type IN ('drama', 'musical', 'comedy', 'horror', 'adventure')"),
        CheckConstraint("wheelchair_accessible IN ('Yes', 'No')"),
    )


class Store(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    menu_item = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    # Relationships
    orders = db.relationship('Order', backref='store', lazy=True)

    # Check constraints
    __table_args__ = (
        CheckConstraint("category IN ('Food stall', 'Ice cream parlor', 'Restaurant', 'Gift Shop', 'Apparels')"),
    )


class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    ticket_method = db.Column(db.String(6), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    visit_date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(6), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False)
    visitor_id = db.Column(db.Integer, ForeignKey('visitor.visitor_id'), nullable=False)
    payment_id = db.Column(db.Integer, ForeignKey('payment.payment_id'), nullable=False)
    # Check constraints
    __table_args__ = (
        CheckConstraint("ticket_method IN ('Online', 'Onsite')"),
        CheckConstraint("type IN ('Child', 'Adult', 'Senior', 'Member')"),
    )


class Parking(db.Model):
    parking_id = db.Column(db.Integer, primary_key=True)
    lot = db.Column(db.String(50), nullable=False)
    spot_number = db.Column(db.Integer, nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=False)
    fee = db.Column(db.Numeric(10, 2), nullable=False)
    visitor_id = db.Column(db.Integer, ForeignKey('visitor.visitor_id'), nullable=False)
    payment_id = db.Column(db.Integer, ForeignKey('payment.payment_id'), nullable=False)


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    store_id = db.Column(db.Integer, ForeignKey('store.store_id'), nullable=False)
    visitor_id = db.Column(db.Integer, ForeignKey('visitor.visitor_id'), nullable=False)
    payment_id = db.Column(db.Integer, ForeignKey('payment.payment_id'), nullable=False)


class VisitorAttraction(db.Model):
    visitor_id = db.Column(db.Integer, ForeignKey('visitor.visitor_id'), primary_key=True)
    attraction_id = db.Column(db.Integer, ForeignKey('attraction.attraction_id'), primary_key=True)


class VisitorShow(db.Model):
    visitor_id = db.Column(db.Integer, ForeignKey('visitor.visitor_id'), primary_key=True)
    show_id = db.Column(db.Integer, ForeignKey('show.show_id'), primary_key=True)




