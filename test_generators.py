import os
import json
import openai
import guidance
from dotenv import load_dotenv

from ai_generators.generate_questions import generate_questions
from ai_generators.generate_evaluations import generate_evaluations
from helper.grades_standards import academic_standards, academic_grades, max_num_questions

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

gpt4 = guidance.llms.OpenAI("gpt-4")


# Generates a "student" with a grade, standard, topic, and number of questions.
def generate_student():
    student = guidance('''
        {{#system~}}        
        Your task is to generate a relevant topic based on the student's Grade level and Core Learning Standard.
        This ia a list of the academic_standards, randomly choose one: {{academic_standards}}}
        This is a list of academic_grades, randomly choose one: {{academic_grades}}
        Please choose appropriate number of questions for the topic, ranging from 1 to a maximum of {{max_num_questions}}.
        Finally, based on the student's Grade level and Core Learning Standard, you will generate a topic of interest. 
        The topic of interest should be relevant to both the Core Learning Standard and the Grade level, for example, if the student is in 4th grade and Core Learning Standard is Reading: Literature, the topic should be relevant to 4th graders and should be relevant to Reading: Literature.
        Please think of new examples to provide each time. Avoid using the given examples when creating the output. Only create unique outputs based on the selections made.                       
        Return the response only in JSON format (nothing else). 
        - - - - - - - - - - - - - - - - - - - - 
        Example JSON response:
        {
          "grade": "4",
          "standard": "Writing",
          "topic": "Baseball",
          "num_questions": 3
        }
        {{~/system}}
        {{#assistant~}}
              {{gen 'generate_student' temperature=0.7 max_tokens=750}}
        {{~/assistant}}
    ''', llm=gpt4)

    student = student(
        academic_standards=academic_standards,
        academic_grades=academic_grades,
        max_num_questions=max_num_questions
    )
    return json.loads(str(student).split("<|im_start|>assistant")[1][:-15])


# Answers questions based on a student's grade, standard, topic, and number of questions. Provides potential grade for each answer and a potential final grade.
def answer_questions(questions: dict, student: dict):
    answer_questions = guidance('''
    {{#system~}}        
    Your task is to engage in academic role-play. You'll be portraying a student of a specific grade level, responding to a series of questions informed by a Core Learning Standard.
    Your foremost goal isn't just answering correctly, but emulating the educational level and understanding of the given Grade level. 
    The input you receive will consist of three elements: 
    1. The student's grade level: {{grade}}
    2. The related Core Learning Standard: {{standard}}
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
        standard=student['standard'],
        questions=questions['questions']
    )
    return json.loads(str(answer_questions).split("<|im_start|>assistant")[1][:-15])


# Converts a list of answers to a dictionary with question IDs as keys and answers as values. 
def convert_answers_to_dict(answers: list) -> dict:
    answers_for_evaluation = {}
    for answer in answers:
        if "id" in answer:
            answers_for_evaluation[answer["id"]] = answer["answer"]
    return answers_for_evaluation


# Evaluates the consistency of the grades between the answers and evaluations. Prints warnings if individaul question grades are inconsistent.
def check_grades_consistency(answers, evaluations):
    # Get the final grades from both evaluations
    a1_final_grade = answers[-1]["finalGrade"]
    a2_final_grade = evaluations["finalGrade"]

    # Check if the final grades are consistent
    if abs(a1_final_grade - a2_final_grade) > 1:
        print("Final grades are not consistent.")
        return False

    # Get the grades for each question from both evaluations
    a1_grades = {answer["id"]: answer["grade"] for answer in answers if "id" in answer}
    a2_grades = {evaluation["id"]: evaluation["grade"] for evaluation in evaluations["evaluations"]}

    # Check if the grades for each question are consistent
    inconsistent_grades = []
    for question_id in a1_grades:
        if question_id not in a2_grades:
            print(f"Question {question_id} not found in A2 evaluations.")
            return False
        if abs(a1_grades[question_id] - a2_grades[question_id]) > 2:
            inconsistent_grades.append((question_id, a1_grades[question_id], a2_grades[question_id]))

    # Print a warning if there is inconsistency in the individual question grades
    if inconsistent_grades:
        print("Warning: Inconsistent grades for the following questions:")
        for question_id, a1_grade, a2_grade in inconsistent_grades:
            print(f"Question {question_id}: A1 grade = {a1_grade}, A2 grade = {a2_grade}")
            for answer in answers:
                if answer.get("id") == question_id:
                    print(f"A1 answer: {answer.get('answer')}")
                    break

    # Check if there are any questions in A2 evaluations that are not in A1 answers
    for question_id in a2_grades:
        if question_id not in a1_grades:
            print(f"Question {question_id} not found in A1 answers.")
            return False

    # If all checks pass, the grades are consistent
    print("Grades are consistent.")
    return True


def test():
    print('-------------------')
    print('START OF TEST')

    student = generate_student()
    print('STUDENT: ')
    print(student)
    print('-------------------')

    questions = generate_questions(grade=student['grade'], standard=student['standard'], topic=student['topic'], num_questions=student['num_questions'])
    print('QUESTIONS: ')
    print(questions)
    print('-------------------')

    answers = answer_questions(questions=questions, student=student)
    print('ANSWER QUESTIONS: ')
    print(answers)
    print('-------------------')

    evaluations = generate_evaluations(grade=student['grade'], standard=student['standard'], topic=student['topic'], questions=questions['questions'], answers=convert_answers_to_dict(answers))
    print('EVALUATIONS: ')
    print(evaluations)
    print('-------------------')

    check_grades_consistency(answers, evaluations)
    print('-------------------')
    print('END OF TEST')


# uncomment test function and run file to test consistency
# test()