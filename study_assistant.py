import google.generativeai as genai
import os 
from dotenv import load_dotenv
import sys

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_topic():
    while True:
        topic = input("Enter a study topic (or 'exit/quit' to quit): ").strip()
        if topic.lower() == "exit" or topic.lower() == "quit":
            print("Program ending...")
            sys.exit(0)
        elif topic:
            return topic
        else:
            print("Please enter a valid topic.")

def prompt():
    Prompt= '''
    you are an experienced tutor.
    write the topics(each one followed by its subtopics) regarding the topic.
    Format (for study plan):
        1. Topic 1: Description of topic 1
            a. Subtopic 1.1: Description of subtopic 1.1
            b. Subtopic 1.2: Description of subtopic 1.2        
    keep the descriptions in study plan under 25 words.
    keep the topics and subtopics from basics to deeper concepts.
    For follow-up questions, adapt explanations to the apparent knowledge level of the user.
    Format (for follow-up questions):
        small paragraphs with clear explanations and examples.
    keep the length of explanations for follow-up questions under 100 words.
    do slight formatting in answers to make them more readable in terminal.
    do not ask questions while generating the study plan, just provide the topics and subtopics with their descriptions.
    do not go off-topic unless specified by the user. '''
    return Prompt

def create_chat(system_prompt):
    model = genai.GenerativeModel(
        model_name = "gemini-2.5-flash",
        system_instruction = system_prompt
    )

    chat = model.start_chat(history = [])
    return chat

def study_plan(chat, topic):
    message = f"Generate a study plan for the topic: {topic}."
    response = chat.send_message(message)

    return response.text

def show_plan(plan):
    print("\n" + "=" * 50)
    print(" " * 15 + "STUDY PLAN")
    print("=" * 50)
    print("\n" + plan + "\n")
    print("=" * 50)

def chat_loop(chat):
    question_count = 0

    while True:
        question = input("\nEnter a question (or 'exit/quit' to quit): ").strip()

        if question.lower() == "exit" or question.lower() == "quit":
            break

        elif not question:
            print("Please enter a valid question.")
            continue

        try:
            response = chat.send_message(question)
            print(f"\nAnswer: {response.text}")
            question_count += 1

        except Exception as e:
            print(f"Error occurred: {e}")

    return question_count

def session_summary(topic, question_count):
    print("\n" + "=" * 50)
    print(" " * 15 + "SESSION SUMMARY")
    print("=" * 50)
    print(f"Topic: {topic}")
    print("Study Plan: Generated")
    print(f"Questions Answered: {question_count}")
    print("=" * 50)
    
def main():
    topic = get_topic()
    system_prompt = prompt()
    chat = create_chat(system_prompt)

    try:
        plan = study_plan(chat, topic)
    except Exception as e:
        print(f"Error generating study plan: {e}")
        return
    
    show_plan(plan)
    question_count = chat_loop(chat)
    session_summary(topic, question_count)


if __name__ == "__main__":
    main()