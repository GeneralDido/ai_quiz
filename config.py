import os
from dotenv import load_dotenv


load_dotenv()

COMMON_CORE_LEARNING_STANDARD_TOPICS = ['Writing', 'Reading: Literature', 'Reading: Informational Text']
GRADE = ['4', '5', '6', '7', '8', '9', '10', '11', '12']
COMMON_CORE_LEARNING_STANDARD_NUM = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
MAX_NUM_QUESTIONS = 4


AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY', "")
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', "")
STUDENT_TABLE = os.getenv('STUDENT_TABLE', "")
QUESTIONS_ANSWERS_TABLE = os.getenv('QUESTIONS_ANSWERS_TABLE', "")
EVALUATIONS_TABLE = os.getenv('EVALUATIONS_TABLE', "")
FEEDBACK_TABLE = os.getenv('FEEDBACK_TABLE', "")
