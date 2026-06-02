# NovaPay Digital Bank Core API Engine

NovaPay Core is an enterprise-grade digital banking backend engineered with strict architectural guardrails, automated contract validation, and an immutable CI/CD pipeline matrix. The platform is designed to handle high-throughput, compliant transaction processing with an emphasis on code security and structural validation.

---

## 🛠️ System Architecture & Tech Stack

* **Core Framework:** FastAPI (Python 3.10)
* **Object-Relational Mapping (ORM):** SQLAlchemy 2.0
* **Database Engine:** SQLite (Local Testing Ecosystem)
* **Automated Testing Suite:** PyTest with Starlette TestClient
* **Static Application Security Testing (SAST):** Bandit
* **Supply Chain Vulnerability Management:** AquaSecurity Trivy Natively Audited
* **Automation Framework:** GitHub Actions Runner Matrix

---

## 🗺️ Project Milestones & Progress

### 🟩 Sprint 1: Git Architecture & Build Hardening — **[COMPLETE]**
* Established explicit pipeline orchestration patterns.
* Enforced sequential job gates separating source checkout from testing executions.
* Integrated automated package caching structures to minimize runner overhead times.

### 🟩 Sprint 2: The Security Shield — **[COMPLETE]**
* Implemented automated python static analysis via **Bandit** to prevent low/medium/high-level script vulnerabilities.
* Integrated **Trivy FileSystem Scanner** to continuously audit dependencies against upstream CVE registries, enforcing a failure gate on `CRITICAL` vulnerability presence.

### 🟩 Sprint 3: Database Evolution & Refactoring — **[COMPLETE]**
* Successfully decoupled legacy data schemas by removing the monolithic `name` column across endpoints, Pydantic schemas, and SQLAlchemy data layers.
* Migrated banking models to a cleaner split-string layout tracking `first_name` and `last_name` individually.
* Hardened the testing runtime database session lifecycle using dynamic API dependency overrides to prevent local pipeline run pollution.

### 🟦 Sprint 4: Zero-Downtime Orchestration — **[UP NEXT]**
* Design of high-traffic rollout strategies (Canary/Blue-Green architectures).
* Zero-disruption container version updates.

### 🟨 Sprint 5: Regulatory Compliance Automation — **[PLANNED]**
* Automated audit trial formatting and banking configuration security reporting.

---

## 🚀 CI/CD Pipeline Lifecycle Matrix

The repository implements a fully automated, multi-stage workflow triggered on every code `push` or `pull_request` targeting the `main` branch. 

```text
[Stage 1: Source & Validation] ──► [Stage 2: Build & Test] ──► [Stage 3 & 4: Security Shield]
     (Dependency Caching)             (Unit Validation)            (Bandit SAST & Trivy CVE)
