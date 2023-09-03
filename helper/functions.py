import streamlit as st
import json
import secrets
from faker import Faker


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


# Saves a string to a file.
def save_to_file(string, file_path):
    with open(file_path, 'w') as f:
        f.write(string)


# Generates a JSON response from the output of the AI.
def json_response(response: str):
    return json.loads(str(response).split("<|im_start|>assistant")[1][:-15])


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