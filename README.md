# Enterprise DevSecOps Pipeline for a Containerized FastAPI Application

## Overview

This project demonstrates the design and implementation of a secure, multi-stage CI/CD pipeline across the full Software Development Lifecycle (SDLC).

The pipeline introduces structured delivery stages (code → build → release → deploy) and integrates security controls at each step.  
It is designed to reflect how a small SaaS team can transition from ad-hoc development to a controlled and security-aware delivery process.

---

## Business Context

A small SaaS company is developing a web application with:

- frequent code changes
- no standardized CI/CD process
- no security validation before release

This introduces risks such as:

- accidental exposure of secrets
- vulnerable dependencies entering production
- unverified container images being deployed
- lack of release control and traceability

This project addresses those gaps by implementing a secure and structured DevSecOps pipeline.

---

## Objectives

- Integrate security controls directly into the CI/CD pipeline
- Enforce security policies (not just detect issues)
- Establish a clean and scalable delivery workflow
- Apply secure-by-design and secure-by-default principles
- Demonstrate production-minded pipeline design

---

## Architecture Summary

The application is a lightweight FastAPI service that includes:

- health endpoint
- configuration endpoint
- token validation logic
- protected endpoint
- unit tests

The application is containerized and validated through multiple pipeline stages before being promoted to release.

---

## CI/CD Pipeline Overview

The pipeline follows a **build-once, promote-artifact** strategy:

1. Code is pushed to a feature branch  
2. Pull Request is opened against `main`  
3. CI pipeline runs quality and security checks  
4. Merge is blocked if checks fail  
5. Approved code is merged into `main`  
6. Docker image is built and pushed to GHCR (tagged with commit SHA)  
7. Release workflow promotes the image to a versioned tag  
8. Staging deployment validates the release configuration  

---

## Security Controls

The pipeline integrates the following tools:

- **Black** — code formatting  
- **Flake8** — linting  
- **Pytest** — unit testing  
- **Bandit** — static analysis (SAST)  
- **pip-audit** — dependency vulnerability scanning  
- **Gitleaks** — secrets detection  
- **Hadolint** — Dockerfile best practices  
- **Trivy** — container vulnerability scanning  

### Enforcement

Security is enforced through:

- failing CI jobs on violations  
- pull request validation  
- protected `main` branch  
- required status checks before merge  

---

## Pipeline Stages

### 1. Code Quality & Security

- formatting validation  
- linting  
- unit tests  
- static analysis (SAST)  
- dependency vulnerability scanning  
- secrets detection  

### 2. Container Security

- Docker image build  
- Dockerfile linting  
- container vulnerability scanning  
- policy enforcement (fail on high/critical findings)  
- image push to GHCR with immutable SHA tag  

### 3. Release Promotion

- promotion of pre-built image  
- version tagging without rebuilding  

### 4. Staging Deployment

- environment-based configuration  
- deployment validation using Docker Compose  

---

## Repository Structure

```text
devsecops-pipeline/
├── app/
│   ├── routes/
│   ├── services/
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
├── docker/
│   └── Dockerfile
├── deploy/
│   ├── docker-compose.yml
│   └── staging/
├── docs/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── security.yml
│       ├── release.yml
│       └── deploy.yml
└── README.md

## Local Development

Run locally:

uvicorn app.main:app --reload

Run tests:

pytest app/tests -v

Build Docker image:

docker build -f docker/Dockerfile -t devsecops-demo-api:local .

Run container:

docker run --rm -p 8000:8000 devsecops-demo-api:local

## Pipeline Stages

1. Code Quality & Security

-formatting validation
-linting
-unit testing
-static analysis (SAST)
-dependency vulnerability scanning
-secrets detection

2. Container Security

-Docker image build
-Dockerfile linting and best-practice enforcement
-image vulnerability scanning
-container policy enforcement
-publication to GHCR using an immutable SHA tag

3. Release Promotion

-promotion of a tested image
-version tagging without rebuilding 

4. Staging Deployment

-environment-based configuration
-deployment validation using Docker Compose


## Security Enforcement Demo

A controlled test was performed by introducing a fake secret into a pull request.

Expected behavior:
-Gitleaks detects the secret
-CI pipeline fails
-the pull request is blocked from merging into main
-This confirms that the pipeline actively enforces security policies and prevents unsafe code from reaching the main branch.

Example Outputs

## Future Improvements

-cloud-based deployment (AWS)
-Infrastructure as Code (Terraform)
-monitoring and alerting
-runtime security controls

