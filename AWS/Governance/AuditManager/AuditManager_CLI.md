# AWS Audit Manager CLI Commands

The Audit Manager CLI allows you to start assessments and retrieve evidence for compliance reporting.

## 1. List Available Frameworks
Find the compliance frameworks (like PCI-DSS or GDPR) that AWS provides out of the box.

```bash
aws auditmanager list-assessment-frameworks --framework-type Standard
```
**Simple Explanation:** Returns a list of all the standard regulatory templates you can use to start an audit.

## 2. Start a New Assessment
Begin collecting evidence for a specific compliance audit.

```bash
aws auditmanager create-assessment --name "Annual_PCI_Audit" --assessment-reports-destination destinationType=S3,destination=s3://my-audit-reports-bucket --roles roleType=PROCESS_OWNER,roleArn=arn:aws:iam::123456789012:role/AuditAdmin --framework-id a1b2c3d4
```
**Simple Explanation:** Starts a new audit called "Annual_PCI_Audit" based on a specific framework, assigns an owner, and tells AWS to save the final report in your S3 bucket.
