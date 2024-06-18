import os
import re
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain_community.llms import Ollama


def getEnhancedPrompt(prompt):
    load_dotenv()

    # Initialize the LM Studio endpoint
    lm_studio_endpoint = "http://localhost:8008/v1"
    ollama_endpoint = "http://localhost:12345"

    chat_model = Ollama(model="llama3")  # devrait servir de model

    os.environ['TOKENIZERS_PARALLELISM'] = 'false'

    current_memo_path = "chat_history.txt"
    full_memo_path = "Conversation.txt"

    exchange_numbers = []
    exchanges_text = []
    with open(full_memo_path, 'r') as file:
        j = -1
        for line in file:
            if line.startswith('['):
                number = int(line.strip()[1:-1])
                exchange_numbers.append(number)
                j = j + 1
                exchanges_text.append('')
            if line.strip():
                line = re.sub(r'(\r\n|\r|\n)+', ' ', line)
                exchanges_text[j] += line
    last_elements = ' '.join(exchanges_text[-3:])

    persist_directoryT = 'Automate'
    persist_directoryL = 'Loras_doc'
    embedding_f = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True})
    vectorstore = Chroma(persist_directory=persist_directoryL, embedding_function=embedding_f)

    sys_prompt: PromptTemplate = PromptTemplate(
        input_variables=["current_chat_history", "user_query", "vdb_search"],
        template="""**System Prompt** Your role is to generate a prompt suitable for stable diffusion using the information 
        provided to you. That information will start with **Start of Context** and ends at **End of Context**. 
        The rest is the prompt or query. ONLY include what is relevant. Stick to the guidelines.
    
        It is essential to rely on this context for improved results. indicate the beginning ot the prompt with *Prompt:*
        Adhere to the following guidelines when crafting your responses:
    
        1. **Stand alone Query**: If the query is specific and NOT directly related to the information within 
        your provided context, Try your best to use as many keywords in reference to the topic as possible.
        Separate your positive prompt (what you want) from your negative prompt with *Negative Prompt:*
        keywords in a prompt have to be separated by a comma (,), and loras are recognized by the < and > surrounding it.
        the way you call a lora should never change otherwise it won't work.
        you can stress the importance of a keyword by surrounding it with parenthesis. 
    
        2. **Related Queries** If the query is tied with the context you have, then try to keep the prompts you have as example
        and change them to meet the user's request. Be as detailed as possible and avoid vague terms. 
        
        here is an example: user:"I want an image of a girl in a sweater in her garden at night with fireflies".
        Your response should be as follows: 1girl, beauty, good proportions, masterpiece, 8k, photorealistic, (detailed),
        outdoors, garden, nature, wearing sweater, (sweater), starry sky, night, moon, dark, warm colors, <lora:4960_fireflies:1>,
        fireflies *Negative Prompt:* blurry, grainy, bad anatomy, easynegative, bad proportions, worst quality, ugly, 
        difformed, day, sun, man, multiple people
    
        This refined approach ensures you effectively communicate the limitations of the provided context and 
        guide users to where they might find a more complete answer, thus improving the user experience 
        by setting clear expectations. You will get a cookie if you add as many describing keywords as possible **End of System Prompt** 
        """)

    system_message_prompt = SystemMessagePromptTemplate(prompt=sys_prompt)

    student_prompt: PromptTemplate = PromptTemplate(
        input_variables=["current_chat_history", "user_query", "vdb_search"],
        template="Using only {current_chat_history} and {vdb_search}, write a prompt for {user_query}. Follow the Guidelines!")

    student_message_prompt = HumanMessagePromptTemplate(prompt=student_prompt)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, student_message_prompt])

    style_paraphrase_chain = LLMChain(llm=chat_model, prompt=chat_prompt,
                                      output_key='final_output')


    with open(current_memo_path, 'r') as file:
        chat_history = file.read()

    chat_history = chat_history + last_elements

    test_text = vectorstore.similarity_search_with_score(prompt, 3) 

    result = style_paraphrase_chain.invoke({'current_chat_history': chat_history, 'user_query': prompt,
                                            "vdb_search": test_text})
    print(result['final_output'])
    return result['final_output']
