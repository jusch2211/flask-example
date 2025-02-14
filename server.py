from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for flash messages

# JSON-Objekt für Login
USER_CREDENTIALS = {
    "username": "admin",
    "password": "1234"
}

# In-Memory-Datenbank für CRUD-Operationen
coffee_db = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            return redirect(url_for('homepage'))
        else:
            flash('Ungültige Anmeldedaten. Bitte versuchen Sie es erneut.')

    return render_template('login.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/hallo', methods=['GET', 'POST'])
def hallo():
    name = None
    if request.method == 'POST':
        name = request.form['name']
    return render_template('hallo.html', name=name)

# CRUD-Routen
@app.route('/crud/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        coffee_name = request.form['name']
        coffee_description = request.form['description']
        coffee_db.append({"name": coffee_name, "description": coffee_description})
        flash('Kaffee erfolgreich hinzugefügt!')
        return redirect(url_for('read'))
    return render_template('crud/create.html')

@app.route('/crud/read')
def read():
    return render_template('crud/read.html', coffees=coffee_db)

@app.route('/crud/update/<int:index>', methods=['GET', 'POST'])
def update(index):
    if index < 0 or index >= len(coffee_db):
        flash('Ungültiger Index!')
        return redirect(url_for('read'))

    coffee = coffee_db[index]

    if request.method == 'POST':
        coffee['name'] = request.form['name']
        coffee['description'] = request.form['description']
        flash('Kaffee erfolgreich aktualisiert!')
        return redirect(url_for('read'))

    return render_template('crud/update.html', coffee=coffee, index=index)

@app.route('/crud/delete/<int:index>', methods=['POST'])
def delete(index):
    if index < 0 or index >= len(coffee_db):
        flash('Ungültiger Index!')
    else:
        coffee_db.pop(index)
        flash('Kaffee erfolgreich gelöscht!')
    return redirect(url_for('read'))

# Kontextprozessor für Menü
### TODO: Noch nicht verwendet in allen Templates!
@app.context_processor
def inject_menu():
    menu_links = [
        {"name": "Startseite", "url": url_for('homepage')},
        {"name": "Impressum", "url": url_for('impressum')},
        {"name": "Hallo", "url": url_for('hallo')},
        {"name": "CRUD Übersicht", "url": url_for('read')}
    ]
    return {"menu_links": menu_links}


if __name__ == '__main__':
    app.run(debug=True)
