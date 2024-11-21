# Exploring Dependency-Related Build Breakages in the NPM Ecosystem

This project investigates dependency-related build failures in the NPM ecosystem by analyzing 24 JavaScript projects. The study identifies the challenges posed by dependency management, examines the duration of breakages, and categorizes common issues. These insights aim to improve the reliability of software projects leveraging NPM and propose strategies for enhanced dependency management practices.

---

## Overview

Modern software systems heavily rely on third-party dependencies, making dependency management crucial for maintaining project stability. This study specifically explores:

- **Prevalence of Dependency-Related Breakages**: 11.7% of project failures stemmed from dependency issues.
- **Breakage Duration**: Breakages persisted anywhere from 2 minutes (automated fixes) to 5 months (manual interventions).
- **Breakage Categories**: Issues like peer dependency conflicts, lock file mismatches, and incompatible Node.js versions were among the most frequent.

By replaying builds locally and analyzing build outcomes, this study provides actionable insights for developers, researchers, and project managers to address dependency-related challenges.

---

## Key Features

### 1. Dataset Collection
- Projects were selected based on popularity, activity, and reproducibility criteria:
  - Minimum 1,000 downloads.
  - At least 700 commits.
  - Contained GitHub CI configuration files with `npm install` steps.

### 2. Build Replay
- Local builds were replayed using **act**, a tool for reproducing GitHub Actions workflows locally in Docker containers.
- Commits impacting `package.json` were traced, and isolated environments were created for each build.

### 3. Dependency-Related Analysis
- Build logs were manually reviewed to classify outcomes as "failed" or "passed."
- Dependency-related failures were further categorized into seven distinct types:
  - Peer Dependency Conflicts
  - Lock File Version Mismatches
  - Incomplete Installations
  - Missing/Undefined Dependencies
  - Incompatible Node.js Versions
  - Frozen Lock File Errors
  - Enoent (File Not Found) Errors

---

## Results Summary

1. **Dependency-Related Breakages**:
   - Accounted for 11.7% of project failures.
   - Highlighted the importance of robust dependency management practices.

2. **Breakage Duration**:
   - Average fix time: **12 days**.
   - Fastest fix: **2 minutes** (via automation).
   - Longest fix: **5 months** (manual intervention).

3. **Breakage Categories**:
   - **Peer Dependency Conflicts**: Represented 60% of dependency-related failures.
   - Other issues included lock file mismatches, incompatible Node.js versions, and incomplete installations.

