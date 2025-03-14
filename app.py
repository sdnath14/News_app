from flask import Flask, render_template, request
import requests
from config import NEWS_API_KEY

# Create a Flask app
app = Flask(__name__)

@app.route("/")
def index():
    query = request.args.get("query", "latest")
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    
    # Handle API errors
    if response.status_code != 200:
        return f"API Error: {response.json().get('message', 'Something went wrong')}"

    news_data = response.json()
    articles = news_data.get('articles', [])

    # Ensure safe key access and filtering
    filtered_articles = [
        article for article in articles
        if "Yahoo" not in article.get("source", {}).get("name", "")
        and 'removed' not in article.get("title", "").lower()
    ]

    return render_template("index.html", articles=filtered_articles, query=query)

if __name__ == "__main__":
    app.run(debug=True)
