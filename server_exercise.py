import logging
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import worker  # Import the worker module

# Initialize Flask app and CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.logger.setLevel(logging.ERROR)

# Define the route for the index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # Render the index.html template

# Define the route for processing messages
@app.route('/process-message', methods=['POST'])
def process_message_route():
    
    # TODO: Extract the user's message from the request
    # TODO: Process the user's message using the worker module
    # TODO: Return the bot's response as JSON

    user_message = request.json['userMessage']  # Extract the user's message from the request
    print('user_message', user_message)
    bot_response = worker.process_prompt(user_message)  # Process the user's message using the worker module
    # Return the bot's response as JSON
    return jsonify({
        "botResponse": bot_response
    }), 200


    
# Define the route for processing documents
@app.route('/process-document', methods=['POST'])
def process_document_route():
    # TODO: Check if a file was uploaded  --> use if 'file' not in request file then return jsofify message and error code 400
    # TODO: Save the uploaded file --> extracte the file with request 
    # TODO: Process the saved file --> create proper file_path for saving
    # TODO: Send a response indicating that the document is ready for queries --> retrun jsonify message with code 200

    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({
            "botResponse": "It seems like the file was not uploaded correctly, can you try "
                           "again. If the problem persists, try using a different file"
        })
    file = request.files['file']  # Extract the uploaded file from the request
    file_path = 'documents/' + file.filename  # Define the path where the file will be saved
    file.save(file_path)  # Save the file
    worker.process_document(file_path)  # Process the document using the worker module
    # Return a success message as JSON
    return jsonify({
        "botResponse": "Thank you for providing your PDF document. I have analyzed it, so now you can ask me any "
                       "questions regarding it!"
    })

# Run the Flask app (later you need to add "python main block" ==> if __name__ == "__main__":
app.run(debug=True, port=8000, host='0.0.0.0')