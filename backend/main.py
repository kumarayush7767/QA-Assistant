from flask import Flask, render_template, request, jsonify
import os
from query_answer import get_answer_from_query
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "data"

@app.route('/')
def upload_file():
    return render_template('index.html')

@app.route('/delete', methods=['DELETE'])
def delete_files():
    try:
        # Iterate over files in the data folder and delete them
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return "Files deleted successfully", 200
    except Exception as e:
        return f"Failed to delete files: {str(e)}", 500

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file:
        # Save the file to the upload directory
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        print(file.filename)
        print(file_path)

        # Check if file is saved successfully
        if os.path.exists(file_path):
            return "File uploaded successfully", 200
        else:
            return "Failed to save file", 500

@app.route('/question-answer', methods=['POST'])
def question_answer():
    # Get the question from the request data
    question_data = request.json
    question = question_data.get('question')

    # Here you would process the question, get the answer from the transcript, and return it
    # For demonstration purposes, we'll just echo back the question as the answer
    answer = get_answer_from_query(question)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)