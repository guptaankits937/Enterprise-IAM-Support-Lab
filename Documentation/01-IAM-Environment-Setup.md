# IAM Environment Setup

**Version:** 1.0  
**Project:** Enterprise IAM Support Lab  
**Platform:** Keycloak  
**Environment:** Ubuntu Server / VirtualBox

---

## Objective

The objective of this phase was to prepare a working Identity and Access Management environment using Keycloak on an Ubuntu Server virtual machine.

The environment was designed to support later IAM activities including:

- User and group administration
- Role-Based Access Control
- MFA
- OIDC application integration
- Single Sign-On
- Authorization testing
- IAM event investigation
- Administrative auditing

---

## Environment Components

| Component | Purpose |
|---|---|
| Ubuntu Server | Hosts Keycloak and test applications |
| VirtualBox | Provides the virtualized lab environment |
| Keycloak | Identity Provider and IAM platform |
| OpenJDK | Java runtime required by Keycloak |
| Python 3 | Runtime for OIDC test applications |
| Windows Host | Browser and remote administration |
| Host-Only Network | Communication between Windows and Ubuntu VM |

---

## Keycloak Installation

Keycloak was installed directly from the official release package rather than through Docker.

The extracted Keycloak directory contained key components including:

```text
bin
conf
lib
providers
themes
```

The `bin` directory contains the Keycloak management scripts including `kc.sh`.

---

## Java Runtime

Keycloak requires a Java runtime.

Java availability was verified using:

```bash
java --version
```

OpenJDK was installed on the Ubuntu Server before starting Keycloak.

---

## Keycloak Startup

Keycloak was started in development mode using:

```bash
cd ~/keycloak-26.7.3
bin/kc.sh start-dev --http-host=0.0.0.0
```

The option:

```text
--http-host=0.0.0.0
```

allows Keycloak to listen on all available IPv4 network interfaces.

This was required so that the Keycloak web interface could be accessed from the Windows host rather than only from the Ubuntu Server itself.

Development mode was used only for this isolated home lab.

---

## Bootstrap Administrator

A temporary bootstrap administrator was created for initial Keycloak administration.

The bootstrap administrator was used to access the Keycloak Administration Console and create the dedicated IAM lab realm.

Passwords and administrative credentials are not stored in this repository.

---

## Network Troubleshooting

During the initial setup, Keycloak was running correctly but could not be reached from the Windows browser.

Keycloak was confirmed to be listening on port `8080`.

The issue was not the Keycloak service itself.

Windows network configuration was reviewed using:

```powershell
ipconfig
```

The Windows host had an interface on the:

```text
192.168.57.0/24
```

virtual network.

The Ubuntu VM also had an interface on the same network.

The correct host-to-VM communication path was therefore:

```text
Windows Host
     |
Host-Only Network
     |
Ubuntu VM
     |
Keycloak :8080
```

After using the correct Ubuntu VM interface, the Keycloak Administration Console became reachable from the Windows browser.

---

## Networking Concepts Reinforced

The setup reinforced several important support concepts.

### localhost

```text
127.0.0.1
```

refers to the local system itself.

A service bound only to localhost is generally not reachable from another machine.

### 0.0.0.0

```text
0.0.0.0
```

means that the service listens on all available IPv4 interfaces.

### IP Address

An IP address identifies a network interface on a system.

A system may have several IP addresses when multiple network adapters are configured.

### Port

Keycloak used:

```text
8080
```

for the lab HTTP service.

Later test applications used separate ports:

```text
Finance Portal   :5000
Employee Portal  :5001
```

---

## Basic Connectivity Troubleshooting Logic

The troubleshooting sequence used in the lab was:

```text
Is the application running?
        |
Is the expected port listening?
        |
Which network interface is it listening on?
        |
Can the client reach the server network?
        |
Are the client and server using the correct IP addresses?
        |
Is a firewall or routing problem present?
```

This troubleshooting approach is relevant to IAM Support, Application Support, and general infrastructure troubleshooting.

---

## Realm Creation

After accessing the Administration Console, a dedicated realm was created:

```text
enterprise-iam-lab
```

The Keycloak `master` realm was kept separate from the lab identities.

The resulting logical structure was:

```text
Keycloak
|
+-- master
|   |
|   +-- Keycloak administrative identities
|
+-- enterprise-iam-lab
    |
    +-- Lab users
    +-- Groups
    +-- Roles
    +-- OIDC clients
    +-- Authentication configuration
```

---

## Why a Separate Realm Was Used

A realm represents an isolated identity and security boundary.

Using a dedicated realm provides separation between:

- Keycloak administration
- Enterprise users
- Application clients
- Roles and groups
- Authentication policies
- User sessions

This also demonstrated why users created in the `enterprise-iam-lab` realm were not visible when viewing users in the `master` realm.

---

## Verification

The environment setup was considered successful when:

- Java was available
- Keycloak started successfully
- Port `8080` was listening
- Keycloak was reachable from the Windows host
- The Administration Console login succeeded
- The dedicated `enterprise-iam-lab` realm was created
- Realm isolation was verified

---

## Security Notes

The following practices were followed during the lab:

- No passwords were stored in GitHub
- OTP secrets were not captured
- MFA QR codes were not published
- Session tokens were not published
- Internal identifiers are sanitized where appropriate
- Development mode is documented as lab-only
- Public screenshots are reviewed before publication

---

## Outcome

A functional Keycloak IAM environment was successfully deployed on Ubuntu Server and made accessible from the Windows host.

The environment provided the foundation for subsequent IAM exercises involving:

```text
RBAC
MFA
Identity Lifecycle
OIDC
Authorization
SSO
Event Analysis
Administrative Auditing
```
