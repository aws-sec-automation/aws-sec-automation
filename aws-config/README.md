# AWS Config Automation

![alt text](./AWS_Config_remediation.png)

## Getting Started

This cloudformation stack deploys and configures the following resources:

* AWS Config
* AWS Config Recorder
* AWS Delivery Channel
* AWS Role for AWS Config
* AWS S3 Bucket (To store AWS Configuration Snapshots)
* AWS Lambda
* AWS Lambda Execution Role
* AWS Log Group for sending AWS Lambda logs to Cloudwatch Logs
* IAM Policy
* AWS Cloudwatch Event rule based on events
* Three AWS Config Rules
