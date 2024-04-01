from dotenv import load_dotenv
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from src.openai.telemetry import TestOpenAIInstrumentor
import logging
import sys


class MyCustomInstrumentor:  
    instance = None

    def __init__(self):
        self.span_processors = []  
        self.log_filters = []  
        self.azure_monitor_settings = None  
  
    @classmethod    
    def get_instance(cls):
        if MyCustomInstrumentor.instance is None:
            MyCustomInstrumentor.instance =  MyCustomInstrumentor()  
        return MyCustomInstrumentor.instance 
    

    def withSpanEnrichers(self, span_enrichers=[]): 
        self.span_enrichers = span_enrichers  
        return self 
    
    def withLogFilters(self, log_filters=[]):  
        self.log_filters = log_filters  
        return self  
  
    def withAzureMonitorSettings(self, azure_monitor_settings =None):  
        self.azure_monitor_settings = azure_monitor_settings  
        return self  
    
    def instrument(self):  
        logging.basicConfig(
            level=logging.INFO,
            stream=sys.stdout,
            format="%(asctime)s [%(levelname)s] traceId=%(otelTraceID)s spanId=%(otelSpanID)s %(message)s",
        )
        logging.getLogger("azure.monitor.opentelemetry").setLevel(logging.WARNING)
        logging.getLogger("azure.core.pipeline.policies").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        # Note: This instrumentation should be the first before any other instrumentation
        LoggingInstrumentor().instrument()
        configure_azure_monitor()
        TestOpenAIInstrumentor().instrument()
