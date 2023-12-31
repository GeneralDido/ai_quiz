import random

from ai.testing.ResponseGenerator import ResponseGenerator
from ai.user.QuestionGenerator import QuestionGenerator
from ai.user.Evaluator import Evaluator
from ai.testing.TopicGenerator import TopicGenerator
from config import GRADE, COMMON_CORE_LEARNING_STANDARD_TOPICS, COMMON_CORE_LEARNING_STANDARD_NUM

from config import MAX_NUM_QUESTIONS
from db.AirtableManager import AirtableManager
from helper.functions import convert_answers_to_dict, check_grades_consistency, generate_session_id, generate_student_name


def test_application():
    print('-------------------')
    print('START OF AUTOMATED TEST')

    print('-------------------')
    print('START OF AI TEST')
    grade = random.choice(GRADE)
    standardTopic = random.choice(COMMON_CORE_LEARNING_STANDARD_TOPICS)
    standardNum = random.choice(COMMON_CORE_LEARNING_STANDARD_NUM)
    numQuestions = random.randint(1, MAX_NUM_QUESTIONS)
    session_id = generate_session_id()
    student_name= generate_student_name()

    student = TopicGenerator(grade=grade, standardTopic=standardTopic, standardNum=standardNum, numQuestions=numQuestions).generate_topic()
    student['student_name'] = student_name

    print('STUDENT: ')
    print(student)
    print('-------------------')

    questions = QuestionGenerator(
        grade=student['grade'], 
        standard=student['standard_topic'], 
        standardNum=student['standard_num'], 
        topic=student['topic'], 
        num_questions=student['num_questions']
    ).generate_questions()
    print('QUESTIONS: ')
    print(questions)
    print('-------------------')

    answers = ResponseGenerator(questions=questions, student=student).answer_questions()
    print('ANSWER QUESTIONS: ')
    print(answers)
    print('-------------------')

    evaluations = Evaluator(
        grade=student['grade'], 
        standard=student['learning_standard'], 
        topic=student['topic'], 
        questions=questions['questions'], 
        answers=convert_answers_to_dict(answers)
    ).generate_evaluations()
    print('EVALUATIONS: ')
    print(evaluations)
    print('-------------------')

    check_grades_consistency(answers, evaluations)
    print('-------------------')
    print('END OF AI TEST')
    print('-------------------')

    print('START OF AIRTABLE INTEGRATION')
    print('-------------------')


    airtable_manager = AirtableManager(
        sessionId= session_id,
        session= 'Automated',
        student= student,
        questions= questions,
        answers= answers,
        evaluations= evaluations
    )
    
    print("Inserting student record into Airtable...")
    airtable_manager.insert_student_record()
    print("Successfully inserted student record into Airtable.")
    print('-------------------')

    for question in questions['questions']:
        print(f"Inserting question/answer record with id: {question['id']} into Airtable...")
        airtable_manager.insert_questions_answers_record(question_id= question['id'])
        print(f"Successfully inserted question/answer record with id {question['id']} into Airtable.")
        print('-------------------')
    
    print("Inserting evaluations record into Airtable...")
    airtable_manager.insert_evaluations_record()
    
    print("Successfully inserted evaluations record into Airtable.")
    print('-------------------')
    print('END OF AIRTABLE INTEGRATION')
    print('-------------------')
    print('END OF AUTOMATED TEST')
    print('-------------------')

# run to test application
test_application()
