# CodeCommit Repositories backup

## Description: 
This package provides cloudformation and python source code for deployment of a codecommit repository backup solution in specified region. The solution periodically will pull the content from codecommit repositories and dump them into an S3 bucket. BackUpRepo.drawio or BackUpRepo.png gived an overview of the solution architecture.

CloudWatch Event Rules triggers Triggerbackup Lambda which lists all the repositories in codecommit.
Than it invokes in asynchronous manner ExecuteBackup Lambda which clones the master branch of the repo and dumps into S3. 

The TriggerBackup function takes two parameters via environment variables:
"BACKUP_LAMBDA_ARN" - ARN of ExecuteBackup Lambda (automatically parsed within cloudformation template)
"REPOSITORIES" - Optionally you can pass the list of repos you want to backup rather than backing up all the repos. You need to pass the environment variable as a string array, like:
"repo1,repo2,repo3,repo4". Default value is set to "*"

The TriggerBackup function takes one parameter via environment variables:
"S3BUCKET" - Target S3 bucket where to dump repositories content.



## Prerequisits:
This module requires following pre-requists to be create berfore hand:
- Target S3 bucket where to backup the repositories

This pre-requisits can be deployed using provided cloudformation template:
```bash
aws s3 mb s3://bucket-name --region region-name
```

## Deployment commands: 
All deployemnts are done using makefile, following commands are available: 
 - ```make createS3bucket```    - creates S3 bucket where this command uploads the artifacts that are referenced in your template
 - ```make build```             - Packages the local artifacts (local paths) that your AWS CloudFormation template references.
 - ```make apply```             - Deploys  the specified AWS CloudFormation template by creating and then executing a change set. 
 - ```make deploy```            - executes make createS3bucket, make build and make apply
 - ```make destroy```           - destroies cloudformation stack
 - ```make clean```             - deletes the artifact bucket


## Parametrising deployment:
Deployments can be parametrised by providing variable for make commands i.e.:
```make deploy AWS_REGION=eu-central-1 3_BUCKET=example-bucket TARGET_S3_BUCKET=example-target-bucket STACK_NAME=BackUp``` - will deploy  in eu-central-1 for base region, create artifact bucket "example-bucket" and override cloudformation parameter BucketName to example-target-bucket



Following terraform paramteres are available for override: 
 - ```BucketName```             - Target S3 bucket where to backup the repositories
 - ```ScheduledExpression```     - Cron according to which backup will be triggered. Default "cron(0 23 ? * FRI *)"

