import os
import json
import openai
import guidance
from dotenv import load_dotenv

gpt4 = guidance.llms.OpenAI("gpt-4")

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

    Your questions should be appropriate for the age level / Grade level of the student. For example, if the student is in the 4th Grade, you should make questions specifically designed for 4th graders. 
    If the question is for higher Grade levels, for example for 12th grade, you should also check factual knowledge and stimulate critical thinking and creativity (based on the Grade level). Generally, avoid generating extremely simple or yes/no questions. Focus on questions that demonstrate an understanding of the topic relative to the learning standard and to the grade level of the student. 
    Also, please make sure the questions are designed in a way that can be answered optimally from the student in maximum 750 characters or less.

    Remember, educational impact and engagement are key. Make sure to avoid inappropriate or offensive content. Be supportive, encouraging, and accessible with your language.

    You will also generate an introduction to the questions that provides context for the student. This introduction should be short and should provide a brief overview of the topic and the questions that follow. Make sure it is written in a language appropriate for the Grade level of the student. Example: If the student is in 4th grade, the introduction should be written for 4th graders.
    Return the response only in JSON format (nothing else), containing the introduction ("introduction"), and questions. The questions should be an array of objects, each containing a question ("question") and a question id ("id").
    {{~/system}}
    {{#assistant~}}
            {{gen 'questions' temperature=0.7 max_tokens=2200}}
    {{~/assistant}}
    ''', llm=gpt4)

    questions = questions(
        grade=grade,
        standard=standard,
        topic=topic,
        num_questions=num_questions
    )
    print(questions)
    return json.loads(str(questions).split("<|im_start|>assistant")[1][:-15])