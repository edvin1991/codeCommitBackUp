# CloudFormation Makefile

.ONESHELL:
SHELL := /bin/bash

##Parameters
AWS_REGION			 ?= eu-west-1
S3_BUCKET  		  	 ?= example-bucket
TARGET_S3_BUCKET  	 ?= example-target-bucket
STACK_NAME 		  	 ?= CodeCommitBackUp
SCHEDULED_EXPRESSION ?= 'cron(0 23 ? * FRI *)' 
##System paramteres
current_dir 	:=  $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SOURCE_TEMPLATE	:=	$(current_dir)/cloudFormation.yaml
OUTPUT_TEMPLATE	:=	$(current_dir)/outputtemplate.yaml


createS3bucket:
	@aws s3 mb s3://$(S3_BUCKET) --region $(AWS_REGION)

build: 
	@aws cloudformation package --template-file $(SOURCE_TEMPLATE) \
	 --s3-bucket ehallvax-sam2 \
	 --output-template-file $(OUTPUT_TEMPLATE)

apply: 
	@aws cloudformation deploy \
	--template-file $(OUTPUT_TEMPLATE) \
	--stack-name $(STACK_NAME) \
	--capabilities CAPABILITY_NAMED_IAM \
	--parameter-overrides BucketName=$(TARGET_S3_BUCKET) ScheduledExpression=$(SCHEDULED_EXPRESSION) \
	--region $(AWS_REGION)

deploy: createS3bucket build apply

destroy: 
	@aws cloudformation delete-stack \
	--stack-name $(STACK_NAME) \
	--region $(AWS_REGION)

clean:
	@aws s3 rb s3://$(S3_BUCKET) --force \
	--region $(AWS_REGION)

	
