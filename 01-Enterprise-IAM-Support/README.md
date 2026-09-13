# Enterprise IAM Support & Identity Security Lab

## Overview

This project demonstrates a practical Identity and Access Management (IAM) environment built with Keycloak and two Flask test applications.

The lab was designed to develop hands-on experience with identity administration, Role-Based Access Control (RBAC), Joiner-Mover-Leaver lifecycle management, Multi-Factor Authentication (MFA), OpenID Connect (OIDC), application authorization, Single Sign-On (SSO), and IAM event investigation.

The environment was built and tested in a controlled home lab.

---

## IAM Scenario

A centralized IAM environment was created to simulate common enterprise identity and application-access requirements.

The environment included:

- Centralized identity management with Keycloak
- Department-based groups
- Role-Based Access Control
- Standard and privileged access
- Joiner-Mover-Leaver lifecycle changes
- TOTP Multi-Factor Authentication
- OpenID Connect application integration
- Authorization based on identity claims
- Single Sign-On across multiple applications
- Authentication-event investigation
- Administrative audit-event review

Two local test applications were used:

- Finance Portal
- Employee Portal

The applications were created specifically to validate IAM authentication, authorization, and SSO behavior.

---

## IAM Workflow

### 1. Keycloak Realm

A dedicated Keycloak realm was created:

```text
enterprise-iam-lab
```

The realm was kept separate from the Keycloak `master` realm used for platform administration.

---

### 2. Role-Based Access Control

Custom realm roles were created:

```text
employee
finance-user
finance-admin
it-support
```

Two department groups were configured:

```text
Finance
IT-Support
```

Role mapping:

```text
Finance
├── employee
└── finance-user

IT-Support
├── employee
└── it-support
```

The privileged `finance-admin` role was intentionally kept separate from normal Finance group access.

This allowed privileged access to be assigned directly only where required.

---

### 3. User and Access Validation

Multiple test identities were created to validate different access scenarios.

Examples included:

- Standard Finance access through group membership
- Standard IT Support access through group membership
- Privileged Finance access through a direct administrator role

Inherited and directly assigned roles were reviewed to verify effective access.

---

### 4. Joiner-Mover-Leaver Lifecycle

The identity lifecycle was tested using controlled user changes.

#### Joiner

A new employee identity was created and assigned to the Finance group.

The user inherited the appropriate Finance roles through group membership.

#### Mover

The same identity was moved from Finance to IT-Support.

The old group membership was removed and the new group membership was assigned.

Effective access changed accordingly.

#### Leaver

The test identity was disabled, active sessions were reviewed, and remaining group access was removed.

This demonstrated the importance of removing access when an identity leaves the organization.

---

### 5. Multi-Factor Authentication

TOTP-based Multi-Factor Authentication was configured and tested.

The authentication flow required:

```text
Username
    ↓
Password
    ↓
TOTP
    ↓
Authentication Successful
```

MFA enrollment and successful OTP authentication were verified without publishing QR codes, OTP secrets, or live one-time passwords.

---

### 6. OpenID Connect Integration

A Flask-based Finance Portal was integrated with Keycloak using OpenID Connect.

Client:

```text
finance-portal
```

The client used:

- OpenID Connect
- Authorization Code Flow
- PKCE S256
- Public-client configuration
- No client secret

The authentication flow was:

```text
Finance Portal
      ↓
Keycloak
      ↓
User Authentication
      ↓
Authorization Code
      ↓
Application Callback
      ↓
Token Exchange
      ↓
Application Session
```

---

### 7. Application Authorization

Authentication and authorization were intentionally tested as separate controls.

The Finance Portal required:

```text
finance-user
```

A user from the IT-Support group successfully authenticated through Keycloak but did not possess the required Finance role.

Result:

```text
Authentication: Successful
Authorization: Denied
HTTP Status: 403
```

This demonstrated that successful authentication does not automatically mean that a user is authorized to access an application.

---

### 8. OIDC Role-Claim Troubleshooting

During testing, a Finance user had the correct Keycloak role but was initially denied application access.

The investigation followed the complete identity path:

```text
User
  ↓
Group
  ↓
Role
  ↓
OIDC Claim
  ↓
Application Authorization
```

The Keycloak role assignment was correct, but the expected realm-role information was not available to the application in the required claim.

A realm-role protocol mapper was configured so that roles were exposed through:

```text
realm_access.roles
```

After a fresh authentication session, the Finance user was successfully authorized.

This provided a practical example of troubleshooting an IAM issue where:

```text
Identity configuration was correct
        ↓
Authentication succeeded
        ↓
Application still denied access
        ↓
Token / claim mapping investigated
        ↓
Authorization restored
```

---

### 9. Single Sign-On

A second Flask application was created:

```text
employee-portal
```

Both applications trusted the same Keycloak realm.

After authenticating to the Finance Portal, the Employee Portal was opened within the same browser session.

Keycloak reused the existing authenticated session and no additional username, password, or MFA challenge was required.

This validated Single Sign-On across the two applications.

---

### 10. Authentication Event Investigation

Keycloak user-event logging was enabled.

