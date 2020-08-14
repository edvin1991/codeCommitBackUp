import json
import boto3
import os

codecommit = boto3.client('codecommit')
lambdaClient = boto3.client('lambda')
arn = os.environ['BACKUP_LAMBDA_ARN']
repositories = os.environ['REPOSITORIES']

def lambda_handler(event, context):
    if repositories == "*":
        response = codecommit.list_repositories()['repositories']
        for repository in response:
            inputRepository = {
                "Repository": repository['repositoryName']
            }
            invocation(inputRepository)
    else:
        repositoriesList = repositories.split(",")
        for repository in repositoriesList:
            inputRepository = {
                "Repository": repository
            }
            invocation(inputRepository)


def invocation(repository):
    invocation = lambdaClient.invoke(
            FunctionName = arn,
            InvocationType = 'Event',
            Payload = json.dumps(repository)
            )
    