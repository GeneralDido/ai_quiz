import streamlit as st
import matplotlib.pyplot as plt

from generate_questions import generate_questions
from generate_evaluations import generate_evaluations


def main():
    # Disable button after click
    def disable_btn(button):
        st.session_state["disabled"] = True

    # Set page title and description
    st.set_page_config(page_title="AI-driven Knowledge Assessment", page_icon=":books:", layout="wide", initial_sidebar_state="expanded")
    st.title("AI-driven Knowledge Assessment")
    st.write("This app generates a set of knowledge assessment questions based on the user's input. The questions are generated using AI and are designed to test the user's understanding of a particular topic. The user can select the grade level, academic standard, topic, and number of questions they want to generate. Once the questions are generated, the user can answer them one by one and receive immediate feedback. This app is useful for educators, students, and anyone who wants to test their knowledge on a particular topic.")

    # Initialize states
    if 'app_state' not in st.session_state:
        st.session_state.app_state = 'generation'
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'questions_data' not in st.session_state:
        st.session_state.questions_data = {}

    # Input Interface
    with st.sidebar:
        st.markdown("### Made by Dimitris Panouris")
        grade = st.selectbox('Select Grade Level:', ['4', '5', '6', '7', '8', '9', '10', '11', '12'])
        standard = st.selectbox('Select Academic Standard:', ['Reading: Literature', 'Reading: Informational Text', 'Writing'])
        topic = st.text_input('Enter your interest topic:', 'baseball')
        num_questions = st.number_input('Enter the number of questions you want to generate:', min_value=1, max_value=4, value=1, step=1)

        # Change app state based on button press
        if st.button("Generate Questions"):
            st.session_state.app_state = 'submission'
            st.session_state.questions_data = generate_questions(grade=grade, standard=standard, topic=topic, num_questions=num_questions)
            st.session_state.questions = st.session_state.questions_data["questions"]
            st.session_state.user_answers = {q["id"]: "" for q in st.session_state.questions}

    # Display content based on the app state
    if st.session_state.app_state == 'submission':
        # Display introduction
        st.markdown(f"#### {st.session_state.questions_data['introduction']}")

        # Using a form to group the questions and answers
        with st.form(key="question_form"):
            # Display each question with a text input
            for q in st.session_state.questions:
                st.write(q["question"])
                answer_key = f"answer_{q['id']}"
                st.session_state.user_answers[q["id"]] = st.text_area("Your Answer in Markdown", st.session_state.user_answers[q["id"]], key=answer_key)

            # Form Submit button
            if st.form_submit_button("Submit", on_click=disable_btn, args=(True,), disabled=st.session_state.get("disabled", False)):
                st.session_state.app_state = 'results'

    
    if st.session_state.app_state == 'results':
        # Fetch evaluations
        evaluations = generate_evaluations(grade, standard, topic, st.session_state.questions, st.session_state.user_answers)

        # Display Thank You message and user responses
        st.write("Thank you for answering all the questions.")

        for q in st.session_state.questions:
            # Group each question, answer, and explanation
            with st.expander(f"Question {q['id']} - Click to Expand", expanded=True):
                st.write("### Question:")
                st.write(q["question"])
                
                st.write("### Your Answer:")
                st.markdown(f"**{st.session_state.user_answers[q['id']]}**")

                # Fetch the corresponding evaluation for the question
                eval_item = next((item for item in evaluations['evaluations'] if item["id"] == q["id"]), None)
                if eval_item:
                    st.write("### Grade:")
                    st.write(f"{eval_item['grade']}")
                    
                    st.write("### Explanation:")
                    st.write(f"{eval_item['explanation']}")
                else:
                    st.write("Error: Evaluation not found for this question.")
        
        # Display final feedback and grade
        st.write(f"### Final Grade: {evaluations['finalGrade']}")
        st.write(f"### Final Feedback: {evaluations['finalFeedback']}")

        # Visualize grades using a bar chart
        question_ids = [str(q["id"]) for q in st.session_state.questions]
        grades = [item['grade'] for item in evaluations['evaluations']]
        
        # Add the final grade to the grades list
        question_ids.append("Final")
        grades.append(evaluations['finalGrade'])

        # Adjusting the size of the graph
        fig, ax = plt.subplots(figsize=(6, 4))  # Adjust these values as needed
        ax.bar(question_ids, grades, color='skyblue')
        ax.set_xlabel('Questions')
        ax.set_ylabel('Grades')
        ax.set_title('Grades for Each Question and Final Grade')
        ax.set_ylim(1, 5)  # Grade Scale is 1 to 5
        st.pyplot(fig, use_container_width=False)





if __name__ == "__main__":
    main()