A controlled incorrect-password attempt was generated.

The resulting event showed:

```text
LOGIN_ERROR
```

with:

```text
invalid_user_credentials
```

The event was reviewed to understand how failed authentication activity can be investigated using IAM logs.

---

### 11. Administrative Audit Events

Administrative event logging was enabled to record IAM configuration changes.

A temporary test realm role was created and then deleted.

The administrative audit trail recorded both:

```text
CREATE
DELETE
```

events.

This demonstrated how IAM administrative changes can be reviewed for audit and troubleshooting purposes.

---

## Key Tools and Techniques

- Keycloak
- Identity and Access Management
- Role-Based Access Control
- Least Privilege
- User and Group Administration
- Joiner-Mover-Leaver Lifecycle
- Multi-Factor Authentication
- TOTP
- OpenID Connect
- OAuth 2.0 concepts
- Authorization Code Flow
- PKCE S256
- Identity Claims
- Application Authorization
- Single Sign-On
- User Event Investigation
- Administrative Audit Events
- Linux
- Python
- Flask
- Authlib
- IAM Troubleshooting
- Access Validation

---

## IAM Validation Results

The lab successfully demonstrated the following scenarios:

- Dedicated IAM realm created
- Custom roles configured
- Department groups configured
- Group-based role inheritance verified
- Privileged direct-role assignment verified
- Joiner access provisioning tested
- Mover access changes tested
- Leaver account disabling and access removal tested
- TOTP MFA enrollment and authentication verified
- Finance Portal integrated using OIDC
- PKCE S256 used with the public OIDC client
- Successful authentication verified
- Authentication-success / authorization-denied scenario verified
- Realm-role claim issue identified and corrected
- Finance application authorization verified
- SSO across two applications verified
- Controlled failed-login event investigated
- Administrative CREATE and DELETE events reviewed

A key troubleshooting lesson from the project was that application-access problems should be investigated across the complete identity chain rather than assuming that successful login means the access configuration is correct.

The investigation path used was:

```text
User
  ↓
Account Status
  ↓
Group Membership
  ↓
Role Assignment
  ↓
Authentication
  ↓
MFA
  ↓
OIDC Client
  ↓
Claims
  ↓
Application Authorization
  ↓
Events / Audit Logs
```

---

## Evidence

Sanitized screenshots documenting the IAM implementation and validation are available in:

[`Screenshots/`](Screenshots/)

The evidence set covers:

- Realm creation
- Role configuration
- Group-role mapping
- Role inheritance
- Privileged access
- Joiner-Mover-Leaver lifecycle
- MFA
- OIDC authentication
- Authorization denial
- Successful application authorization
- SSO
- Authentication-event investigation
- Administrative audit events

Screenshots intended for the public repository were reviewed and sanitized before publication.

---

## Detailed IAM Report

Detailed technical documentation is maintained in:

[`Documentation/Enterprise-IAM-Support.md`](Documentation/Enterprise-IAM-Support.md)

The detailed documentation contains the implementation steps, IAM concepts, configuration decisions, troubleshooting process, validation results, evidence references, and lessons learned during the project.

Additional project components are maintained in:

- [`Architecture/`](Architecture/)
- [`Applications/`](Applications/)
- [`Screenshots/`](Screenshots/)

The application directory contains the sanitized source used for the Finance Portal and Employee Portal test applications.

---

## Skills Demonstrated

- Identity and Access Management
- Keycloak Administration
- User Lifecycle Management
- Role-Based Access Control
- Least-Privilege Access
- Group-Based Access Management
- Privileged Role Assignment
- Multi-Factor Authentication
- TOTP
- OpenID Connect
- OAuth 2.0 Concepts
- PKCE
- Identity Claims
- Authentication Troubleshooting
- Authorization Troubleshooting
- Application Access Control
- Single Sign-On
- Identity Event Investigation
- Administrative Audit Logging
- Linux Administration
- Python
- Flask
- Technical Troubleshooting
- Evidence Collection
- Technical Documentation

---

## Outcome

The project successfully demonstrated a practical enterprise-style IAM workflow covering identity creation, access assignment, lifecycle changes, strong authentication, application integration, authorization, SSO, event investigation, and administrative auditing.

The lab also demonstrated an important IAM support principle:

```text
Successful Authentication ≠ Successful Authorization
```

Access issues may exist at multiple layers including account status, group membership, role assignment, identity claims, application configuration, and authorization logic.

The project therefore focused not only on configuring IAM controls, but also on understanding how to systematically investigate and troubleshoot identity and application-access problems.

---

## Repository Information

- **Repository:** Enterprise-IAM-Support-Lab
- **Section:** 01-Enterprise-IAM-Support
- **Lab:** Enterprise IAM Support & Identity Security Lab
- **Documentation:** Documentation/Enterprise-IAM-Support.md
- **Architecture:** Architecture/
- **Applications:** Applications/
- **Screenshots:** Screenshots/
- **Status:** Completed
- **Environment:** Controlled Home Lab
- **Platforms:** Keycloak, Linux, Python, Flask, OIDC
- **Version:** 1.0
