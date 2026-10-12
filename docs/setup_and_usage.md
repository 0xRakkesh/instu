# Setup and Usage Guide

This document describes how to set up the environment and run Instagram fetching scripts.

---

## 1. Prerequisites

- Python 3.8 or higher
- `pip` package manager
- WSL (Ubuntu) or any Linux / macOS / Windows terminal

---

## 2. Virtual Environment Setup

It is recommended to run inside an isolated Python virtual environment:

```bash
# Navigate to the project root
cd /home/rakesh/instu

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

---

## 3. Install Dependencies

Install `instaloader`:

```bash
pip install instaloader
```

To freeze dependencies for later use:

```bash
pip freeze > requirements.txt
```

---

## 4. Quick Execution Test

You can test fetching using the Python interactive shell or a quick test command:

```bash
python3 -c "import instaloader; L = instaloader.Instaloader(); print('Instaloader ready!')"
```

---

## 5. Troubleshooting Common Issues

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `ProfileNotExistsException` | Post deleted or private account | Check URL and verify post is publicly visible in an incognito browser |
| `QueryReturnedBadRequestException` | Rate limited by Instagram | Add delay (`time.sleep(3)`), wait 10-15 minutes, or log in with a session |
| `LoginRequiredException` | Instagram forced login wall | Run `instaloader --login=username` and load the saved session |
| `ModuleNotFoundError: No module named 'instaloader'` | Virtual environment not active | Activate virtual environment (`source venv/bin/activate`) or re-run `pip install instaloader` |
