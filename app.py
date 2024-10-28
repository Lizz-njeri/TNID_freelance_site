import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

freelancers = []

# Your API key
api_key = '' 

# Function to verify TNID
def verify_tnid(freelancer_data):
    url = 'https://api.tnid.com/verify' 
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=freelancer_data)

        if response.status_code == 200:
            data = response.json()
            if data.get('verified'):
                print('Freelancer is verified')
                return True
            else:
                print('Verification failed:', data.get('reason'))
                return False
        else:
            print('Error:', response.status_code, response.text)
            return False
    except requests.exceptions.RequestException as e:
        print('Request failed:', e)
        return False

@app.route('/')
def index():
    return render_template('index.html', freelancers=freelancers)

@app.route('/add_freelancer', methods=['POST'])
def add_freelancer():
    name = request.form.get('name')
    skills = request.form.get('skills')
    tnid = request.form.get('tnid')
    
    freelancer_data = {
        'name': name,
        'tnid': tnid,
        # Add other necessary fields for verification here
    }

    if verify_tnid(freelancer_data):
        freelancers.append({'name': name, 'skills': skills})
        flash('Freelancer registered successfully!', 'success')
    else:
        flash('Invalid TNID. Please try again.', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
