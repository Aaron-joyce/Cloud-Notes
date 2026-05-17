# AWS Systems Manager (SSM) CLI Commands

Systems Manager has many features. The CLI is heavily used for Parameter Store (secrets) and Run Command (running scripts on servers remotely).

## 1. Save a Secret in Parameter Store
Store a configuration value (like a database password) securely.

```bash
aws ssm put-parameter --name "/myapp/db-password" --value "SuperSecret123!" --type SecureString
```
**Simple Explanation:** Saves a new parameter named "/myapp/db-password". The `SecureString` type tells AWS to encrypt it before saving.

## 2. Retrieve a Secret
Get a value back from Parameter Store.

```bash
aws ssm get-parameter --name "/myapp/db-password" --with-decryption
```
**Simple Explanation:** Fetches the value you saved earlier and decrypts it so you can read the actual password.

## 3. Run a Command on a Server
Execute a script on an EC2 instance without needing to SSH into it.

```bash
aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids "i-1234567890abcdef0" --parameters commands=["yum update -y"]
```
**Simple Explanation:** Tells AWS to silently connect to the specified EC2 instance and run the server update command.
