# Installation

## Production Installation (Recommended)

ChangeLens is distributed as a pre-built Python Wheel via GitHub Releases.

Install the latest release directly with pip:

```bash
python -m pip install changelens
```

Alternatively, if `pip` is already available on your PATH:

```bash
pip install changelens
```

### Windows Users

If `changelens` is not recognized after installation:

```text
'changelens' is not recognized as an internal or external command
```

add your Python **Scripts** directory to your `PATH`.

For a standard per-user installation, it is typically located at:

```text
C:\Users\<YourUsername>\AppData\Local\Python\pythoncore-<PythonVersion>\Scripts
```

Restart your terminal after updating your PATH.

You can also invoke the executable directly from that directory if needed.

---

## Local Development Setup

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/Mohamed-Zouari-dev/Change_Lens.git
cd Change_Lens
python -m pip install -e .
```

# Getting Started

Once installed, the `changelens` command is available from your terminal. If you're on Windows and the command isn't recognized, add your Python `Scripts` directory to your `PATH` as described above.

---
## Verify Installation

Confirm that ChangeLens was installed successfully:

```bash
changelens --help
```

Expected output:

```text
Usage: changelens [OPTIONS] COMMAND [ARGS]...

Commands:
  init
  verify
  diff
```

## 1. Initialize a Baseline Snapshot

Scan a target directory and freeze its state.

You can pass inline exclusions or rely on a local `.changelensignore` file placed in the target directory root.

```bash
changelens init /etc/nginx --output nginx_baseline.json --exclude "*.tmp"
```

Example output:

```
Baseline created successfully.
Files scanned: 12543
Snapshot saved: nginx_baseline.json
```

---

## 2. Verify System Integrity

Compare a live directory against a historical baseline to detect:

- Unauthorized modifications
- Malware persistence
- Configuration drift
- Software changes
- Security breaches

```bash
changelens verify nginx_baseline.json /etc/nginx
```

---

## 3. Generate Automation and Audit Logs

Export structural details to feed external alerting pipelines, SIEM systems, or CI/CD reports.

```bash
changelens verify nginx_baseline.json /etc/nginx \
    --save-json audit_report.json \
    --save-md summary.md
```

Generated reports:

```
audit_report.json
summary.md
```

---

## 4. Offline Directory Diffing

Compare two completely separate snapshots taken at different points in time without accessing the original filesystem.

```bash
changelens diff monday_baseline.json friday_snapshot.json
```

Useful for:

- Incident response investigations
- Compliance audits
- Historical forensic analysis

---

# Advanced Hardening: Tamper Protection

To prevent attackers with elevated privileges from modifying tracking baselines, ChangeLens supports cryptographic snapshot signing using HMAC-SHA256.

## Sign the Baseline During Initialization

Set a high-entropy secret key:

```bash
export CHANGELENS_SECRET="your-high-entropy-signing-key"
```

Create a signed snapshot:

```bash
changelens init /var/www/html -o secure.json
```

---

## Verify With Strict Authenticity Checks

```bash
export CHANGELENS_SECRET="your-high-entropy-signing-key"

changelens verify secure.json /var/www/html
```

If an attacker manually modifies `secure.json` to forge malicious file changes, the signature validation engine detects the alteration using constant-time comparison, aborts verification, and raises a critical integrity alert.

---

# Architecture Overview

ChangeLens is designed around four main components:

```
                +----------------+
                |  CLI Interface |
                +--------+-------+
                         |
                         v
                +----------------+
                | Snapshot Engine |
                +--------+-------+
                         |
        +----------------+----------------+
        |                                 |
        v                                 v
+---------------+              +----------------+
| Hash Workers  |              | Ignore Parser  |
| SHA-256 Engine|              | Contract Rules |
+---------------+              +----------------+
        |
        v
+----------------+
| Snapshot Store |
| JSON Metadata  |
+----------------+
```

---

# Security Model

ChangeLens provides:

| Feature | Protection |
|---------|------------|
| SHA-256 hashing | Detects file content changes |
| HMAC-SHA256 signing | Prevents snapshot tampering |
| Ignore contract | Prevents inconsistent scans |
| Offline diffing | Enables forensic analysis |
| JSON reports | Integrates with security tooling |

---

# Example Use Cases

## Enterprise Servers

Monitor critical directories:

```bash
changelens init /etc --output etc_baseline.json
```

Verify periodically:

```bash
changelens verify etc_baseline.json /etc
```

---

## Web Application Security

Monitor deployed applications:

```bash
changelens init /var/www/application \
    --output production.json
```

Detect unauthorized changes after deployment.

---

## Compliance Auditing

Generate evidence reports:

```bash
changelens verify baseline.json /secure/data \
    --save-md compliance_report.md
```

Useful for:

- Security audits
- Change management
- Regulatory compliance

---

# Roadmap

## v1.0

- [x] SHA-256 file hashing
- [x] Directory snapshots
- [x] Integrity verification
- [x] JSON reporting
- [x] Markdown reporting

## v1.1

- [ ] Parallel hashing optimization
- [ ] `.changelensignore` support
- [ ] HMAC snapshot signing
- [ ] Advanced diff engine

## v2.0

- [ ] SIEM integrations
- [ ] Real-time filesystem monitoring
- [ ] Web dashboard
- [ ] Distributed agent architecture

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
