from dataclasses import dataclass, field
from adalflow.core.base_data_class import DataClass
from adalflow.components.output_parsers.dataclass_parser import DataClassParser
from typing import List, Dict

@dataclass
class Assistant(DataClass):
    
    question: str = field(
        metadata = {"desc": "A user research question"}
    )
    
    assistant_type : str= field(
        metadata = {"desc":"A research assistant specialized in a area of expertise."}
    )
    
    assistant_instruction: str = field(
        metadata = {"desc":"Specific instruction for the assistant"}
    )
    

    __input_fields__=   ["question"]
    __output_fields__ = ['assistant_type','assistant_instruction']
    

@dataclass
class WebQuery(DataClass):
    
    search_query: List[str] = field(
        metadata = {"desc": "Web search query for user topic"}
    )
    
    __output_fields__ = ['search_query']


@dataclass
class Summary(DataClass):
    
    summary: str = field(
        metadata = {"desc": "Summary of the given topic"}
    )
    
    __output_fields__ = ['summary']