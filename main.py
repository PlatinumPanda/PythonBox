from flask import Flask, render_template, request, jsonify
import getter

app = Flask(__name__)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/query', methods=['GET'])
def result():
	keywords = str(request.args['keyword'])
	result = getter.parse_ebay_json(getter.get_from_ebay(keywords))
	return jsonify(**result)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404