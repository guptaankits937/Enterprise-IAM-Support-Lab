# Evidence Screenshots

This directory contains sanitized evidence captured during the Enterprise IAM Support & Identity Security Lab.

## Evidence Index

| # | Screenshot | Evidence |
|---|---|---|
| 01 | `01-realm-created.jpg` | Dedicated `enterprise-iam-lab` realm created successfully in Keycloak. |
| 02 | `02-custom-realm-roles.jpg` | Custom realm roles created for employee, Finance, privileged Finance, and IT Support access. |
| 03 | `03-finance-group-role-mapping.jpg` | Finance group mapped to the `employee` and `finance-user` realm roles. |
| 04 | `04-it-support-group-role-mapping.jpg` | IT-Support group mapped to the `employee` and `it-support` realm roles. |
| 05 | `05-finance-user-inherited-roles.jpg` | Finance user inherited standard access through Finance group membership. |
| 06 | `06-it-support-user-inherited-roles.jpg` | IT Support user inherited standard access through IT-Support group membership. |
| 07 | `07-finance-manager-direct-admin-role.jpg` | Privileged Finance identity received `finance-admin` directly while standard roles remained inherited. |
| 08 | `08-joiner-finance-access.jpg` | Joiner workflow showing a new employee receiving Finance access through group membership. |
| 09 | `09-mover-finance-to-it-support.jpg` | Mover workflow showing Finance access removed and IT Support access assigned. |
| 10 | `10-leaver-user-disabled-no-sessions.jpg` | Leaver workflow showing the user disabled and no active sessions present. |
| 11 | `11-mfa-otp-enforced.jpg` | TOTP MFA enforcement verified during user authentication without exposing the OTP secret or code. |
| 12 | `12-finance-portal-home.jpg` | Finance Portal application available for OIDC authentication testing. |
| 13 | `13-oidc-login-success.jpg` | Successful OpenID Connect authentication through Keycloak. |
| 14 | `14-authentication-success-authorization-denied.jpg` | User authenticated successfully but was denied Finance Portal access because the required role was missing. |
| 15 | `15-finance-user-authorization-granted.jpg` | Finance user successfully authorized after the required realm role claim was exposed to the application. |
| 16 | `16-oidc-sso-second-application.jpg` | Single Sign-On verified across the Finance Portal and Employee Portal using the existing Keycloak session. |
| 17 | `17-login-error-event-troubleshooting.jpg` | Keycloak user-event investigation showing a controlled `LOGIN_ERROR` caused by invalid credentials. |
| 18 | `18-admin-event-role-created.jpg` | Administrative audit event showing creation of the temporary test realm role. |
| 19 | `19-admin-event-create-delete-audit.jpg` | Administrative audit trail showing both creation and deletion of the temporary test role. |
