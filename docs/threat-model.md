# Threat Model

## 1. Define Scope

### 1.1 System under review

This review is mainly focused on the CI/CD pipeline and, more specifically, on the path from code to the deployment process.

The pipeline is examined as a secure software delivery chain.

### 1.2 Objective

The main objective is to detect threats that can affect the CIA triad (Confidentiality, Integrity, Availability) of the pipeline.

This analysis is performed on an already implemented pipeline, with the goal of evaluating its security posture, identifying potential weaknesses, and proposing improvements to enhance the overall security of the system.

- pipeline integrity
- secure handling of secrets
- trusted and secure artifact
- secure and controlled deployment

### 1.3 In scope

- source code
- pipeline configuration files
- automated scans
- Dockerfile
- container build process
- registry
- artifact/image
- secrets and credentials
- release workflow
- deployment workflow

### 1.4 Out of scope

- deep application and API security analysis

## 2. System Understanding

### 2.1 Actors

- Developer
- Approver / Reviewer
- CI/CD System
- Container Security System
- GHCR
- Release Operator (Developer / Project Manager)
- Deployment Operator (Developer / Project Manager)

### 2.2 Flows

1. Developer commits and pushes code to the feature branch
2. A pull request against the main branch is created
3. The CI pipeline runs quality and security scans on the code
4. The Container Security pipeline creates an image from the Dockerfile, applies a SHA tag, runs a vulnerability scan, and pushes the image to GHCR
5. The approver or another developer must review and approve the pull request
6. If everything is completed correctly, merge is allowed
7. Another developer or "Project Manager" manually executes the release pipeline, which retrieves the already tested image from the registry and applies a version tag
8. Lastly, the deployment process is also manually executed, retrieving the versioned image and deploying it to a staging-simulated environment

### 2.3 Trust boundaries

- Between the 1st Developer and the feature branch:  
  Code is introduced into the system

- Between the feature branch and the CI pipeline:  
  Untrusted code triggers automated code scans and also enforces best practices on the Dockerfile

- Between the feature branch and the Container Security pipeline:  
  Login to GHCR takes place here (credentials are being used inside the pipeline), the image is built and tested, and if the pipeline is completed correctly, the image is considered trusted

- Between the Container Security pipeline and GHCR:  
  The trusted image is pushed to GHCR

- Between the Approver or 2nd Developer and the PR request:  
  Trust depends on the human factor here, since the 2nd developer must approve the pull request after the automated checks and allow the merge to main

- Between the 3rd Developer and the release pipeline:  
  Trust depends on the human factor here, since the 3rd developer must manually execute the release workflow with the proper SHA tag

- Between the release pipeline and GHCR:  
  The release process retrieves a trusted and tested image (credentials are being used again inside the pipeline)

- Between the "Project Manager" (hypothetically) and the deployment pipeline:  
  Trust depends on the human factor here, since the PM must manually execute the deployment workflow with the proper version tag

- Between the deployment pipeline and the runtime environment:  
  Trusted artifacts are deployed

## 3. Asset Identification

### 3.1 Asset Categories

- Pipeline execution assets
- Container assets
- Secrets assets
- Deployment assets
- Log assets

### 3.2 Specific Assets

#### Pipeline execution assets

- application source code
- Pipeline Runner
- CI pipeline configuration file
- container security pipeline configuration file
- release pipeline configuration file
- deployment pipeline configuration file
- pipeline execution logic (jobs, stages, commands...)
- main branch

#### Container assets

- image/artifact
- Dockerfile
- SHA-tagged and version-tagged images

#### Secrets assets

- GHCR credentials used in pipelines
- environment variables containing sensitive data

#### Deployment assets

- environment configuration file

#### Log assets

- pipeline execution logs, job logs, scan logs
- pull request history and approvals
- release history and tagging metadata

### 3.3 Security Properties

- application source code: Integrity  
  (Altered source code can be injected through the pipeline, not only in a malicious way but also through accidental logical changes in the code)

- Pipeline Runner & execution environment: Confidentiality & Integrity  
  (Critical point of the pipeline. It executes code and has access to sensitive credentials and artifacts)

- CI pipeline configuration file: Integrity  
  (Unauthorized modification could bypass security checks or introduce malicious behavior)

- container security pipeline configuration file: Integrity  
  (Unauthorized modification could bypass security checks or introduce malicious behavior)

- release pipeline configuration file: Integrity  
  (Unauthorized modification could bypass security checks or introduce malicious behavior)

- deployment pipeline configuration file: Integrity  
  (Unauthorized modification could bypass security checks or introduce malicious behavior)

