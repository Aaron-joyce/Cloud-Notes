# Amazon CloudFront CLI Commands

The AWS CLI for CloudFront is primarily used for automating cache clearing (invalidations) and managing distribution settings.

## 1. List Distributions
Find the IDs and status of all your CloudFront distributions.

```bash
aws cloudfront list-distributions
```
**Simple Explanation:** Returns a list of all your CDNs, showing their domain names (like `d111111abcdef8.cloudfront.net`) and exactly which origins they connect to.

## 2. Invalidate the Cache
Force CloudFront to clear its cache so users see the newest version of your files immediately.

```bash
aws cloudfront create-invalidation --distribution-id EDFDVBD632BHDS5 --paths "/*"
```
**Simple Explanation:** Tells CloudFront to delete every single cached file (`/*`) for this specific distribution. The next time a user visits the site, CloudFront will fetch the fresh files directly from your origin server.

## 3. Check Invalidation Status
Check if the cache has finished clearing.

```bash
aws cloudfront get-invalidation --distribution-id EDFDVBD632BHDS5 --id I2J0I21PEYTNWS
```
**Simple Explanation:** Using the Invalidation ID you got from the previous command, this checks if the invalidation process is still "InProgress" or has "Completed" across the global edge network.
