from flask import Flask, url_for, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#cartitem1 = CartItem(id = 1, name = "Apple", cost = 10)
#cartitem2 = CartItem(id = 2, name = "Banana", cost = 5)
#cartitem3 = CartItem(id = 3, name = "Orange", cost = 8)
#cartitem4 = CartItem(id = 4, name = "Watermelon", cost = 20)
        
#db.session.add(cartitem1)
#db.session.add(cartitem2)
#db.session.add(cartitem3))
#db.session.add(cartitem4)
#db.session.commit()

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    cost = db.Column(db.Integer, nullable = False)
    # quantity is 0 by default
    quantity = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return '<CartItem %r>' % self.id


@app.route('/')
def index():
    cartitems = CartItem.query.all()
    total_quantity = 0
    total_cost = 0
    shipping_cost = 0
    total_prehst = 0
    hst = 0
    total = 0
    try:
        for cartitem in cartitems:
            total_quantity += (cartitem.quantity)
            total_cost += (cartitem.quantity) * (cartitem.cost)
        if 0 < total_cost < 50:
            shipping_cost = 15
        elif 50 <= total_cost < 100:
            shipping_cost = 5
        else:
            shipping_cost = 0
        total_prehst = total_cost + shipping_cost
        hst = round(0.13 * total_prehst, 2)
        total = total_prehst + hst
        return render_template('index.html', cartitems=cartitems, total_quantity=total_quantity, total_cost=total_cost, \
            shipping_cost=shipping_cost, total_prehst=total_prehst, hst=hst, total=total)
    except:
        return render_template('index.html', cartitems=cartitems, total_quantity=total_quantity, total_cost=total_cost, \
            shipping_cost=shipping_cost, total_prehst=total_prehst, hst=hst, total=total)

    
@app.route('/add/<int:id>', methods=['POST'])
def add(id):
    # addedcartitem is the cart item which was just added to
    addedcartitem = CartItem.query.get_or_404(id)

    if request.method == 'POST':
        try:
            prev_quantity = addedcartitem.quantity
            addedcartitem.quantity = request.form['quantity']
            db.session.commit()
            new_quantity = addedcartitem.quantity
            addedcartitem.quantity = prev_quantity + new_quantity
            db.session.commit()
            return redirect('/')
        except:
            return redirect('/')
    
    return "Error in add route"

@app.route('/delete/<int:id>')
def delete(id):
    cartitem_to_delete = CartItem.query.get_or_404(id)
    try:
        cartitem_to_delete.quantity = 0
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

if __name__ == "__main__":
    app.run(debug=True)

