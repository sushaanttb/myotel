import abc

class BaseSpanEnricher(abc.ABC):

    def process_span(self, span, obj):
        raise NotImplementedError("process_span is not implemented")

    def can_process(self, span, obj) -> bool:
        return False
    
class SpanEnricher(BaseSpanEnricher):

    def process_span(self, span, obj):
        print(f"Adding attributes in span.. {span}")
        span.set_attribute("coles.fromSpanProcessor", "From Span Processor")
      
    def can_process(self, span, obj):
        return True
    