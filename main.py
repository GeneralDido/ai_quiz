import streamlit as st
import matplotlib.pyplot as plt

from streamlit_star_rating import st_star_rating
from ai_generators.generate_questions import generate_questions
from ai_generators.generate_evaluations import generate_evaluations
from db.airtable_integration import insert_evaluations_record, insert_feedback_record, insert_questions_answers_record, insert_student_record
from helper.functions import disable_feedback_btn, disable_generate_btn, disable_submit_btn
from src.app_state import initialize_session_state
from src.bar_chart import visualise_bar_chart
from src.input_interface import get_user_input

def main():
    
    # Set page title and description
    st.set_page_config(page_title="AI-driven Knowledge Assessment", page_icon=":books:", layout="centered", initial_sidebar_state="expanded")
    st.title("AI-driven Knowledge Assessment")
    st.write("This app generates a set of knowledge assessment questions based on the user's input. The questions are generated using AI and are designed to test the user's understanding of a particular topic. The user can select the grade level, academic standard, topic, and number of questions they want to generate. Once the questions are generated, the user can answer them one by one and receive immediate feedback. This app is useful for educators, students, and anyone who wants to test their knowledge on a particular topic.")

    # Initialize states
    initialize_session_state()

    # Input Interface
    with st.sidebar:
        grade, standardTopic, standardNum, topic, num_questions, student_name = get_user_input()

        # Change app state based on button press
        if st.button("Generate Questions", on_click=disable_generate_btn, args=(True,), disabled=st.session_state.get("disabled_generate", False)):
            st.session_state.app_state = 'submission'
            
            # Save student to session state
            st.session_state.student = { 
                'grade': grade, 
                'standard_topic': standardTopic, 
                'standard_num': standardNum, 
                'topic': topic, 
                'num_questions': num_questions, 
                'student_name': student_name, 
            }
            
            # Generate questions
            st.session_state.questions_data = generate_questions(grade=grade, standard=standardTopic, standardNum=standardNum, topic=topic, num_questions=num_questions)

            st.session_state.questions = st.session_state.questions_data["questions"]
            st.session_state.user_answers = {q["id"]: "" for q in st.session_state.questions}
        st.write("*Please be patient while the questions are being generated. This may take some time.*")

    # Display the questions and collect the user's answers
    if st.session_state.app_state in ['submission', 'results', 'feedback_submitted']:
        st.markdown(f"##### Learning Standard")
        st.markdown(f"{st.session_state.questions_data['learning_standard']}")
        
        # Display introduction
        st.markdown(f"### Introduction")
        st.markdown(f"{st.session_state.questions_data['introduction']}")

        # Using a form to group the questions and answers
        with st.form(key="question_form"):
            # Display each question with a text input
            for q in st.session_state.questions:
                st.write(f"##### {q['question']}")
                answer_key = f"answer_{q['id']}"
                st.session_state.user_answers[q["id"]] = st.text_area("Your Answer in Markdown, max: 750 characters", st.session_state.user_answers[q["id"]], key=answer_key,height=200, max_chars=750)
            # Form Submit button
            if st.form_submit_button("Submit", on_click=disable_submit_btn, args=(True,), disabled=st.session_state.get("disabled_submit", False)):
                st.session_state.app_state = 'results'
            st.write("*Please be patient while the answers are being evaluated. This may take some time.*")
    
    if st.session_state.app_state in ['results', 'feedback_submitted']:
        # Fetch evaluations
        evaluations = generate_evaluations(grade, st.session_state.questions_data['learning_standard'], topic, st.session_state.questions, st.session_state.user_answers)

        # Display Thank You message and user responses
        st.write("Thank you for answering all the questions.")

        for q in st.session_state.questions:
            # Group each question, answer, and explanation
            with st.expander(f"Question {q['id']} - Click to Expand", expanded=True):
                st.write("##### Question:")
                st.write(q["question"])
                
                st.write("##### Your Answer:")
                st.markdown(f"**{st.session_state.user_answers[q['id']]}**")

                # Fetch the corresponding evaluation for the question
                eval_item = next((item for item in evaluations['evaluations'] if item["id"] == q["id"]), None)
                if eval_item:
                    
                    st.write(f"##### Grade: {eval_item['grade']}")
                    
                    st.write("##### Explanation:")
                    st.write(f"{eval_item['explanation']}")
                else:
                    st.write("Error: Evaluation not found for this question.")
        with st.expander(f"Final Feedback - Click to Expand", expanded=True):
            # Display final feedback and grade
            st.write(f"##### Final Grade: {evaluations['finalGrade']}")

            st.write("##### Final Feedback:")
            st.write(f"{evaluations['finalFeedback']}")

        # Visualize grades using a bar chart
        question_ids = [str(q["id"]) for q in st.session_state.questions]
        grades = [item['grade'] for item in evaluations['evaluations']]
        
        # Add the final grade to the grades list
        question_ids.append("Final")
        grades.append(evaluations['finalGrade'])

        visualise_bar_chart(question_ids, grades)

    if st.session_state.app_state == 'results':
        if not st.session_state.saved_data_to_airtable:
            # Save Session data to Airtable
            insert_student_record(
                sessionId= st.session_state.session_id,
                session= 'User',
                student_name= st.session_state.student['student_name'],
                grade= st.session_state.student['grade'],
                learning_standard_topic= st.session_state.student['standard_topic'],
                learning_standard_num= st.session_state.student['standard_num'],
                num_questions= st.session_state.student['num_questions'],
                topic= st.session_state.student['topic'],
                learning_standard= st.session_state.questions_data['learning_standard'].split(':')[0],
                learning_standard_definition= st.session_state.questions_data['learning_standard'].split(':')[1],
                introduction= st.session_state.questions_data['introduction']
            )

            for question in st.session_state.questions:
                insert_questions_answers_record(
                    sessionId= st.session_state.session_id,
                    session= 'User',
                    question_id= question['id'],
                    question= question['question'],
                    answer= st.session_state.user_answers[question['id']],
                    grade= evaluations['evaluations'][int(question['id'])-1]['grade'],
                    evaluation= evaluations['evaluations'][int(question['id'])-1]['explanation'],
                )

            insert_evaluations_record(
                sessionId= st.session_state.session_id,
                session= 'User',
                final_grade= evaluations['finalGrade'],
                final_evaluation= evaluations['finalFeedback']
            )
            st.session_state.saved_data_to_airtable = True

        # User can submit feedback for the app
        with st.form(key="feedback_form"):
            # Display feedback form
            st.markdown("We'd appreciate your feedback to improve this app!")

            # Display the star rating widget
            st.session_state.app_rating = st_star_rating("Rate the app:", maxValue=5, defaultValue=st.session_state.app_rating, key="rating")

            # Feedback form
            st.session_state.user_feedback = st.text_area("Share your thoughts or suggestions (optional)", st.session_state.user_feedback, height=300, max_chars=1500)

            # If the user submits feedback
            if st.form_submit_button("Submit Feedback", on_click=disable_feedback_btn, args=(True,), disabled=st.session_state.get("disabled_feedback", False)):
                st.session_state.app_state = 'feedback_submitted'
    
    if st.session_state.app_state == 'feedback_submitted':
        st.markdown("""
        ## Thank You! :heart:
        We truly appreciate your feedback and the time you took to use our app. Your insights are invaluable to us. We hope you had a pleasant experience and look forward to any future interactions!
        """)

        # Insert feedback into Airtable
        if not st.session_state.saved_user_feedback:
            insert_feedback_record(
                sessionId= st.session_state.session_id,
                rating= st.session_state.app_rating,
                feedback= st.session_state.user_feedback
            )
            st.session_state.saved_user_feedback = True


if __name__ == "__main__":
    main()