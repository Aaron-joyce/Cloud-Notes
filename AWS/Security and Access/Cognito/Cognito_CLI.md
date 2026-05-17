# Amazon Cognito CLI Commands

The AWS CLI for Cognito is frequently used by administrators to manually manage user accounts, trigger password resets, or configure pool settings.

*(Note: Cognito commands use `cognito-idp` for User Pools and `cognito-identity` for Identity Pools).*

## 1. List Users in a Pool
View all the registered users in your application.

```bash
aws cognito-idp list-users --user-pool-id us-east-1_xxxxxxxxx
```
**Simple Explanation:** Returns a list of all users in the specified User Pool, including their email addresses, account status (e.g., CONFIRMED or UNCONFIRMED), and when they last logged in.

## 2. Force an Admin Password Reset
If a user is locked out, an admin can explicitly set a temporary password for them.

```bash
aws cognito-idp admin-set-user-password --user-pool-id us-east-1_xxxxxxxxx --username "johndoe@example.com" --password "TempP@ssw0rd!" --permanent
```
**Simple Explanation:** Immediately changes the user's password. The `--permanent` flag means they won't be forced to change it on their next login (remove this flag to make it a temporary password).

## 3. Disable a User Account
Instantly prevent a specific user from logging into your application.

```bash
aws cognito-idp admin-disable-user --user-pool-id us-east-1_xxxxxxxxx --username "badactor@example.com"
```
**Simple Explanation:** Locks the user account. If the user currently has active, valid tokens, they will fail upon the next refresh or authorization check against Cognito.
