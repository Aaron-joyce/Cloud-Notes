# AWS Config CLI Commands

AWS Config tracks the setup of your resources. The CLI allows you to query this data and check if you are following the rules.

## 1. Check Rule Compliance
See a summary of whether your resources are passing or failing your compliance rules.

```bash
aws configservice describe-compliance-by-config-rule
```
**Simple Explanation:** Shows you a list of all your active Config Rules and tells you if they are currently "COMPLIANT" or "NON_COMPLIANT".

## 2. Get Resource History
Look up the configuration history of a specific resource to see how it has changed over time.

```bash
aws configservice get-resource-config-history --resource-type AWS::EC2::Instance --resource-id i-1234567890abcdef0
```
**Simple Explanation:** Pulls up a timeline of every setting change made to the specified EC2 instance.
