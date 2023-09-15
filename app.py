
from flask import Flask, render_template, request, redirect, url_for
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


# Database model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    stock_on_hand = db.Column(db.Integer, nullable=False)


@app.route('/generate', methods=['GET'])
def generate_products():
    for i in range(1, 51):
        product = Product.query.filter_by(name=f'Item {i}').first()
        if product:
            product.stock_on_hand = random.randint(20, 50)
        else:
            product = Product(name=f'Item {i}', stock_on_hand=random.randint(20, 50))
            db.session.add(product)

    db.session.commit()
    return redirect(url_for('index'))


per_page = 20

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=per_page, error_out=True)
    return render_template('index.html', products=products)


# sort product by name
@app.route('/sort_name')
def sort_name():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.name).paginate(page=page, per_page=per_page, error_out=True)
    return render_template('index.html', products=products)


# sort stock in descending order
@app.route('/sort_stock_desc')
def sort_stock_desc():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.stock_on_hand.desc()).paginate(page=page, per_page=per_page, error_out=True)
    return render_template('index.html', products=products)


# decrease the no of stocks by 2
@app.route('/reduce_stock')
def reduce_stock():
    products = Product.query.all()
    for product in products:
        if product.stock_on_hand < 2:
            product.stock_on_hand = 0
        else:
            product.stock_on_hand -= 2

    db.session.commit()
    return redirect(url_for('index'))


# increase even no items stock on hand by 2
@app.route('/increase_even')
def increase_even():
    products = Product.query.all()
    for product in products:
        if int(product.name.split()[-1]) % 2 == 0:
            product.stock_on_hand += 2
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



