from opentelemetry.trace import SpanKind
from opentelemetry.semconv.ai import SpanAttributes, LLMRequestTypeValues
import logging
from importlib.metadata import version

SPAN_NAME = "openai.completion"
LLM_REQUEST_TYPE = LLMRequestTypeValues.COMPLETION

OPENAI_API_VERSION = "openai.api_version"
OPENAI_API_BASE = "openai.api_base"
OPENAI_API_TYPE = "openai.api_type"

OPENAI_LLM_USAGE_TOKEN_TYPES = ["prompt_tokens", "completion_tokens"]

logger = logging.getLogger(__name__)

def _with_tracer_wrapper(func):
    def _with_tracer(tracer):
        def wrapper(wrapped, instance, args, kwargs):
            return func(tracer, wrapped, instance, args, kwargs)

        return wrapper

    return _with_tracer

@_with_tracer_wrapper
def completion_wrapper(tracer, wrapped, instance, args, kwargs):
    # span needs to be opened and closed manually because the response is a generator
    span = tracer.start_span(
        SPAN_NAME,
        kind=SpanKind.CLIENT,
        attributes={SpanAttributes.LLM_REQUEST_TYPE: LLM_REQUEST_TYPE.value},
    )

    _handle_request(span, kwargs, instance)
    response = wrapped(*args, **kwargs)
    _handle_response(model_as_dict(response), span)

    span.end()
    return response

def model_as_dict(model):
    if version("pydantic") < "2.0.0":
        return model.dict()
    if hasattr(model, "model_dump"):
        return model.model_dump()
    elif hasattr(model, "parse"):  # Raw API response
        return model_as_dict(model.parse())
    else:
        return model
    
def _handle_request(span, kwargs, instance):
    _set_request_attributes(span, kwargs)

def _handle_response(response, span):
    _set_response_attributes(span, response)

def _set_request_attributes(span, kwargs):
    if not span.is_recording():
        return

    try:
        _set_span_attribute(span, SpanAttributes.LLM_VENDOR, "OpenAI")
        _set_span_attribute(span, SpanAttributes.LLM_REQUEST_MODEL, kwargs.get("model"))
        _set_span_attribute(
            span, SpanAttributes.LLM_REQUEST_MAX_TOKENS, kwargs.get("max_tokens")
        )
        _set_span_attribute(
            span, SpanAttributes.LLM_TEMPERATURE, kwargs.get("temperature")
        )
        _set_span_attribute(span, SpanAttributes.LLM_TOP_P, kwargs.get("top_p"))
        _set_span_attribute(
            span, SpanAttributes.LLM_FREQUENCY_PENALTY, kwargs.get("frequency_penalty")
        )
        _set_span_attribute(
            span, SpanAttributes.LLM_PRESENCE_PENALTY, kwargs.get("presence_penalty")
        )
        _set_span_attribute(span, SpanAttributes.LLM_USER, kwargs.get("user"))
        _set_span_attribute(
            span, SpanAttributes.LLM_HEADERS, str(kwargs.get("headers"))
        )
        _set_span_attribute(
            span, SpanAttributes.LLM_IS_STREAMING, kwargs.get("stream") or False
        )
    except Exception as ex:  # pylint: disable=broad-except
        logger.warning(
            "Failed to set input attributes for openai span, error: %s", str(ex)
        )

def _set_span_attribute(span, name, value):
    if value is not None:
        if value != "":
            span.set_attribute(name, value)
    return

def _set_response_attributes(span, response):
    if not span.is_recording():
        return

    try:
        _set_span_attribute(
            span, SpanAttributes.LLM_RESPONSE_MODEL, response.get("model")
        )

        usage = response.get("usage")
        if not usage:
            return


        _set_span_attribute(
            span, SpanAttributes.LLM_USAGE_TOTAL_TOKENS, usage.get("total_tokens")
        )
        _set_span_attribute(
            span,
            SpanAttributes.LLM_USAGE_COMPLETION_TOKENS,
            usage.get("completion_tokens"),
        )
        _set_span_attribute(
            span, SpanAttributes.LLM_USAGE_PROMPT_TOKENS, usage.get("prompt_tokens")
        )

        return
    except Exception as ex:  # pylint: disable=broad-except
        logger.warning(
            "Failed to set response attributes for openai span, error: %s", str(ex)
        )
