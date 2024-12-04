from datamodels import Summary, WebQuery, Assistant
from fewshots import find_experts_few_shots
from prompts import (
    summarizer_prompt
   ,research_report_prompt
   ,query_rewrite_prompt    
   ,find_expert_template
)
from adalflow.components.output_parsers.outputs import JsonOutputParser
from adalflow.core.generator import Generator
from adalflow.components.model_client.ollama_client import OllamaClient
from adalflow.components.output_parsers.dataclass_parser import DataClassParser

host = "127.0.0.1:11434"

assistants_few_shots = [Assistant.from_dict(few_shot) for few_shot in find_experts_few_shots]
assistant_parser = DataClassParser(Assistant)

assistant_finder = Generator(
    model_client = OllamaClient(host=host)
   ,model_kwargs = {"model":"llama3.2:1b"}
   ,template = find_expert_template
   ,prompt_kwargs ={"examples": assistant_parser.get_examples_str(examples=assistants_few_shots)
                    ,"output_format_str": assistant_parser.get_output_format_str()
                   }
   ,name ="Find Assistant" 
   ,output_processors =  JsonOutputParser(data_class=Assistant)
)

webquery_parser = DataClassParser(WebQuery)
query_generator = Generator(
    model_client = OllamaClient(host=host)
   ,model_kwargs = {"model":"llama3.2:1b"}
   ,template = query_rewrite_prompt
   ,prompt_kwargs ={
                    "output_format_str": webquery_parser.get_output_format_str()
                   }
   ,output_processors= JsonOutputParser(data_class=WebQuery)
   ,name ="Query rewriter" 
)

summary_parser = DataClassParser(Summary)
summary_generator = Generator(
    model_client = OllamaClient(host=host)
   ,model_kwargs = {"model":"llama3.2:1b"}
   ,template = summarizer_prompt
   ,prompt_kwargs ={
                    "output_format_str": summary_parser.get_output_format_str()
                   }
   ,output_processors= JsonOutputParser(data_class=Summary)
   ,name ="Query rewriter" 
)


report_generator = Generator(
    model_client = OllamaClient(host=host)
   ,model_kwargs = {"model":"llama3.2:1b"}
   ,template = research_report_prompt
   ,name ="Report generator" 
)