- pipeline execution logic: Integrity, (Confidentiality)  
  (Obviously, unauthorized modification can damage the pipeline, but untrusted reconnaissance of pipeline behavior can also have a negative impact)

- main branch: Integrity & Confidentiality  
  (The main branch contains everything, so it is very critical to keep it trustworthy, modified only by authorized people, and accessed only by authorized people)

- image/artifact: Integrity  
  (The artifact is the final product of the whole pipeline, so it must be trusted. Unauthorized modifications and alterations of the artifact can have crucial impact)

- Dockerfile: Integrity  
  (The creation of the image is based on the Dockerfile. Modification, either malicious or accidental, can have critical impact)

- SHA-tagged and version-tagged images: Integrity  
  (For an organized and controlled software delivery process, the tags used in release and deployment must remain unaltered)

- GHCR credentials used in pipelines: Confidentiality  
  (The GitHub token must be protected. Unauthorized access to the registry could lead to deployment of untrusted artifacts)

- environment variables containing sensitive data: Confidentiality  
  (Exposure could allow unauthorized access)

- environment configuration file: Integrity  
  (Alteration of the environment configuration file can lead to unexpected or malicious runtime behavior)

- pipeline execution logs, job logs, scan logs: Integrity & Availability & Accountability  
  (Logs must remain trustworthy for auditing and incident investigation)

- pull request history and approvals: Integrity & Availability & Accountability  
  (These records must remain trustworthy for auditing and incident investigation)

- release history and tagging metadata: Integrity & Availability & Accountability  
  (These records must remain trustworthy for auditing and incident investigation)

### 3.4 Critical Assets

- Pipeline Runner & execution environment
- CI/CD pipeline configuration
- GHCR credentials
- artifact
- deployment pipeline (environment configuration file)
- main branch

## 4. Threat Identification (STRIDE)

### Threat: Pipeline Runner & execution environment compromise

- Asset: CI Runner
- STRIDE Category: Tampering, Information Disclosure, Elevation of Privilege
- Actor: Malicious code or attacker with repository access

- Description:  
  Untrusted code executed within the CI runner may access sensitive environment variables and credentials or manipulate the build process.

- Impact:
  - Exposure of secrets (e.g. registry or deployment credentials)
  - Tampering of build artifacts
  - Unauthorized access or privilege escalation within the pipeline

### Threat: Pipeline Configuration Tampering

- Asset: CI/CD Pipeline Configuration
- STRIDE Category: Tampering
- Actor: Developer or attacker with repository access

- Description:  
  An attacker could modify the pipeline configuration to disable security checks or inject malicious steps.

- Impact:
  - Bypass of security controls
  - Execution of malicious code
  - Full compromise of the software delivery process

### Threat: GHCR Credential Leakage

- Asset: GHCR Credentials
- STRIDE Category: Information Disclosure, Elevation of Privilege
- Actor: Attacker or malicious pipeline execution

- Description:  
  Exposure of registry credentials through pipeline logs, misconfiguration, or phishing could allow unauthorized access.

- Impact:
  - Unauthorized push or modification of container images
  - Deployment of malicious artifacts
  - Loss of integrity of the container registry

### Threat: Artifact Tampering

- Asset: Container Image
- STRIDE Category: Tampering
- Actor: Attacker with registry or pipeline access

- Description:  
  An attacker could replace or modify container images in the registry or during the build process.

- Impact:
  - Deployment of malicious code
  - Compromise of the runtime environment
  - Loss of trust in the software delivery pipeline

### Threat: Environment configuration file tampering

- Asset: Environment configuration file
- STRIDE Category: Tampering
- Actor: Attacker or malicious code execution

- Description:  
  Malicious or unauthorized modifications of the environment configuration file.

- Impact:  
  Unexpected and malicious runtime behavior

### Threat: Unauthorized or Malicious Merge

- Asset: Source Code Integrity (main branch)
- STRIDE Category: Tampering, Elevation of Privilege
- Actor: Malicious insider or compromised reviewer account

- Description:  
  Unauthorized or malicious approval of pull requests could introduce untrusted code into the main branch.

- Impact:
  - Injection of malicious code into the trusted codebase
  - Propagation of compromised code through the pipeline

### Threat: Unauthorized or Incorrect Release/Deployment Execution

- Asset: Release and Deployment Process
- STRIDE Category: Tampering, Elevation of Privilege
- Actor: Developer or operator with release permissions

- Description:  
  A user with release or deployment permissions could trigger execution using an unverified or incorrect artifact.

