import random

from ai_generators.answer_questions import answer_questions
from ai_generators.generate_questions import generate_questions
from ai_generators.generate_evaluations import generate_evaluations
from ai_generators.generate_topic import generate_topic
from config import GRADE, COMMON_CORE_LEARNING_STANDARD_TOPICS, COMMON_CORE_LEARNING_STANDARD_NUM

from config import MAX_NUM_QUESTIONS
from helper.functions import convert_answers_to_dict, check_grades_consistency, generate_session_id, generate_student_name
from db.airtable_integration import insert_student_record, insert_questions_answers_record, insert_evaluations_record


def test_application():
    print('-------------------')
    print('START OF AUTOMATED TEST')

    print('-------------------')
    print('START OF AI TEST')
    grade = random.choice(GRADE)
    standardTopic = random.choice(COMMON_CORE_LEARNING_STANDARD_TOPICS)
    standardNum = random.choice(COMMON_CORE_LEARNING_STANDARD_NUM)
    numQuestions = random.randint(1, MAX_NUM_QUESTIONS)

    student = generate_topic(grade=grade, standardTopic=standardTopic, standardNum=standardNum, numQuestions=numQuestions)
    print('STUDENT: ')
    print(student)
    print('-------------------')

    questions = generate_questions(
        grade=student['grade'], 
        standard=student['standard_topic'], 
        standardNum=student['standard_num'], 
        topic=student['topic'], 
        num_questions=student['num_questions']
    )
    print('QUESTIONS: ')
    print(questions)
    print('-------------------')

    answers = answer_questions(questions=questions, student=student)
    print('ANSWER QUESTIONS: ')
    print(answers)
    print('-------------------')

    evaluations = generate_evaluations(
        grade=student['grade'], 
        standard=student['learning_standard'], 
        topic=student['topic'], 
        questions=questions['questions'], 
        answers=convert_answers_to_dict(answers)
    )
    print('EVALUATIONS: ')
    print(evaluations)
    print('-------------------')

    check_grades_consistency(answers, evaluations)
    print('-------------------')
    print('END OF AI TEST')
    print('-------------------')

    print('START OF AIRTABLE INTEGRATION')
    print('-------------------')
    session_id = generate_session_id()
    print("Inserting student record into Airtable...")
    insert_student_record(
        sessionId= session_id,
        session= 'Automated',
        student_name= generate_student_name(),
        grade= grade,
        learning_standard_topic= standardTopic,
        learning_standard_num= standardNum,
        num_questions= numQuestions,
        topic= student['topic'],
        learning_standard= student['learning_standard'],
        learning_standard_definition= student['learning_standard_definition'],
        introduction= questions['introduction']
    )
    print("Successfully inserted student record into Airtable.")
    print('-------------------')

    for question in questions['questions']:
        print(f"Inserting question/answer record with id: {question['id']} into Airtable...")
        insert_questions_answers_record(
            sessionId= session_id,
            session= 'Automated',
            question_id= question['id'],
            question= question['question'],
            answer= answers[int(question['id'])-1]['answer'],
            grade= evaluations['evaluations'][int(question['id'])-1]['grade'],
            evaluation= evaluations['evaluations'][int(question['id'])-1]['explanation'],
            automated_grade= answers[int(question['id'])-1]['grade']
        )
        print(f"Successfully inserted question/answer record with id {question['id']} into Airtable.")
        print('-------------------')

    print("Inserting evaluations record into Airtable...")
    insert_evaluations_record(
        sessionId= session_id,
        session= 'Automated',
        final_grade= evaluations['finalGrade'],
        final_evaluation= evaluations['finalFeedback'],
        automated_final_grade= answers[-1]['finalGrade']
    )
    print("Successfully inserted evaluations record into Airtable.")
    print('-------------------')
    print('END OF AIRTABLE INTEGRATION')
    print('-------------------')
    print('END OF AUTOMATED TEST')
    print('-------------------')

# run to test application
test_application()