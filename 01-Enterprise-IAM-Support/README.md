# Enterprise IAM Support & Identity Security Lab

## Overview

This project demonstrates a practical enterprise-style Identity and Access Management (IAM) support environment using Keycloak, Ubuntu Server, Python, Flask, and OpenID Connect.

The objective was to build and troubleshoot common IAM workflows including user and group administration, Role-Based Access Control (RBAC), least privilege, Joiner-Mover-Leaver identity lifecycle management, Multi-Factor Authentication (MFA), OIDC application integration, role-based authorization, Single Sign-On (SSO), and IAM event investigation.

The lab was performed in a controlled home-lab environment using test identities and locally hosted applications.

---

## IAM Scenario

A simulated organization required centralized identity and access management for Finance and IT Support users.

The IAM environment needed to support:

- Centralized identity administration
- Department-based group membership
- Role-Based Access Control
- Least-privilege access
- Controlled privileged access
- Joiner-Mover-Leaver lifecycle management
- Multi-Factor Authentication
- OIDC-based application authentication
- Role-based application authorization
- Single Sign-On between applications
- Failed-login troubleshooting
- User event monitoring
- Administrative audit logging

A dedicated Keycloak realm was created to keep the enterprise lab identities and applications separate from the Keycloak `master` administrative realm.

---

## IAM Workflow

### 1. Keycloak Environment Setup

Keycloak was installed on an Ubuntu Server virtual machine.

The server was configured so that the Keycloak Administration Console could be accessed from the Windows host.

The environment included:

- Ubuntu Server
- VirtualBox
- Keycloak
- OpenJDK
- Windows browser access
- Host-only management networking

Keycloak was started in development mode for the isolated lab environment.

---

### 2. Dedicated IAM Realm

A dedicated realm was created:

```text
enterprise-iam-lab
```

The realm contained the lab:

- Users
- Groups
- Roles
- OIDC clients
- Authentication configuration
- Sessions
- User events
- Administrative events

This also demonstrated realm isolation between:

```text
master
```

and:

```text
enterprise-iam-lab
```

---

### 3. Role-Based Access Control

Custom realm roles were created:

```text
employee
finance-user
finance-admin
it-support
```

Department groups were also created:

```text
Finance
IT-Support
```

The Finance group received:

```text
employee
finance-user
```

The IT-Support group received:

```text
employee
it-support
```

Users inherited standard department access through group membership instead of receiving every role directly.

---

### 4. Least-Privilege Access

Standard Finance users inherited:

```text
employee
finance-user
```

The elevated role:

```text
finance-admin
```

was not assigned to the entire Finance group.

It was assigned only to a selected privileged Finance identity.

This demonstrated separation between:

```text
Standard Access
```

and:

```text
Privileged Access
```

---

### 5. Joiner-Mover-Leaver Lifecycle

A test employee identity was used to simulate the identity lifecycle.

#### Joiner

The identity was created and assigned to the required department group.

The user inherited access automatically through the group.

#### Mover

The user was transferred from one department to another.

The previous department membership was removed and the new department group was assigned.

This changed the user's effective access without manually maintaining individual department permissions.

#### Leaver

The user account was disabled.

The following checks were also performed:

- Active sessions reviewed
- Department group membership removed
- Remaining access reviewed

This demonstrated controlled offboarding and access removal.

---

### 6. Multi-Factor Authentication

TOTP-based MFA was configured for test users.

The authentication process was verified as:

```text
Username
   ↓
Password
   ↓
One-Time Code
   ↓
Authentication Successful
```

The MFA enrollment process used an authenticator application.

QR codes, OTP secrets, and live one-time codes were intentionally excluded from repository evidence.

---

### 7. Finance Portal OIDC Integration

A test Finance Portal was created using:

- Python
- Flask
- Authlib

The application was registered in Keycloak as an OpenID Connect client.

The client used:

```text
Authorization Code Flow
+
PKCE S256
```

The Finance Portal authentication workflow was:

```text
User
   ↓
Finance Portal
   ↓
Keycloak
   ↓
Password + MFA
   ↓
Authorization Code
   ↓
Application Callback
   ↓
Token Exchange
   ↓
Authenticated Application Session
```

---

### 8. Authentication vs Authorization

The lab separately tested:

```text
Authentication
```

and:

```text
Authorization
```

An IT Support user successfully authenticated through Keycloak.

However, the user did not have the required:

```text
finance-user
```

role.

The Finance Portal returned:

```text
Authentication Successful
Access Denied
Required Role: finance-user
```

This demonstrated that successful authentication does not automatically mean that a user is authorized to access every application.

---

### 9. OIDC Role Claim Troubleshooting

