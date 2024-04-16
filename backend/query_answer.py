from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from process_file import process_file
import os

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=1, top_p=0.9)

PROMPT_TEMPLATE = """
You are a helpful Q&A AI assistant that only generate response based on the provided video transcription.

Follow these instructions:
1. Get the video transcript from user.
2. Answer only based on that video transcription.
3. Make sure that you get your response for the user query from the transcription or generate one on your own.

TRANSCRIPTION: {transcription}

QUERY: {query}

ANSWER: """

def get_answer(query, transcription):

    prompt = (PromptTemplate.from_template(PROMPT_TEMPLATE)).format_prompt(
        query=query, transcription=transcription
    )

    try:
        return model.invoke(prompt).content
    except Exception:
        return "Something went wrong!"


def get_answer_from_query(query):
    data_folder = "data"

    # List all files in the data folder
    files = os.listdir(data_folder)

    if not files:
        return "No files found in the data folder"

    # Get the first file found
    file_path = os.path.join(data_folder, files[0])
    
    transcript = process_file(file_path)

    answer = get_answer(query=query, transcription=transcript)

    return answer