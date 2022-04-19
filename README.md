# cdktf-python-aws-iam

The Cloud Development Kit for Terraform (CDKTF) allows you to define your infrastructure in a familiar programming language such as TypeScript, Python, Go, C#, or Java.

In this tutorial, you will provision an EC2 instance on AWS using your preferred programming language.

## Prerequisites

* [Terraform](https://www.terraform.io/downloads) >= v1.0
* [CDK for Terraform](https://learn.hashicorp.com/tutorials/terraform/cdktf-install) >= v0.8
* A [Terraform Cloud](https://app.terraform.io/) account, with [CLI authentication](https://learn.hashicorp.com/tutorials/terraform/cloud-login) configured
* [an AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=default&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start)
* AWS Credentials [configured for use with Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication)


Credentials can be provided by using the AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and optionally AWS_SESSION_TOKEN environment variables. The region can be set using the AWS_REGION or AWS_DEFAULT_REGION environment variables.

```shell
$ export AWS_ACCESS_KEY_ID="anaccesskey"
$ export AWS_SECRET_ACCESS_KEY="asecretkey"
$ export AWS_REGION="us-west-2"
```

## Install project dependencies

```shell
mkdir learn-cdktf
cd learn-cdktf
cdktf init --template="python"
```

## Install AWS provider

```shell
pipenv install cdktf-cdktf-provider-aws
```

## Define your CDK for Terraform Application

Replace the contents of main.py with the following code for a new Python application

```python
#!/usr/bin/env python
import cdktf_cdktf_provider_aws
from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_aws import AwsProvider, iam

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # define resources here
        myRegion = "us-east-1"
        AwsProvider(self, 'aws', region=myRegion)
        
        newGroup = iam.IamGroup(self, 'mygroup', name="group-devops")

        newUser = iam.IamUser(self, 'myuser', name="user1")

        assumeRole='''{
        Version: "2012-10-17",
        Statement: [
          {
            Action: "sts:AssumeRole",
            Principal: {
              Service: "ec2.amazonaws.com",
            },
            Effect: "Allow",
          },
        ],
      }'''

        role = iam.IamRole(self, 'iam-role',assume_role_policy=assumeRole)
        
        
        policy = '''
        {
        Version: "2012-10-17",
        Statement: [
          {
            Action: "*",
            Resource: ["arn:aws:ec2:*:*:client-vpn-endpoint/*"],
            Effect: "Allow",
          },
        ],
      } '''
        role_policy = iam.IamPolicy(self, "iam-policy", policy=policy)


        membership = iam.IamGroupMembership(self, "group-membership",name="group-membership", group=newGroup.name, users=[newUser.name])
       
        role_attachement = iam.IamPolicyAttachment(self,"application-managed-policy",name="iampolicyattachement", groups=[newGroup.name],roles=[role.name],policy_arn=role_policy.arn,users=[newUser.name])


app = App()
MyStack(app, "cdktf-python-aws-iam")

app.synth()

```
## Provision infrastructure
```shell
cdktf deploy
```
After the instance is created, visit the AWS EC2 Dashboard.

## Clean up your infrastructure
```shell
cdktf destroy
```