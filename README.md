# Enterprise IAM Support Lab

## Overview

This project is a hands-on Identity and Access Management (IAM) lab built using Keycloak.

The lab simulates common enterprise IAM support activities including user and group administration, Role-Based Access Control (RBAC), least privilege, identity lifecycle management, Multi-Factor Authentication (MFA), OpenID Connect (OIDC), Single Sign-On (SSO), application authorization, troubleshooting, and audit logging.

The objective was to understand how identity, authentication, authorization, roles, claims, applications, and troubleshooting work together in an enterprise IAM environment.

---

## Ticket Information

**Request Type:** IAM Implementation and Support Lab  
**Environment:** Ubuntu Server / VirtualBox  
**Identity Platform:** Keycloak  
**Applications:** Python Flask OIDC Test Applications  
**Scope:** Identity Administration, Authentication, Authorization, SSO, and Troubleshooting

---

## Scenario

A simulated organization requires centralized identity and access management for employees working in different departments.

The IAM environment must support:

- Centralized user identity management
- Department-based access control
- Role-Based Access Control
- Least-privilege access
- Controlled privileged access
- Joiner-Mover-Leaver lifecycle management
- Multi-Factor Authentication
- OIDC-based application authentication
- Role-based application authorization
- Single Sign-On across applications
- Authentication and authorization troubleshooting
- User event logging
- Administrative audit logging

A separate Keycloak realm was created to isolate enterprise users and applications from the Keycloak `master` administrative realm.

---

## Environment

| Component | Purpose |
|---|---|
| Ubuntu Server | Keycloak and application host |
| VirtualBox | Virtual lab environment |
| Keycloak | Identity Provider and IAM platform |
| Python 3 | Test application runtime |
| Flask | Lightweight test web application |
| Authlib | OIDC/OAuth client integration |
| Windows Host | Browser and administrative access |
| TOTP Authenticator | MFA verification |

---

## Tasks Completed

- Installed and configured Keycloak
- Created a dedicated `enterprise-iam-lab` realm
- Created custom realm roles:
  - `employee`
  - `finance-user`
  - `finance-admin`
  - `it-support`
- Created Finance and IT-Support groups
- Assigned appropriate roles to groups
- Verified inherited group-based access
- Configured direct privileged role assignment
- Applied least-privilege principles
- Performed Joiner-Mover-Leaver scenarios
- Disabled and cleaned up a leaver account
- Configured and tested TOTP-based MFA
- Created an OIDC client for the Finance Portal
- Configured Authorization Code Flow with PKCE
- Created a Flask-based OIDC test application
- Configured callback and redirect URIs
- Tested authentication separately from authorization
- Implemented `finance-user` role-based authorization
- Troubleshot missing OIDC role claims
- Configured a User Realm Role protocol mapper
- Exposed realm roles through `realm_access.roles`
- Verified successful Finance Portal authorization
- Created a second OIDC client and application
- Verified Single Sign-On between two applications
- Enabled Keycloak user event logging
- Generated and investigated a failed login
- Identified `invalid_user_credentials`
- Enabled administrative audit events
- Verified CREATE and DELETE role operations

---

## Key Commands

### Start Keycloak

```bash
cd ~/keycloak-26.7.3
bin/kc.sh start-dev --http-host=0.0.0.0
```

### Verify Listening Port

```bash
sudo ss -lntp | grep 8080
```

### Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Application Dependencies

```bash
pip install flask authlib requests
```

### Verify Python Syntax

```bash
python -m py_compile app.py
```

### Start Finance Portal

```bash
python app.py
```

### Start Employee Portal

```bash
python employee_app.py
```

---

## Verification

### RBAC Verification

The Finance group was mapped to:

```text
employee
finance-user
```

The IT-Support group was mapped to:

```text
employee
it-support
```

Users inherited these roles through group membership.

A privileged Finance user also received the `finance-admin` role directly, while normal Finance access remained inherited through the Finance group.

### Joiner-Mover-Leaver Verification

A new employee was initially assigned to the Finance group and inherited Finance access.

The user was later moved from Finance to IT Support.

Old Finance access was removed and the new IT Support access was inherited.

For the leaver scenario:

- The account was disabled
- Active sessions were reviewed
- Remaining department group membership was removed

### MFA Verification

TOTP-based MFA was configured and tested.

The authentication flow required:

```text
Username
→ Password
→ One-Time Code
→ Successful Authentication
```

### OIDC Verification

The Finance Portal redirected users to Keycloak for authentication and received the authentication response through the configured callback.

The client used:

```text
Authorization Code Flow
+
PKCE S256
```

### Authorization Verification

An IT Support user successfully authenticated but did not have the required `finance-user` role.

Result:

```text
Authentication Successful
Authorization Failed
HTTP 403 Access Denied
```

A Finance user with the required role was then tested.

Result:

```text
Authentication Successful
Authorization Successful
Finance Portal Access Granted
```

### SSO Verification

Two separate OIDC clients were configured:

```text
Finance Portal
Employee Portal
```

After authentication to the Finance Portal, the Employee Portal was opened in the same browser session.

Keycloak recognized the existing authenticated session and did not request the username, password, or MFA code again.

Single Sign-On was successfully verified.

