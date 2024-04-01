from openai import AzureOpenAI
from dotenv import load_dotenv
import os
from src.decorators.tracer import start_as_current_span
from src.filters.logger import PIIFilter
import logging

load_dotenv()

log = logging.getLogger(__name__)
log.addFilter(PIIFilter())
my_func_name ="test"
client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key = os.getenv("AZURE_OPENAI_KEY"),  
    api_version = os.getenv("AZURE_OPENAI_VERSION")
)

@start_as_current_span("call_openai", pass_span=True)
def make_open_ai_call(span, message_text:any):
    log.info(f"Making OpenAI request: {message_text}")    
    global client

    completion = client.chat.completions.create(
      model="gpt-4",
      messages = message_text,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    
    span.set_attribute("coles.fromInsideFunction", "from inside function code")  
    log.info(f"Received OpenAI response: {completion}")
    call_me_along()

@start_as_current_span("call_me_along" , {"coles.fromAnnotation": my_func_name})
def call_me_along():
    log.info("Call me along!")

@start_as_current_span("call_me_separately")
def call_me_separately():
    log.info("Call me separately!")

@start_as_current_span("sensitive_call")
def sensitive_call():
    log.info("My cat can be contacted on example@example.com, or 1800 555-5555")

message_text = [
    {"role":"system","content":"You are an AI assistant that is expert in OpenTelemetry & Python. You help people find information."},
    {"role":"user","content":"Hi"}]

make_open_ai_call(message_text)

call_me_separately()

sensitive_call()