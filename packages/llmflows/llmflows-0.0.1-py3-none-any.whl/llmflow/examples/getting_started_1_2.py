# pylint: skip-file

"""
This script demonstrates how to use the llmflow package to generate prompts and format 
them with user input.

The script defines a prompt template with a placeholder for a product, and uses the 
PromptTemplate class to generate a prompt with the product "colorful socks". It then 
prints the formatted prompt to the console.

Example:
    $ python getting_started_1_2.py
    What is a good name for a company that makes colorful socks?

Note:
    This script requires the llmflow package to be installed, as well as an OpenAI API 
    key with access to the GPT-3 API.
"""

"""
The most basic building block of LangChain is calling an LLM on some input. Let’s walk 
through a simple example of
how to do this. For this purpose, let’s pretend we are building a service that 
generates a company name based on what
the company makes. In order to do this, we first need to import the LLM wrapper.
"""

from llmflow.llms.openai_chat import OpenAIChat

"""
We can then initialize the wrapper with any arguments. In this example, 
we probably want the outputs to be MORE 
random, so we’ll initialize it with a HIGH temperature.
"""

llm = OpenAIChat()

"""
We can now call it on some input!
"""

llm.add_message(
    "What would be a good company name for a company that makes colorful socks?"
)
answer = llm.chat()

print(answer)

"""
Calling an LLM is a great first step, but it’s just the beginning. Normally when you 
use an LLM in an application, 
you are not sending user input directly to the LLM. Instead, you are probably taking 
user input and constructing a 
prompt, and then sending that to the LLM.

For example, in the previous example, the text we passed in was hardcoded to ask 
for a name for a company that made 
colorful socks. In this imaginary service, what we would want to do is take only 
the user input describing what the 
company does, and then format the prompt with that information.

This is easy to do with LangChain!

First lets define the prompt template:
"""

from llmflow.prompts.prompt_template import PromptTemplate

prompt_template = PromptTemplate(
    prompt="What is a good name for a company that makes {product}?"
)

"""
Let’s now see how this works! We can call the .get_prompt method to format it.
"""

print(prompt_template.get_prompt(product="colorful socks"))

"""
Chains: Combine LLMs and prompts in multi-step workflows
Up until now, we’ve worked with the PromptTemplate and LLM primitives by themselves. 
But of course, a real application 
is not just one primitive, but rather a combination of them.

A chain in LangChain is made up of links, which can be either primitives like LLMs 
or other chains.

The most core type of chain is an LLMChain, which consists of a PromptTemplate and an 
LLM.

Extending the previous example, we can construct an LLMChain which takes user input, 
formats it with a PromptTemplate, 
and then passes the formatted response to an LLM.
"""
