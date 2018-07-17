from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
	return "Index!"

@app.route("/members")
def members():
	return "Members"

@app.route("/members/<string:name>/")
def getMember(name):
	return "Hello " + name

if __name__ == "__main__":
	app.run()
