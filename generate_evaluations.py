import os
import json
import openai
import guidance
from dotenv import load_dotenv

gpt4 = guidance.llms.OpenAI("gpt-4")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_evaluations(grade: str, standard: str, topic: str, questions: list, answers: dict):
    evaluations = guidance('''
        {{#system~}}
        As an AI tutor, your task is to evaluate students' responses to open-ended questions based on a given topic, grade level, and Common Core learning standard. 
        Input: a Common Core learning standard: {{standard}}, a topic of interest: {{topic}}, a Student Grade: {{grade}}, a list of questions: {{questions}} and a dictionary with the students' answers to each of those questions: {{answers}}.
        For each question, you should evaluate the student's response based on the student's Grade level (i.e., the explanation for a 4th-grade student should differ from that of a 12th-grade student), relevance to the topic, and the quality of the answer. The grade should be appropriate for the Grade level of the student, for example if the student is in 4th grade, you should grade the answer as if it was written by a 4th grader.
        The quality of the answer should be rated on a scale from 1 to 5, with 1: Unacceptable, 2: Needs Improvement, 3: Satisfactory, 4: Good and 5: Excellent. Rate the answer based on multiple factors, including the student's Grade level, understanding of the topic and the question, the depth and quality of response for the Grade level.
        In addition to the evaluation, you should provide an explanation for your evaluation that is relevant to the student's grade level and response. Use appropriate languge based on the Grade level. Your explanation should be respectful, helpful, insightful, and suggest possible improvements.
        Finally, you should calculate a total grade for the student based on all their responses and provide final feedback.
        If the user has not responded at all to the particular question or has responded randomly, please address it in a nice, instructive way. Remember, your goal is to provide a supportive and constructive learning experience for the student, not just merely grade responses. Be respectful, insightful, creative, and thorough.
        
        Example output JSON:
        {"evaluations":[
            0:{
                "id":1
                "grade":5
                "explanation":"<explanation>"
            }
            1:{ ... }
            2:{ ... }
        ]
        "finalGrade":4
        "finalFeedback":"Overall, you've done a good job on this assignment. You demonstrated a strong understanding of Steve Jobs' personality, leadership style, and work ethic, as well as his influence on technology. However, there's still room for improvement. Make sure to answer all parts of the question and don't hesitate to ask questions, even if you're not sure about them. Keep up the good work and continue to strive for excellence. You're on the right path to becoming a better reader and thinker!"
        }
        {{~/system}}
        {{#assistant~}}
            {{gen 'evaluations' temperature=0.7 max_tokens=3000}}
        {{~/assistant}}
    ''', llm=gpt4)

    evaluations = evaluations(
        grade=grade,
        standard=standard,
        topic=topic,
        questions=questions,
        answers=answers
    )
    return json.loads(str(evaluations).split("<|im_start|>assistant")[1][:-15])
