from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World! <h1>Hello<h1>"

@app.route('/<string:name>')
def user(name: str):
    return f"Hello {name}!"

@app.route('/admin')
def admin():
    return redirect(url_for('home', name='Admin!'))

if __name__ == '__main__':
    app.run()
