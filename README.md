# Introduction 
A sample library to instrument OpenAI calls. The library is exposed via it's main class MyCustomInstrumentor.py which sets up everything.
The main class internally refers to another class "TestOpenAIInstrumentor.py" which is basically a custom Instrumentor class based on OpenTelemetry API. This class actually does the instrumerntation of OpenAI calls. 
Further the instrumentation library also exposes a log filter and custom tracer annoation which can be used by developers as required.
An example app.py class has been created as a reference to show how a developer can leverage all that.

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
