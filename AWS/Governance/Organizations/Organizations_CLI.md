# AWS Organizations CLI Commands

This guide covers basic AWS CLI commands to manage your AWS Organizations setup.

## 1. Create a New Organization
If you are starting fresh, this command turns your current AWS account into the master account of a new organization.

```bash
aws organizations create-organization --feature-set ALL
```
**Simple Explanation:** Creates a new organization with all features enabled (allowing you to use Service Control Policies, not just consolidated billing).

## 2. List Accounts in the Organization
To see all the AWS accounts that are currently part of your organization.

```bash
aws organizations list-accounts
```
**Simple Explanation:** Returns a list of every account (and its details like Email and Account ID) under your central management.

## 3. Create an Organizational Unit (OU)
OUs are folders where you can group accounts together.

```bash
aws organizations create-organizational-unit --parent-id r-examplerootid --name "Production_OU"
```
**Simple Explanation:** Creates a new folder (OU) named "Production_OU" under your main organization root. You replace `r-examplerootid` with your actual root ID.
