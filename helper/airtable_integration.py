import os
from dotenv import load_dotenv
from pyairtable import Api, retry_strategy


load_dotenv()
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY', "")
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', "")
STUDENT_TABLE = os.getenv('STUDENT_TABLE', "")
QUESTIONS_ANSWERS_TABLE = os.getenv('QUESTIONS_ANSWERS_TABLE', "")
EVALUATIONS_TABLE = os.getenv('EVALUATIONS_TABLE', "")
FEEDBACK_TABLE = os.getenv('FEEDBACK_TABLE', "")

airtable_api = Api(AIRTABLE_API_KEY, retry_strategy=retry_strategy(total=2))
student_table = airtable_api.table(AIRTABLE_BASE_ID, STUDENT_TABLE)
questions_answers_table = airtable_api.table(AIRTABLE_BASE_ID, QUESTIONS_ANSWERS_TABLE)
evaluations_table = airtable_api.table(AIRTABLE_BASE_ID, EVALUATIONS_TABLE)
feedback_table = airtable_api.table(AIRTABLE_BASE_ID, FEEDBACK_TABLE)

def insert_student_record(
      sessionId: str, 
      session: str, 
      student_name: str, 
      grade: str,
      learning_standard_topic: str,
      learning_standard_num: str,
      num_questions: int,
      topic: str,
      learning_standard: str,
      learning_standard_definition: str,
      introduction: str
    ):
    student_record = {
        'SessionID': sessionId,
        'Session': session,
        'StudentName': student_name,
        'GradeLevel': grade,
        'LearningStandardTopic': learning_standard_topic,
        'LearningStandardNum': learning_standard_num,
        'NumQuestions': num_questions,
        'Topic of Interest': topic,
        'CommonCoreLearningStandard': learning_standard,
        'CommonCoreLearningStandardDefinition': learning_standard_definition,
        'QuestionsIntroduction': introduction,
  }
    student_table.create(student_record)



def insert_questions_answers_record(
      sessionId: str, 
      session: str, 
      question_id: str,
      question: str,
      answer: str,
      grade: str,
      evaluation: str,
      automated_grade: str = None
    ):
    questions_answers_record = {
        'SessionID': sessionId,
        'Session': session,
        'QuestionID': question_id,
        'Question': question,
        'Answer': answer,
        'Grade': grade,
        'Evaluation': evaluation,
        'AutomatedGrade': automated_grade
    }
    questions_answers_table.create(questions_answers_record)


def insert_evaluations_record(
      sessionId: str, 
      session: str, 
      final_grade: str,
      final_evaluation: str,
      automated_final_grade: str = None
    ):
    evaluations_record = {
        'SessionID': sessionId,
        'Session': session,
        'FinalGrade': final_grade,
        'FinalEvaluation': final_evaluation,
        'AutomatedFinalGrade': automated_final_grade
    }
    evaluations_table.create(evaluations_record)


def insert_feedback_record(
      sessionId: str, 
      rating: str,
      feedback: str
    ):
    feedback_record = {
        'SessionID': sessionId,
        'AppRating': rating,
        'UserFeedback': feedback
    }
    feedback_table.create(feedback_record)