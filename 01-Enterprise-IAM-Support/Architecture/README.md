# Enterprise IAM Support Architecture

This document describes the end-to-end architecture used in the Enterprise IAM Support & Identity Security Lab.

## Architecture Flow

```text
Users
  |
  v
Keycloak
enterprise-iam-lab
  |
  +-----------------------------+
  |                             |
  v                             v
Groups                       Authentication
Finance                      Password + MFA
IT-Support                       |
  |                              v
  v                         OIDC / PKCE
Realm Roles                      |
employee                         v
finance-user                Applications
finance-admin              Finance Portal
it-support                 Employee Portal
  |                             |
  +-------------+---------------+
                |
                v
        Authorization Decision
                |
        +-------+-------+
        |               |
        v               v
   Access Granted    Access Denied
        |
        v
   SSO Session
        |
        v
User Events + Admin Audit Events
```

## Identity Layer

Keycloak was used as the centralized Identity and Access Management platform.

A dedicated realm was created:

```text
enterprise-iam-lab
```

The realm contained:

- Users
- Groups
- Realm roles
- Authentication configuration
- OIDC clients
- User sessions
- User events
- Administrative events

The Keycloak `master` realm remained separate for platform administration.

## Access Control Layer

### Groups

Department-based groups were used to organize identities:

```text
Finance
IT-Support
```

### Roles

Custom realm roles were used to represent access:

```text
employee
finance-user
finance-admin
it-support
```

Standard access was inherited through group membership.

The elevated `finance-admin` role was assigned only to a selected privileged identity.

This demonstrated Role-Based Access Control and least privilege.

## Identity Lifecycle Layer

The lab implemented the Joiner-Mover-Leaver lifecycle.

```text
Joiner
  ↓
Create Identity
  ↓
Assign Group
  ↓
Receive Required Roles

Mover
  ↓
Remove Old Group
  ↓
Assign New Group
  ↓
Update Effective Access

Leaver
  ↓
Disable Identity
  ↓
Review Sessions
  ↓
Remove Remaining Access
```

## Authentication Layer

Password authentication was combined with TOTP-based Multi-Factor Authentication.

```text
Username
   ↓
Password
   ↓
TOTP
   ↓
Authentication Successful
```

MFA secrets, QR codes, and live one-time codes are not included in the public repository.

## Application Integration Layer

Two locally hosted test applications were integrated with Keycloak:

```text
Finance Portal
Employee Portal
```

OpenID Connect was used for authentication.

The clients used:

```text
Authorization Code Flow
+
PKCE S256
```

The authentication flow was:

```text
Application
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

## Authorization Layer

The Finance Portal required the realm role:

```text
finance-user
```

A user could successfully authenticate but still be denied access if the required role was missing.

```text
Authentication Successful
        ↓
Check Required Role
        ↓
   +----+----+
   |         |
   v         v
Role Found  Role Missing
   |         |
   v         v
Access      HTTP 403
Granted     Access Denied
```

Realm roles were exposed to the application through:

```text
realm_access.roles
```

This demonstrated the relationship between:

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

## Single Sign-On Layer

The Finance Portal and Employee Portal trusted the same Keycloak realm.

After successful authentication to the first application, Keycloak reused the existing authenticated session when the second application was accessed.

```text
Finance Portal
      ↓
Keycloak Login + MFA
      ↓
Authenticated SSO Session
      ↓
Employee Portal
      ↓
No Additional Login Required
```

## Monitoring and Audit Layer

### User Events

User event logging was used to investigate authentication activity.

A controlled incorrect-password test generated:

```text
LOGIN_ERROR
```

with:

```text
invalid_user_credentials
```

### Administrative Events

Admin event logging was used to record IAM configuration changes.

A temporary realm role was created and removed.

The audit trail recorded:

```text
CREATE
DELETE
```

operations.

## IAM Support Principle

Access problems were investigated across the complete identity path rather than assuming that one configuration item was responsible.

The troubleshooting model was:

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
Token / UserInfo Claims
  ↓
Application Authorization
  ↓
Events and Audit Logs
```

## Architecture Summary

```text
Identity
   ↓
Groups
   ↓
Roles
   ↓
Authentication
   ↓
MFA
   ↓
OIDC
   ↓
Claims
   ↓
Authorization
   ↓
SSO
   ↓
Monitoring
   ↓
Audit
```
