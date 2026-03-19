# Architecture Overview

## 1. Introduction

This document describes the architecture of the DevSecOps pipeline and the application delivery flow.

The system is designed to demonstrate a secure, structured, and production-minded CI/CD pipeline for a containerized web application.

## 2. Main Components

- Application Layer(FastAPI)
- CI/CD Pipeline(Github Actions)
- Container Registry(GHCR)
- Deployment Layer(Docker compose - staging simulation)

## 3. Application Architecture

A very small FastAPI service just to demostrate the pipeline:

- REST API Endpoints
- basic token auth logic
- unit tests
- configuration-based behaviour

Structure:

app/
├── routes/
├── services/
├── tests/
├── main.py
└── requirements.txt

## 4.CI/CD Pipeline Architecture

The pipeline is triggered on:

- push to feature branches
- pull requests to  `main`
- release & deployment pipeline is triggered manually

Pipeline automated Flow:

Developer Push / Pull Request
↓
(1) Code Quality & Testing

- Code formatting (Black)
- Linting (Flake8)
- Unit tests (Pytest)

    ↓

(2) Application Security Checks

- Static Application Security Testing (SAST - Bandit)
- Secrets scanning (Gitleaks)
- Dependency vulnerability scanning (pip-audit)
- Dockerfile best-practices enforcement (Hadolint)

    ↓

(3) Container Security & Build

- GHCR authentication
- Assign immutable image tag (commit SHA)
- Build Docker image
- Image vulnerability scanning (Trivy)
- Policy gate (fail on critical vulnerabilities)
- Push image to GHCR

    ↓

(4) Release Promotion (Manual Workflow)

- Promote previously tested image
- Apply version tag (no rebuild)

    ↓

(5) Deployment Pipeline

- Controlled deployment(choosing by image version from the release workflow)
- Staging deployment using Docker Compose

## 5. Security Architecture

Security is integrated across all stages of the pipeline.

### Security Controls Mapping

| Stage                | Control                    | Tool        |

-------------------------------------------------------------------
| Push/PR              | Branch Protection & Enforcement| Branch rule |
| Code Quality         | Formatting & Linting       | Black, Flake8|
| Testing              | Unit Tests                 | Pytest      |
| SAST                 | Static Code Analysis       | Bandit      |
| Dependencies         | Vulnerability Scanning     | pip-audit   |
| Secrets              | Secret Detection           | Gitleaks    |
| Container Build      | Dockerfile Best Practices  | Hadolint    |
| Container Runtime    | Image Vulnerability Scan   | Trivy       |
| Release              | Release the already tested image + versioning|
| Deploy               | Controlled and organised deployment|

## 6. Artifact Flow

The pipeline follows a **build-once, promote-artifact** strategy:

- Images are built once per commit
- Tagged with immutable SHA
- Promoted to versioned releases without rebuild(manually)
- Deployed by version(manually)

This ensures:

- traceability
- reproducibility
- reduced risk of drift
- scalabilty
- better control
- better security

## 7. Deployment Architecture

Deployment is implemented as a staging simulation using Docker Compose.

Key characteristics:

- environment-based configuration
- separation between build and deploy
- controlled release promotion

## 8. Summary

This architecture demonstrates how a secure and scalable CI/CD pipeline can be designed for a modern application.

It emphasizes:

- security integration across the SDLC
- policy enforcement instead of passive scanning
- controlled artifact promotion
- production-oriented delivery workflow
