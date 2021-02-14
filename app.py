from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

co2_dict = {}
with open('data/co2_scores.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    for row in data:
        co2_dict[row[0]] = float(row[1])


class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return '<Grocery %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        new_stuff = Grocery(name=name, quantity=quantity)

        if name.lower() not in co2_dict:
            return "Dit ingredient zit niet in het recept"

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new stuff."

    else:
        groceries = Grocery.query.order_by(Grocery.created_at).all()
        return render_template('index.html', groceries=groceries)


@app.route('/delete/<int:id>')
def delete(id):
    grocery = Grocery.query.get_or_404(id)

    try:
        db.session.delete(grocery)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    grocery = Grocery.query.get_or_404(id)

    if request.method == 'POST':
        grocery.name = request.form['name']
        grocery.quantity = request.form['quantity']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html', title=title, grocery=grocery)

@app.route('/calculate', methods=['GET'])
def calculate():
    groceries = Grocery.query.all()

    co2_score = 0.0
    success = True
    for grocery in groceries:
        grocery_name = grocery.name
        try:
            co2_score += (grocery.quantity / 1000) * co2_dict[grocery_name.lower()]
        except:
            success = False

    result = {"co2_score": co2_score, "success": success}

    return result

@app.route('/deleteall')
def deleteall():
    groceries = Grocery.query.all()

    for grocery in groceries:
        db.session.delete(grocery)
        db.session.commit()

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
