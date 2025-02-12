# 📂 tools/ - LLM Utility Tools

This folder contains auxiliary scripts and modules that enhance the functionality of the **LLM (Large Language Model) pipeline**. 
It provides specialized tools that require **optional dependencies**, which are not included by default in the base environment.

---

## 🛠️ Underlying Mechanics

### 1️⃣ Dependencies Management
- The tools in this folder rely on external Python libraries like `numpy` and `pandas`, which may **not be installed by default**.
- To ensure these tools function correctly, a **`requirements.txt`** file is included in this directory.
- This mechanism allows tools to be added dynamically without modifying the core environment and re-building container

### 2️⃣ Runtime Installation Approach
- During **container startup**, an `entrypoint.sh` script will check for `requirements.txt` inside `/app/tools/`.
- The application in container environment dynamically **installs missing dependencies** using:
  ```bash
  pip install --no-cache-dir -r /app/tools/requirements.txt
  ```
  This ensures that the required libraries are installed only when the `tools/` folder is mounted and utilized.


---

## 📁 Files Overview

| File                | Description |
|---------------------|-------------|
| `toy_tools.py`      | A module containing helper functions for data manipulation using **`numpy`** and **`pandas`**. |
| `requirements.txt`  | A list of dependencies required for the tools module (currently includes `numpy` and `pandas`). |

---

## 🚀 Usage

### 🧪 Test the provided toy agent to see how it works
Have a look and give a try to `tools_agent` present in hte package by default. It will:
1. Generate a random **`numpy` matrix**.
2. Summarize a sample **`pandas` DataFrame**.
Under the hood it auto-imports the mounted `toy_tools.py` module and installs the dependencies from `requirements.txt` 

### 🎼 Write your own tools
- Create python files containing tools for your agents in `tools/` folder, they will be available during runtime
- Don't forget to add your imports to `requirements.txt` so that no missing imports occur

---

## 📝 Notes
- This directory is designed to be **mounted** at runtime to allow flexible tool additions without modifying the core system.
- If no dependencies are installed and `requirements.txt` is missing, the tools in this folder **will not function** due to missing imports.
