import requests

# Test data for requirements submission
test_data = {
    'csrfmiddlewaretoken': '',  # Will be filled from the form
    'name': 'Test User',
    'email': 'test@example.com',
    'contact_number': '9876543210',
    'location': 'Kolkata',
    'budget_range': '50l_1cr',
    'property_type': 'residential',
    'requirement_type': 'buy',
    'area_needed': '1200 sq ft',
    'specific_requirements': 'Need 2-3 BHK apartment with parking',
    'agreed_to_terms': 'on'
}

# First get the requirements page to extract CSRF token
response = requests.get('http://127.0.0.1:8000/requirements/')
if response.status_code == 200:
    print("Requirements page loaded successfully")
    # Extract CSRF token from the response (simple approach)
    csrf_start = response.text.find('csrfmiddlewaretoken')
    if csrf_start != -1:
        csrf_value_start = response.text.find('value="', csrf_start) + 7
        csrf_value_end = response.text.find('"', csrf_value_start)
        csrf_token = response.text[csrf_value_start:csrf_value_end]
        test_data['csrfmiddlewaretoken'] = csrf_token
        print(f"CSRF token extracted: {csrf_token[:20]}...")
        
        # Now submit the form
        submit_response = requests.post('http://127.0.0.1:8000/theme/requirements_submission/', data=test_data)
        print(f"Form submission status: {submit_response.status_code}")
        print(f"Response URL: {submit_response.url}")
        
        if submit_response.status_code == 200:
            print("Form submitted successfully!")
        else:
            print(f"Form submission failed with status: {submit_response.status_code}")
    else:
        print("CSRF token not found")
else:
    print(f"Failed to load requirements page: {response.status_code}")