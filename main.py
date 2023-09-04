import streamlit as st

from streamlit_star_rating import st_star_rating

from ai_generators.generate_questions import generate_questions
from ai_generators.generate_evaluations import generate_evaluations

from db.AirtableManager import AirtableManager

from helper.functions import disable_feedback_btn, disable_generate_btn, disable_submit_btn

from src.app_state import initialize_session_state
from src.bar_chart import visualise_bar_chart
from src.input_interface import get_user_input

def main():
    
    # Set page title and description
    st.set_page_config(page_title="AI-driven Knowledge Assessment", page_icon=":books:", layout="centered", initial_sidebar_state="expanded")
    st.title("AI-driven Knowledge Assessment")
    st.write("This app generates a set of knowledge assessment questions. The questions are generated using AI and are designed to test a student's understanding of a particular topic.")
    st.write("The student can select the Grade level, Common Core Learning Standard Topic and number, topic of interest, and number of questions to generate. You can also enter any username you like (does not impact anything on the app).")
    st.write("Once the questions are generated, the student can answer them and receive immediate feedback. This app is useful for educators, students, and anyone who wants to test their knowledge on a particular topic.")
    st.write("The app saves anonymous usage data (no IP or user tracking) for feedback and research purposes. The data is used to improve the AI models and the app.")
    st.write("We would appreciate your feedback to improve this app. Please share your thoughts and suggestions at the end of the assessment.")
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
        st.session_state.evaluations = generate_evaluations(grade, st.session_state.questions_data['learning_standard'], topic, st.session_state.questions, st.session_state.user_answers)

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
                eval_item = next((item for item in st.session_state.evaluations['evaluations'] if item["id"] == q["id"]), None)
                if eval_item:
                    
                    st.write(f"##### Grade: {eval_item['grade']}")
                    
                    st.write("##### Explanation:")
                    st.write(f"{eval_item['explanation']}")
                else:
                    st.write("Error: Evaluation not found for this question.")
        with st.expander(f"Final Feedback - Click to Expand", expanded=True):
            # Display final feedback and grade
            st.write(f"##### Final Grade: {st.session_state.evaluations['finalGrade']}")

            st.write("##### Final Feedback:")
            st.write(f"{st.session_state.evaluations['finalFeedback']}")

        # Visualize grades using a bar chart
        question_ids = [str(q["id"]) for q in st.session_state.questions]
        grades = [item['grade'] for item in st.session_state.evaluations['evaluations']]
        
        # Add the final grade to the grades list
        question_ids.append("Final")
        grades.append(st.session_state.evaluations['finalGrade'])

        visualise_bar_chart(question_ids, grades)

    if st.session_state.app_state == 'results':
        if not st.session_state.saved_data_to_airtable:
            
            # Save Session data to Airtable
            airtable_manager = AirtableManager(
                sessionId= st.session_state.session_id,
                session= 'User',
                student= st.session_state.student,
                questions= st.session_state.questions_data,
                answers= st.session_state.user_answers,
                evaluations= st.session_state.evaluations
            )

            airtable_manager.insert_student_record()
            for question in st.session_state.questions:
                airtable_manager.insert_questions_answers_record(question_id= question['id'])
            airtable_manager.insert_evaluations_record()

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