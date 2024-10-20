import json
from app import lambda_handler

text = "Does this model even work ?"
event = {"src_lang": "en", "tgt_lang": "fr", "text": text}
event = json.dumps(event)
event = json.loads(event)
context = None

response = lambda_handler(event, context)
print(response)