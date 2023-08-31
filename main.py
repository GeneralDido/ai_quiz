import streamlit as st
from generate_questions import generate_questions


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
        grade = st.selectbox('Select Grade Level:', ['4', '5', '6', '7', '8', '9', '10', '11', '12'])
        standard = st.selectbox('Select Academic Standard:', ['Reading: Literature', 'Reading: Informational Text', 'Writing', 'Language', 'Mathematics'])
        topic = st.text_input('Enter your interest topic:', 'baseball')
        num_questions = st.number_input('Enter the number of questions you want to generate:', min_value=1, max_value=5, value=1, step=1)

        # Change app state based on button press
        if st.button("Generate Questions"):
            st.session_state.app_state = 'submission'
            # st.session_state.questions_data = generate_questions(grade=grade, standard=standard, topic=topic, num_questions=num_questions)

            # only for dev purposes, so it does not make multiple calls to OpenAI API
            st.session_state.questions_data = {
            "introduction": "Steve Jobs was a visionary and co-founder of Apple Inc., one of the world's leading technology companies. His life story and innovative thinking continue to inspire millions around the globe. In this assignment, we will delve into his life, achievements, and the impact he made on the world of technology using informational texts. Remember, this isn't just about recalling facts. Try to think critically about the information, analyze it, and form your own opinions.",
            "questions": [
                {
                "id": 1,
                "question": "Based on the texts you've read about Steve Jobs, how would you describe his personality, leadership style, and work ethic? Provide specific examples to support your answer."
                },
                {
                "id": 2,
                "question": "What significant challenges did Steve Jobs face in his career, and how did he overcome them? How did these experiences shape him as a leader and innovator?"
                },
                {
                "id": 3,
                "question": "In your own words, explain how Steve Jobs' innovations in technology have influenced and shaped our everyday lives. Provide at least three examples."
                },
                {
                "id": 4,
                "question": "If you had a chance to interview Steve Jobs, what three questions would you ask him and why? Explain how these questions relate to your understanding of his life and contributions."
                }
            ]
        }

            st.session_state.questions = st.session_state.questions_data["questions"]
            st.session_state.user_answers = {q["id"]: "" for q in st.session_state.questions}

    # Display content based on the app state
    if st.session_state.app_state == 'submission':
        # Display introduction
        st.write(st.session_state.questions_data["introduction"])

        # Using a form to group the questions and answers
        with st.form(key="question_form"):
            # Display each question with a text input
            for q in st.session_state.questions:
                st.write(q["question"])
                answer_key = f"answer_{q['id']}"
                st.session_state.user_answers[q["id"]] = st.text_area("Your Answer", st.session_state.user_answers[q["id"]], key=answer_key)

            # Form Submit button
            if st.form_submit_button("Submit", on_click=disable_btn, args=(True,), disabled=st.session_state.get("disabled", False)):
                st.session_state.app_state = 'results'


    # If the user has submitted, display the answers
    if st.session_state.app_state == 'results':
        # Display Thank You message and user responses
        st.write("Thank you for answering all the questions.")
        for q in st.session_state.questions:
            st.write(q["question"])
            st.write("Your answer: " + st.session_state.user_answers[q["id"]])
    print(st.session_state.user_answers)
    print(st.session_state.questions_data)


if __name__ == "__main__":
    main()