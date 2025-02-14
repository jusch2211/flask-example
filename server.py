from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for flash messages

# JSON-Objekt für Login
USER_CREDENTIALS = {
    "username": "admin",
    "password": "1234"
}

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

if __name__ == '__main__':
    app.run(debug=True)