---

## Troubleshooting

### Issue 1 - Keycloak Not Reachable from Windows

Keycloak was running correctly, but the initial VM network interface used from Windows was not reachable from the Windows host.

Windows network configuration and the Ubuntu VM interfaces were reviewed.

The correct shared host-only network was identified and browser access to Keycloak succeeded.

### Issue 2 - HTTP 401 During Administration

A Keycloak administrative operation temporarily returned:

```text
HTTP 401 Unauthorized
```

The administrative session was refreshed and the previously created configuration was confirmed to still exist.

The issue was related to the administrative session rather than configuration loss.

### Issue 3 - Python Virtual Environment Failure

The virtual environment initially failed because the Ubuntu Python venv package was missing.

The required package was installed:

```bash
sudo apt install python3.12-venv -y
```

The virtual environment was then recreated successfully.

### Issue 4 - Missing Python Dependency

The Flask application initially failed with:

```text
ModuleNotFoundError: No module named 'requests'
```

The missing dependency was installed inside the project virtual environment:

```bash
pip install requests
```

### Issue 5 - Python Indentation Error

An authorization block produced an:

```text
IndentationError
```

The affected lines were reviewed using:

```bash
nl -ba app.py | sed -n '30,60p'
```

The indentation was corrected and verified using:

```bash
python -m py_compile app.py
```

### Issue 6 - Finance User Received Access Denied

The Finance user had the correct `finance-user` role in Keycloak but the Finance Portal still returned Access Denied.

The investigation identified that the realm role was not available to the application through the expected OIDC claim.

A `User Realm Role` protocol mapper was configured with:

```text
Token Claim Name: realm_access.roles
Multivalued: ON
Add to ID token: ON
Add to access token: ON
Add to userinfo: ON
```

After a fresh authentication, the Finance Portal successfully detected the `finance-user` role and granted access.

### Issue 7 - Failed User Login

A failed login was deliberately generated and investigated through Keycloak User Events.

The event showed:

```text
LOGIN_ERROR
error: invalid_user_credentials
client: finance-portal
auth_method: openid-connect
auth_type: code
```

This confirmed an authentication failure caused by invalid user credentials.

---

## Evidence

Sanitized screenshots are maintained in the `Screenshots` directory.

Evidence includes:

- Realm creation
- Custom IAM roles
- Finance group role mapping
- IT-Support group role mapping
- Inherited user roles
- Direct privileged role assignment
- Joiner scenario
- Mover scenario
- Leaver account disablement
- MFA enforcement
- Finance Portal
- OIDC login success
- Authentication success with authorization denial
- Successful Finance authorization
- OIDC Single Sign-On
- Failed login event investigation
- Administrative audit events

Passwords, OTP secrets, QR codes, authentication tokens, session identifiers, unnecessary private IP addresses, and local system identifiers are excluded or sanitized before publication.

---

## Detailed Documentation

Detailed technical documentation is maintained in the `Documentation` directory.

```text
01-IAM-Environment-Setup.md
02-RBAC-and-Least-Privilege.md
03-Joiner-Mover-Leaver.md
04-MFA-and-Authentication.md
05-OIDC-SSO-and-Authorization.md
06-Events-and-Troubleshooting.md
```

---

## Skills Demonstrated

- Identity and Access Management
- Keycloak Administration
- User and Group Administration
- Role-Based Access Control
- Least Privilege
- Identity Lifecycle Management
- Joiner-Mover-Leaver
- Authentication
- Authorization
- Multi-Factor Authentication
- TOTP
- OpenID Connect
- OAuth 2.0 Concepts
- Authorization Code Flow
- PKCE
- Single Sign-On
- OIDC Claims
- Protocol Mappers
- Application Integration
- IAM Troubleshooting
- Event Analysis
- Administrative Auditing
- Basic Python
- Flask
- Linux Administration
- Network Troubleshooting

---

## Interview Relevance

This lab provides practical examples for discussing common IAM support scenarios such as:

- A user can authenticate but cannot access an application
- A user has the correct role in the Identity Provider but the application cannot detect it
- Troubleshooting OIDC redirect and callback configuration
- Differentiating authentication failures from authorization failures
- Investigating failed login events
- Assigning access through groups instead of direct permissions
- Managing access during Joiner-Mover-Leaver lifecycle changes
- Enforcing MFA
- Troubleshooting OIDC role claims
- Verifying SSO across multiple applications
- Reviewing administrative audit activity

The project demonstrates both IAM configuration and structured troubleshooting rather than only theoretical IAM knowledge.

---

## Outcome

The lab successfully implemented and tested an enterprise-style IAM environment using Keycloak.

The final environment demonstrated:

```text
Identity Management
        +
RBAC
        +
Least Privilege
        +
Joiner-Mover-Leaver
        +
MFA
        +
OIDC / PKCE
        +
Application Authorization
        +
SSO
        +
Event Troubleshooting
        +
Administrative Auditing
```

The project provided hands-on experience with common IAM support tasks and identity security troubleshooting workflows.

---

## Repository Information

**Project:** Mission IT Job  
**Section:** Identity and Access Management  
**Lab:** Enterprise IAM Support Lab  
**Status:** Completed
