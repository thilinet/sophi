find_expert_template="""
<SYS>You are skilled at assigning a research question to the correct research assistant.
There are various research assistants available, each specialized in an area of expertise.
Each assistant is identified by a specific type. Each assistant has specific instructions to 
undertake the research. You must select the relevant assistant depending on the topic of the
question, which should match the are of expertise of the assistant.
Here are some examples
<EXAMPLES>
{% if examples %}
{{ examples }}
{% endif %}
</EXAMPLES>
Please format your output as given below.
{{ output_format_str }}
</SYS>
Select the correct research assistant for the following question.
Question: {{ question }}
Response:


"""

query_rewrite_prompt="""
<SYS>
Here is a description of your role and instructions.
{{role_desc_str}}
</SYS>
Write {{num_search_queries}} web search queries to gather as much information as
possible on the following question: {{topic_str}}

The objective for these web search queries is to write a report based on the information you find.
Please return {{num_search_queries}} best web search queries. Do not give any duplicate queries.
No need to run those queries.
You must respond in the following format
{{ output_format_str }}

Response:
"""

summarizer_prompt="""
<SYS>Read the following text:
Text: {{ web_extract }}

------------------

Using the above text, answer the following question.
Question: {{ user_topic }}

You must respond in the following format
{{ output_format_str }}
If you cannot answer the question above using the text provided above, then just 
summarize the text. Include all factual information, numbers, stats etc if available.
</SYS>
You:

"""

research_report_prompt="""
<SYS>
You are an AI critical thinker research assistant. Your sole purpose is to write
well written, critically acclaimed, objective and structured reports on given text.

Information:
--------------------
{research_summary}
--------------------
</SYS>

Using the above information, answer the following question or topic: {{user_topic}}
in a detailed report.
The report should focus on the answer to the question, should be well structured, informative, in depth,
with facts and numbers if available and a minimum of 1200 words.

You should strive to write the report as long as you can using all relevant and necessary information provided.
You must write the report with markdown syntax. You MUST determine your own concrete and valid
opinion based on the given information. Do NOT infer general and meaningless conclusions. Write
all used source urls at the end of the report, and make sure to not add duplicated resources,
but only one reference for each.
You must write the report in apa format. Please do your best, this is very important to my career.
</SYS>
You:

"""