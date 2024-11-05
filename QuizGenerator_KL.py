import streamlit as st
from openai import OpenAI
import json
import os

client = OpenAI(api_key="your_api_key_here")

# Welcome user
st.title("🧠 Interactive Quiz with OpenAI")
st.markdown("Welcome to the Interactive Quiz! Test your knowledge and learn something new. Enjoy the quiz and good luck! 💡")

class Question:
    def __init__(self, question, options, correct_answer, explanation=None):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation

class Quiz:
    def __init__(self):
        self.questions = self.load_or_generate_questions()
        self.initialize_session_state()


    def load_or_generate_questions(self):
        # Check if questions already exist in the session state
        if 'questions' not in st.session_state:
            # Predefined questions or load from a source
            st.session_state.questions = [
                Question("What is the capital of France?", ["London", "Paris", "Berlin", "Madrid"], "Paris",
                         "Paris is the capital and most populous city of France."),
                Question("Who developed the theory of relativity?",
                         ["Isaac Newton", "Albert Einstein", "Nikola Tesla", "Marie Curie"], "Albert Einstein",
                         "Albert Einstein is known for developing the theory of relativity, one of the two pillars of modern physics."),
                # Μore static questionσ added
                Question("What is the largest planet in our Solar System?",
                         ["Earth", "Mars", "Jupiter", "Saturn"], "Jupiter",
                         "Jupiter is the largest planet in our Solar System."), 
                Question("What is the smallest unit of life?",
                         ["Atom", "Molecule", "Cell", "Organism"], "Cell",
                         "The cell is the smallest unit of life, which can perform all life processes.")
            ]
        return st.session_state.questions


    def initialize_session_state(self):
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'answers_submitted' not in st.session_state:
            st.session_state.answers_submitted = 0  # Track the number of answers submitted
        if 'user_answer' not in st.session_state:
            st.session_state.user_answer = None


    def display_quiz(self):
        self.update_progress_bar()
        if st.session_state.answers_submitted >= len(self.questions):
            self.display_results()
        else:
            self.display_current_question()


    def display_current_question(self):
        question = self.questions[st.session_state.current_question_index]
        st.write(f"**Question {st.session_state.current_question_index + 1}/{len(self.questions)}:** {question.question}")
        options = question.options
        # Use a unique key for the radio to avoid option persistence across questions
        st.session_state.user_answer = st.radio("Choose one:", options, key=f"question_{st.session_state.current_question_index}")
        
        # Add a submit button with a callback to check the answer
        if st.button("Submit Answer", key=f"submit_{st.session_state.current_question_index}"):
            self.check_answer(st.session_state.user_answer)
            st.button("Next Question", type="primary") 
            st.session_state.answers_submitted += 1
            if st.session_state.current_question_index < len(self.questions) - 1:
                st.session_state.current_question_index += 1
            else:
                st.session_state.quiz_completed = True
    
    def check_answer(self, user_answer):
        correct_answer = self.questions[st.session_state.current_question_index].correct_answer
        if user_answer == correct_answer:
            st.session_state.score += 1
            st.success("Correct! 🎉")
        else:
            st.error("Wrong answer! ❌")
        if self.questions[st.session_state.current_question_index].explanation:
            st.info(self.questions[st.session_state.current_question_index].explanation)


    def display_results(self):
        st.write(f"Quiz completed! Your score: {st.session_state.score}/{len(self.questions)}")
        # Changed passing score from 100% to 70%
        if  st.session_state.score/len(self.questions) == 1.0:
            st.success("Congratulations! You scored perfectly! 🏆")
            st.balloons()
        elif st.session_state.score/len(self.questions) >= 0.7:
            st.success("Congratulations! You passed the quiz! ✅") 
            st.snow()
        else:
            st.error("Quiz completed. Better luck next time! 🚀")
        if st.button("Restart Quiz"):
            self.restart_quiz()


    def update_progress_bar(self):
        total_questions = len(self.questions)
        progress = st.session_state.answers_submitted / total_questions
        st.progress(progress)


    def restart_quiz(self):
        st.session_state.current_question_index = 0
        st.session_state.score = 0
        st.session_state.answers_submitted = 0
        st.session_state.user_answer = None
        st.session_state.quiz_completed = False


# Function to convert the GPT response into a Question object and append it to the questions list
# Function to generate a new question via GPT-3 and append it to the session state questions
def generate_and_append_question(user_prompt):
    history = ""
    for q in st.session_state.questions:
        history += f"Question: {q.question} Answer: {q.correct_answer}\n"

    #st.write(history)
    # User Input Validation before the API call
    if not user_prompt.strip():
        st.error("Please enter a valid topic or category.")
        return
        
    gpt_prompt = '''Generate a JSON response for a trivia question including the question, options, correct answer, and explanation. The format should be as follows:

{
  "Question": "The actual question text goes here?",
  "Options": ["Option1", "Option2", "Option3", "Option4"],
  "CorrectAnswer": "TheCorrectAnswer",
  "Explanation": "A detailed explanation on why the correct answer is correct."
}'''
    try:
        with st.spinner('Generating your question...'):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": gpt_prompt},
                    {"role": "user", "content": f"Create a question about : {user_prompt} that is different from those : {history}"}
                ]
            )
            gpt_response = json.loads(response.choices[0].message.content)  # Assuming this returns the correct JSON structure
            # Check if received response is in the expected json format
            if "Question" in gpt_response and "Options" in gpt_response and "CorrectAnswer" in gpt_response:
                new_question = Question(
                    question=gpt_response["Question"],
                    options=gpt_response["Options"],
                    correct_answer=gpt_response["CorrectAnswer"],
                    explanation=gpt_response["Explanation"]
                )
                #st.write(gpt_response) # Commented this line so that the user cannot see the correct answer to the new question, therefore avoid cheating
                st.session_state.questions.append(new_question)
                st.success("New question generated successfully!")
            else:
                st.error("Received response is not in the expected format.")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Main app logic
if 'quiz_initialized' not in st.session_state:
    st.session_state.quiz = Quiz()
    st.session_state.quiz_initialized = True
    
st.session_state.quiz.display_quiz()

st.divider()

st.markdown("**Add a New Question**")
user_input = st.text_input("Type the topic or category of your new question:")

if st.button('Generate New Question'):
    generate_and_append_question(user_input)
