# Enterprise IAM Support & Identity Security Lab — Detailed Documentation

## Lab Information

**Lab Name:** Enterprise IAM Support & Identity Security Lab  
**Project Folder:** `01-Enterprise-IAM-Support`  
**Repository:** `Enterprise-IAM-Support-Lab`  
**Lab Type:** End-to-End Identity and Access Management Support Lab  
**Environment:** Controlled Home Lab  
**Status:** Completed  
**Version:** 1.0  

### Objective

The objective of this project was to build and troubleshoot a practical Identity and Access Management environment using Keycloak.

The project was designed to develop hands-on experience in:

- Identity and Access Management
- Keycloak administration
- User administration
- Group administration
- Role-Based Access Control
- Least privilege
- Privileged role assignment
- Joiner-Mover-Leaver lifecycle management
- Multi-Factor Authentication
- TOTP
- OpenID Connect
- OAuth 2.0 concepts
- Authorization Code Flow
- PKCE
- Application authentication
- Application authorization
- OIDC claims
- Protocol mappers
- Single Sign-On
- Login troubleshooting
- User event analysis
- Administrative audit logging
- Basic application integration
- Basic network troubleshooting

The lab used controlled test identities and locally hosted applications.

No production systems or real user accounts were used.

---

## Ticket Information

**Ticket ID:** N/A — Project-Based IAM Support Lab  
**Category:** Identity and Access Management / Identity Security  
**Priority:** Lab Exercise  
**Identity Platform:** Keycloak  
**Affected Systems:** Controlled IAM Realm and Test Applications  
**Support Type:** Identity Administration, Authentication, Authorization, SSO and Troubleshooting  

### Support Question

Can a centralized IAM platform be configured to manage identities, groups, roles, MFA, application authentication, authorization, SSO, and audit events while also supporting structured troubleshooting of common access problems?

---

## Scenario

A simulated organization required centralized identity and access management for employees working in different departments.

Two main departments were represented:

```text
Finance
IT-Support
```

The IAM platform needed to support:

- Centralized user identities
- Department groups
- Standard employee roles
- Department-specific roles
- Elevated Finance access
- Least-privilege administration
- User onboarding
- Department transfers
- User offboarding
- MFA
- OIDC application authentication
- Role-based application authorization
- SSO across multiple applications
- Login-event troubleshooting
- Administrative audit trails

A dedicated Keycloak realm was used to separate enterprise test identities from the Keycloak administrative realm.

The high-level identity workflow was:

```text
User Identity
      ↓
Department Group
      ↓
Assigned / Inherited Roles
      ↓
Authentication
      ↓
MFA
      ↓
OIDC Client
      ↓
Application
      ↓
Authorization Decision
```

Two test applications were later used:

```text
Finance Portal
Employee Portal
```

The Finance Portal was used to test role-based authorization.

The Employee Portal was used together with the Finance Portal to verify Single Sign-On.

---

## Environment

### Server Environment

- Ubuntu Server
- VirtualBox
- Keycloak
- OpenJDK
- Python 3
- Flask
- Authlib
- Requests library
- Bash
- SSH

### Client Environment

- Windows host
- Web browser
- PowerShell
- Incognito browser sessions
- TOTP authenticator application

### IAM Environment

Realm:

```text
enterprise-iam-lab
```

Custom realm roles:

```text
employee
finance-user
finance-admin
it-support
```

Groups:

```text
Finance
IT-Support
```

OIDC clients:

```text
finance-portal
employee-portal
```

### Application Ports

The applications used separate HTTP ports in the controlled lab.

```text
Keycloak        → 8080
Finance Portal  → 5000
Employee Portal → 5001
```

Exact private lab addressing is intentionally omitted from this public documentation.

---

## Lab Duration

This was a multi-session practical project completed in a controlled home-lab environment.

The work was completed in several phases:

