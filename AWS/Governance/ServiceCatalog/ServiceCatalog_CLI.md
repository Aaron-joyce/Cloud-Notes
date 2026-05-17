# AWS Service Catalog CLI Commands

The Service Catalog CLI allows users to view and launch pre-approved infrastructure templates (Products).

## 1. See What You Are Allowed to Launch
Find out what approved products the administrators have made available to you.

```bash
aws servicecatalog search-products-as-admin
```
*(For regular users, use `search-products` instead).*

**Simple Explanation:** Lists all the IT-approved products (like "Standard Web Server" or "Data Science Workspace") that you are allowed to deploy.

## 2. Launch an Approved Product
Provision one of the approved templates.

```bash
aws servicecatalog provision-product --product-id prod-abc123def456 --provisioning-artifact-id pa-xyz789 --provisioned-product-name "MyDataWorkspace"
```
**Simple Explanation:** Tells AWS to build the specific product you selected. It's like clicking "Buy" on an internal company app store.
