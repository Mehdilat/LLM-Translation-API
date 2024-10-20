import json
import boto3
from boto3.dynamodb.conditions import Key
import os
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from uuid import uuid4
from datetime import datetime

AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DYNAMODB_TABLE = os.getenv('AWS_DYNAMODB_TABLE')

dynamodb = boto3.resource('dynamodb', region_name = AWS_DEFAULT_REGION, aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
table = dynamodb.Table(AWS_DYNAMODB_TABLE)

SUPPORTED_LANGUAGES = ["en", "fr", "de"]

def query_total(table):

    total_count = 0
    last_evaluated_key = None
    
    while True:
        scan_params = {
            'Select': 'COUNT'
        }
        
        if last_evaluated_key:
            scan_params['ExclusiveStartKey'] = last_evaluated_key
        
        response = table.scan(**scan_params)
        
        total_count += response.get('Count', 0)
        
        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break

    return total_count

def lambda_handler(event, context):
    #1. Parse out query string params
    
    inferenceSrcLang = event.get('src_lang')
    inferenceTgtLang = event.get('tgt_lang')
    inferenceText = event.get('text', 'N/A')

    if inferenceSrcLang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported source language: {inferenceSrcLang}. Supported languages are: {', '.join(SUPPORTED_LANGUAGES)}")
    if inferenceTgtLang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported target language: {inferenceTgtLang}. Supported languages are: {', '.join(SUPPORTED_LANGUAGES)}")
    if inferenceSrcLang == inferenceTgtLang:
        raise ValueError("Source and target languages must be different")
    
    #2. Perform Inference
    #model_path = '/var/task/model'
    model_path = './model'

    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    task = f"translation_{inferenceSrcLang}_to_{inferenceTgtLang}"
    pipe = pipeline(task, model=model, tokenizer=tokenizer)

    translatedText = pipe(inferenceText)[0]['translation_text']            

    #3. Write into DynamoDB database
    translation_record = {
        'id': str(uuid4()),
        'text': inferenceText,
        'translated_text': translatedText,
        'src_lang': inferenceSrcLang,
        'tgt_lang': inferenceTgtLang,
        'timestamp': str(datetime.utcnow())
    }
    table.put_item(Item=translation_record)
    count = query_total(table)

    #4. Construct the body of the http response object and the object itself
    InferenceResponse = {}
    InferenceResponse['translated text'] = translatedText
    InferenceResponse['total translations'] = count

    response = {
        'statusCode': 200,
        'body': json.dumps(InferenceResponse)
    }

    return response
