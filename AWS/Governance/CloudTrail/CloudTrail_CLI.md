# AWS CloudTrail CLI Commands

CloudTrail is your audit log. The CLI is very useful for quickly searching these logs to see who did what.

## 1. Look Up Recent Events
Search your audit logs for recent activity.

```bash
aws cloudtrail lookup-events --max-items 10
```
**Simple Explanation:** Grabs the 10 most recent actions (like someone logging in or deleting a file) that happened in your AWS account.

## 2. Search for a Specific Action
Find out who triggered a specific event, like deleting a server.

```bash
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=TerminateInstances
```
**Simple Explanation:** Filters your audit logs to only show times when someone used the "TerminateInstances" command to delete a server.
