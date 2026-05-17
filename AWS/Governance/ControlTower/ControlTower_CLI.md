# AWS Control Tower CLI Commands

Control Tower is mostly managed via the AWS Console, but the CLI allows you to manage the specific governance rules (controls) it enforces.

## 1. List Enabled Controls
See what rules are currently turned on for a specific folder of accounts (Organizational Unit).

```bash
aws controltower list-enabled-controls --target-identifier arn:aws:organizations::123456789012:ou/o-exampleou/ou-example
```
**Simple Explanation:** Lists all the active security guardrails currently protecting the specified Organizational Unit (OU).

## 2. Enable a New Control
Turn on a specific security rule for an Organizational Unit.

```bash
aws controltower enable-control --control-identifier arn:aws:controltower:us-east-1::control/EXAMPLE_NAME --target-identifier arn:aws:organizations::123456789012:ou/o-exampleou/ou-example
```
**Simple Explanation:** Activates a specific rule (identified by the `control-identifier`) for a specific group of accounts.