1. Keycloak environment preparation
2. Network-access verification
3. Realm creation
4. Role creation
5. Group creation
6. Role mapping
7. User creation
8. RBAC verification
9. Privileged access configuration
10. Joiner-Mover-Leaver testing
11. MFA configuration
12. Finance Portal OIDC registration
13. Python Flask application integration
14. Authentication testing
15. Authorization testing
16. OIDC role-claim troubleshooting
17. Protocol mapper configuration
18. SSO configuration
19. User event investigation
20. Administrative audit testing
21. Cleanup and documentation

The project was intentionally completed phase by phase so that each configuration could be understood and verified before continuing.

---

## Commands Used

### 1. Verify Java

Keycloak requires a Java runtime.

Java availability was checked using:

```bash
java --version
```

OpenJDK was installed before Keycloak was started.

---

### 2. Keycloak Package Installation

Keycloak was downloaded as a release archive and extracted directly on the Ubuntu Server.

The installation contained directories including:

```text
bin
conf
data
lib
providers
themes
```

The Keycloak management script used during the lab was:

```text
bin/kc.sh
```

---

### 3. Start Keycloak

Keycloak was started in development mode.

```bash
cd ~/keycloak-26.7.3
bin/kc.sh start-dev --http-host=0.0.0.0
```

### Purpose

The development server was used only for the isolated home-lab environment.

The option:

```text
--http-host=0.0.0.0
```

allowed Keycloak to listen on available IPv4 network interfaces so that the Administration Console could be reached from the Windows host.

Development mode is not intended for production deployment.

---

## Network Access Verification

Keycloak successfully started on Ubuntu but initial browser access required verification of the VM networking.

The Ubuntu Server had multiple network interfaces because it was also used for other lab environments.

The Windows host also contained VirtualBox network adapters.

The important lesson was that an IP address should not be selected only because it appears to be in a familiar subnet.

The underlying VirtualBox network type must also be understood.

The investigation included:

```bash
ip addr
```

and:

```bash
ip route
```

On Windows:

```powershell
ipconfig
```

The correct management network was identified and browser access to Keycloak succeeded.

---

## Understanding the Network Components

### IP Address

An IP address identifies a network interface.

One computer can have multiple network interfaces and therefore multiple IP addresses.

### Port

A port identifies a network service running on an IP address.

In this lab:

```text
Keycloak → TCP 8080
```

### localhost

```text
127.0.0.1
```

refers to the local machine itself.

### 0.0.0.0

```text
0.0.0.0
```

means that the application listens on all available IPv4 interfaces.

This does not represent an address that should normally be entered into a remote browser.

---

## Realm Creation

A dedicated realm was created:

```text
enterprise-iam-lab
```

The Keycloak `master` realm remained separate.

The logical structure became:

```text
Keycloak
│
├── master
│   └── Keycloak Administration
│
└── enterprise-iam-lab
    ├── Users
    ├── Groups
    ├── Realm Roles
    ├── OIDC Clients
    ├── Authentication
    ├── Sessions
    └── Events
```

### Purpose

The dedicated realm created an isolated identity boundary for the enterprise lab.

This also demonstrated why identities created inside:

```text
enterprise-iam-lab
```

were not visible when viewing users inside:

```text
master
```

---

## Role-Based Access Control

Four custom realm roles were created.

### employee

```text
Basic access role for all company employees
```

### finance-user

```text
Standard access role for Finance department users
```

### finance-admin

```text
Administrative access role for the Finance department
```

### it-support

```text
IT Support access role
```

The objective was to separate:

```text
Department Membership
```

from:

```text
Access Rights
```

Groups represented where a user belonged.

Roles represented what access the user received.

---

## Finance Group

A group named:

```text
Finance
```

was created.

The following roles were assigned to the group:

```text
employee
finance-user
```

The access model became:

```text
Finance
   │
   ├── employee
   └── finance-user
```

A user added to Finance automatically inherited the mapped roles.

---

## IT-Support Group

A second group was created:

```text
IT-Support
```

The following roles were mapped:

```text
employee
it-support
```

The access model became:

```text
IT-Support
    │
    ├── employee
    └── it-support
```

This allowed standard IT Support access to be managed through group membership.

---

