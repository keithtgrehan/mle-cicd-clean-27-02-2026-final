# GitHub Actions

**GitHub Actions** is a CI/CD tool that is built into GitHub. It allows you to **run workflows based on events that happen in your repository**. For example, you can run a workflow when a pull request is opened, or when a new commit is pushed to a branch.

It allows you to run tests, build your code, and deploy your application all from one place. It also has a lot of built-in integrations with other tools like Slack, Jira, and more.

For example you can automatically **run tests** before merging a pull request, or you can automatically **build a Docker image** when a new commit is pushed to a branch and then push it to a Docker registry. 

## How to use GitHub Actions

Let's start simple. We'll create a **workflow** that runs a test when a pull request is opened.

1. Create a **new repository** on GitHub
2. Create a `requirements.txt` file with the following content:

```
pytest
```

3. Create a new file called `tests/test_calculator.py` and add the following code:

```python
from src.calculator import add
import pytest

def test_add():
    assert add(1, 2) == 3
    assert add(-2, 2) == 0
    assert add(0, 0) == 0
```

4. Create a new file called `.github/workflows/test.yml` and add the following code:

```yaml
on:
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11.3'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest
```

5. Push your changes to GitHub into _main_

6. Go to the **Settings** tab in your repository and click on **Actions** -> **General**:
    - Workflow permissions: `Read and write permissions`
    - Check mark: `Allow GitHub Actions to create and approve pull requests`
    - **Save**

    ![](./images/action.png)

7. In the **Settings** go to **Branches** -> `Add classic branch protection rule`:
    - Branch name pattern: `main`
    - Check mark: `Require a pull request before merging`
      - Check mark: `Require approvals`
    - Click on **Create**

    ![](./images/protection-rule.png)

>The checks will run also without this but it is a good practice to require reviews before merging to main.

8. Now create a **new branch**

9. Add a python file called `src/calculator.py` with the following code:

```python
def add(a, b):
    return a + b
```

10. **Commit** your changes and **open a pull request** from your new branch to main. You should see the test running.

    ![](./images/pr-check.png)

Often there are some checks that will run next to pytest. For example, if you have a linter, it will run and check if your code is formatted correctly. One example is [Black](https://black.readthedocs.io/en/stable/integrations/github_actions.html). It has also extensions or plugins for many IDEs like VSCode, PyCharm, etc.


# CI/CD with GitHub Actions

This repository demonstrates a **simple CI/CD pipeline for a Python project using GitHub Actions**.  
It shows how to automatically run **tests**, enforce **code formatting**, and optionally run a **training script** as part of continuous integration.

---

# Overview

The goal of this project is to demonstrate the core CI/CD workflow used in modern ML and software projects:

1. Write code
2. Write tests
3. Push changes to GitHub
4. Automatically run checks in GitHub Actions
5. Merge only if checks pass

This ensures that broken code cannot be merged into the main branch.

---

# Repository Structure
mle-cicd-clean-27-02-2026-final
│
├── src/
│   ├── calculator.py        # simple example function
│   └── train.py             # example ML training script
│
├── tests/
│   └── test_calculator.py   # pytest unit tests
│
├── .github/workflows/
│   ├── test.yml             # runs pytest
│   ├── black.yml            # checks formatting with black
│   └── cml.yaml             # optional training workflow
│
├── requirements.txt
├── pytest.ini
└── README.md

---

# CI Workflows

## Test Workflow

File:

.github/workflows/test.yml

Runs automatically when:

- Code is pushed to `main`
- A Pull Request is opened to `main`

Steps performed by GitHub Actions:

1. Checkout repository
2. Install Python
3. Install dependencies
4. Run unit tests

Command executed:

PYTHONPATH=. python -m pytest -v

Purpose:

- Prevent broken code from being merged
- Ensure all tests pass before integration

---

## Code Formatting Workflow

.github/workflows/black.yml

Runs automatically on pushes and pull requests.

Steps:

1. Install Python
2. Install `black`
3. Check formatting

Command executed:

black –check .

Purpose:

- Enforce consistent Python code formatting
- Prevent style inconsistencies in the repository

Developers should run locally before committing:

black .

---

## Training Workflow (CML Example)

File:

.github/workflows/cml.yaml

Demonstrates how a **training script can run inside CI**.

Steps:

1. Checkout repository
2. Install dependencies
3. Run training script

Command executed:

python src/train.py

Example output:

metrics.txt

This simulates how ML pipelines can generate metrics during automated workflows.

---

# Local Development

Create a Python environment:

pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run tests locally:

PYTHONPATH=. python -m pytest -v

Format code locally:

black .

---

# Typical Development Workflow

Create a feature branch:

git checkout -b feature/new-feature

Make changes and commit:

git add .
git commit -m “Add new feature”

Push the branch:

git push origin feature/new-feature

Create a Pull Request.

GitHub Actions automatically runs:

- Tests
- Formatting checks

If all checks pass, the PR can be merged safely into `main`.

---

# Key Concepts Demonstrated

This repository demonstrates:

- Continuous Integration (CI)
- Automated testing with pytest
- Code style enforcement with black
- GitHub Actions workflows
- Pull request validation
- Basic ML workflow automation

---

# Result

With this setup:

- Every push triggers automated checks
- Pull requests must pass CI before merging
- Code quality and reliability are enforced automatically

This is the **standard CI/CD foundation used in modern ML engineering and software projects**.