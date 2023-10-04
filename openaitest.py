import os
import openai
openai.api_key = "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"
response = openai.Model.list()

print(response)