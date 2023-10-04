import os
import openai
openai.api_key = "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"

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-16k-0613",
  messages=[
    {"role": "system", "content": "Linguist."},
    {"role": "user", "content": "I have a comma-delimited list of words that are potentially synonyms to the Vietnamese word \"Hòa hợp\". Could you please filter out the words that are not correct and provide me with a revised list? The original list is as follows: hòa hợp, phù hợp, sự hoà hợp, hoà âm, hiểu biết, thiện chí, hòa âm nhạc, tương thích, đồng thuận, hài hòa, hòa hợp, nhất trí, sự cân đối, hòa bình, đoàn kết, đồng tính, sự hài hoà, hợp tác, quan hệ họ hàng, âm hưởng, hữu nghị, nhất quán, mối quan hệ, sự phù hợp, sự hoà thuận, sự hoà âm, yên bình, tính tương đồng."}
  ]
)

output = str(completion.choices[0].message['content']).encode('utf-8')
print(output.decode('utf-8'))