## User Role Inheritance

A Finance test identity was added to the Finance group.

Role Mapping showed that:

```text
employee
finance-user
```

were inherited.

The inherited state demonstrated that the roles came through the group rather than through direct assignment.

The same concept was verified using an IT Support identity.

The IT Support identity inherited:

```text
employee
it-support
```

---

## Least Privilege

The Finance group intentionally did not receive:

```text
finance-admin
```

This prevented all Finance users from automatically receiving elevated privileges.

A separate privileged Finance identity was created.

The user received:

```text
employee
finance-user
```

through Finance group membership.

The additional:

```text
finance-admin
```

role was assigned directly only to the privileged identity.

The resulting model was:

```text
Privileged Finance Identity
        │
        ├── Finance Group
        │     ├── employee
        │     └── finance-user
        │
        └── finance-admin
              Direct Role
```

This demonstrated least privilege and separation between standard and elevated access.

---

## Direct vs Inherited Access

The role-mapping interface demonstrated the difference between:

```text
Inherited: True
```

and:

```text
Inherited: False
```

Group-based roles appeared as inherited.

A directly assigned privileged role appeared as non-inherited.

This distinction is useful during IAM troubleshooting because it helps identify where access originates.

---

## Joiner-Mover-Leaver Lifecycle

The identity lifecycle was tested using a controlled test account.

### Joiner

A new employee identity was created.

The account was added to the Finance group.

The user then inherited:

```text
employee
finance-user
```

### Purpose

The Joiner scenario demonstrated how onboarding can be simplified by assigning the user to the correct business group instead of manually assigning each permission.

---

## Mover

The test employee was moved from Finance to IT Support.

The previous Finance membership was removed.

The IT-Support group was assigned.

The effective access changed from:

```text
employee
finance-user
```

to:

```text
employee
it-support
```

### Purpose

The Mover scenario demonstrated that old access should be reviewed and removed when an employee changes job function.

Leaving the old Finance access in place could create:

```text
Privilege Creep
```

---

## Leaver

The same test account was later used for the Leaver scenario.

The account was disabled.

Active sessions were reviewed.

Remaining department group membership was removed.

The identity record was retained rather than immediately deleted.

### Purpose

This demonstrated controlled offboarding.

The sequence was:

```text
Disable Identity
      ↓
Review Sessions
      ↓
Remove Access
      ↓
Retain Record for Audit
```

---

## Multi-Factor Authentication

TOTP-based MFA was configured.

A test user was required to configure an OTP authenticator.

The authentication flow became:

```text
Username
   ↓
Password
   ↓
TOTP One-Time Code
   ↓
Authentication Successful
```

MFA was later also configured for the Finance test identity.

### Security Handling

The following evidence was intentionally not published:

- QR code
- TOTP secret
- Live one-time code

This prevented authentication secrets from being exposed in the repository.

---

## Finance Portal OIDC Client

A Keycloak client was created:

```text
finance-portal
```

Client type:

```text
OpenID Connect
```

The client configuration used:

```text
Client authentication: OFF
Standard flow: ON
Direct access grants: OFF
Implicit flow: OFF
Require PKCE: ON
PKCE Method: S256
```

### Purpose

The Finance Portal represented a browser-based application using OpenID Connect authentication.

PKCE was enabled to provide additional protection to the authorization-code flow.

---

## OIDC Login Settings

The Finance Portal client was configured with:

```text
Root URL
Home URL
Valid Redirect URI
Post Logout Redirect URI
Web Origin
```

Private lab addresses are not reproduced in this public documentation.

The important callback path was:

```text
/callback
```

The authentication process was:

```text
Finance Portal
      ↓
Keycloak Authorization Endpoint
      ↓
User Authentication
      ↓
Authorization Code
      ↓
Finance Portal Callback
      ↓
Token Exchange
```

---

## Understanding the Redirect URI

The redirect URI identifies where the Identity Provider is permitted to return the browser after successful authentication.

The application sent a callback location similar to:

```text
/callback
```

Keycloak validated the requested redirect against the registered client configuration.

