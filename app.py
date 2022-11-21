from flask import Flask, request, jsonify, render_template
import wikipedia
import re
import requests
import bs4

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scrap", methods=["POST"])
def scrap():
    text = request.form.get("text")
    purpose = request.form.get("purpose")
    scrapped_data = ""
    
    if not text:
        scrapped_data += "Please enter your url or search term!"
        return jsonify({ "scrapped_data": scrapped_data })
    elif not purpose:
        scrapped_data += "Please select your purpose!"
        return jsonify({ "scrapped_data": scrapped_data })
    else:
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

        if purpose == "search_term":
                try:
                    scrapped_data += str(wikipedia.search(str(text)))
                except wikipedia.exceptions.PageError:
                    scrapped_data += f"Your search term \"{text}\" did not match any pages!"
        elif purpose == "scrap_url_data":
                url = re.match(regex, text)
                if url is None:
                    scrapped_data += "Please enter a valid url!"
                else:
                    r = requests.get(text)
                    soup = bs4.BeautifulSoup(r.content, 'html.parser')
                    scrapped_data += str(soup.prettify())
        elif purpose == "show_summary":
                try:
                    scrapped_data += str(wikipedia.summary(str(text)))
                except wikipedia.exceptions.PageError:
                    scrapped_data += f"Your search term \"{text}\" did not match any pages!"

        return jsonify({ "purpose": purpose, "text": text, "scrapped_data": scrapped_data })

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
