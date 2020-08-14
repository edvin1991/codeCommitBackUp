from git import Repo
import os
import boto3
import shutil
from datetime import datetime
s3 = boto3.client('s3')
os.environ['HOME'] = '/opt/python'
s3Bucket = os.environ['S3BUCKET']
region = os.environ['AWS_REGION']

def lambda_handler(event,context):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
    repositoryName = event['Repository']
    s3_key = '{}/{}/{}_{}.zip'.format(region, repositoryName, repositoryName, dt_string)
    git_url = 'https://git-codecommit.{}.amazonaws.com/v1/repos/{}'.format(region, repositoryName)
    gitDir = '/tmp/{}'.format(repositoryName)
    os.mkdir(gitDir)
    Repo.clone_from(git_url, gitDir)
    if len(os.listdir(gitDir)) == 1:
        shutil.rmtree(gitDir)
    else:
        shutil.make_archive(gitDir, 'zip', gitDir)
        s3.upload_file(gitDir+'.zip', s3Bucket, s3_key)
        os.remove(gitDir+'.zip')
        shutil.rmtree(gitDir)