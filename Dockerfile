FROM public.ecr.aws/lambda/python:3.12

ENV AWS_DEFAULT_REGION=eu-west-3
ENV AWS_ACCESS_KEY_ID=your-aws-access-key
ENV AWS_SECRET_ACCESS_KEY=your-aws-secret-key
ENV AWS_DYNAMODB_TABLE=Project_LLM_Translation_API

WORKDIR /app

COPY ./model /app/model
COPY app.py /app/app.py
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "app.lambda_handler" ]
