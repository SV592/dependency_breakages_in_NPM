# GitHub Repository Data Extractor

The `refractored_get_info.py` script is designed to retrieve metadata about GitHub repositories using the GitHub GraphQL API. It focuses on extracting detailed information about repositories, including their stars, forks, commit history, and more. This tool is particularly useful for researchers and developers analyzing repository characteristics or trends.

---

## Features

1. **Retry on Rate Limit**:
   - Automatically handles API rate limits by pausing and retrying requests after the reset time.
   - Retries up to 5 times for transient errors (e.g., HTTP 502).

2. **Data Extraction**:
   - Extracts information such as:
     - Repository name and description.
     - URL, privacy status, and fork status.
     - Fork count, stargazer count, and commit history for both `main` and `master` branches.

3. **Error Handling**:
   - Logs and stores failed requests in a `failed_info` file for further inspection.

4. **Output**:
   - Saves processed repository data in a CSV file (`scheme_info`) for easy analysis.

---

## Prerequisites

- **Python 3.8+**
- Required Python libraries:
  - `pandas`
  - `requests`
  - `json`
- A valid GitHub API token with repository read access.

---

## Setup and Usage

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/github-repo-data-extractor.git
cd github-repo-data-extractor
```

### 2. Install Dependencies

```bash
pip install pandas requests
```
