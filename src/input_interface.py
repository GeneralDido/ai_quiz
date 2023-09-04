from config import GRADE, COMMON_CORE_LEARNING_STANDARD_TOPICS, COMMON_CORE_LEARNING_STANDARD_NUM, MAX_NUM_QUESTIONS

import streamlit as st

def get_user_input():
        st.markdown("### Customize your preferences:")
        grade = st.selectbox('Select Grade Level:', GRADE)
        standardTopic = st.selectbox('Select Common Core Learning Standard Topic:', COMMON_CORE_LEARNING_STANDARD_TOPICS)
        standardNum = st.selectbox('Select Common Core Learning Standard Number:', COMMON_CORE_LEARNING_STANDARD_NUM)
        topic = st.text_input('Enter your interest topic:', 'baseball')
        num_questions = st.number_input('Enter the number of questions to generate:', min_value=1, max_value=MAX_NUM_QUESTIONS, value=1, step=1)
        student_name = st.text_input('Enter your Username:', 'John Doe')

        return grade, standardTopic, standardNum, topic, num_questions, student_name