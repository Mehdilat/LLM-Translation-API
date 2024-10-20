from transformers import pipeline

text = "Launch this python code to test the model's effectiveness at translation!"

src_lang='en'
tgt_lang='de'
task = f"translation_{src_lang}_to_{tgt_lang}"

print(task)
print("translation_en_to_fr")
pipe = pipeline(task, model="google-t5/t5-base")

translated_text = pipe(text)[0]['translation_text']

print(translated_text)
