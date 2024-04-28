<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">GEN-AI-PORTFOLIO</h1>
</p>
<p align="center">
    <em><code>Engineering with Generative AI - Portfolio Exam - Task 1 Submission</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/lawRathod/gen-ai-portfolio?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/lawRathod/gen-ai-portfolio?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/lawRathod/gen-ai-portfolio?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/lawRathod/gen-ai-portfolio?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>

<br><!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary><br>

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Modules](#modules)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Tests](#tests)
- [Project Roadmap](#project-roadmap)
- [License](#license)
- [Acknowledgments](#acknowledgments)
</details>
<hr>

## Overview

<code>► INSERT-TEXT-HERE</code>

---

## Features

<code>► INSERT-TEXT-HERE</code>

---

## Repository Structure

```sh
└── gen-ai-portfolio/
    ├── LICENSE
    ├── README.md
    ├── Task_1_Test_Cases.ipynb
    ├── app.py
    ├── cli_prompts.json
    ├── explain_prompts.json
    ├── llm.py
    ├── llm_generate.py
    ├── rag.py
    └── requirements.txt
```

---

## Modules

<details closed><summary>.</summary>

| File                                                                                                         | Summary                         |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------- |
| [requirements.txt](https://github.com/lawRathod/gen-ai-portfolio/blob/master/requirements.txt)               | <code>► INSERT-TEXT-HERE</code> |
| [explain_prompts.json](https://github.com/lawRathod/gen-ai-portfolio/blob/master/explain_prompts.json)       | <code>► INSERT-TEXT-HERE</code> |
| [llm.py](https://github.com/lawRathod/gen-ai-portfolio/blob/master/llm.py)                                   | <code>► INSERT-TEXT-HERE</code> |
| [Task_1_Test_Cases.ipynb](https://github.com/lawRathod/gen-ai-portfolio/blob/master/Task_1_Test_Cases.ipynb) | <code>► INSERT-TEXT-HERE</code> |
| [rag.py](https://github.com/lawRathod/gen-ai-portfolio/blob/master/rag.py)                                   | <code>► INSERT-TEXT-HERE</code> |
| [cli_prompts.json](https://github.com/lawRathod/gen-ai-portfolio/blob/master/cli_prompts.json)               | <code>► INSERT-TEXT-HERE</code> |
| [app.py](https://github.com/lawRathod/gen-ai-portfolio/blob/master/app.py)                                   | <code>► INSERT-TEXT-HERE</code> |
| [llm_generate.py](https://github.com/lawRathod/gen-ai-portfolio/blob/master/llm_generate.py)                 | <code>► INSERT-TEXT-HERE</code> |

</details>

---

## Getting Started

**System Requirements:**

- **Python**: `version 3.9.16`

### Installation

> 1. Clone the `gen-ai-portfolio` repository:
>
> ```console
> $ git clone https://github.com/lawRathod/gen-ai-portfolio
> ```
>
> 2. Change to the project directory:
>
> ```console
> $ cd gen-ai-portfolio
> ```
>
> 3. Install the dependencies:
>
> ```console
> $ make deps
> ```

### Usage

> NOTE: Before beginning make sure to have `AWS_API_KEY`, `OPENWEATHERMAP_API_KEY` in your env OR .env file in project root.

> Run gen-ai-portfolio's streamlit UI using the command below:
>
> ```console
> $ make start
> ```

### Tests

> Run the test suite using the command below:
>
> ```console
> $ pytest
> ```

---

## Project Roadmap

- [x] `Build a way to convert human language to todo app cli command using LLM.`
- [X] `Pass all testcases in Task_1_Test_Cases.ipynb`
- [X] `Build streamlit UI to try out the LLM and prompts`
- [X] `Build weather agent to query for weather in human language`
- [X] `Integrate weather agent to improve logic used for task management`
- [ ] `Extend usage of rag agents to include calendar and search`
- [ ] `Improve available cli understand of llm to cover more actions`
- [ ] `Make prompts cli app agnostic`
- [ ] `Reduce steps to reach to the final command through improving prompts`

---

## License

This project is submission for portfolio exam for Engineering with Generative AI course at RPTU, Kaiserslauter, Germany. Use of source for analytical or research is permitted.

---

## Acknowledgments

- https://github.com/foobuzz/todo
- https://www.llamaindex.ai
- https://docs.llamaindex.ai/en/stable/api_reference/readers/weather/
- https://api.python.langchain.com/
- https://openweathermap.org/appid

[**Return**](#-overview)

---
