from adalflow.core.component import Component
from llms import assistant_finder, query_generator, summary_generator,report_generator
from utils import web_search, web_scrape
import time 
from tqdm import tqdm 

class ResearchAgent(Component):
    """"""
    def __init__(self, research_topic):
        """"""
        super().__init__()
        
        host = "127.0.0.1:11434"
        assert research_topic != None
        self.research_topic = research_topic
        self.assistant_finder = assistant_finder
        self.query_generator = query_generator
        self.summary_generator = summary_generator
        self.report_generator = report_generator

        self.urls = []
        self.contents = []
        
    
    def __call_web(self, web_search_queries):
        """"""
        max_queries = 3
        search_queries = web_search_queries['search_query']
        if not isinstance(search_queries, list):
            search_queries = [search_queries]

        if len(search_queries) > max_queries:
            search_queries = search_queries[:max_queries]
        
        print(f"Start searching the web.")
        sleep_time = 5
        for idx, query in tqdm(enumerate(search_queries)):
            query = query.replace("\"","")
            query = query.strip()
            print(f"Searching '{query}'")
            self.urls.extend(web_search(query))
            print(f"Snooze for {sleep_time} seconds before hitting the next query !")
            time.sleep(sleep_time)
            sleep_time = sleep_time * (idx + 1)
        
        print(f"Start scraping web contents")
        for url in tqdm(self.urls):
            content = web_scrape(url)
            self.contents.append((url, content))


    def __summarize(self):
        """"""
        summary = "\n"

        user_query = {"user_topic": self.research_topic}
        for url, extract in self.contents:
            user_query['web_extract'] = extract 
            summary_result = summary_generator(user_query)
            print(url)
            print(summary_result.data)
            print("***" * 50)
            summary+= summary_result.data["summary"]
            summary+="\n\n"
        return summary 

    
    def call(self):
        """"""
        # Step 1 Find the best assistant
        assistant_result = self.assistant_finder({"question": self.research_topic})
        assistant_details = assistant_result.data 
        assert assistant_details is not None 
        assistant_type = assistant_details['assistant_type']
        assistant_instructions = assistant_details['assistant_instruction']

        print(f"Choosen assistant for the task.....")
        print(f"assistant_type: {assistant_type} \n\n assistant_instruction: {assistant_instructions}\n")
        # Step 2 rewrite the search query with 
        # assistant details
        input_dict = {
            "role_desc_str": f"assistant_type: {assistant_type} \n\n assistant_instruction: {assistant_instructions}\n"
           ,"topic_str": self.research_topic
           ,"num_queries": "2"
        }

        try:
            web_search_queries_result = self.query_generator(input_dict)
            web_search_queries = web_search_queries_result.data
            print(web_search_queries)

            self.__call_web(web_search_queries)
        except Exception as e:
            print(f"Error invoking LLM {e}")
            print(f"Try again")
            return "Error"

        # Summarize the web
        summaries = self.__summarize()
        # Write research topic
        query = {"user_topic":self.research_topic
        ,"research_summary": summaries
        }

        research_essay  = report_generator(query)

        return research_essay.data 
  









        
    
