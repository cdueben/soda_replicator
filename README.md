# Monash SoDa Replication Template

This repository provides a **template for reproducible, collaborative applied-economics projects**. It contains a basic directory structure (`code/`, `paper/`, `data/`), starter scripts, virtual-environment stubs, and a replication checklist that feeds an automated AI code-review workflow. The [main](https://github.com/sodalabsio/soda_replicator/tree/main) branch contains example files to illustrate template use. Download the example-free [clean](https://github.com/sodalabsio/soda_replicator/tree/clean) branch at the outset of every study to lock in best-practice version control, hand-offs between co-authors and supervisors, and generation of replication packages.

### Contents

- [How to Use This Repo](#how-to-use-this-repo) — quick-start guide
  - [Installation](#1-installation)
  - [Understand the Folder Structure](#2-understand-the-folder-structure)
  - [Create the Project Checklist for AI Checks](#3-create-the-project-checklist-for-ai-checks)
  - [Start Coding](#4-start-coding)
  - [Tick Off the Checklist](#5-tick-off-the-checklist)
  - [Run the AI Code Checker](#6-run-the-ai-code-checker)
  - [Create Final Replication Package for Submission](#7-create-final-replication-package-for-submission)
- [Detailed Documentation](#detailed-documentation) — in-depth design decisions
  - [Directory Structure](#directory-structure)
  - [Virtual Environments](#virtual-environments)
  - [Version Control](#version-control)
  - [Code Quality](#code-quality)
  - [Replication Package](#replication-package)
  - [Claude Assistant GitHub Workflow Setup](#claude-assistant-github-workflow-setup)
  - [Useful Resources](#8-useful-resources)

## How to Use This Repo

We have produced a video tutorial for those who do not want to read the documentation or who need more extensive explanations: https://youtube.com/playlist?list=PLqlvVlXl5PP0NMi-91iG-HuafsIa_qcf6&si=d1mzORY3edhCzF7N.

### 1. Installation

1.1  Download the [clean](https://github.com/sodalabsio/soda_replicator/tree/clean) template: **[Code › Download ZIP](https://github.com/sodalabsio/soda_replicator/archive/refs/heads/clean.zip)**.  
1.2  Unpack & rename the folder to your *project name*.  
1.3 Make sure you have Git installed and GitHub [configured](https://docs.github.com/en/get-started/git-basics/set-up-git).

---

#### Option A: If you would prefer to keep your empirical code separate from your LaTeX code:

1.4 Open the GitHub website and create two empty private repositories named `name-of-your-project_code` and `name-of-your-project_paper`, where `name-of-your-project` is a short name (preferably one or two words) for your research project.  
1.5 Open the terminal (Git Bash on Windows) locally in the `code` folder and enter the following commands:
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/your-github-name/name-of-your-project_code.git
git push -u origin main
```
1.6 Repeat step 1.5 for the `paper` directory.

---

#### Option B: If you want to keep the whole project in a single repository:

1.4 Open the GitHub website and create two empty private repositories named `name-of-your-project`, where `name-of-your-project` is a short name (preferably one or two words) for your research project.  
1.5 Open the terminal (Git Bash on Windows) locally in this folder and enter the following commands:
```bash
git init
echo "data/" >> .gitignore
git add .
git commit -m "initial commit"
git remote add origin https://github.com/your-github-name/name-of-your-project.git
git push -u origin main
```

---

1.7 Configure the GitHub repository/ repositories on the website:
+ **Settings › Collaborators** → add co-authors & supervisors
+ (Optional) **Settings › Branches** → protect `main` branch to enforce code review
+ (Optional) Enable GitHub Actions for automated checks

1.8 Share the `data` folder with your collaborators through a cloud storage provider, such as Dropbox or Google Drive.

---

### 2. Understand the Folder Structure

```bash
project-root/
├── code/        # empirical analysis code managed with Git
|    ├── dataprep/
|    ├── analysis/
├── paper/       # manuscript, slides, figures, and tables managed with Git
|    ├── draft/
|    ├── presentation/
|    └── results/
└── data/        # data shared through cloud storage provider
     ├── raw
     ├── interim/
     ├── analysis/
     └── literature/
```

**Use relative paths when scripts reference data, so that code works out of the box on other machines as well!** I.e., use `../data/analysis/baseline.csv` instead of `/home/your_username/cloud_folder/your_project/data/analysis/baseline.csv`.

---

### 3. Create the Project Checklist for AI Checks

3.1 If you chose the structure with two repositories above, open `code/checklist.md` and `paper/checklist.md`. If you selected the single repository instead, create a new `checklist.md` at the top level.  
3.2 With your co-authors/ supervisor, **outline steps** to fit *this* project's data sources, methods, and outputs.  
3.3 Commit changes:  
```bash
git add checklist.md
git commit -m "customize replication checklist"
git push origin main
```

---

### 4. Start Coding

4.1 Activate the virtual environment in `code` ([`renv`](https://rstudio.github.io/renv/)/ [`venv`](https://docs.python.org/3/library/venv.html)/ [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)).  
4.2 Write scripts in `code/dataprep` and `code/analysis`.  
4.3 Test the pipeline, then push:
```bash
git add .
git commit -m "add first data-prep script"
git push origin main
```
4.4 Verify commits and CI status on GitHub ([GitHub guide](https://docs.github.com/en/get-started/quickstart)).

---

### 5. Tick Off the Checklist

After each milestone:
+ Edit `checklist.md`.
+ Select elements with `[x]`.
+ Request review by your co-authors or supervisor via an issue or a pull request.

---

### 6. Run the AI Code Checker

Invoke the AI checker with `@claude` in an issue or a pull request to:
+ Read checklist.md.
+ Evaluate to what extent the contents of the repository align with the checklist.

If this is your first time using Claude on GitHub, read the [setup guide](#claude-assistant-github-workflow-setup) below.

---

### 7. Create Final Replication Package for Submission

7.1 Follow [guidelines](https://github.com/AEADataEditor/replication-template) from AEA Data editor.  
7.2 Have a look at Cynthia Huang's quarto replication [slides](https://cynthiahqy.github.io/monash-quarto-aea/02a-template/) and [template](https://github.com/cynthiahqy/quarto-replication-template).

---
---

## Detailed Documentation

## Introduction
This repository contains a template for a reproducible research project. The focus lies on quantitative social science. Recommendations might not fully apply to other fields.

Download the template at the start of each new research project. The purpose is to ensure the reproducibility of your analyses from day one with little effort. That does not mean following journals' replication package structure throughout the project, but to have a system in place from which you can produce a replication package with little effort.

Whereas a journal replication package is the final project state bundled into a single unit and extensively documented, earlier stages often benefit from a more modular structure. You probably want to manage your code with Git, but you obviously do not upload terabytes of data to GitHub. Furthermore, it is usually inefficient to maintain the extensive, clunky journal replication package documentation from the start of the project. Rather have a setup which allows you to quickly generate that documentation when needed.

While most recommendations here are agnostic of your choice of data science and typesetting language, this readme adds some language-specific comments in a section below.

## Directory Structure
The template offers directory organization in two different flavors: monorepo and multirepo. In either case, we have the `data`, `code`, and `paper` folders at the top level. `data` holds the data, `code` holds the quantitative analysis code, and `paper` holds the markup code. The difference is in the monorepo managing everything in a single Git repository and the multirepo understanding `code` and `paper` as separate repositories. The installation guide above covers both options. The choice between the two comes down to personal preferences and project complexity.

The advantage of a monorepo is that you have everything in one place - GitHub issues are not spread across multiple repositories, etc. A multirepo, in contrast, is less compact and favors isolation of workflows. If you do not want to mix the version history of your manuscript with edits on your empirical code, the multirepo is the way to go. The same holds for projects that rely on dev containers. You probably do not want to run `paper` and `code` in the same container.

### Data
The `data` directory holds the project's data sets. Raw input data, as downloaded from the source or as collected in an experiment, goes into `data/raw`. Processed, evaluation-ready data belongs into `data/analysis`. In projects with long data cleaning pipelines, it might make sense to add a `data/interim` folder.

As already mentioned, Git is designed for code, not for large data sets. It is a good idea to store the data in a folder synced to the cloud, but not to manage it with Git. In a monorepo, we keep `data` out of version control by adding the directory to `.gitignore`. In a multirepo, `data` is not part of a Git repository at all.

If there are multiple input data sets, each of them should have its separate directory in `data/raw`. The template contains two fictional examples: population data downloaded from `example.com` and weather data downloaded from `example.org`. The data set publisher's documentation, sometimes referred to as code book, and a text file documenting the download URL and the download date should accompany the data files. Online resources can change over time. Hence, store all of this information together in one location from the start.

Similarly, different sets of analysis data can be organized into multiple folders in `data/analysis`. They do, of course, not require extra documentation on where they came from or on which day they were created. The information on how to create the files from the raw data belongs into the `code` directory. And that code should produce the analysis data irrespective of the execution date. It is a good habit to document the analysis data files in that code because (i) this checks the documentation into version control and (ii) it keeps the explanations close to the logic creating the data.

Because many researchers share downloaded papers that are relevant to the project with their coauthors in cloud folders, `data` also has a `literature` subdirectory. This is simply for convenience. Downloaded article PDFs are not part of the final replication package submitted to journals. `data/literature` only exists for paper sharing among coauthors while the project is evolving. It is optional and can be omitted.

The reason to place `literature` in `data`, and not in `paper`, is to exclude it from version control. PDFs in the hundreds of pages would simply clutter the git history meant to track files that you are editing yourself and that feed into a subsequent replication package.

### Code
The quantitative analysis code, covering all steps from the raw data to the results shown in the paper, belong into the `code` directory. This is your R, Python, Stata, Julia, C++ code. It should be managed with Git.

The preprocessing steps turning the `data/raw` into the `data/analysis` files are in `code/dataprep` and the steps deriving insights from the `data/analysis` data are in `code/analysis`. You should, especially in larger projects, further divide the `code/dataprep` and `code/analysis` into sub-folders. You could have one folder per input data set in `code/dataprep`, in which you do all the preprocessing of the respective data set. In a file at the `code/dataprep` level (not in a sub-directory), you then only merge the data. This template illustrates this with example files.

The advantage of placing `code` in the same parent directory as `data` is that you can easily reference data sets using relative paths. No paths have to be adjusted when running the code from another computer. `../data/raw/population/population.csv` remains valid (`..` moves up one level from the current directory).

### Paper
The template's `paper` folder organization assumes users to either write their manuscripts locally or to connect their Overleaf project to a Dropbox folder or GitHub. Overleaf users who host their projects entirely on that platform (without external connections) only store tables and figures in `paper`.

As in the case of `code`, you should control the contents of the `paper` directory with Git - as long as you use a markup language. Students who are not yet familiar with LaTeX or Markdown and still use a word processor like Microsoft Word or Libre Office Writer may not experience large benefits from using Git.

`paper` entails three sub-folders: `draft`, `results`, and `presentation`. Throughout the life cycle of a project, there are exploratory phases. You want to try out different empirical models to identify the underlying pattern in the data, and you experiment with theory to craft a framework that your estimations fit into. The `results` folder is the location to collect and discuss ideas. It is the foundation for the official manuscript in `draft`. `presentation` holds the markup code for seminar and conference presentations. As a PhD student also presenting posters, you might have an additional `poster` folder.

## Virtual Environments
Data science software receives updates over time. R packages are not static. Developers fix bugs and change function behavior across releases. It, therefore, happens that you re-execute your code a few years after you wrote it and obtain different results. Because your replication package needs to reproduce the results shown in the paper, you then start digging through previous versions of the programming language and of the packages that you used. Unfortunately, many packages are not isolated pieces of software. Packages have dependencies. Hence, you puzzle together different package version combinations. In the end, you browse tens of thousands of lines of code and spend days and figuring out the source of a discrepancy.

Virtual environments prevent such drama. The `renv` package in R and the `venv` module in Python track package versions at the project level and allow you to use different versions across projects. You can use version 1.0 in one project and version 1.2 in another project. When you come back to a study at a later point or when someone else wants to execute your code, the software obtains the correct package version from the automatically created configuration file and computes the same results as you did initially.

So, before you write any code, open the `code` directory and follow the installation instructions and introductions for [`renv`](https://rstudio.github.io/renv/), [`venv`](https://docs.python.org/3/library/venv.html), or alternatively [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). This template contains automatically created example configuration files.

With C++, you do not need a virtual environment. Just use CMake with detailed flags and track that file with version control.

## Version Control
There are different version control tools out there. Git is the standard nowadays in both academia and industry. Our [video tutorial series](https://youtube.com/playlist?list=PLqlvVlXl5PP0NMi-91iG-HuafsIa_qcf6&si=d1mzORY3edhCzF7N) covers a brief introduction to some Git basics. For a deeper learning experience, check out Monash's courses or one of the many other online resources on the topic.

Overall, Git tracks versions of your files. It circumvents messy organization where you end up with project directories containing `paper.tex`, `paper_new.tex`, `paper_new_new.tex`, `paper_final.tex`, `paper_final_new.tex`. It allows you to jump between commits, which are version checkpoints set by you, without throwing extra tex files into your folder.

Git comes with various labeling options for commits to easily identify versions. Recover the version of your poster that you presented at the conference last year. Roll back the changes which your coauthor made to your beautiful paper introduction. Access the robustness check that you deleted a year ago but now require to satisfy a referee. Have Git mark the lines of code that your coauthor changed last week.

Without Git, you often end up with a number of redundant files and commented out code that does not feed into the current state of the paper but which you might need later. When that later moment comes, you neither remember which of the blocks you need to uncomment nor which of the files produced your current figures and tables in the paper.

With Git, you only keep what generates the current state of the paper in the main branch. Your project looks small and concise. Git commands can recover old content if needed.

Git branches allow you to develop multiple versions in parallel. If your coauthor wants to rephrase the paper, he or she creates a new branch. In the end, you only merge the changes into the main branch, i.e. the official version, that you both agree on.

If you want to collaborate with people based on Git, you need an online platform hosting the repository. GitHub and GitLab are popular choices that give you some extra functionality beyond Git. Pull requests are a tool to verify and discuss changes before they are merged into the official version of your analyses and manuscript. Issues help you keep track of to-does. Milestones mark deadlines. And GitHub Actions facilitates automation, incl. automated tests.

## Refactoring
Git makes refactoring easier, but does not eliminate the need for it. In order to keep your repository clean, you regularly have to get together with your coauthors and figure out what content feeds into the current draft, which of the remaining code blocks and scripts should be removed, and which should be migrated to another branch.

Despite researchers' reluctance to reorganize and rewrite code, this task is essential for reproducible research.

## Clean Code
Clean code helps others and your later self to make sense of code. Use intelligible variable, function, and file names. Adhere to a consistent style. Indent based on scope. Split code into multiple not overly long files. Use comments.

There are many more clean coding recommendations. Write your code so that someone who is not part of the project can easily understand it.

## Replication Package
Once your paper has been conditionally accepted for publication by a journal, you commonly have to hand in a replication package.

As mentioned above, it tends to be inefficient to adhere to the journal replication package format from the start of your project. Instead, you can assemble the required documents in no time, if you stick to the recommendations of this SoDa Replicator template.

You have the information on input data in the documentation in the `data/raw` directory. Your virtual environment configuration file tells you which package versions you utilize. And your code documentation details how your analysis data set variables are defined.

Some journals' data editors are not overly technical. To avoid various rounds of replication package resubmission, you should stick to simple wording in your instructions.

Though requirements are not identical across journals, they tend to be similar. There are various guides on how to craft replication packages more broadly. Cynthia has written fantastic [slides](https://cynthiahqy.github.io/monash-quarto-aea/02a-template/) on replication packages in Quarto. And the [Data and Code Availability Standard](https://datacodestandard.org/) lists rules that a number of journals agree on.

## Claude Assistant GitHub Workflow Setup

This template includes a GitHub workflow for Claude Assistant, an AI-powered code review and assistance tool. Follow these steps to activate it:

### Prerequisites
- GitHub repository with appropriate permissions
- Anthropic API key (get from https://console.anthropic.com/)

### Setup Steps

#### 1. Add Anthropic API Key to Repository Secrets
1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your Anthropic API key
6. Click "Add secret"

#### 2. Verify Workflow File
The workflow file is already included at `.github/workflows/claude.yml`. It will automatically:
- Trigger on issue comments, pull request comments, and reviews
- Respond to issues being opened or assigned
- Use GitHub's built-in `GITHUB_TOKEN` for repository access

#### 3. How It Works
Claude will automatically respond to:
- New issue comments
- New pull request review comments
- Issues being opened or assigned
- Pull request reviews being submitted

#### 4. Testing
To test the workflow:
1. Create a new issue in your repository
2. Comment on the issue mentioning `@claude`
3. Claude should respond automatically within a few minutes

### Notes
- Ensure your Anthropic API key has sufficient usage limits
- Monitor GitHub Actions usage to avoid unexpected costs

## Useful Resources

Video Tutorials on the SoDa Replicator
+ [YouTube Playlist](https://youtube.com/playlist?list=PLqlvVlXl5PP0NMi-91iG-HuafsIa_qcf6&si=d1mzORY3edhCzF7N)

Coding, Data Science, and Reproducibility & Replicability Guides
+ [Grant McDermott - Data Science for Economists](https://github.com/uo-ec607/lectures)
+ [LOST - Library of Statistical Techniques](https://lost-stats.github.io/)
+ [Dan Sullivan - Best Practices When Writing Code](https://www.danielmsullivan.com/pages/tutorial_workflow_3bestpractice.html)
+ [Model to Meaning](https://marginaleffects.com/)
+ [AEA Data Editor](https://aeadataeditor.github.io/aea-de-guidance/)
+ [Koenker & Zeileis - On Reproducible Econometric Research](http://www.econ.uiuc.edu/~roger/research/repro/)

Stata
+ [Poverty Action Lab Stata Guide](https://povertyaction.github.io/guides/cleaning/readme/)
+ [Asjad Naqvi - The Stata Guide](https://medium.com/the-stata-guide)
+ [Julian Reif - Stata Coding Guide](https://julianreif.com/guide/)

R
+ [Fixest Walkthrough](https://cran.r-project.org/web/packages/fixest/vignettes/fixest_walkthrough.html)
+ [R for Data Science](https://r4ds.hadley.nz/)
+ [Introduction to data.table](https://cran.r-project.org/web/packages/data.table/vignettes/datatable-intro.html)
+ [Hans H. Sievertsen - Applied Economics with R](https://hhsievertsen.github.io/applied_econ_with_r/)

Python
+ [Monash SoDa Labs - Web Scraping with Python](https://monashdatafluency.github.io/python-web-scraping/)

LaTeX
+ [Overleaf](https://www.overleaf.com/)
+ [TeX Live](https://tug.org/texlive/)
+ [TeX Live Dev Container](https://github.com/sodalabsio/tex_live_dev_container)

---
