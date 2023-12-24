# app.py

from flask import Flask, request, Response
import requests
import os
import json

app = Flask(__name__)

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # Get the OpenAI API key from the environment variable


@app.route('/', methods=['GET'])
def generate_response():
    # Get parameters from the GET request
    request_params = {
        "type": request.args.get('type'),
        "topic": request.args.get('topic'),
        "length": request.args.get('length'),
        "k1": request.args.get('k1'),
        "k2": request.args.get('k2'),
        "k3": request.args.get('k3'),
    }

    # Build the prompt using the parameters
    prompt = f"write a {request_params['type']} on {request_params['topic']}. Make sure its length is about {request_params['length']}. Be sure to include keywords: {request_params['k1']}, {request_params['k2']}, {request_params['k3']}. Never start the response with a lower case letter."

    # Prepare the data for the OpenAI API request
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Be an amazing writer"},
            {"role": "user", "content": prompt},
        ]
    }

    # Make the POST request to the OpenAI API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    response = requests.post(OPENAI_API_URL, json=data, headers=headers)

    # Get only the selected headers from the OpenAI API response
    selected_headers = {
        "Content-Type": response.headers.get("Content-Type"),
        "access-control-allow-origin": response.headers.get("access-control-allow-origin")
    }

    # Get the content from the OpenAI API response
    openai_content = response.json()

    # Return the selected headers and content in the Flask response
    return Response(json.dumps({'headers': selected_headers, 'content': openai_content}, sort_keys=True),
                    mimetype='application/json')


if __name__ == '__main__':
    # Run the Flask app using Gunicorn
    # Use the command: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    command = "gunicorn -b 0.0.0.0:5000 app:app"

    # Run the Gunicorn command as a subprocess
    import subprocess

    subprocess.run(command, shell=True, check=True)
