# Amazon Cognito

Amazon Cognito is an identity and access management service that provides authentication, authorization, and user management for web and mobile apps.

## 1. Identity Architecture & Directories

### User Pools
A managed identity directory that handles sign-up, sign-in, and stores user profile attributes. It provides a secure user directory that scales to hundreds of millions of users.

### Identity Pools (Federated Identities)
Allows you to grant your users access to other AWS services. It works by exchanging third-party tokens (like Google, Facebook, or tokens from a User Pool) for temporary, limited-privilege AWS IAM credentials.

### App Clients & Secrets
- **App Clients**: Entities within a User Pool that represent a specific application (e.g., your iOS app vs your web app) connecting to Cognito.
- **Client Secrets**: Used for server-side applications to authenticate. Cognito supports App Client Secrets Rotation to maintain high security without downtime.

### Multi-Tenancy Design Patterns
When building SaaS apps:
- **Pool-per-tenant**: Creates a separate User Pool for every tenant (highest isolation, harder to manage at scale).
- **Group-per-tenant**: Uses a single User Pool but assigns users to specific IAM/Cognito Groups representing their tenant (easier to manage, shared infrastructure).

## 2. Authentication, Tokens, & Standards

### OAuth 2.0 Grant Flows
- **Authorization Code Grant with PKCE**: The recommended, highly secure flow for web and mobile apps.
- **Client Credentials**: Used for Machine-to-Machine (M2M) communication where no human user is present.

### JSON Web Tokens (JWT) Management
Cognito issues three types of tokens upon successful authentication:
1. **ID Token**: Contains claims about the identity of the authenticated user (name, email).
2. **Access Token**: Contains scopes and groups, used to authorize API calls (e.g., to API Gateway).
3. **Refresh Token**: Used to fetch new ID and Access tokens when they expire without requiring the user to log in again. Cognito allows extensive customization of token lifespans and **Refresh Token Rotation Mechanics** for enhanced security.

### Inbound Federation
Cognito supports enterprise federation, allowing users to log in using their corporate identities via **OpenID Connect (OIDC)** and **SAML 2.0**.

## 3. Security, Governance, & Customization

### Core Feature Tiers
Cognito offers varying levels of features:
- **Lite**: Basic authentication.
- **Essentials**: Standard use cases.
- **Plus**: Unlocks the highest tier of security and analytics.

### Advanced Security Features (Plus Tier)
- **Adaptive Authentication**: Evaluates the risk of a sign-in attempt (based on location, device, etc.) and can prompt for MFA if the risk is high.
- **Compromised Credentials Detection**: Blocks logins if the user's password has been found in a public data breach.

### Hosted UI & Branding
Cognito provides a **Managed Login Experience**, offering a hosted UI that developers can quickly deploy and customize via Visual Editors to match their brand.

### AWS WAF Integration
You can natively integrate AWS Web Application Firewall (WAF) directly with Cognito hosted login endpoints to protect against brute-force attacks and botnets.

### Custom Lambda Triggers
You can customize the authentication workflow by triggering AWS Lambda functions at specific lifecycle events:
- **Pre-Sign-up**: To auto-confirm users or perform custom validation.
- **Pre-Token Generation**: To add custom claims or attributes to the JWT before it is sent to the user.
- **Post-Authentication**: To log login events or sync user data to a database.
- **Custom Message**: To dynamically generate customized email or SMS verification messages.
