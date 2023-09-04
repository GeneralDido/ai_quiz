import re
import streamlit as st
import json
import secrets
from faker import Faker


# Converts answers to a dictionary with question IDs as keys and answers as values. 
def convert_answers_to_dict(answers: dict) -> dict:
    answers_for_evaluation = {}
    for answer in answers.get("answers", []):
        if "id" in answer:
            answers_for_evaluation[answer["id"]] = answer["answer"]
    return answers_for_evaluation


def check_final_grades_consistency(a1_final_grade, a2_final_grade, tolerance=1):
    return abs(a1_final_grade - a2_final_grade) <= tolerance


def check_individual_grades_consistency(answers, evaluations, tolerance=2):
    inconsistent_grades = []
    answers_map = {answer["id"]: answer["answer"] for answer in answers}
    a1_grades = {answer["id"]: answer["grade"] for answer in answers}
    a2_grades = {evaluation["id"]: evaluation["grade"] for evaluation in evaluations}
    
    for question_id, a1_grade in a1_grades.items():
        a2_grade = a2_grades.get(question_id)
        if a2_grade is None:
            print(f"Question {question_id} not found in A2 evaluations.")
            return False
        if abs(a1_grade - a2_grade) > tolerance:
            inconsistent_grades.append((question_id, a1_grade, a2_grade, answers_map[question_id]))
            
    if inconsistent_grades:
        print("Warning: Inconsistent grades for the following questions:")
        for question_id, a1_grade, a2_grade, answer_text in inconsistent_grades:
            print(f"Question {question_id}: A1 grade = {a1_grade}, A2 grade = {a2_grade}")
            print(f"A1 answer: {answer_text}")
    
    return not bool(inconsistent_grades)


# Checks if the grades are consistent between the two applications, tolerance is the absolute difference between two grades.
def check_grades_consistency(answers, evaluations, final_grade_tolerance=1, individual_grade_tolerance=2):
    if not check_final_grades_consistency(answers["finalGrade"], evaluations["finalGrade"], final_grade_tolerance):
        print("Final grades are not consistent.")
        return False
    
    if not check_individual_grades_consistency(answers["answers"], evaluations["evaluations"], individual_grade_tolerance):
        return False
    
    print("Grades are consistent.")
    return True


# Generates a JSON response from the output of the AI.
def json_response(response: str):
    # Extracting content after the "assistant" keyword
    assistant_part = str(response).split("<|im_start|>assistant")[1]
    # Using regex to match the entire JSON structure (from the first '{' to the last '}')
    match = re.search(r'\{.*\}', assistant_part, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    else:
        raise ValueError("No valid JSON found in the response")


# Disable buttons after click
def disable_generate_btn(button):
    st.session_state["disabled_generate"] = True
def disable_submit_btn(button):
    st.session_state["disabled_submit"] = True
def disable_feedback_btn(button):
    st.session_state["disabled_feedback"] = True


# Generates a random session ID/key.
def generate_session_id(length=16):
    return secrets.token_hex(length)


# Generates a random student name.
def generate_student_name():
    fake = Faker()
    return fake.name()
