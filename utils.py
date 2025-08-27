from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

# import os

def generate_script(subject, video_length, creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "Please come up with a catchy title for your video on the topic '{subject}'")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """You are a blogger with a short video channel. Based on the following title and relevant information, write a video script for your short video channel.
                Video Title: {title}, Video Length: {duration} minutes. The generated script should be as long as possible within the video duration requirements.
                The beginning should capture the key points, the middle should provide valuable content, and the end should include a surprise. The script should also be formatted as [beginning, middle, end].
                The overall content should be presented in a light-hearted and engaging manner to appeal to young people.
                You can incorporate the following Wikipedia search information into your script, but this is for reference only. Only relevant information should be included and any irrelevant information should be omitted:
                ```{wikipedia_search}```""")
        ]
    )

    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity)

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    search = WikipediaAPIWrapper(lang="en")
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result}).content

    return search_result, title, script

# print(generate_script("sora模型", 1, 0.7, os.getenv("OPENAI_API_KEY")))