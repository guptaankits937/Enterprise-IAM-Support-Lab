# IAM Test Applications

This directory contains the two Flask applications used in the Enterprise IAM Support & Identity Security Lab.

## Applications

### Finance Portal

`Finance-Portal/app.py`

Used to validate:

- OpenID Connect authentication through Keycloak
- Authorization Code Flow with PKCE S256
- Realm-role claim handling
- Application authorization using the `finance-user` role
- HTTP 403 access denial when authentication succeeds but authorization fails

### Employee Portal

`Employee-Portal/employee_app.py`

Used to validate:

- OpenID Connect authentication through Keycloak
- Reuse of an existing Keycloak authenticated session
- Single Sign-On across a second application
- Separate Flask session-cookie naming for the second local application

## Keycloak Configuration

The public GitHub copy does not contain the private lab IP address.

Before running the applications, set the Keycloak base URL for your own environment:

```bash
export KEYCLOAK_BASE="http://<KEYCLOAK_HOST>:8080"
```

The applications use the following realm and clients:

```text
Realm: enterprise-iam-lab
Finance client: finance-portal
Employee client: employee-portal
```

Both clients were configured as public OpenID Connect clients using Authorization Code Flow with PKCE S256.

## Security Notes

- No client secret is stored because these were public OIDC clients.
- Flask session secret material is generated at runtime using `os.urandom(24)`.
- Passwords, MFA secrets, OTP values, tokens, and session identifiers are not stored in this repository.
- The private lab IP address was removed from the public source copy.

## Ports

```text
Finance Portal: 5000
Employee Portal: 5001
Keycloak: 8080
```
