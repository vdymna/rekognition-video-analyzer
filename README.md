# Rekognition Video Analyzer
Serverless project using Boto3 and Python Lambda functions to automate interaction with Amazon Rekognition to analyze videos. Rekognition label detection analysis is trigger by uploading a video file to configured S3 bucket. The results of the analysis are stored in a DynamoDB table. Video files need to be in mp4 format.

## Prerequisites
Install [serverless framework](https://serverless.com/) using npm   
`npm install serverless -g`

Install [pipenv](https://docs.pipenv.org/en/latest/) to manage a virtualenv and dependencies  
`pip3 install pipenv`

# Development and Deployment
Create `config.dev.json` file based on config template and specify aws profile to use, desired S3 bucket name and DynamoDB table name. Serverless framework will create those resources during deployment.

To deploy run  
`serverless deploy`

