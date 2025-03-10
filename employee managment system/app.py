from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Global variables to store the username and password
current_username = 'admin'
current_password = '1221'

@app.route('/', methods=['GET', 'POST'])
def login():
    global current_username, current_password
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            flash('All fields are required', 'error')
        elif username == current_username and password == current_password:
            flash('Login is successful', 'success')
            return redirect(url_for('success'))  # Redirect to a success page
        else:
            flash('Wrong credentials', 'error')
    return render_template('index.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    global current_username, current_password
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        if new_username == '' or new_password == '':
            flash('All fields are required', 'error')
        elif new_username == current_username or new_password == current_password:
            flash('New username or password must be different from old ones', 'error')
        else:
            current_username = new_username
            current_password = new_password
            flash('New user created successfully', 'success')
            return redirect(url_for('login'))  # Redirect back to login
    return render_template('create_user.html')

@app.route('/success')
def success():
    return "Welcome to the Employee Management System!"

if __name__ == '__main__':
    app.run(debug=True)