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
        For each question, you should evaluate the student's response based on the student's Grade level (i.e., the explanation for a 4th-grade student should differ from that of a 12th-grade student), relevance to the topic, and the quality of the answer. 
        The quality of the answer should be rated on a scale from 1 to 5, with 1: Unacceptable, 2: Needs Improvement, 3: Satisfactory, 4: Good and 5: Excellent. Rate the answer based on multiple factors, including the student's Grade level, understanding of the topic and the question, the depth and quality of response for the Grade level.
        In addition to the evaluation, you should provide an explanation for your evaluation that is relevant to the student's grade level and response. Use appropriate languge based on the Grade level. Your explanation should be respectful, helpful, insightful, and suggest possible improvements.
        Finally, you should calculate a total grade for the student based on all their responses and provide final feedback.
        Your output should be in JSON format and include the evaluation for each question ("evaluation", with the question id: "id"), your explanation for each evaluation ("explanation), the final grade ("finalGrade", it should be an integer), and final feedback ("finalFeedback").
        Remember, your goal is to provide a supportive and constructive learning experience for the student, not just merely grade responses. Be respectful, insightful, creative, and thorough.
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
