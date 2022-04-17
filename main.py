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
