import os
import openai
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import json
import subprocess


load_dotenv()


app = Flask(__name__)

# Set API keys directly (for testing purposes only)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PAGESPEED_API_KEY = os.getenv('PAGESPEED_API_KEY')



# Load API keys from environment variables
openai.api_key = OPENAI_API_KEY.strip()

SSL_LABS_API_ENDPOINT = "https://api.ssllabs.com/api/v3/analyze"
PAGESPEED_API_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

def perform_webcompanion_tasks(prompt):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message['content'].strip()
        return response_text
    except Exception as e:
        return str(e)


def get_webcompanion_response(prompt):
    output = perform_webcompanion_tasks(prompt)
    return output

def get_performance_score(url):
    response = requests.get(f"{PAGESPEED_API_ENDPOINT}?url={url}&key={PAGESPEED_API_KEY}")
    output = json.dumps(response.json(), indent=4)
    return output

def get_security_score(url):
    response = requests.get(f"{SSL_LABS_API_ENDPOINT}?host={url}")
    output = json.dumps(response.json(), indent=4)
    return output

def get_seo_score(url):
    return "SEO checking not implemented"

def get_error_score(url, output_format="xml"):
    command = ["linkchecker", "--check-extern", f"--output={output_format}", url]
    try:
        output = subprocess.check_output(command, text=True)
        if output_format == "json":
            output_json = json.loads(output)
            formatted_output = json.dumps(output_json, indent=4)
            return formatted_output
        return output
    except subprocess.CalledProcessError as e:
        return f"Error checking failed: {e.output}"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON: {str(e)}"
    except Exception as e:
        return f"Error checking failed: {str(e)}"


# @app.route('/scan', methods=['POST'])
# def scan_website():
#     data = request.json
#     url = data.get('url')
#     task = data.get('task')

#     if not url or not task:
#         return jsonify({"error": "URL and task are required"}), 400

#     if task == "performance":
#         response = requests.get(f"{PAGESPEED_API_ENDPOINT}?url={url}&key={PAGESPEED_API_KEY}")
#         return jsonify(response.json())
#     elif task == "errors":
#         # Simulate an error check (replace with actual error checking tool if available)
#         return jsonify({"message": "Error checking not implemented"})
#     elif task == "security":
#         response = requests.get(f"{SSL_LABS_API_ENDPOINT}?host={url}")
#         return jsonify(response.json())
#     elif task == "seo":
#         # Simulate an SEO check (replace with actual SEO checking tool if available)
#         return jsonify({"message": "SEO checking not implemented"})
#     elif task == "chat":
#         prompt = f"Please scan the website at '{url}' for any performance, error, security, SEO, and accessibility issues. Provide a detailed report and remediation plan."
#         response = perform_webcompanion_tasks(prompt)
#         return jsonify({"response": response})
#     else:
#         return jsonify({"error": "Invalid task"}), 400

# @app.route('/')
# def index():
#     return send_from_directory('.', 'index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

