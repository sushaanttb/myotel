from opentelemetry import trace
import functools  
from src.instrumentor import MyCustomInstrumentor
 
def start_as_current_span(span_name , custom_attributes=None , pass_span=False):  
    def decorator(func):  
        @functools.wraps(func)  
        def wrapper(*args, **kwargs):  
            with trace.get_tracer(__name__).start_as_current_span(span_name) as span: 
                
                if custom_attributes:  
                    for attr, value in custom_attributes.items():  
                        span.set_attribute(attr, value)  

                for span_enricher in MyCustomInstrumentor.get_instance().span_enrichers:
                    if span_enricher.can_process(span, None):
                        span_enricher.process_span(span, None)

                if pass_span:  
                    return func(span, *args, **kwargs)  
                else:  
                    return func(*args, **kwargs) 
            
        return wrapper  
    return decorator