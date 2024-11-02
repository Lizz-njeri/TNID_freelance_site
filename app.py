import requests
from flask import Flask, render_template, request, redirect, url_for, flash
import aiohttp
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
app = Flask(__name__)

# app.secret_key = 'b21wYW55X2lkIjoiM2EwNWQzYWEtZj'  
 
freelancers = []
api_key =''

def search_people(bearer_token, freelancer_data, query_name = None, email = None, phone_number = None):
    transport = AIOHTTPTransport(
        url="https://api.staging.v2.tnid.com/company",
        headers=
        {
            "Authorization": f"Bearer {bearer_token}"
        }
    )

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql(
        """
       query (
        	$name: String
        	$email: String
        	$telephoneNumber: String
        	
          ) {
        	users (
          	name: $name
          	email: $email
          	telephoneNumber: $telephoneNumber
        	) {
          	id
          	firstName
          	lastName
          	middleName
          	username
	}
  }

        """
    )

    params = { "name": query_name,  "email": email, "telephoneNumber": phone_number }

    try:
        response = client.execute(query, params)
        # print(f"Response OK when searching people: {response}")
        return response.get('users', [])
    except Exception as e:
        print(f"Exception when searching people: {e}")
        return []




def verify_tnid(freelancer_data):
    # This function will implement your verification logic.
    search_results = search_people(api_key, freelancer_data)

   
    if search_results:
        for user in search_results:
        # Check if the returned user's name and email match the freelancer's data
            if ((user['firstName'] == freelancer_data.get('firstName') or
                user['lastName'] == freelancer_data.get('lastName')) or
                (user.get('email') == freelancer_data.get('Email'))):
                return True  # Verification successful
    
        return False  # No matches found after checking all users

@app.route('/')
def index():
    return render_template('index.html', freelancers=freelancers)

@app.route('/add_freelancer', methods=['POST'])
def add_freelancer():
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    skills = request.form.get('skills')
    email = request.form.get('email')
    phone = request.form.get('TelephoneNumber')

    freelancer_data = {
        'firstName': firstName,
        'lastName': lastName,
        'Email': email,
        'phone': phone
    }
    

    is_verified = verify_tnid(freelancer_data)

    if is_verified:
        freelancers.append({'firstName': firstName, 'lastName':lastName, 'skills': skills})
        return redirect(url_for('index', message='Freelancer registered successfully!', category='success'))
    else:
        return redirect(url_for('index', message='Unverified User. Kindly try again. Please try again.', category='error'))

    

if __name__ == '__main__':
    app.run(debug=True)
