from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class CarCleaningGoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    producer = db.Column(db.String(120), unique=True)
    country = db.Column(db.String(120), unique=True)
    sales_per_day = db.Column(db.String(120), unique=True)
    price = db.Column(db.String(120), unique=True)
    quality = db.Column(db.String(120), unique=True)

    def __init__(self, name, producer, country,
                 sales_per_day, price, quality):
        self.name = name
        self.producer = producer
        self.country = country
        self.sales_per_day = sales_per_day
        self.price = price
        self.quality = quality


class GoodSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'producer', 'country', 'sales_per_day', 'price', 'quality')


good_schema = GoodSchema()
goods_schema = GoodSchema(many=True)


# endpoint to create new good
@app.route("/good", methods=["POST"])
def add_good():
    name = request.json['name']
    producer = request.json['producer']
    country = request.json['country']
    sales_per_day = request.json['sales_per_day']
    price = request.json['price']
    quality = request.json['quality']
    
    new_good = CarCleaningGoods(name, producer, country, sales_per_day, price, quality)

    db.session.add(new_good)
    db.session.commit()

    return jsonify(new_good)


# endpoint to show all goods
@app.route("/good", methods=["GET"])
def get_good():
    all_goods = CarCleaningGoods.query.all()
    result = goods_schema.dump(all_goods)
    return jsonify(result.data)


# endpoint to get good detail by id
@app.route("/good/<id>", methods=["GET"])
def good_detail(id):
    good = CarCleaningGoods.query.get(id)
    return good_schema.jsonify(good)


# endpoint to update good
@app.route("/good/<id>", methods=["PUT"])
def good_update(id):
    good = CarCleaningGoods.query.get(id)
    name = request.json['name']
    producer = request.json['producer']
    country = request.json['country']
    sales_per_day = request.json['sales_per_day']
    price = request.json['price']
    quality = request.json['quality']

    good.name = name
    good.producer = producer
    good.country = country
    good.sales_per_day = sales_per_day
    good.price = price
    good.quality = quality

    db.session.commit()
    return good_schema.jsonify(good)


# endpoint to delete good
@app.route("/good/<id>", methods=["DELETE"])
def good_delete(id):
    good = CarCleaningGoods.query.get(id)
    db.session.delete(good)
    db.session.commit()

    return good_schema.jsonify(good)


if __name__ == '__main__':
    app.run(debug=True)
