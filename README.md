# Automated LLM-Based Multi-Language Translation API

This project implements an Automated Multi-Language Translation API utilizing a Large Language Model (LLM). The API is designed to translate text between supported languages (English, French, and German) using AWS services and Docker for deployment.

## Technologies Used
- **AWS Services**: AWS Lambda, Amazon DynamoDB.
- **Containerization**: Docker for deploying the application.
- **Continuous Integration/Continuous Deployment (CI/CD)**: Jenkins for automating the build and deployment processes.
- **Machine Learning**: Hugging Face Transformers for handling the translation model.

## Supported Languages
- English (en)
- French (fr)
- German (de)

## Usage
1. Deploy the application to AWS using the CI/CD pipeline.
2. Invoke the Lambda function with a JSON payload specifying the source language, target language, and text to translate.
3. The function will return the translated text along with the total translation count from DynamoDB.

## Example Payload
```json
{
  "src_lang": "en",
  "tgt_lang": "fr",
  "text": "Does this model even work?"
}
