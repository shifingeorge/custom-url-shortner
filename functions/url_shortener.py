from flask import Flask, request, jsonify
import string
import random

app = Flask(__name__)

url_mapping = {}

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['original_url']
        custom_code = request.form.get('custom_code')

        short_code = custom_code if custom_code else generate_short_code()

        # Check if the custom code is already used
        if short_code in url_mapping:
            return jsonify({'error': 'Short code already in use. Try another one.'}), 400

        url_mapping[short_code] = original_url
        return jsonify({'shortened_url': f'shifiyy.link/{short_code}'}), 200

    return '''
        <form method="POST">
            <input type="text" name="original_url" placeholder="Enter the original URL" required>
            <input type="text" name="custom_code" placeholder="Enter custom short code (optional)">
            <button type="submit">Shorten URL</button>
        </form>
    '''

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in url_mapping:
        return redirect(url_mapping[short_code])
    else:
        return jsonify({'error': 'URL not found'}), 404

def handler(event, context):
    return app(event, context)