This prevents authentication responses from being redirected to an unauthorized destination.

A redirect URI troubleshooting workflow can include checking:

```text
Client ID
Protocol
Hostname
Port
Path
Trailing Slash
Registered Redirect URI
```

---

## Python Application Environment

A separate application directory was created for the Finance Portal.

Python availability was verified:

```bash
python3 --version
```

Python 3.12 was available.

A project virtual environment was then attempted:

```bash
python3 -m venv venv
```

The first attempt failed because the required Ubuntu venv package was missing.

---

## Install Python Virtual Environment Support

The required package was installed:

```bash
sudo apt install python3.12-venv -y
```

The incomplete virtual environment was removed:

```bash
rm -rf ~/finance-portal/venv
```

The environment was recreated:

```bash
cd ~/finance-portal
python3 -m venv venv
```

It was then activated:

```bash
source venv/bin/activate
```

---

## Install Flask and OIDC Libraries

The application dependencies were installed inside the virtual environment.

```bash
pip install flask authlib
```

A later runtime dependency required:

```bash
pip install requests
```

The environment included:

```text
Flask
Authlib
Requests
```

---

## Finance Portal Application

A small Flask application was created.

The application contained four main routes:

```text
/
```

Home page.

```text
/login
```

Redirects the browser to Keycloak.

```text
/callback
```

Receives the OIDC authorization response.

```text
/logout
```

Clears the local Flask application session.

The purpose of the application was not to develop a production web platform.

It was created to understand and test the IAM authentication and authorization flow end to end.

---

## Application Syntax Verification

Before running the application, Python syntax was checked:

```bash
python -m py_compile app.py
```

No output indicated that the syntax check succeeded.

---

## Application Runtime Dependency Error

The first attempt to start the Flask application failed with:

```text
ModuleNotFoundError: No module named 'requests'
```

The missing dependency was installed:

```bash
pip install requests
```

The application then started successfully.

---

## Start Finance Portal

The application was started using:

```bash
python app.py
```

The Flask development server listened on:

```text
0.0.0.0:5000
```

This allowed access from the Windows host through the lab management network.

---

## Initial OIDC Authentication Test

The Finance Portal initially displayed:

```text
You are not logged in.
Login with Keycloak
```

A test IT Support identity selected:

```text
Login with Keycloak
```

The user authenticated successfully through Keycloak.

The Finance Portal then displayed the authenticated identity.

This confirmed that:

```text
Finance Portal
      ↓
Keycloak
      ↓
Authentication
      ↓
Callback
      ↓
Application Session
```

was working.

---

## Authentication vs Authorization

The first application version verified only authentication.

This meant that an IT Support user could successfully authenticate to the Finance Portal even though the user should not have Finance access.

The application was then updated to require:

```text
finance-user
```

before granting access.

The authorization logic checked the roles available in the user session.

If the required role was absent, the application returned:

```text
HTTP 403
Access Denied
```

---

## Authorization Test — IT Support User

The IT Support identity authenticated successfully.

The user did not have:

```text
finance-user
```

The result was:

```text
Authentication successful
Access Denied
Required role: finance-user
```

This demonstrated the difference between:

```text
Authentication
Who are you?
```

and:

```text
Authorization
What are you allowed to access?
```

---

## Python Indentation Troubleshooting

During creation of the authorization block, Python returned:

```text
IndentationError
```

The relevant source lines were reviewed using:

```bash
nl -ba app.py | sed -n '30,60p'
```

The nested `return` statement was corrected so that it belonged to the intended `if` block.

Syntax was verified again:

```bash
python -m py_compile app.py
```

No error was returned.

---

## Finance Authorization Test

A Finance identity was prepared for application testing.

The user belonged to the Finance group and therefore had:

```text
finance-user
```

in Keycloak.

However, the Finance Portal still returned:

```text
Access Denied
```

This indicated that the IAM assignment itself was not necessarily the problem.

---

## OIDC Role Claim Investigation

The troubleshooting sequence became:

