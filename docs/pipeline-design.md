# Pipeline Design

## Overview

This document describes the end-to-end CI/CD and DevSecOps delivery flow implemented in this project.

The pipeline is designed to separate validation, trusted artifact creation, release promotion, and deployment into controlled stages.

---

## Pipeline Flow Diagram

![Pipeline Flow Diagram](docs/images/PipelineFlowDiagram.png)

The diagram below illustrates the end-to-end delivery flow of the project, from feature branch development and pull request validation to trusted artifact publication, release promotion, and staged deployment.

It highlights the separation between validation workflows on pull requests and artifact publication workflows on the main branch, as well as the immutable release tag policy enforced during release promotion.

---

## Pipeline Stages

### 1. Development and Pull Request Creation

A developer works on a short-lived feature branch and opens a pull request against the `main` branch.

### 2. Pull Request Validation

The pull request triggers automated validation workflows, including:

- code quality checks
- unit tests
- static analysis
- dependency scanning
- secrets detection
- Dockerfile validation
- container image validation

At this stage, images are built and scanned, but they are **not pushed** to the registry.

### 3. Trusted Artifact Creation

After approval and successful validation, the pull request is merged into `main`.

A new build is created from the trusted `main` branch state, validated again, and then pushed to GHCR using an immutable SHA-based tag.

### 4. Release Promotion

A manual release workflow promotes a previously tested SHA-tagged image to a human-readable version tag.

Release tags are treated as immutable references. If a version tag already exists, the release workflow fails and prevents reassignment.

### 5. Deployment

A separate deployment workflow deploys the approved release tag to a staging-style environment using Docker Compose.

This maintains a clear separation between artifact creation, release management, and deployment execution.

---

## Design Principles

The pipeline was designed around the following principles:

- shift-left security
- controlled promotion of artifacts
- separation of validation and publication
- immutable release versioning
- staged deployment flow
