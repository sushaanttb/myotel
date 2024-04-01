from setuptools import setup, find_packages  
  
setup(  
    name='myotel',  
    version='0.1',  
    url='https://github.com/sushaanttb/myotel',  
    author='Sushant Bhalla',  
    author_email='sushantbhalla@ymail.com',  
    description='A sample library to instrument OpenAI calls.',  
    packages=find_packages(),      
    install_requires=["wrapt",
                        "python-dotenv",
                        "opentelemetry-api",
                        "opentelemetry-instrumentation",
                        "azure-monitor-opentelemetry",
                        "opentelemetry-semantic-conventions-ai",
                        "opentelemetry-instrumentation-logging",
                        "scrubadub",
                        "openai"
                    ],  
)  