```text
Does user have correct group?
        ↓
Does group have correct role?
        ↓
Does user inherit role?
        ↓
Does application receive role?
```

The Finance identity correctly inherited:

```text
finance-user
```

The issue was therefore located between Keycloak role assignment and the application's OIDC claims.

---

## User Realm Role Protocol Mapper

A dedicated client mapper was created for the Finance Portal.

Mapper type:

```text
User Realm Role
```

Configuration included:

```text
Name: realm-roles
Multivalued: ON
Token Claim Name: realm_access.roles
Claim JSON Type: String
Add to ID token: ON
Add to access token: ON
Add to userinfo: ON
```

### Purpose

This exposed Keycloak realm roles to the OIDC client using:

```text
realm_access.roles
```

The application was already looking for roles at that claim location.

---

## Authorization Verification After Mapper

A fresh authentication was performed so that a new token and UserInfo response would contain the updated claim.

The Finance Portal then displayed:

```text
OIDC Login Successful
```

for the Finance identity.

The previous Access Denied result was resolved.

This demonstrated a real IAM troubleshooting sequence:

```text
Role exists in IAM
      ↓
Application still denies access
      ↓
Inspect claim mapping
      ↓
Configure protocol mapper
      ↓
Generate fresh token
      ↓
Application detects role
      ↓
Access Granted
```

---

## Finance MFA

TOTP MFA was also configured for the Finance identity.

This strengthened the final Finance authentication flow:

```text
Username
   ↓
Password
   ↓
TOTP
   ↓
OIDC Authentication
   ↓
Role Validation
   ↓
Finance Portal Access
```

---

## Employee Portal OIDC Client

A second OIDC client was created:

```text
employee-portal
```

The configuration also used:

```text
OpenID Connect
Standard Flow
PKCE S256
```

The Employee Portal used a different application port from the Finance Portal.

This allowed both applications to run at the same time.

---

## Employee Portal Application

The working Finance Portal Flask application was copied and adapted for the Employee Portal.

The second application used:

```text
CLIENT_ID = "employee-portal"
```

A separate Flask session-cookie name was configured.

This was important because browser cookies are associated with hosts and are not isolated purely by TCP port.

The Employee Portal did not enforce the Finance role.

Its purpose was to verify authentication and SSO.

---

## Start Employee Portal

The Employee Portal was started using:

```bash
python employee_app.py
```

The application listened on:

```text
0.0.0.0:5001
```

---

## Single Sign-On Test

The Finance identity first authenticated to the Finance Portal.

The user completed:

```text
Password
+
MFA
```

Keycloak created an authenticated SSO session.

In the same Incognito browser window, the Employee Portal was opened.

The user selected:

```text
Login with Keycloak
```

Keycloak recognized the existing authenticated browser session.

The user was not prompted again for:

```text
Username
Password
MFA
```

The Employee Portal displayed:

```text
OIDC SSO Login Successful
```

This verified SSO between:

```text
Finance Portal
      +
Employee Portal
```

using the same Keycloak realm.

---

## User Event Logging

Keycloak User Events were enabled.

A short event-expiration period was configured for the lab.

A controlled authentication failure was then generated using an incorrect password.

The user-facing result showed:

```text
Invalid username or password
```

---

## Failed Login Event Investigation

The Keycloak event log recorded:

```text
LOGIN_ERROR
```

The event included details such as:

```text
auth_method: openid-connect
auth_type: code
client: finance-portal
error: invalid_user_credentials
```

The event also contained:

- Event time
- User identifier
- Test username
- Client
- Redirect URI
- Source address

### Purpose

This demonstrated an IAM support troubleshooting workflow:

```text
User reports login issue
       ↓
Review IdP Events
       ↓
Find LOGIN_ERROR
       ↓
Review affected client
       ↓
Review identity
       ↓
Review error reason
       ↓
Identify invalid credentials
```

---

## Administrative Event Logging

Keycloak Admin Events were enabled.

Administrative event representation was also enabled for the lab.

A temporary realm role was created:

```text
audit-test-role
```

