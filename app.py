import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# In-memory storage for freelancers and requests
freelancers = []
requests_list = []

# Mock TNID verification function
def verify_tnid(tnid):
    # Simulate an API call to verify TNID
    # Replace this with the actual API call
    # response = requests.get(f'http://tnid-verification-api.com/verify/{tnid}')
    # return response.json().get('is_valid', False)
    
    # For demonstration, let's assume all TNIDs ending with '1' are valid
    return tnid.endswith('1')

@app.route('/')
def index():
    return render_template('index.html', freelancers=freelancers)

@app.route('/request_freelancer', methods=['GET', 'POST'])
def request_freelancer():
    if request.method == 'POST':
        req = request.form.get('request')
        requests_list.append(req)
        return redirect(url_for('index'))
    return render_template('request_freelancer.html')

@app.route('/add_freelancer', methods=['GET', 'POST'])
def add_freelancer():
    if request.method == 'POST':
        name = request.form.get('name')
        skills = request.form.get('skills')
        tnid = request.form.get('tnid')

        if verify_tnid(tnid):
            freelancers.append({'name': name, 'skills': skills, 'tnid': tnid})
            flash('Freelancer registered successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid TNID. Please try again.', 'error')

    return render_template('request_freelancer.html')

@app.route('/freelancers')
def freelancers_page():
    return render_template('freelancers.html', freelancers=freelancers)

if __name__ == '__main__':
    app.run(debug=True)



