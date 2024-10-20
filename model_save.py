from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = 'google-t5/t5-base'

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

model.save_pretrained('./model')
tokenizer.save_pretrained('./model')