- Impact:
  - Deployment of untrusted or vulnerable code
  - Bypass of validation and approval processes
  - Compromise of the target environment

## 5. Risk Assessments & Mitigations

The risk assessment is performed using a qualitative method.

### Threat: pipeline Runner & execution environment compromise

- Likelihood: Medium
- Impact: High
- Risk Level: High

- Risk description:  
  The runner executes pipeline code and may have access to sensitive credentials and artifacts. Exploitation requires influence over pipeline execution or repository changes, but the potential impact is severe.

- Mitigations:
  - Use isolated and ephemeral runners
  - Restrict secrets to specific jobs only
  - Apply least privilege to runner permissions
  - Separate build and deployment permissions
  - Monitor privileged pipeline executions

### Threat: Pipeline Configuration tampering

- Likelihood: Medium
- Impact: High
- Risk Level: High

- Risk description:  
  The configuration files are crucial to the secure software delivery process. Unauthorized modifications, whether malicious or accidental, can have a major negative impact on the pipeline's behavior.

- Mitigations:
  - protect the main branch
  - require PR reviews for pipeline files
  - restrict who can modify workflow files
  - alert on workflow file changes
  - maintain an audit trail for pipeline configuration modifications
  - logs and monitoring

### Threat: GHCR Credential leakage

- Likelihood: Medium
- Impact: High
- Risk Level: High

- Risk description:  
  Although GHCR credentials are used within the pipeline, which reduces direct human handling, if they are stolen or used by an unauthorized person they can lead to malicious image management, tampering, and an incorrect release/deployment process.

- Mitigations:
  - token rotation
  - apply least privilege registry permissions
  - allow registry access only to the workflows that actually need it
  - monitor registry activity and logs
  - alert on unexpected pushes or tag overwrites
  - avoid exposing secrets to PR workflows

### Threat: Artifact tampering

- Likelihood: Low
- Impact: High
- Risk Level: Medium

- Risk description:  
  The artifact is the final product that gets deployed into the production environment. If it gets altered, the impact is severe and can lead to many negative consequences. This exploit path is difficult because it requires multiple steps and there is no direct access to modify the artifact. On the other hand, if accounts are compromised or there is a malicious insider, it can happen much more easily. For this reason, the likelihood is considered low and the overall risk level medium.

- Mitigations:
  - restrict permissions to modify the artifact (e.g. RBAC)
  - continuous monitoring of Dockerfile changes, logs, and alerts on modifications
  - release/deployment pipeline logs
  - enforce review of the specific image version before deployment
  - test the image locally or in an isolated environment before deployment to production
  - use immutable image references (SHA-based)
  - implement image signing

### Threat: environment configuration file tampering

- Likelihood: Low
- Impact: High
- Risk Level: Low

- Risk description:  
  Although it can negatively affect the runtime environment, I consider this a difficult exploitation path. With strong surrounding controls, the overall risk level is low.

- Mitigations:
  - restrict permissions to modify the file (e.g. RBAC)
  - continuous monitoring of docker-compose files and environment variables, with logs and alerts on modifications

### Threat: Unauthorized or Malicious merge

- Likelihood: Medium
- Impact: High
- Risk Level: High

- Risk description:  
  A malicious insider or a compromised reviewer account could approve and merge untrusted code into the main branch. This would introduce unauthorized or harmful changes into the trusted codebase, which would then propagate through the CI/CD pipeline.

- Mitigations:
  - enforce branch protection rules on the main branch
  - require pull request reviews (at least one or two reviewers)
  - use CODEOWNERS for critical files (e.g. pipeline configurations)
  - restrict direct pushes to the main branch
  - require all CI checks to pass before merge
  - log and audit all merge activities
  - revert unauthorized or suspicious commits and revalidate pipeline execution
  - enforce multi-approval for critical operations

### Threat: Unauthorized or Incorrect release/deployment execution

- Likelihood: Medium
- Impact: High
- Risk Level: High

- Risk description:  
  A user with release or deployment permissions could manually trigger execution using an unverified, outdated, or malicious artifact. This could result in deploying untrusted or vulnerable code to the target environment.

- Mitigations:
  - restrict release and deployment permissions to specific roles
  - require manual approval before release and deployment execution
  - ensure only validated and tested artifacts are eligible for release
  - use immutable image references (e.g. SHA-based tags)
  - log and monitor all release and deployment executions
  - roll back to the last known trusted version if needed
  - revoke or adjust permissions in case of misuse
  - enforce multi-approval for critical operations
