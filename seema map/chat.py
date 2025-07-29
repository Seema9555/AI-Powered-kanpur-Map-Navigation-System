import requests

GEMINI_API_KEY = 'AIzaSyD0dD7ecD17Wcrq7LWS7iPOlrhFBfQ49Fo'

def ask_gemini(prompt):
    # Use the correct model (gemini-1.5-pro) in the URL
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
    
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(f"{url}?key={GEMINI_API_KEY}", headers=headers, json=data)
    print("Response:", response.status_code, response.text)  # Print response for debugging
    
    if response.status_code == 200:
        # Correct the parsing of the response
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return reply
    else:
        return f"Error: {response.status_code} - {response.text}"

