# Rekognition Video Analyzer
Python serverless project to automate interaction with Amazon Rekognition to analyze videos (label detection) loaded into S3 bucket.

## Prerequisites
Install [serverless framework](https://serverless.com/) using npm   
`npm install serverless -g`

Install [pipenv](https://docs.pipenv.org/en/latest/) to manage a virtualenv and dependencies  
`pip3 install pipenv`

# Development and Deployment
Create `config.dev.json` file based on config template and specify aws profile to use, desired S3 bucket name and Dynamo DB table name. Serverless framework will create those resources on deployment.

To deploy run  
`serverless deploy`