The Admin Events page recorded:

```text
Resource Type: REALM_ROLE
Operation: CREATE
```

The temporary test role was then deleted.

A second event recorded:

```text
Resource Type: REALM_ROLE
Operation: DELETE
```

---

## Admin Audit Purpose

The audit trail demonstrated the ability to answer questions such as:

```text
What changed?
Which resource was affected?
When did the change occur?
Which administrative identity performed the action?
```

The temporary role was removed after testing.

---

## Verification Results

### Keycloak Environment

Verified:

- Java runtime available
- Keycloak started successfully
- Administration Console reachable
- Dedicated realm successfully created
- Realm isolation understood and verified

---

### RBAC

Finance:

```text
employee
finance-user
```

IT Support:

```text
employee
it-support
```

Privileged Finance identity:

```text
employee       → inherited
finance-user   → inherited
finance-admin  → direct
```

---

### Least Privilege

The elevated:

```text
finance-admin
```

role was not granted to all Finance users.

Only the selected privileged Finance identity received the elevated role.

---

### Joiner-Mover-Leaver

Joiner:

```text
Identity Created
→ Finance Assigned
→ Finance Roles Inherited
```

Mover:

```text
Finance Removed
→ IT-Support Assigned
→ Old Finance Access Removed
→ New IT Access Inherited
```

Leaver:

```text
Account Disabled
→ Sessions Reviewed
→ Group Access Removed
```

---

### MFA

TOTP-based MFA was configured and tested.

A valid one-time code was required after password authentication.

---

### OIDC

The Finance Portal successfully redirected authentication to Keycloak and received the authorization response through its callback.

Authorization Code Flow with PKCE was used.

---

### Authentication

Successful OIDC authentication was verified for test users.

---

### Authorization

IT Support identity:

```text
Authentication: Successful
Authorization: Failed
Result: HTTP 403 Access Denied
```

Finance identity after role claim mapping:

```text
Authentication: Successful
Authorization: Successful
Result: Finance Portal Access Granted
```

---

### Role Claim Mapping

The Finance access problem was resolved by exposing realm roles through:

```text
realm_access.roles
```

A fresh authentication confirmed the corrected application authorization.

---

### Single Sign-On

Two separate OIDC applications reused the same Keycloak authenticated session.

The second application did not request credentials or MFA again.

---

### Login Event Investigation

The controlled failed login generated:

```text
LOGIN_ERROR
```

with:

```text
invalid_user_credentials
```

---

### Administrative Auditing

Role creation and deletion generated:

```text
CREATE
DELETE
```

Admin Event records.

---

## Troubleshooting

### 1. Docker Registry Connectivity

Docker was initially considered for Keycloak deployment.

Docker was installed successfully.

However, container-image pulls produced inconsistent registry connectivity errors including TLS timeout and HTTP/HTTPS behavior.

Direct HTTPS connectivity to public registries was separately tested.

Because container troubleshooting was outside the main IAM learning objective, the Docker deployment path was discontinued.

Keycloak was installed directly from the release archive instead.

This prevented unrelated container networking issues from blocking the IAM lab.

---

### 2. Multiple VM Network Interfaces

The Ubuntu VM contained several interfaces because it was already being used for other labs.

The Windows host could not automatically reach every VM interface.

The correct management network was identified without removing the existing SOC lab interfaces.

This reinforced the importance of understanding:

```text
Network Adapter
Subnet
Routing
VirtualBox Network Type
IP Address
Port
```

rather than assuming that any VM IP should work.

---

### 3. HTTP 401 During Role Creation

A Keycloak administrative operation returned:

```text
HTTP 401 Unauthorized
```

The previously created configuration remained present.

Refreshing the administrative session allowed the task to continue.

This demonstrated that an authorization/session error does not automatically mean that previously saved configuration has been deleted.

---

### 4. Python Virtual Environment Package Missing

The command:

```bash
python3 -m venv venv
```

initially failed because:

```text
ensurepip is not available
```

The required Ubuntu package was installed:

```bash
sudo apt install python3.12-venv -y
```

