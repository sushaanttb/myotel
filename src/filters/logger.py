import logging  
import scrubadub  
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

# An example LogFilter  
class PIIFilter(logging.Filter):  
    def filter(self, record):  
        redacted_string = scrubadub.clean(record.msg)  
        # print(f"Is {record.msg} & it's redacted version same? {record.msg == redacted_string} ")
        return record.msg == redacted_string
