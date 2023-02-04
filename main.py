from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from data import users, offers, orders


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


with app.app_context():
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        first_name = db.Column(db.String)
        last_name = db.Column(db.String)
        age = db.Column(db.Integer)
        email = db.Column(db.String)
        role = db.Column(db.String)
        phone = db.Column(db.String)

        def get_dict(self):
            return {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'age': self.age,
                'email': self.email,
                'role': self.role,
                'phone': self.phone
                    }


    class Order(db.Model):
        __tablename__ = 'order'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String)
        description = db.Column(db.String)
        start_date = db.Column(db.Date)
        end_date = db.Column(db.Date)
        address = db.Column(db.String)
        price = db.Column(db.Integer)
        customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def get_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'address': self.address,
                'price': self.price,
                'customer_id': self.customer_id,
                'executor_id': self.executor_id
                    }


    class Offer(db.Model):
        __tablename__ = 'offer'
        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
        executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def get_dict(self):
            return {
                'id': self.id,
                'order_id': self.order_id,
                'executor_id': self.executor_id
                    }


    # db.drop_all()
    db.create_all()

    with db.session.begin():
        for user in users:
            db.session.add(User(**user))

        for order in orders:
            order['start_date'] = datetime.strptime(order['start_date'], '%m/%d/%Y')
            order['end_date'] = datetime.strptime(order['end_date'], '%m/%d/%Y')
            db.session.add(Order(**order))

        for offer in offers:
            db.session.add(Offer(**offer))


@app.get('/users')
def all_users_page():
    result = User.query.all()
    all_users = [us.get_dict() for us in result]
    return jsonify(all_users)


@app.get('/users/<int:uid>')
def user_by_id_page(uid):
    result = User.query.get(uid)
    return jsonify(result.get_dict())


@app.post('/users')
def add_user():
    new_data = request.json
    new_user = User(**new_data)
    db.session.add(new_user)
    db.session.commit()
    return '', 201


@app.put('/users/<int:uid>')
def update_user(uid):
    new_data = request.json
    user_to_update = User.query.get(uid)
    user_to_update.first_name = new_data['first_name']
    user_to_update.last_name = new_data['last_name']
    user_to_update.age = new_data['age']
    user_to_update.email = new_data['email']
    user_to_update.role = new_data['role']
    user_to_update.phone = new_data['phone']
    db.session.add(user_to_update)
    db.session.commit()
    return '', 201


@app.delete('/users/<int:uid>')
def delete_user(uid):
    user_to_delete = User.query.get(uid)
    db.session.delete(user_to_delete)
    db.session.commit()
    return '', 204


@app.get('/orders')
def get_all_orders():
    result = Order.query.all()
    all_orders = []
    for order_ in result:
        order_dict = order_.get_dict()
        order_dict['start_date'] = str(order_dict['start_date'])
        order_dict['end_date'] = str(order_dict['end_date'])
        all_orders.append(order_dict)

    return jsonify(all_orders)


@app.get('/orders/<int:uid>')
def order_by_id_page(uid):
    result = Order.query.get(uid)
    return jsonify(result.get_dict())


@app.post('/orders')
def add_order():
    new_data = request.json
    new_data['start_date'] = datetime.strptime(new_data['start_date'], '%Y-%m-%d')
    new_data['end_date'] = datetime.strptime(new_data['end_date'], '%Y-%m-%d')
    new_user = Order(**new_data)
    db.session.add(new_user)
    db.session.commit()
    return '', 201


@app.put('/orders/<int:uid>')
def update_order(uid):
    new_data = request.json
    user_to_update = Order.query.get(uid)
    user_to_update.name = new_data['name']
    user_to_update.description = new_data['description']
    user_to_update.start_date = datetime.strptime(new_data['start_date'], '%Y-%m-%d')
    user_to_update.end_date = datetime.strptime(new_data['end_date'], '%Y-%m-%d')
    user_to_update.address = new_data['address']
    user_to_update.price = new_data['price']
    user_to_update.customer_id = new_data['customer_id']
    user_to_update.executor_id = new_data['executor_id']
    db.session.add(user_to_update)
    db.session.commit()
    return '', 201


@app.delete('/orders/<int:uid>')
def delete_order(uid):
    user_to_delete = Order.query.get(uid)
    db.session.delete(user_to_delete)
    db.session.commit()
    return '', 204


@app.get('/offers')
def get_all_offers():
    result = Offer.query.all()
    all_offers = [of.get_dict() for of in result]
    return jsonify(all_offers)


@app.get('/offers/<int:uid>')
def offer_by_id_page(uid):
    result = Offer.query.get(uid)
    return jsonify(result.get_dict())


@app.post('/offers')
def add_offer():
    new_data = request.json
    new_user = Offer(**new_data)
    db.session.add(new_user)
    db.session.commit()
    return '', 201


@app.put('/offers/<int:uid>')
def update_offer(uid):
    new_data = request.json
    user_to_update = Offer.query.get(uid)
    user_to_update.order_id = new_data['order_id']
    user_to_update.executor_id = new_data['executor_id']
    db.session.add(user_to_update)
    db.session.commit()
    return '', 201


@app.delete('/offers/<int:uid>')
def delete_offer(uid):
    user_to_delete = Offer.query.get(uid)
    db.session.delete(user_to_delete)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
