from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime
import csv
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = "some_random"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# Dictionary containing all foods
co2_dict = {}
with open('data/cycle_data_en.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)
    for row in data:
        if row[0] != '':
            co2_dict[row[0].lower()] = True

nl_data = []
# updated diet data
with open('data/nl_diet_data.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    for row in data:
        if row[3] == '':
            nl_data.append(
                {
                    'id': row[0],
                    'name': row[1],
                    'parent': row[4],
                    'color': row[5]
                }
            )
        else:
            nl_data.append(
                {
                    'id': row[0],
                    'name': row[1],
                    'parent': row[4],
                    'value': round(float(row[3]), 2),
                    'kg_co2': round(float(row[3]) / 100 * 5.4, 2),
                    'color': row[5]
                }
            )

cycle_dict = {}
with open('data/cycle_data_en.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)  # skip the headers
    for row in data:
        if row[0] != '':
            cycle_dict[row[0]] = row[1:8]

cycle_data = []
with open('data/user_sunburst_data.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)
    for row in data:
        if row[0] != '':
            if row[3] == '':
                cycle_data.append(
                    {
                        'id': row[0],
                        'name': row[1],
                        'parent': row[4],
                        'sliced': False,
                        'color': row[5]
                    }
                )
            else:
                cycle_data.append(
                    {
                        'id': row[0],
                        'name': row[1],
                        'parent': row[4],
                        'value': float(row[3]),
                        'sliced': False
                    }
                )


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'groceries' not in session:
        session['groceries'] = []

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']

        if name.lower() not in co2_dict:
            return "Dit ingredient zit niet in het recept"

        groceries = session.get('groceries')

        groceries.append({'id': name.strip(), 'name': name, 'quantity': int(quantity)})

        session['groceries'] = groceries

        return redirect('/')

    if not session['groceries']:
        users_ingredients = []
    else:
        user_data = []
        groceries = session.get('groceries')
        total_kg_co2 = 0.0

        for grocery in groceries:
            total_kg_co2 += (grocery['quantity'] / 1000) * sum([float(x) for x in cycle_dict[grocery['name']]])

        for grocery in groceries:
            for i in range(len(cycle_data)):
                if cycle_data[i]['name'] == grocery['name']:
                    temp_dict = cycle_data[i].copy()
                    # value = percentage co2 emission of total emission in kg
                    temp_dict['value'] = round((temp_dict['value'] * (grocery['quantity'] / 10) / total_kg_co2), 2)
                    temp_dict['kg_co2'] = round(temp_dict['value'] / 100 * total_kg_co2, 2)
                    user_data.append(temp_dict)

        for i in range(len(user_data)):
            cur_parent_id = user_data[i]['parent']
            if cur_parent_id != '':
                parent_dict = next(item for item in cycle_data if item["id"] == cur_parent_id)
                if parent_dict not in user_data:
                    user_data.append(parent_dict)
        user_data.append({'id': '0.1', 'name': 'Food', 'parent': '', 'kg_co2': round(total_kg_co2, 2), 'color': '#fcfcdc'})
        user_data.append({'id': '1.1', 'name': 'Vegetal Products', 'parent': '0.1', 'color': '#b3e2cd'})
        user_data.append({'id': '1.2', 'name': 'Animal Products', 'parent': '0.1', 'color': '#fdcdac'})

        users_ingredients = user_data

    return render_template('index.html', groceries=session.get('groceries'), data=json.dumps(nl_data),
                           cycle_dict=json.dumps(cycle_dict), cycle_data=json.dumps(cycle_data),
                           users_ingredients=json.dumps(users_ingredients))


@app.route('/process_userdata', methods=['GET'])
def process_userdata():
    """
    Takes the users product list and preprocesses it to the sunburst visualization for the user.

    * Removed total CO2 calculation
    """
    user_data = []
    groceries = session.get('groceries')
    total_kg_co2 = 0.0

    for grocery in groceries:
        total_kg_co2 += (grocery['quantity'] / 1000) * sum([float(x) for x in cycle_dict[grocery['name']]])

    for grocery in groceries:
        for i in range(len(cycle_data)):
            if cycle_data[i]['name'] == grocery['name']:
                temp_dict = cycle_data[i].copy()
                # value = percentage co2 emission of total emission in kg
                temp_dict['value'] = round((temp_dict['value'] * (grocery['quantity'] / 10) / total_kg_co2), 2)
                temp_dict['kg_co2'] = round(temp_dict['value'] / 100 * total_kg_co2, 2)
                user_data.append(temp_dict)

    for i in range(len(user_data)):
        cur_parent_id = user_data[i]['parent']
        if cur_parent_id != '':
            parent_dict = next(item for item in cycle_data if item["id"] == cur_parent_id)
            if parent_dict not in user_data:
                user_data.append(parent_dict)
    user_data.append({'id': '0.1', 'name': 'Food', 'parent': '', 'kg_co2': round(total_kg_co2, 2), 'color': '#fcfcdc'})
    user_data.append({'id': '1.1', 'name': 'Vegetal Products', 'parent': '0.1', 'color': '#b3e2cd'})
    user_data.append({'id': '1.2', 'name': 'Animal Products', 'parent': '0.1', 'color': '#fdcdac'})
    print(user_data)
    return jsonify({'user_data': user_data})


@app.route('/delete/<id>')
def delete(id):
    temp_groceries = []
    groceries = session.get('groceries')
    for grocery in groceries:
        if grocery['id'] != id:
            temp_groceries.append(grocery)

    session['groceries'] = temp_groceries

    return redirect('/')


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    name = None
    for grocery in session.get('groceries'):
        if grocery['id'] == id:
            temp_grocery = grocery
            name = grocery['name']

    if request.method == 'POST':
        temp_groceries = []
        groceries = session.get('groceries')
        for grocery in groceries:
            if grocery['id'] != id:
                temp_groceries.append(grocery)

        session['groceries'] = temp_groceries

        # name = request.form['name']
        quantity = request.form['quantity']

        if name not in cycle_dict:
            return "Dit ingredient zit niet in het recept"

        groceries = session.get('groceries')

        groceries.append({'id': name.strip(), 'name': name, 'quantity': int(quantity)})

        session['groceries'] = groceries

        return redirect('/')

    else:
        return render_template('update.html', grocery=temp_grocery)


@app.route('/calculate', methods=['GET'])
def calculate():
    groceries = session.get('groceries')

    co2_score = 0.0
    success = True
    for grocery in groceries:
        grocery_name = grocery['name']
        try:
            # co2_score += (grocery['quantity'] / 1000) * co2_dict[grocery_name.lower()][1]
            print(grocery_name, sum([float(x) for x in cycle_dict[grocery_name]]))
            co2_score += (grocery['quantity'] / 1000) * sum([float(x) for x in cycle_dict[grocery_name]])
        except:
            success = False

    result = {"co2_score": co2_score, "success": success}

    return result


@app.route('/deleteall')
def deleteall():
    session['groceries'] = []

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)