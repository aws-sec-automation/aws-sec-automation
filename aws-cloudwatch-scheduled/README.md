# AWS Cloudwatch Scheduled Event - Security Automation Solution
![alt text](./AWS_Cloudwatch_remediation.png)

## Getting Started

This cloudformation stack deploys and configures the following resources:

* AWS Lambda
* AWS Lambda Execution Role
* AWS Log Group for sending AWS Lambda logs to Cloudwatch Logs
* IAM Policy
* AWS Cloudwatch Event

## Scenario

In this case a cloudwatch event is programmed to be triggered each one hour. It's not necessary to use AWS Config in this case, only Cloudwatch and the Lambda function provided are needed.
In this scenary we are not working with events but with scheduled actions. Boto3 SDK is used to call the AWS API and receive all the information in order to check three things:

  * If there are Security Groups with the SSH port open to the Internet.
  * If there are buckets with public ACL for reading or writing permissions.
  * If there are users with the MFA deactivated.

  
Once all the information is collected from the API through the SDK, we can remediate the security problems.
1. In the SSH case, it revokes the old rule in the Security Group.
2. For the Public permissions in the S3 buckets, the function is able to change the ACL to a private status.
3. Finally, for the MFA it attaches a restrictive IAM policy to the non compliant user, this policy only allows the user to activate his MFA. When this problem has been solved, in the following execution of the scheduled event, the lambda function will detach the restrictive policy to the user.

## Lambda Function
![alt text](./lambda2.png)

## DEMO
[![Watch Video](https://img.youtube.com/vi/3-K7uLUBQms/0.jpg)](https://www.youtube.com/watch?v=3-K7uLUBQms)

