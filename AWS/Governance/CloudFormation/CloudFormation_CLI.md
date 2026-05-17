# AWS CloudFormation CLI Commands

The CloudFormation CLI is how you deploy and manage your Infrastructure as Code templates.

## 1. Deploy a Template (Create a Stack)
Take a template file and tell AWS to build the resources inside it.

```bash
aws cloudformation create-stack --stack-name MyNetworkStack --template-body file://network-template.yaml
```
**Simple Explanation:** Uploads the `network-template.yaml` file from your computer and builds all the resources in it, grouping them under the name "MyNetworkStack".

## 2. Check the Status of a Deployment
See if your stack is still building or if it finished successfully.

```bash
aws cloudformation describe-stacks --stack-name MyNetworkStack
```
**Simple Explanation:** Returns details about the stack, most importantly its current `StackStatus` (like `CREATE_IN_PROGRESS` or `CREATE_COMPLETE`).

## 3. Delete a Stack
Tear down everything you built with a template.

```bash
aws cloudformation delete-stack --stack-name MyNetworkStack
```
**Simple Explanation:** Safely deletes every single resource that was created as part of "MyNetworkStack", ensuring nothing is left behind.
