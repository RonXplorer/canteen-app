from app import db, login_manager
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modelo de Usuario
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # worker, provider, finance
    is_validated = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.name}>"

# Modelo de Menú
class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    img_url = db.Column(db.String(200), nullable=True)

    food_post = db.relationship('User', backref='dishes')
    orders_list = db.relationship('Order', backref='dish_detail', cascade="all, delete")
    available_start_date = db.Column(db.Date, nullable=False)
    available_end_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Dish {self.name}>"
    
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    deliver_to = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pendiente')

    dish = db.relationship('Dish', backref='orders')
    worker = db.relationship('User', backref='orders')