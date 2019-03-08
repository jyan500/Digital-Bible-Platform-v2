if __name__ == "__main__":
	from config import app
	app.run(debug=True, host='0.0.0.0', port=5000)
	# app.run(ssl_context='adhoc')
	# app.run(ssl_context=('cert.pem', 'key.pem'), port=5000, debug=True)