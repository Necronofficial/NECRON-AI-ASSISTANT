#decision_maker_module.py
from groq import Groq

class DecisionMaker:
    def __init__(self, groq_api_key, assistant_name, username):
        self.client = Groq(api_key=groq_api_key)
        self.assistant_name = assistant_name
        self.username = username

        self.preamble_decision = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write an application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'Youtube (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'Youtube 1st topic, Youtube 2nd topic' and so on.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

        self.system_prompt_general = f"""Hello, I am {self.username}, You are a very accurate and advanced AI chatbot named {self.assistant_name} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

    def decide_query_type(self, query):
        messages = [
            {"role": "system", "content": self.preamble_decision},
            {"role": "user", "content": query}
        ]
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192", # Or another suitable Groq model
                temperature=0.0, # Keep temperature low for precise decision making
                max_tokens=128,
            )
            decision = chat_completion.choices[0].message.content.strip()
            print(f"Decision Maker: Decided -> {decision}")
            return decision
        except Exception as e:
            print(f"Error in decision making with Groq: {e}")
            return f"general {query}" # Fallback to general if error

    def get_llm_response(self, query, get_chat_history_func):
        messages = [
            {"role": "system", "content": self.system_prompt_general},
        ]
        # Incorporate chat history for better context
        chat_history = get_chat_history_func(limit=5) # Get last 5 conversations
        for user_q, ai_r in chat_history:
            messages.append({"role": "user", "content": user_q})
            messages.append({"role": "assistant", "content": ai_r})
        
        messages.append({"role": "user", "content": query}) # Add current query

        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192", # Use a capable model for conversational AI
                temperature=0.7, # Adjust for creativity vs. factual accuracy
                max_tokens=1024,
            )
            response = chat_completion.choices[0].message.content.strip()
            return response
        except Exception as e:
            print(f"Error in LLM response with Groq: {e}")
            return "I am sorry, I am having trouble connecting right now. Please try again later."

    def get_realtime_response(self, query):
        # This function needs integration with a real-time data source.
        # For demonstration, we'll simulate a search.
        print(f"Decision Maker: Searching real-time data for: {query}")
        try:
            # Integrate with a web search API (e.g., Google Search API, SerpApi, Brave Search API)
            # Example using a placeholder for a real search:
            # from Google Search_api import search # Assuming you have this
            # search_results = search(query)
            # return f"Based on recent information, here's what I found about '{query}': {search_results}"

            # For now, a placeholder response:
            return f"I am retrieving real-time information for '{query}'. Please bear with me as I access the latest data."
        except Exception as e:
            print(f"Error fetching real-time data: {e}")
            return "I couldn't retrieve real-time information at the moment."
