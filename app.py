from flask import Flask, url_for, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    cost = db.Column(db.Integer, nullable = False)
    # quantity is 0 by default
    quantity = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return '<CartItem %r>' % self.id

cartitem1 = CartItem(id = 1, name = "Apple", cost = 10)
cartitem2 = CartItem(id = 2, name = "Banana", cost = 5)
cartitem3 = CartItem(id = 3, name = "Orange", cost = 8)
cartitem4 = CartItem(id = 4, name = "Watermelon", cost = 20)

try:
    db.session.add(cartitem1)
    db.session.add(cartitem2)
    db.session.add(cartitem3)
    db.session.add(cartitem4)
    db.session.commit()
except:
    print("Database exists")




@app.route('/')
def index():
    return render_template('index.html')

    
@app.route('/add/<int:id>', methods=['GET', 'POST'])
def add(id):
    # returns the cart item which was just added to
    addedcartitem = CartItem.query.get_or_404(id)

    if request.method == 'POST':
        addedcartitem.quantity = request.form['content']

        try:
            db.session.commit()
            



if __name__ == "__main__":
    app.run(debug=True)