A Finance user had the correct role configured in Keycloak but initially still received:

```text
Access Denied
```

The investigation confirmed that:

```text
finance-user
```

was correctly assigned in Keycloak.

The issue was that the application was not receiving the realm role through the expected OIDC claim.

A User Realm Role protocol mapper was configured.

The role claim was exposed through:

```text
realm_access.roles
```

The mapper was configured to include the role information in:

- ID token
- Access token
- UserInfo

After a new authentication session was created, the Finance Portal successfully detected the required role.

The result became:

```text
Authentication Successful
Authorization Successful
Finance Portal Access Granted
```

This demonstrated troubleshooting across:

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

---

### 10. Single Sign-On

A second OIDC client and Flask application were created:

```text
Employee Portal
```

The first application was:

```text
Finance Portal
```

The user authenticated to the Finance Portal using Keycloak and MFA.

The Employee Portal was then opened in the same browser session.

Keycloak recognized the existing authenticated session.

The user was not required to enter:

- Username
- Password
- MFA code

again.

The Employee Portal successfully displayed the authenticated identity.

This verified Single Sign-On across two separate OIDC applications.

---

### 11. Failed Login Investigation

Keycloak user-event logging was enabled.

A controlled login failure was generated using an incorrect password.

The event log recorded:

```text
LOGIN_ERROR
```

The event details included:

```text
auth_method: openid-connect
auth_type: code
client: finance-portal
error: invalid_user_credentials
```

Additional event information included the test identity, client, redirect URI, time, and source address.

This demonstrated how IAM support teams can use Identity Provider events to investigate login problems.

---

### 12. Administrative Auditing

Administrative event logging was enabled.

A temporary test realm role was created:

```text
audit-test-role
```

Keycloak recorded the administrative:

```text
CREATE
```

operation.

The temporary role was then removed.

Keycloak also recorded the:

```text
DELETE
```

operation.

The audit trail demonstrated visibility into:

- Administrative action
- Resource type
- Resource path
- Time
- Administrative identity

The temporary role was removed after testing.

---

## Key Tools and Techniques

- Keycloak
- Ubuntu Server
- VirtualBox
- OpenJDK
- Identity and Access Management
- User Administration
- Group Administration
- Role-Based Access Control
- Least Privilege
- Privileged Access Concepts
- Joiner-Mover-Leaver Lifecycle
- Multi-Factor Authentication
- TOTP
- OpenID Connect
- OAuth 2.0 Concepts
- Authorization Code Flow
- PKCE
- OIDC Claims
- Protocol Mappers
- Application Authorization
- Single Sign-On
- Python
- Flask
- Authlib
- IAM Event Analysis
- Administrative Auditing
- Network Troubleshooting
- Authentication Troubleshooting

---

## IAM Validation Results

### Realm Isolation

The enterprise test identities were maintained in:

```text
enterprise-iam-lab
```

and were separate from the Keycloak administrative identities in:

```text
master
```

---

### RBAC Validation

Finance users inherited:

```text
employee
finance-user
```

from the Finance group.

IT Support users inherited:

```text
employee
it-support
```

from the IT-Support group.

A privileged Finance identity additionally received:

```text
finance-admin
```

through direct role assignment.

---

### Identity Lifecycle Validation

The Joiner-Mover-Leaver workflow successfully demonstrated:

```text
Identity Creation
        ↓
Department Access Assignment
        ↓
Department Transfer
        ↓
Old Access Removal
        ↓
New Access Assignment
        ↓
Account Disablement
        ↓
Final Access Cleanup
```

---

### MFA Validation

A user could not complete authentication using only a password after MFA had been configured.

A valid TOTP one-time code was required.

---

### OIDC Validation

The Finance Portal successfully authenticated users through Keycloak.

The application received the authentication response through its registered callback.

---

### Authorization Validation

IT Support user:

```text
Authentication: Successful
Authorization: Failed
Result: HTTP 403 Access Denied
```

Finance user:

```text
Authentication: Successful
Authorization: Successful
Result: Finance Portal Access Granted
```

---

### SSO Validation

The Finance Portal and Employee Portal were registered as separate OIDC clients.

After the Finance user authenticated to the first application, the second application reused the existing Keycloak SSO session.

No second password or MFA challenge was required.

---

### Event Validation

A controlled incorrect-password test generated:

```text
LOGIN_ERROR
```

with:

```text
invalid_user_credentials
```

This confirmed that the authentication failure could be investigated through Keycloak user events.

---

### Audit Validation

Administrative role creation and deletion produced recorded:

```text
CREATE
```

and:

```text
DELETE
```

events.

