# GitHub Build Reproduction

The `build_logs.py` script automates the process of replaying builds for specific commits in a GitHub repository and extracting detailed build logs. This script is particularly useful for analyzing Continuous Integration (CI) workflows and their associated builds.

---

## Features

1. **Commit-Based Build Replay**:
   - Replays builds for specific commits from a list provided in a CSV file.
   - Supports user interaction to select specific jobs within GitHub Actions workflows.

2. **Build Information Parsing**:
   - Extracts and displays details of GitHub Actions workflows and associated build jobs using the `act` tool.

3. **Build Logs Storage**:
   - Saves build logs for each commit to a specified directory for further analysis.

4. **Change Detection**:
   - Identifies changes in `.yml` files under `.github/workflows/` between commits to highlight potential workflow modifications.

---

## Prerequisites

1. **Repositories**:
   - The target repositories must be downloaded locally before running the script.
   - Use `git clone` to ensure the repository is in the correct location.

2. **Python 3.8+**:
   - Install required Python libraries:
     ```bash
     pip install pandas
     ```

3. **Git**:
   - Git must be installed and available in your system's PATH.

4. **act**:
   - Install `act` for local GitHub Actions workflow emulation:
     ```bash
     brew install act  # MacOS
     sudo apt install act  # Linux
     ```

5. **Docker**:
   - Docker is required for running builds via `act`. Install it from [Docker's official website](https://www.docker.com/).

---

## Setup and Usage

### 1. Prepare Input Files

- **Commits File**:
  - Create a CSV file listing commit hashes in a column named `hash` (e.g., `Commits/aerospike-client-nodejs commits.csv`).
- **Local Repository**:
  - Ensure the target repository is downloaded locally and matches the `repo_path` specified in the script.

### 2. Configure the Script

- Update the `repo_path` variable to the local path of your cloned repository:
  ```python
  repo_path = "./github/aerospike-client-nodejs"


### 3. Update dir path
- Update the logs_directory variable to the directory where build logs will be stored:
```python
logs_directory = "C:\\Users\\YourUsername\\Desktop\\BuildLogs"
```

## Authors
Shaquille Pearson
Mahmoud Alfadel
