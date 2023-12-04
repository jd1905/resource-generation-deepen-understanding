#------------------------------------------------------
#---- Streamlit application to generate resources -----
#---- POC: Ariena Chi 
#---- Modified: Nov 13, 2023
#------------------------------------------------------

# Import from 3rd party libraries
import streamlit as st
import streamlit_scrollable_textbox as stx
from annotated_text import annotated_text

# Import AI-related modules 
import openai

st.title("Master Basic Sounds with Confidence: Resources")

with st.expander("About this site"):
    st.write("""
        This site provides prototype examples to complement interventionhelper.org.
        Use this site in parallel with inteventionhelper.org to pull resources for use in your classroom. 
    """)

# Set the model engine and your OpenAI API key
model_engine = "gpt-4"
openai.api_key = "" ## redacted

# ----------------------------------------------
# Strategy: Master basic sounds with confidence
# ----------------------------------------------

# Provide inputs
word_type = st.selectbox(
    'What are your students struggling with?',
    ('Long vowel sound', 'Short vowel sound', 'Vowel-consonant-e','Vowel combinations oa, ea, ee, ai','Vowel diphthongs oi, oy, ou, ew', 'R-controlled vowels','Consonant-le'))

grade_level = st.slider(
    'What grade level are your students?', min_value=3, max_value=8, step=1)

topic = st.text_input(
    'What topic is this lesson about?')

time = st.slider(
    'How much time do you have to practice (in minutes)?', min_value=5, max_value=20, step=5)

tab1, tab2, tab3 = st.tabs(['Vocabulary List','Worksheet','Reading Materials'])

# ----------------------
# Tab 1: Vocabulary List
# ----------------------

with tab1: 

    def DefinitionsForVowelSounds(text):
        ''' 
        This function returns the definitions and several examples for vowel sounds. 
        '''

        if text == "Long vowel sound":
            definition_and_example = "Long vowels are those in which the sounds of the letters A, E, I, O, and U match the spoken name of the letter. Some words with long vowel sounds are me, labor and polar."

        if text == "Short vowel sound":
            definition_and_example = "Short vowel sounds occur when the letter is not pronounced the way it sounds. Some words with long vowel sounds are cap and digger."

        if text == "Vowel-consonant-e":
            definition_and_example = "Words ending with a vowel-consonant-e. For example, cake, mistake, mule, bike, cove, stove."

        if text == "Vowel combinations oa, ea, ee, ai":
            definition_and_example = "Words with the oa, ea, ee, and ai combinations have long vowel sounds. For example, boat, meat, meet, remain, teachable."

        if text == "Vowel diphthongs oi, oy, ou, ew":
            definition_and_example = "Words with the oi, oy, ou, ew combinations. For example, toy, destroy, newsworthy."

        if text == "R-controlled vowels":
            definition_and_example = "Words where a vowel is accompanied by the letter r. For example, car, fur, personable."

        if text == "Consonant-le":
            definition_and_example = "Words ending in -le. For example, battle, belittle, reconcile, personable."

        return definition_and_example

    # ChatGPT functions
    def ChatGPTVocabList(definition):
        ''' 
        This function uses the OpenAI API to create a vocabulary list
        '''

        number_of_words = time

        vocab_prompt = f"""Prepare three vocabulary lists (easy, medium and hard) with {number_of_words} words each related to the topic {topic} for students with Grade {grade_level} reading level.
                        {definition} Every word in the vocabulary list should have {word_type}. Include the definition of the word and which vowel has the {word_type}. 
                        Double check your work before giving your final answer."""
        conversation = [{'role':'system',
                        'content':"""You are an experienced intervention specialist who helps students who are struggling to read. 
                        You will generate resources that teachers can use in their instructional time with students. 
                        Do not include anything in your response other than the specific resources that a teacher can use with their students."""}]

        conversation.append({'role':'user', 'content':f'{vocab_prompt}'})

        # Use the OpenAI API to generate a word list
        word_list = openai.ChatCompletion.create(
                                    model = model_engine,
                                    messages = conversation,
                                    )
        word_list_output = word_list['choices'][0]['message']['content']

        return word_list_output

    # Main body of Tab 1 
    definitions_and_examples = DefinitionsForVowelSounds(word_type)

    word_list_output = ChatGPTVocabList(definitions_and_examples)

    stx.scrollableTextbox(word_list_output)

    st.download_button(
        label="Download as text file",
        data=word_list_output,
        file_name='vocab_list.txt'
    )

# ----------------------
# Tab 2: Worksheet
# ----------------------

with tab2:

    def ChatGPTWorksheet():
        ''' 
        This function uses the OpenAI API to create a worksheet for students
        '''

        worksheet_prompt = f"""Create three worksheets (easy, medium and hard) on the topic {topic} for students in Grade {grade_level}. 
                               For each worksheet, ask students to identify whether each word in a list of words have a short or long vowel sound. 
                               Remember that long vowels are those in which the sounds of the letters A, E, I, O, and U match the spoken name of the letter.
                               Short vowel sounds occur when the letter is not pronounced the way it sounds.
                               Do not include the answer key."""

        conversation = [{'role':'system',
                        'content':"""You are an experienced intervention specialist who helps students who are struggling to read. 
                        You will create worksheets that students can use during their class time. Your worksheets include clear instructions for students."""}]

        conversation.append({'role':'user', 'content':f'{worksheet_prompt}'})

        # Use the OpenAI API to generate a paragraph about the topic
        worksheet_query = openai.ChatCompletion.create(
                                    model = model_engine,
                                    messages = conversation,
                                    )
        worksheet_query_output = worksheet_query['choices'][0]['message']['content']

        return worksheet_query_output
    
    # Main body of Tab 2
    worksheet_query_output = ChatGPTWorksheet()

    stx.scrollableTextbox(worksheet_query_output)

    st.download_button(
        label="Download as text file",
        data=worksheet_query_output,
        file_name='student_worksheet.txt'
    )

# -------------------------
# Tab 3: Relevant Passage
# -------------------------

with tab3:

    def ChatGPTPassage():
        ''' 
        This function uses the OpenAI API to create a passage for students
        '''

        passage_prompt = f"""Create three one-paragraph reading passages (easy, medium, hard) for students in Grade {grade_level}. 
                             The reading passages should let students practice identifying short and long vowel sounds. 
                             Remember that long vowels are those in which the sounds of the letters A, E, I, O, and U match the spoken name of the letter.
                             Short vowel sounds occur when the letter is not pronounced the way it sounds.
                             Paragraph should be related to the topic {topic}"""

        conversation = [{'role':'system',
                        'content':"""You are an experienced intervention specialist who helps students who are struggling to read. 
                        You will generate resources that teachers can use in their instructional time with students. 
                        Do not include anything in your response other than the specific resources that a teacher can use with their students."""}]

        conversation.append({'role':'user', 'content':f'{passage_prompt}'})

        # Use the OpenAI API to generate a paragraph about the topic
        passage_query = openai.ChatCompletion.create(
                                    model = model_engine,
                                    messages = conversation,
                                    )
        passage_query_output = passage_query['choices'][0]['message']['content']

        return passage_query_output
    
    # Main body of Tab 2
    passage_query_output = ChatGPTPassage()

    stx.scrollableTextbox(passage_query_output)

    st.download_button(
        label="Download as text file",
        data=passage_query_output,
        file_name='student_reading_passages.txt'
    )