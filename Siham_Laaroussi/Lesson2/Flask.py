
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/books")
def allbooks():
    return "all books!"
# Doesn't work

if __name__ == "__main__":
    app.run()