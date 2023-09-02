import os
import json
import random
import openai
import guidance
from dotenv import load_dotenv

from ai_generators.generate_questions import generate_questions
from ai_generators.generate_evaluations import generate_evaluations
from helper.grades_standards import academic_standards, academic_grades, academic_standards_num, max_num_questions
from helper.functions import convert_answers_to_dict, check_grades_consistency, capture_output, save_to_file, json_response


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

gpt4 = guidance.llms.OpenAI("gpt-4")


# Generates a "student" with a grade, standard, topic, and number of questions.
def generate_student(grade: str, standardTopic: str, standardNum: str, numQuestions: int):
    student = guidance('''
        {{#system~}}        
            Your task is to generate a relevant topic based on the student's Grade level and a specific Core Learning Standard, which you will also generate.
            This is the Core Learning Standard Topic: {{standardTopic}}
            This is the student Grade level: {{grade}}
            This is the Core Learning Standard number: {{standardNum}}
            You will generate {{numQuestions}} questions.
                        
            Based on the Grade, Core Learning Standard Topic, and Core Learning Standard number, you will generate a specific Core Learning Standard. 
            As an example: Grade: 4, Core Learning Standard: Writing, Core Learning Standard number: 9 should give: CCSS.ELA-LITERACY.W.4.9
            
            You will generate a topic of interest for the student, based on the Grade level of the student and the Core Learning Standard. 
            The topic of interest should be relevant to the potential student, for example, if the student is in 4th grade, the topic should be relevant to 4th graders.
            Please think of new examples to provide each time. Avoid using the given examples when creating the output. Only create unique outputs based on the selections made.                       
            Return the response only in JSON format (nothing else). 
            - - - - - - - - - - - - - - - - - - - - 
            Example JSON response:
            {
                "grade": "4",
                "standard_topic": "Writing",
                "standard_num": "9",
                "learning_standard": "CCSS.ELA-LITERACY.W.4.9",
                "topic": "Baseball",
                "num_questions": 3
            }
        {{~/system}}
        {{#assistant~}}
            {{gen 'student' temperature=0.7 max_tokens=750}}
        {{~/assistant}}
    ''', llm=gpt4)

    student = student(
        grade=grade,
        standardTopic=standardTopic,
        standardNum=standardNum,
        numQuestions=numQuestions
    )
    return json_response(student)


# Answers questions based on a student's grade, standard, topic, and number of questions. Provides potential grade for each answer and a potential final grade.
def answer_questions(questions: dict, student: dict):
    answer_questions = guidance('''
    {{#system~}}        
    Your task is to engage in academic role-play. You'll be portraying a student of a specific grade level, responding to a series of questions informed by a Common Core Learning Standard.
    Your foremost goal isn't just answering correctly, but emulating the educational level and understanding of the given Grade level. 
    The input you receive will consist of three elements: 
    1. The student's grade level: {{grade}}
    2. The related Common Core Learning Standard: {{standard}}
    3. A dictionary of questions, each with a unique ID: {{questions}}

    With this data, you are to respond to each question in a way that corresponds to the understanding level of the grade you are simulating. Ensure that your responses vary in quality, capturing the full spectrum from 'Unacceptable' to 'Excellent', reflecting grades from 0 to 5 on our evaluation scale.

    Your output, returned in a JSON format, will contain an array of objects for each question answered. Each object will include:
    1. Your answer to the question ("answer"),
    2. The corresponding question's unique ID ("id"),
    3. The grade you believe the answer would receive, based on our 0-5 scale ("grade").

    Based on the individual grades of your responses, you should include a final, cumulative grade ("finalGrade"). 
    Keep in mind that each of your answers should not exceed a length of 750 characters. 

    Avoid including any specifics from test cases in your responses. 
    Be unique and creative in your approach, ensuring a diverse range of responses that accurately reflect the varying understanding at each grade level.        
    Return the response only in JSON format (nothing else). 
    {{~/system}}
    {{#assistant~}}
            {{gen 'answer_questions' temperature=0.7 max_tokens=2000}}
    {{~/assistant}}
    ''', llm=gpt4)

    answer_questions = answer_questions(
        grade=student['grade'],
        standard=student['learning_standard'],
        questions=questions['questions']
    )
    return json_response(answer_questions)


def test():
    print('-------------------')
    print('START OF TEST')

    student = generate_student(grade=random.choice(academic_grades), standardTopic=random.choice(academic_standards), standardNum=random.choice(academic_standards_num), numQuestions=random.randint(1, max_num_questions))
    print('STUDENT: ')
    print(student)
    print('-------------------')

    questions = generate_questions(grade=student['grade'], standard=student['standard_topic'], standardNum=student['standard_num'], topic=student['topic'], num_questions=student['num_questions'])
    print('QUESTIONS: ')
    print(questions)
    print('-------------------')

    answers = answer_questions(questions=questions, student=student)
    print('ANSWER QUESTIONS: ')
    print(answers)
    print('-------------------')

    evaluations = generate_evaluations(grade=student['grade'], standard=student['learning_standard'], topic=student['topic'], questions=questions['questions'], answers=convert_answers_to_dict(answers))
    print('EVALUATIONS: ')
    print(evaluations)
    print('-------------------')

    check_grades_consistency(answers, evaluations)
    print('-------------------')
    print('END OF TEST')
    print('-------------------')


# run to test consistency and write output to txt file
output = capture_output(test)
save_to_file(output, 'test_output.txt')