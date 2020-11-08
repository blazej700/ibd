from app import db

order_tea = db.Table('order_tea',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
        db.Column('tea_id', db.Integer, db.ForeignKey('tea.id'))
    )

user_order = db.Table('user_order',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('order_id', db.Integer, db.ForeignKey('order.id'))
    )

