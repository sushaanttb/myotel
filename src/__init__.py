from dotenv import load_dotenv
from src.instrumentor import MyCustomInstrumentor
from src.processors.span import SpanEnricher

load_dotenv()

MyCustomInstrumentor.get_instance() \
    .withSpanEnrichers([SpanEnricher()]) \
    .withLogFilters() \
    .withAzureMonitorSettings().instrument()  
