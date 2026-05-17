# AWS CloudTrail & Security Monitoring Runbook
**Project:** Securing S3 Origins with CloudFront, CloudTrail, and CloudWatch.

---

## 1. CloudTrail Configuration (The Audit Layer)
CloudTrail is your source of truth. For this project, you must capture both **Management Events** (who changed the bucket policy) and **Data Events** (who accessed the `index.html`).

### **Setup Steps**
1.  **Create a Trail:**
    * Navigate to **CloudTrail > Trails > Create trail**.
    * **Trail name:** `SecurityAuditTrail`.
    * **Storage location:** Create a new S3 bucket (e.g., `cloudtrail-logs-unique-id`).
2.  **Enable CloudWatch Logs (Crucial for Real-time Debugging):**
    * Check the **Enabled** box under the CloudWatch Logs section.
    * **Log Group:** Keep the default `/aws/cloudtrail/SecurityAuditTrail`.
    * **IAM Role:** Click **Next** to allow AWS to create a service-linked role.
3.  **Configure Event Selectors:**
    * **Management Events:** Keep "Read" and "Write" enabled.
    * **Data Events:** * Data event source: **S3**.
        * Under **Individual bucket selection**, browse and select your website bucket (`website-bucket-07102004`).
        * Ensure both **Read** and **Write** are checked.
4.  **Review and Create.**

---

## 2. Common Error Cases & Debugging
When working with CloudFront and S3, "Access Denied" is the most common hurdle. Use this table to diagnose the root cause.

| Error Symptom | Potential Cause | How to Debug (CloudTrail/CloudWatch) |
| :--- | :--- | :--- |
| **403 Forbidden** (Browser) | S3 Bucket Policy is missing OAC permissions. | Search CloudWatch Logs for `errorCode: AccessDenied`. Check if `userIdentity` is `cloudfront.amazonaws.com`. |
| **Empty Logs** in CloudWatch | Data Events not enabled or IAM Role lacks permissions. | Check Trail settings. Ensure "Data Events" specifically lists your S3 bucket ARN. |
| **404 Not Found** | Default Root Object not set in CloudFront. | In CloudTrail, look for a `GetObject` event where the `key` is empty or just `/`. |
| **Delayed Logs** | AWS Processing Latency. | Wait 5–15 minutes. CloudTrail is not instantaneous. |

---

## 3. Step-by-Step Debugging Workflow
If you see an error in your browser, follow this "Triangle of Truth" workflow:

### **Phase A: The CloudFront Check**
* **Is it Deployed?** Check Distribution Status. If "Deploying," your changes aren't live.
* **Is OAC Selected?** Go to **Origins > Edit**. Ensure "Origin access control settings" is selected, not "Public."

### **Phase B: The S3 Policy Check**
* Does the policy include `/*`? 
    * *Fix:* `arn:aws:s3:::bucket-name/*`
* Does the `SourceArn` match your Distribution ARN?
    * *Fix:* Copy the ARN from the CloudFront General tab and paste it into the S3 Policy `Condition` block.

### **Phase C: The CloudWatch Deep Dive**
Use **CloudWatch Logs Insights** to find the exact reason for failure. Run this query:
```sql
fields @timestamp, eventName, errorCode, errorMessage, userIdentity.invokedBy
| filter errorCode = "AccessDenied"
| sort @timestamp desc
| limit 20
```
* **If `invokedBy` is empty:** The request never reached S3. Check CloudFront Geo-restrictions or WAF.
* **If `invokedBy` is `cloudfront.amazonaws.com`:** S3 received the request but rejected it. Your Bucket Policy is definitely the issue.

---

## 4. Solving the "Access Denied" Loop
If you have fixed the policy but the error persists:
1.  **Invalidate Cache:** CloudFront caches the "403 Forbidden" response. 
    * Go to **CloudFront > Invalidations > Create Invalidation**.
    * Object Path: `/*`.
2.  **Check Object Ownership:** * In S3, go to **Permissions > Object Ownership**.
    * Set to **Bucket owner enforced**. This ensures the policy has the right to grant access to the files.

---

## 5. Summary Checklist for Success
* [ ] CloudTrail is logging **Data Events** for the specific S3 bucket.
* [ ] CloudWatch Log Group shows recent `GetObject` activity.
* [ ] CloudFront has `index.html` set as the **Default Root Object**.
* [ ] S3 Bucket Policy grants `s3:GetObject` to the `cloudfront.amazonaws.com` service principal.

***

### **Pro-Tip for IndiaSkills Competition:**
In a timed environment, the **Invalidation** step is often forgotten. If you fix a setting and nothing changes, **invalidate the cache immediately**. It is the most common reason students lose points while troubleshooting correctly!