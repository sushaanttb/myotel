from typing import Any, Collection

import wrapt
from opentelemetry.trace import get_tracer

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from src.openai.telemetry.utils import completion_wrapper

_instruments =  ("openai >= 0.27.0",)
SPAN_NAME = "openai.AzureOpenAI.chat.completion"

class TestOpenAIInstrumentor(BaseInstrumentor):

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments
    
    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, 1, tracer_provider)
        print("wrapping completions call..")
        print(f"tracer_provider {tracer_provider}")
        print(f"tracer {tracer}")
        wrapt.wrap_function_wrapper("openai.resources.chat.completions", "Completions.create", completion_wrapper(tracer))
        print("completions call wrapped successfully.")
        
    def _uninstrument(self, **kwargs):
        pass