This confirmed that administrative IAM changes could be traced through Keycloak audit events.

---

## Troubleshooting Highlights

### Keycloak Browser Connectivity

The Keycloak service was running, but the initial IP address used from the Windows host belonged to a different virtual network path.

The VM and Windows host network configuration were reviewed and the correct host-only management interface was identified.

---

### Administrative Session 401

A role-creation attempt returned:

```text
HTTP 401 Unauthorized
```

The administrative session was refreshed.

The previously saved IAM configuration remained available and the operation succeeded after the session was renewed.

---

### Python Virtual Environment

The Python virtual environment initially failed because:

```text
python3.12-venv
```

was not installed.

The required package was installed and the environment was recreated successfully.

---

### Missing Python Dependency

The Flask OIDC application initially returned:

```text
ModuleNotFoundError: No module named 'requests'
```

The missing package was installed inside the Python virtual environment.

---

### Python Indentation Error

An authorization code block produced an:

```text
IndentationError
```

The affected code was reviewed by line number, corrected, and verified before the application was restarted.

---

### Missing OIDC Role Claim

The Finance user had the required IAM role but the Finance Portal still denied access.

The issue was traced to the role not being exposed to the application through the expected OIDC claim.

The User Realm Role protocol mapper resolved the issue.

---

## Evidence

Sanitized screenshots documenting the IAM implementation are available in:

[`Screenshots/`](Screenshots/)

The evidence set covers:

- Realm creation
- Custom IAM roles
- Department groups
- Group role mapping
- Inherited user access
- Privileged direct role assignment
- Joiner-Mover-Leaver lifecycle
- MFA enforcement
- Finance Portal
- OIDC authentication
- Authorization denial
- Successful Finance authorization
- Single Sign-On
- Failed-login investigation
- Administrative audit events

Screenshots intended for the public repository are reviewed before upload.

The repository does not intentionally expose:

- Passwords
- MFA QR codes
- OTP secrets
- One-time codes
- Authentication tokens
- Session identifiers
- Personal information
- Unnecessary internal system information

---

## Detailed IAM Report

Detailed technical documentation is maintained in:

[`Documentation/Enterprise-IAM-Support.md`](Documentation/Enterprise-IAM-Support.md)

The detailed documentation contains the environment setup, IAM configuration, practical steps, authentication and authorization workflow, OIDC application integration, SSO testing, troubleshooting, verification results, evidence, and lessons learned during the project.

Additional project components are maintained in:

- [`Architecture/`](Architecture/)
- [`Applications/`](Applications/)
- [`Screenshots/`](Screenshots/)

---

## Skills Demonstrated

- Identity and Access Management
- Keycloak Administration
- User Administration
- Group Administration
- Role-Based Access Control
- Least Privilege
- Privileged Access Concepts
- Access Provisioning
- Access Revocation
- Joiner-Mover-Leaver Lifecycle
- Authentication
- Authorization
- Multi-Factor Authentication
- TOTP
- OpenID Connect
- OAuth 2.0 Concepts
- Authorization Code Flow
- PKCE
- OIDC Client Configuration
- Redirect URI Configuration
- OIDC Claims
- Protocol Mappers
- Application Authorization
- Single Sign-On
- IAM Troubleshooting
- Login Failure Investigation
- Event Analysis
- Administrative Audit Logging
- Basic Python
- Flask
- Authlib
- Linux Administration
- Basic Network Troubleshooting
- Technical Documentation

---

## Outcome

The project demonstrated a complete enterprise-style IAM support workflow using Keycloak.

The final lab successfully implemented and validated:

```text
Identity Administration
        ↓
Groups and Roles
        ↓
RBAC
        ↓
Least Privilege
        ↓
Joiner-Mover-Leaver
        ↓
MFA
        ↓
OIDC + PKCE
        ↓
Authentication
        ↓
Role-Based Authorization
        ↓
SSO
        ↓
User Event Investigation
        ↓
Administrative Auditing
```

The project also demonstrated structured troubleshooting by identifying and resolving authentication, networking, application dependency, OIDC claim, and authorization issues.

Most importantly, the lab provided practical IAM support experience rather than only theoretical identity and access management knowledge.

---

## Repository Information

- **Repository:** Enterprise-IAM-Support-Lab
- **Section:** 01-Enterprise-IAM-Support
- **Lab:** Enterprise IAM Support & Identity Security Lab
- **Status:** Completed
- **Environment:** Controlled Home Lab
- **Identity Platform:** Keycloak
- **Applications:** Finance Portal, Employee Portal
- **Protocols:** OpenID Connect, OAuth 2.0 / PKCE
- **Version:** 1.0
