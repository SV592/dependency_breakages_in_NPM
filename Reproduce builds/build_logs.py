import subprocess
import pandas as pd
import re

def run_command(cmd, cwd):
    print(f"Executing command: {cmd}")

    # Execute the command
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd, text=True, encoding='utf-8')

    # Check if the command execution was successful
    if result.returncode != 0:
        print(f"Error executing command: {cmd}")
        if result.stderr:
            print(result.stderr)
        return None

    return result.stdout.strip()


def determine_build_job(job_lines):
    job_mapping = {}
    for line in job_lines:
        match = re.match(r"(\d+)\s+(\w+)\s+(.+?)\s{2,}(.+?)\s{2,}(.+?)\s{2,}(.+)", line)
        if match:
            job_id = match.group(1)
            job_name = match.group(3)
            workflow_name = match.group(4)
            workflow_file = match.group(5)
            events = match.group(6)
            job_mapping[f"{job_name}_{job_id}"] = {'workflow_name': workflow_name.strip(), 'workflow_file': workflow_file.strip()}
    return job_mapping


def main():
    # Read commit hashes from a CSV file
    commits_df = pd.read_csv("./Commits/aerospike-client-nodejs commits.csv")  # Updated CSV file name
    commits = commits_df["hash"]

    # Specify the commit from which the script should start, if any
    start_commit = ""
    if start_commit:
        start_index = commits[commits == start_commit].index[0]
        commits = commits[start_index:]

    repo_path = "./github/aerospike-client-nodejs"
    logs_directory = "aerospike builds"  # Updated logs directory

    prev_commit = None
    for commit in commits:
        # Check if any .yml file in .github/workflows has changed
        if prev_commit is not None:
            result = subprocess.run(['git', 'diff', '--name-only', prev_commit, commit], capture_output=True, text=True)
            if any(file for file in result.stdout.splitlines() if file.startswith('.github/workflows/') and file.endswith('.yml')):
                input("A build file has changed. Press Enter to continue...")

        # Commands to execute for each commit
        commands = [
            "git reset --hard",
            f"git checkout {commit}",
            "act -l",
        ]

        print(f"Building commit {commit}...")

        for cmd in commands:
            # Execute the command and capture the output
            output = run_command(cmd, repo_path)

            if cmd == "act -l":
                if output is None:
                    print("Error: Unable to retrieve build information.")
                    continue  # Skip processing if output is None

                # Print the output in the desired format
                print("Output from 'act -l':\n")
                lines = output.strip().split("\n")
                for i, line in enumerate(lines, start=0):
                    if line:  # Exclude empty lines from numbering
                        print(f"{i}. {line}")

                # Parse the output to extract job information
                job_mapping = determine_build_job(output.strip().split("\n")[1:])
                # print("Job Mapping:", job_mapping)  # Print job_mapping for debugging purposes

                # Prompt the user to select a build job based on the associated YAML file
                break  # Exit the loop after processing the output

        print("\n")
        selected_job_index = int(input("Enter the number of the build job you want to run: "))
        print("Selected Job Index:", selected_job_index)  # Print selected job index for debugging purposes
        if 0 <= selected_job_index < len(job_mapping):
            selected_job = list(job_mapping.keys())[selected_job_index]

            # Execute the selected build job and save the output to a file
            run_build_cmd = f'act -v -j {selected_job} > "{logs_directory}\\{commit}.txt"'
            run_command(run_build_cmd, repo_path)
        else:
            print("Invalid selection. Please choose a valid build job.\n")
    
    prev_commit = commit
    print("Builds complete!")

if __name__ == "__main__":
    # Entry point of the script
    main()
