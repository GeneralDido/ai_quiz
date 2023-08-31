import os
import json
import openai
import guidance
from dotenv import load_dotenv

gpt4 = guidance.llms.OpenAI("gpt-4")
gpt3 = guidance.llms.OpenAI("gpt-3.5-turbo")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_questions(grade: str, standard: str, topic: str, num_questions: int):
    questions = guidance('''
    {{#system~}}
    You are an expert tutor. Your task is to generate educational, free-response questions based on given parameters. You'll receive four inputs: a Common Core learning standard, a topic of interest, a student grade, and the number of questions to be created.

    Consider the Common Core learning standard as a guideline for the academic level of the questions. Use the topic of interest to make the questions engaging and relevant for students. Match the complexity of the questions to the grade level supplied. The number of questions you're asked to generate dictates the quantity of your output.

    For clarity: 
    Input: 
    1. Common Core Learning Standard: {{standard}}
    2. Topic of Interest: {{topic}}
    3. Student Grade: {{grade}}
    4. Number of Questions to Generate: {{num_questions}}}

    Output:
    A set of educational, free-response questions based on the provided learning standard and topic of interest, suitably tailored for the provided grade level. The quantity of questions should match the number given in the input.

    Your questions should not only check factual knowledge but also stimulate critical thinking and creativity. Avoid generating overly simple or yes/no questions. Instead, focus on questions that require detailed responses and demonstrate a comprehensive understanding of the topic relative to the learning standard and grade level. 

    Remember, educational impact and engagement are key. Make sure to avoid inappropriate or offensive content. Be supportive, encouraging, and accessible with your language.

    You will also generate an introduction to the questions that provides context for the student. This introduction should be a short paragraph that provides a brief overview of the topic and the questions that follow.
    Return the response in JSON format, containing the introduction ("introduction") and questions. The questions should be an array of objects, each containing a question ("question") and a question id ("id").
    {{~/system}}
    {{#assistant~}}
            {{gen 'questions' temperature=0.7 max_tokens=3000}}
    {{~/assistant}}
    ''', llm=gpt4)

    questions = questions(
        grade=grade,
        standard=standard,
        topic=topic,
        num_questions=num_questions
    )
    return json.loads(str(questions).split("<|im_start|>assistant")[1][:-15])