from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_ollama.chat_models import ChatOllama

class LLMOutput:
    def __init__(self, template, modelName):
        self.llm = ChatOllama(model=modelName)
        self.template = template

    def generate_opinion(self, content: str, object_model):
        
        output_parser = JsonOutputParser(pydantic_object=object_model)
        format_instructions = output_parser.get_format_instructions()
        
        prompt = PromptTemplate(template=self.template, input_variables=["content"],
                                partial_variables={"format_instructions": format_instructions})
        
        
        formatted_prompt = prompt.format(content=content)
        messages = [HumanMessage(content=formatted_prompt)]
        
        # Get the LLM response's content based on the prompt
        result = self.llm.invoke(messages).content
        
        try:
            return output_parser.parse(result)
        except Exception as e:
           print(f"Error parsing LLM response: {e}")
           print(f"Actual response content: {result}")
           return f"Error: {str(e)}"