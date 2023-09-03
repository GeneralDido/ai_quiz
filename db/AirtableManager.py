from dataclasses import dataclass
from pyairtable import Api, retry_strategy

from config import AIRTABLE_API_KEY
from config import AIRTABLE_BASE_ID
from config import STUDENT_TABLE
from config import QUESTIONS_ANSWERS_TABLE
from config import EVALUATIONS_TABLE
from config import FEEDBACK_TABLE

airtable_api = Api(AIRTABLE_API_KEY, retry_strategy=retry_strategy(total=2))
student_table = airtable_api.table(AIRTABLE_BASE_ID, STUDENT_TABLE)
questions_answers_table = airtable_api.table(AIRTABLE_BASE_ID, QUESTIONS_ANSWERS_TABLE)
evaluations_table = airtable_api.table(AIRTABLE_BASE_ID, EVALUATIONS_TABLE)
feedback_table = airtable_api.table(AIRTABLE_BASE_ID, FEEDBACK_TABLE)


@dataclass
class AirtableManager:
    sessionId: str
    session: str
    student: dict
    questions: dict
    answers: list[dict] or dict
    evaluations: dict


    def insert_student_record(self):
        student_record = {
            'SessionID': self.sessionId,
            'Session': self.session,
            'StudentName': self.student['student_name'],
            'GradeLevel': self.student['grade'],
            'LearningStandardTopic': self.student['standard_topic'],
            'LearningStandardNum': self.student['standard_num'],
            'NumQuestions': self.student['num_questions'],
            'Topic of Interest': self.student['topic'],
            'CommonCoreLearningStandard': self.questions['learning_standard'].split(':')[0],
            'CommonCoreLearningStandardDefinition': self.questions['learning_standard'].split(':')[1],
            'QuestionsIntroduction': self.questions['introduction'],
    }
        student_table.create(student_record)


    def insert_questions_answers_record(self, question_id: int):
        questions_answers_record = {
            'SessionID': self.sessionId,
            'Session': self.session,
            'QuestionID': question_id,
            'Question': self.questions['questions'][question_id-1]['question'],
            'Answer': self.answers[question_id] if self.session == 'User' else self.answers[question_id-1]['answer'],
            'Grade': self.evaluations['evaluations'][question_id-1]['grade'],
            'Evaluation': self.evaluations['evaluations'][question_id-1]['explanation'],
            'AutomatedGrade': self.answers[question_id-1]['grade'] if self.session == 'Automated' else None
        }
        questions_answers_table.create(questions_answers_record)


    def insert_evaluations_record(self):
        evaluations_record = {
            'SessionID': self.sessionId,
            'Session': self.session,
            'FinalGrade': self.evaluations['finalGrade'],
            'FinalEvaluation': self.evaluations['finalFeedback'],
            'AutomatedFinalGrade': self.answers[-1]['finalGrade'] if self.session == 'Automated' else None
        }
        evaluations_table.create(evaluations_record)


# This function is called once and it is separate from the others, so we can use it outside of the class
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