The failed partial environment was removed and recreated successfully.

---

### 5. Missing Requests Dependency

The Flask application initially failed with:

```text
ModuleNotFoundError: No module named 'requests'
```

The missing package was installed inside the active virtual environment:

```bash
pip install requests
```

The application then started successfully.

---

### 6. Python Indentation Error

After the role-checking block was added, Python returned:

```text
IndentationError
```

The affected source region was inspected using:

```bash
nl -ba app.py | sed -n '30,60p'
```

The nested block indentation was corrected.

The application was then verified using:

```bash
python -m py_compile app.py
```

---

### 7. Finance Role Present but Access Denied

The Finance identity had the correct role in Keycloak but the application returned:

```text
Access Denied
```

This ruled out a simple missing-group or missing-role assignment.

The OIDC claim mapping was investigated.

A User Realm Role mapper was created.

Realm roles were exposed through:

```text
realm_access.roles
```

A new authentication session generated updated claims and authorization succeeded.

This was one of the most important troubleshooting scenarios in the project.

---

### 8. Master Realm Appeared to Have Missing Users

After reopening the Keycloak Administration Console, only the administrative identity was initially visible.

The issue was not data loss.

The Administration Console was displaying:

```text
master
```

rather than:

```text
enterprise-iam-lab
```

After selecting the correct realm, the enterprise users and configuration were visible again.

This reinforced the concept of realm isolation.

---

## Evidence

Evidence is maintained in:

```text
Screenshots/
```

The screenshot set documents major project milestones including:

- Dedicated realm creation
- Custom realm roles
- Finance group configuration
- IT-Support group configuration
- Group role mappings
- Inherited roles
- Privileged direct role assignment
- Joiner scenario
- Mover scenario
- Leaver scenario
- MFA enforcement
- Finance Portal
- Successful OIDC authentication
- Authorization denial
- Finance authorization success
- SSO across two applications
- Failed login event
- Expanded login-error investigation
- Administrative role creation audit
- Administrative role deletion audit

Only meaningful evidence is retained.

Public screenshots are sanitized before upload.

The repository does not intentionally expose:

- Passwords
- Authentication secrets
- MFA QR codes
- TOTP secrets
- One-time codes
- Access tokens
- ID tokens
- Refresh tokens
- Session identifiers
- Unnecessary private IP addresses
- Local usernames
- Local hostnames
- Personal information

---

## Lessons Learned

### Authentication and Authorization Are Different

Successful authentication only confirms the identity of a user.

It does not automatically grant application access.

The IT Support test demonstrated:

```text
Authentication Successful
Authorization Failed
```

This is a core IAM troubleshooting distinction.

---

### Group Membership Simplifies Access Administration

Managing standard access through groups makes role administration more consistent.

Instead of directly assigning the same role to many users:

```text
User → Role
User → Role
User → Role
```

the model becomes:

```text
Users
  ↓
Group
  ↓
Role
```

This supports onboarding, transfers, and access removal.

---

### Old Access Must Be Removed During Transfers

The Mover scenario demonstrated that assigning new access is only part of a department transfer.

Old access must also be reviewed and removed.

Otherwise the user can accumulate unnecessary permissions.

This is privilege creep.

---

### Elevated Access Should Remain Separate

Standard Finance users did not require:

```text
finance-admin
```

Keeping the privileged role separate reduced unnecessary elevated access.

---

### MFA Strengthens Authentication

Password authentication alone does not provide the same level of protection as password plus a second factor.

TOTP MFA required possession of the configured authenticator in addition to the password.

---

### Redirect URIs Are Security Controls

OIDC redirect URIs are not only application addresses.

They restrict where Keycloak is allowed to send an authentication response.

Incorrect redirect URI configuration can break authentication.

Overly broad redirect configuration can also weaken security.

---

### Roles Must Reach the Application

A role existing inside the IAM platform does not automatically mean that an application can use it.

The Finance authorization issue demonstrated the full chain:

