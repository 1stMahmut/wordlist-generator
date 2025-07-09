from flask import Flask , render_template , request
import os
from dotenv import load_dotenv
import requests
import json


load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('GROQ_API_key')


def api_answer(name,year,interest1):
        
        
        prompt = f"Generate a single-column list of potential password base words combining every permutation of {name}, birth year '{year}', and hobbie '{interest1}' with separators (_, -, .). Provide all possible variations without any headers or additional text"
        
        # This is the information we send to the API
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        
        # This tells the API who we are (authentication)
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Send the request to OpenRouter
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=data,
            headers=headers
        )
        
        # Get the AI's response
        result = response.json()
        ai_answer = result['choices'][0]['message']['content']

        print(ai_answer)
        
        return ai_answer

@app.route('/', methods = ['GET','POST'])
def home():
  

    user_message = None
    ai_responce = None
    name = None 
    age = None
    interest = None
  
   
    if request.method == 'POST':
        
        name = request.form.get('name')
        age = request.form.get('birthdate')
        interest = request.form.get('interest')
         
        ai_responce = api_answer(name,age,interest)
        print(f"Fake Ai responce: {ai_responce}" )
        
    return render_template('index.html',user_message = user_message,ai_responce=ai_responce)
if __name__ == '__main__':
    app.run(debug=True) 
