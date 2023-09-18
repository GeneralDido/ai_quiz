# AI-driven Knowledge Assessment App

The AI-driven Knowledge Assessment app leverages the power of artificial intelligence to generate and assess educational questions tailored to user specifications.

## Table of Contents
- [Description](#description)
- [Setup and Installation](#setup-and-installation)
- [Features](#features)
- [Automated Sessions](#automated-sessions)
- [Details](#details)

## Description

The AI-driven Knowledge Assessment app provides users with a dynamic way to generate questions based on their selected grade, CommonCoreLearningStandard (CCSS), topic, and number of questions they wish to attempt. 

You can access the app here:
https://questions.streamlit.app/

Once the questions are answered, the app evaluates the responses and offers instant feedback. The app offers automated assessments for evaluation of consistency.

As this is currently a demonstration, all interactions are saved to Airtable for future reference. 

You can access the data here:
https://airtable.com/app0kvv1O1zwFN1mb/shrIUTmCb4LDCw8Fb/tblBhCpv5BKFrvruu/viwInAygWxoddKtf8

Implementation details & Q/A here:
https://docs.google.com/document/d/1XPISIq5qPTBAw0936xqbhUSWYKa2hI_zUCgVw-UROtA/edit?usp=sharing

You can learn more about CCSS here:
https://www.thecorestandards.org/ELA-Literacy/

## Setup and Installation

#### Clone repository and Install required packages (Virtual environment recommended, Python 3.11+):
```
pip install -r requirements.txt
```

#### Set Up Environment Variables (see .env.example) and run the app:

```
streamlit run main.py
```

## Features
1. **Selection**:  The user can select the following variables: 
    - `Student Grade level`: *4th Grade up to 12th Grade* 
    - `Academic Standard Topic and Number`: *Writing, Reading: Literature, Reading: Informational Text*
    - `Interest Topic`: *Topic of choice* 
    - `Number of Questions`: *1 to 4*

2. **Question Generation**: The app dynamically generates relevant questions tailored to CCSS, Grade level and related topic.
3. **Evaluation**: After the student answers the questions, the app evaluates the responses and produces feedback and insights per question as well as a final feedback and recommendations. The grade system is from 0 to 5, as follows: 
    
    - `0: Did not answer`
    - `1: Unacceptable` 
    - `2: Needs Improvement` 
    - `3: Satisfactory` 
    - `4: Good` 
    - `5: Excellent`

4. **Feedback Loop**: Optionally, after answering, the student can provide feedback and rate the app.
5. **Automated Sessions**: You can emulate a session using AI. The emulation is used to test consistency in the app and in the answers.
6. **Data Storage**: All sessions (user and automated) are saved to Airtable for feedback/reference.

## Automated Sessions
    
  **How it works**:
  
  A random AI-student will be generated, and a topic will be chosen based on the student Grade level and CCLS. The AI-student will interact with the app and generate answers that vary in quality, capturing the full spectrum from 'Unacceptable' to 'Excellent' in the evaluation scale. 

  The student-generated AI will also generate its own predictions of how the answers will be evaluated by the tutor-AI. After the evaluator outputs the response, all grades from all answers are compared, and are checked for consistency.

  **How consistency works**: For this app, the cumulative grades are considered consistent if: 
  - `|FinalGradeA - FinalGradeB| <= 1`
  
  For individual grades:
  - `|IndividualGradeA - IndividualGradeB| <= 2`


To run the test:
```bash
python test_application.py
```