```text
User
  ↓
Group
  ↓
Role
  ↓
Token / UserInfo Claim
  ↓
Application
  ↓
Authorization Decision
```

Every stage matters.

---

### New Tokens May Be Required After Configuration Changes

After claim mapping was changed, a fresh authentication was required.

Existing tokens do not automatically gain new claims after they have already been issued.

---

### SSO Depends on the Identity Provider Session

The Employee Portal did not need to know the Finance Portal password or MFA result.

Both applications trusted the same Keycloak Identity Provider.

Keycloak recognized the existing authenticated browser session and provided SSO.

---

### Events Are Important for IAM Support

A user-facing message such as:

```text
Invalid username or password
```

provides limited information.

Keycloak events provided additional context such as:

```text
Client
Username
Authentication method
Authentication type
Redirect URI
Error reason
Time
```

This makes event analysis important for IAM troubleshooting.

---

### Administrative Changes Should Be Auditable

The Admin Event test demonstrated that configuration changes should be traceable.

This helps answer:

```text
Who changed what?
When?
Which resource?
Which operation?
```

---

### Application Code Was Used as a Test Tool

The Python Flask applications were not intended to demonstrate full web-development expertise.

They were used to create a controlled application environment for understanding:

- OIDC redirects
- Callbacks
- Tokens
- Sessions
- Roles
- Authorization
- SSO

The important IAM skill was understanding and troubleshooting the identity flow.

---

## Skills Demonstrated

- Identity and Access Management
- Keycloak
- Keycloak Administration
- Identity Provider Concepts
- Realm Administration
- User Administration
- Group Administration
- Realm Roles
- Role Mapping
- Role Inheritance
- Role-Based Access Control
- Least Privilege
- Privileged Access Concepts
- Access Provisioning
- Access Revocation
- Joiner-Mover-Leaver
- Identity Lifecycle Management
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
- UserInfo
- OIDC Claims
- Protocol Mappers
- Application Authorization
- Single Sign-On
- IAM Troubleshooting
- Authentication Failure Investigation
- User Event Analysis
- Administrative Event Analysis
- Audit Logging
- Python
- Python Virtual Environments
- Flask
- Authlib
- Basic Application Integration
- Ubuntu Server
- Linux Administration
- Network Troubleshooting
- VirtualBox Networking
- HTTP
- Ports
- Technical Documentation

---

## Outcome

The project successfully demonstrated an end-to-end enterprise-style Identity and Access Management support workflow.

The lab implemented and verified:

```text
Keycloak Environment
        ↓
Dedicated IAM Realm
        ↓
Users
        ↓
Groups
        ↓
Roles
        ↓
RBAC
        ↓
Least Privilege
        ↓
Joiner-Mover-Leaver
        ↓
MFA
        ↓
OIDC
        ↓
Authorization Code + PKCE
        ↓
Application Authentication
        ↓
Role Claim Mapping
        ↓
Application Authorization
        ↓
Single Sign-On
        ↓
User Event Investigation
        ↓
Administrative Auditing
```

The project also produced several realistic troubleshooting scenarios, including:

- VM network-path confusion
- Administrative session authorization failure
- Python environment dependency issues
- Python syntax and indentation troubleshooting
- Authentication vs authorization failure
- Missing OIDC role claims
- Realm-selection confusion
- Invalid user credentials

Most importantly, the project demonstrated practical IAM support reasoning by following identity and access problems from the user account through groups, roles, claims, authentication, application authorization, and event logs.

---

## Repository Information

**Repository:** `Enterprise-IAM-Support-Lab`  
**Section:** `01-Enterprise-IAM-Support`  
**Lab:** `Enterprise IAM Support & Identity Security Lab`  
**Documentation:** `01-Enterprise-IAM-Support/Documentation/Enterprise-IAM-Support.md`  
**Screenshots:** `01-Enterprise-IAM-Support/Screenshots/`  
**Applications:** `01-Enterprise-IAM-Support/Applications/`  
**Architecture:** `01-Enterprise-IAM-Support/Architecture/`  
**Status:** Completed  
**Version:** 1.0
