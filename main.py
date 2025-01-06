from flask import Flask, jsonify, render_template
import subprocess
from dendrite_sdk import Dendrite

app = Flask(__name__)
# CORS(app)  # Enable CORS for your React app

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/auth', methods=['GET'])
def run_dendrite_auth():
    try:
        process = subprocess.Popen(
            ["dendrite", "auth", "--url", "facebook.com"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        # Initialize Dendrite with the saved Instagram session
        browser = Dendrite(auth=["facebook.com", "instagram.com", "tiktok.com", "youtube.com", "linkedin.com"], dendrite_api_key="sk_d6aacf77ee8acba13ce14c8da02e1c7f22e7c9b83451ffb80ed7b2a9b5f97028", playwright_options={ "headless": True})
        
        # Navigate to Instagram
        browser.goto(
            "https://linkedin.com/",
            expected_page="You should see a personalized feed"
        )
        
        # Get description of first post
        desc = browser.ask("What's the latest post?")
        print(desc)
        
        # Clean up
        browser.close()
        
        return jsonify({
            "success": True,
            "description": desc,
            # "stdout": stdout
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(port=5000)
