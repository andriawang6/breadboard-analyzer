from flask import Flask

app = Flask(__name__)

#Members API Route
@app.route("/fruit")
def members():
    return {"fruit": ["apple", "banana", "orange"]}

if __name__ == "__main__":
    app.run(debug=True)

