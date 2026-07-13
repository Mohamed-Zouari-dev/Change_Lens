# ChangeLens

ChangeLens is a high-performance, point-in-time File Integrity Monitor (FIM) and cryptographic auditing CLI utility. Built for security compliance, automated system auditing, and post-incident forensics, ChangeLens captures deterministic snapshots of file states and instantly detects unauthorized file modifications, additions, or deletions.

---

# Core Features

* **Multi-Threaded Performance**  
  Concurrent, zero-leak cryptographic file hashing optimized for large, deep enterprise filesystems.

* **Cryptographic Tamper Protection**  
  Optional snapshot signing via HMAC-SHA256 to prevent attackers from altering baseline logs.

* **Persistent Exclusion Contract**  
  Local `.changelensignore` wildcards (similar to `.gitignore`) are compiled directly into the snapshot contract so verification runs remain completely drift-proof.

* **Offline Forensic Diff Engine**  
  Compare two historical snapshots completely offline without requiring access to the live environment.

* **CI/CD & Automation Ready**  
  Structured JSON summaries for SIEM pipelines alongside clean Markdown summaries for automated GitHub Action/GitLab CI job logs.

---

# Installation

## Production Installation (Recommended)

ChangeLens is distributed as a pre-compiled Python Wheel via GitHub Releases. You do not need to clone the source code to use it.

Download and install the latest release directly via pip:

```bash
pip install pip install https://github.com/Mohamed-Zouari-dev/Change_Lens/releases/download/v1.0.0/changelens-1.0.0-py3-none-any.whl
```

---

## Local Development Setup

To contribute to the project or inspect the codebase, clone the repository and install it in editable mode:

```bash
git clone https://github.com/Mohamed-Zouari-dev/Change_Lens.git
cd changelens
pip install -e .
```

---

# Getting Started

Once installed, the global `changelens` binary is available anywhere on your system path.

---

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