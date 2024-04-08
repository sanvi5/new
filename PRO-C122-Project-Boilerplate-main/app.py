from flask import Flask, render_template, request, jsonify
import text_sentiment_prediction
from predict_bot_response import bot_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# API listening to POST requests and predicting sentiments
@app.route('/predict', methods=['POST'])
def predict():
    response = {}
    review = request.json.get('customer_review')
    if not review:
        response = {'status': 'error',
                    'message': 'Empty Review'}
    else:
        # calling the predict method from text_sentiment_prediction.py module
        sentiment, path = text_sentiment_prediction.predict(review)
        response = {'status': 'success',
                    'message': 'Got it',
                    'sentiment': sentiment,
                    'path': path}
    return jsonify(response)

# Creating an API to save the review when the user clicks on the Save button
@app.route('/save', methods=['POST'])
def save():
    # Extracting date, product name, review, and sentiment associated from the JSON data
    date = request.json.get('date')
    product = request.json.get('product')
    review = request.json.get('review')
    sentiment = request.json.get('sentiment')

    # Creating a final variable separated by commas
    data_entry = f"{date},{product},{review},{sentiment}\n"

    # Open the file in the 'append' mode
    with open('./static/assets/datafiles/data_entry.csv', 'a') as f:
        # Log the data in the file
        f.write(data_entry)

    # Return a success message
    return jsonify({'status': 'success', 'message': 'Data Logged'})

# Writing API for chatbot
@app.route("/bot", methods=["POST"])
def bot():
    # Get user input from JSON data
    input_text = request.json.get("user_bot_input_text")

    # Call the method to get bot response
    bot_res = bot_response(input_text)

    # Prepare response JSON
    response = {"bot_response": bot_res}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
