# Monash SoDa Replication Template

**Update: The template has moved into the SoDa account: https://github.com/sodalabsio/soda_replicator.**

This repository provides a **template for reproducible, collaborative applied-economics projects**. It contains a basic directory structure(`code/`, `paper/`, `data/`), starter scripts, virtual-environment stubs, and a replication checklist that feeds an automated AI code-review workflow. The [main](https://github.com/cdueben/soda_replicator/tree/main) branch contains example files to illustrate template use. Download the example-free [clean](https://github.com/cdueben/soda_replicator/tree/clean) branch at the outset of every study to lock in best-practice version control, hand-offs between co-authors and supervisors, and generation of replication packages.

---

## How to Use This Repo

Video tutorial for those who do not want to read the documentation or who need more extensive explanations: https://youtube.com/playlist?list=PLqlvVlXl5PP0NMi-91iG-HuafsIa_qcf6&si=d1mzORY3edhCzF7N.

### 1. Installation 🚀

1.1  Download the [clean](https://github.com/cdueben/soda_replicator/tree/clean) template: **[Code › Download ZIP](https://github.com/cdueben/soda_replicator/archive/refs/heads/clean.zip)**.

1.2  Unpack & rename the folder to your *project name*.

1.3 Make sure you have Git installed and GitHub [configured](https://docs.github.com/en/get-started/git-basics/set-up-git).
+ **Tip:** New to Git? Follow the *Hello World* [tutorial](https://guides.github.com/activities/hello-world).

1.4 Open the GitHub website and create two empty private repositories with the named `name-of-your-project_code` and `name-of-your-project_paper`, with `name-of-your-project` being a short name (probably one or two words) for your research project.

1.5 Open the terminal (Git Bash on Windows) locally in the `code` folder and enter the following commands:

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/your-github-name/name-of-your-project_code.git
git push -u origin main
```

1.7 Repeat step 1.6 for the `paper` directory.

1.8 Configure the two GitHub repositories on the website:
   + **Settings › Collaborators** → add co-authors & supervisors
   + (Optional) Protect `main` branch (enforce code review) & enable GitHub Actions

1.9 Share the `data` folder with your collaborators through a cloud storage provider, like Dropbox or Google Drive.

### 2. Create the Project Checklist 📝

2.1 Open `code/checklist.md` and `paper/checklist.md`.  

2.2 With your co-authors/ supervisor, **outline steps** to fit *this* project's data sources, methods, and outputs.  

2.3 Commit changes:  

```bash
   git add checklist.md
   git commit -m "customize replication checklist"
   git push origin main
```

### 3. Understand the Folder Structure 🏗️

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

**Use relative paths when scripts reference data!** I.e. `../data/analysis/baseline.csv` instead of `/home/your_username/cloud_folder/your_project/data/analysis/baseline.csv`.

### 4. Start Coding 👩‍💻👨‍💻

4.1 Activate the virtual environment in `code` ([`renv`](https://rstudio.github.io/renv/)/ [`venv`](https://docs.python.org/3/library/venv.html)/ [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)).

4.2 Write scripts in `code/dataprep` and `code/analysis`.

4.3 Test the pipeline, then push:

```bash
git add .
git commit -m "add first data-prep script"
git push origin main
```
4.4 Verify commits and CI status on GitHub ([GitHub guide](https://docs.github.com/en/get-started/quickstart)).

### 5. Tick Off the Checklist ✔️

After each milestone:

+ Edit `checklist.md`.
+ Select elements with `[x]`.
+ Request review via an issue or a pull request.

### 6. Run the AI Code Checker 🤖

Invoke the AI checker with `@claude` in an issue or a pull request to:
  + Read checklist.md.
  + Evaluate to what extent the contents of the repository align with the checklist.

### 7. Create Final Replication Package for Submission

7.1 Follow [guidelines](https://github.com/AEADataEditor/replication-template) from AEA Data editor.

7.2 Have a look at Cynthia Huang's quarto replication [slides](https://cynthiahqy.github.io/monash-quarto-aea/02a-template/) and [template](https://github.com/cynthiahqy/quarto-replication-template).

### 8. Useful Resources

8.1 Video Tutorials on the SoDa Replicator
+ [Youtube Playlist](https://youtube.com/playlist?list=PLqlvVlXl5PP0NMi-91iG-HuafsIa_qcf6&si=d1mzORY3edhCzF7N)

8.2 Coding, Data Science, and Reproducibility & Replicability Guides
+ [Grant McDermott - Data Science for Economists](https://github.com/uo-ec607/lectures)
+ [LOST - Library of Statistical Techniques](https://lost-stats.github.io/)
+ [Dan Sullivan - Best Practices When Writing Code](https://www.danielmsullivan.com/pages/tutorial_workflow_3bestpractice.html)
+ [Model to Meaning](https://marginaleffects.com/)
+ [AEA Data Editor](https://aeadataeditor.github.io/aea-de-guidance/)
+ [Koenker & Zeileis - On Reproducible Econometric Research](http://www.econ.uiuc.edu/~roger/research/repro/)

8.3 Stata
+ [Poverty Action Lab Stata Guide](https://povertyaction.github.io/guides/cleaning/readme/)
+ [Asjad Naqvi - The Stata Guide](https://medium.com/the-stata-guide)
+ [Julian Reif - Stata Coding Guide](https://julianreif.com/guide/)

8.4 R
+ [Fixest Walkthrough](https://cran.r-project.org/web/packages/fixest/vignettes/fixest_walkthrough.html)
+ [R for Data Science](https://r4ds.hadley.nz/)
+ [Introduction to data.table](https://cran.r-project.org/web/packages/data.table/vignettes/datatable-intro.html)
+ [Hans H. Sievertsen - Applied Economics with R](https://hhsievertsen.github.io/applied_econ_with_r/)

8.5 Python
+ [Monash SoDa Labs - Web Scraping with Python](https://monashdatafluency.github.io/python-web-scraping/)

8.6 LaTeX
+ [Overleaf](https://www.overleaf.com/)
+ [TeX Live](https://tug.org/texlive/)
+ [TeX Live Dev Container](https://github.com/sodalabsio/tex_live_dev_container)

---

# Documentation
While the above section is a quick manual on how to get started with the template, the following documentation goes more into detail. It explains how to manage the project, which information to store where, etc.

## Introduction
This repository contains a template for a reproducible research project. The focus lies on quantitative social science. Recommendations might not fully apply to other fields.

Download the template at the start of each new research project. The purpose is to ensure the reproducibility of your analyses from day one with little effort. That does not mean following journals' replication package structure throughout the project, but to have a system in place from which you can produce a replication package with little effort.

Whereas a journal replication package is the final project state bundled into a single unit and extensively documented, earlier stages often benefit from a more modular structure. You probably want to manage your code with Git, but you obviously do not upload terabytes of data to GitHub. Furthermore, it is usually inefficient to maintain the extensive, clunky journal replication package documentation from the start of the project. Rather have a setup which allows you to quickly generate that documentation when needed.

While most recommendations here are agnostic of your choice of data science and typesetting language, this readme adds some language-specific comments in a section below.

## Directory Structure
Before we discuss the directory structure, it is important to stress that you are not meant to use the template as a single Git repository. We host the three separate folders (`data`, `code`, and `paper`) jointly in one place so that you can download them in one go and have a good overview of the entire structure. In your project, you administer them as distinct repositories (`code` and `paper`) and one non-Git folder (`data`) located in one parent directory.

To summarize the contents: `data` holds the data, `code` holds the quantitative analysis code, and `paper` holds the markup code.

### Data
The `data` directory holds the project's data sets. Raw input data, as downloaded from the source or as collected in an experiment, goes into `data/raw`. Processed, evaluation-ready data belongs into `data/analysis`. In projects with long data cleaning pipelines, it might make sense to add a `data/interim` folder.

As already mentioned, Git is designed for code, not for large data sets. It is a good idea to store the data in a folder synced to the cloud, but not to manage it with Git.

If there are multiple input data sets, each of them should have its separate directory in `data/raw`. The template contains two fictional examples: population data downloaded from `example.com` and weather data downloaded from `example.org`. The data set publisher's documentation, sometimes referred to as code book, and a text file documenting the download URL and the download date should accompany the data files. Online resources can change over time. Hence, store all of this information together in one location from the start.

Similarly, different sets of analysis data can be organized into multiple folders in `data/analysis`. They do, of course, not require extra documentation on where they came from or on which day they were created. The information on how to create the files from the raw data belongs into the `code` directory. And that code should produce the analysis data irrespective of the execution date. It is a good habit to document the analysis data files in that code because (i) this checks the documentation into version control and (ii) it keeps the explanations close to the logic creating the data.

Because many researchers share downloaded papers that are relevant to the project with their coauthors in cloud folders, `data` also has a `literature` subdirectory. This is simply for convenience. Downloaded article PDFs are not part of the final replication package submitted to journals. `data\literature` only exists for paper sharing among coauthors while the project is evolving. It is optional and can be omitted.

The reason to place `literature` in `data`, and not in `paper`, is to exclude it from version control. PDFs in the hundreds of pages would simply clutter the git history meant to track files that you are editing yourself and that feed into a subsequent replication package.

### Code
The quantitative analysis code, covering all steps from the raw data to the results shown in the paper, belong into the `code` directory. This is your R, Python, Stata, Julia, C++ code. It should be managed with Git.

The preprocessing steps turning the `data/raw` into the `data/analysis` files are in `code/dataprep` and the steps deriving insights from the `data/analysis` data are in `code/analysis`. You should, especially in larger projects, further divide the `code/dataprep` and `code/analysis` into sub-folders. You could have one folder per input data set in `code/dataprep`, in which you do all the preprocessing of the respective data set. In a file at the `code/dataprep` level (not in a sub-directory), you then only merge the data. This template illustrates this with example files.

The advantage of placing `code` in the same parent directory as `data` is that you can easily reference data sets using relative paths. No paths have to be adjusted when running the code from another computer. `../data/raw/population/population.csv` remains valid (`..` moves up one level from the current directory).

### Paper
The template's `paper` folder organization assumes users to either write their manuscripts locally or to connect their Overleaf project to Dropbox folder or GitHub. Overleaf users who host their projects entirely on that platform (without external connections) only store tables and figures in `paper`.

As in the case of `code`, you should control the contents of the `paper` directory with Git - as long as you use a markup language. Students who are not yet familiar with LaTeX or Markdown and still use a word processor like Microsoft Word or Libre Office Writer may not experience large benefits from using Git.

`paper` entails three sub-folders: `draft`, `results`, and `presentation`. Throughout the life cycle of a project, there are exploratory phases. You want to try out different empirical models to identify the underlying pattern in the data, and you experiment with theory to craft a framework that your estimations fit into. The `results` folder is the location to collect and discuss ideas. It is the foundation for the official manuscript in `draft`. `presentation` holds the markup code for seminar and conference presentations. As a PhD student also presenting posters, you might have an additional `poster` folder.

`code` and `paper` are separate repositories because your quantitative analysis code and the work on your manuscript are often not in sync. Joining these two streams of work can lead to messy commit histories and chaotic branches.

## Virtual Environments
Data science software receives updates over time. R packages are not static. Developers fix bugs and change function behavior across releases. It, therefore, happens that you re-execute your code a few years after you wrote it and obtain different results. Because your replication package needs to reproduce the results shown in the paper, you then start digging through previous versions of the programming language and of the packages that you used. Unfortunately, many packages are not isolated pieces of software. Packages have dependencies. Hence, you puzzle together different package version combinations. In the end, you browse tens of thousands of lines of code and spend days and figuring out the source of a discrepancy.

Virtual environments prevent such drama. The `renv` package in R and the `venv` module in Python track package versions at the project level and allow you to use different versions across projects. You can use version 1.0 in one project and version 1.2 in another project. When you come back to a study at a later point or when someone else wants to execute your code, the software automatically obtains the correct package version from the automatically created configuration file and computes the same results as you did initially.

So, before you write any code, open the `code` directory and follow the installation instructions and introductions for [`renv`](https://rstudio.github.io/renv/), [`venv`](https://docs.python.org/3/library/venv.html), or alternatively [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

This template contains automatically created example configuration files.

With C++, you do not need a virtual environment. Just use CMake with detailed flags and track that file with version control.

## Version Control
There are different version control tools out there. Git is the standard nowadays in both academia and industry. A Git tutorial is beyond the scope of this document. If you are not yet familiar with it, check out Monash's courses or one of the many other online resources on the topic. You are good to go with a few basic Git commands, which you can learn in a matter of minutes. If you want to leverage more advanced features, you should watch a few hours of instructional content.

Overall, Git tracks versions of your files. It circumvents messy organization where you end up with project directories containing `paper.tex`, `paper_new.tex`, `paper_new_new.tex`, `paper_final.tex`, `paper_final_new.tex`. It allows you to jump between commits, which are version checkpoints set by you, without throwing extra tex files into your folder.

Git comes with various labeling options for commits to easily identify versions. Recover the version of your poster that you presented at the conference last year. Roll back the changes which your coauthor made to your beautiful paper introduction. Access the robustness check that you deleted a year ago but now require to satisfy a referee. Have Git mark the lines of code that your coauthor changed last week.

Without Git, you often end up with a number of redundant files and commented out code that does not feed into the current state of the paper but which you might need later. When that later moment comes, you neither remember which of the blocks you need to uncomment nor which of the files produced your current figures and tables in the paper.

With Git, you only keep what generates the current state of the paper in the main branch. Your project looks small and concise. Git commands can recover old content if needed.

Git branches allow you to develop multiple versions in parallel. If your coauthor wants to rephrase the paper, he or she can created a new branch and in the end you only merge the changes into the main branch, i.e. the official version, that you both agree on.

If you want to collaborate with people based on Git, you need an online platform hosting the repository. GitHub and GitLab are popular choices that give you some extra functionality beyond Git. Pull requests are a tool to verify and discuss changes before they are merged into the official version of your analyses and manuscript. Issues help you keep track of to-does. And GitHub Actions facilitates automation, incl. automated tests.

## Refactoring
Git makes refactoring easier, but does not eliminate the need for it. In order to keep your repository clean, you regularly have to get together with your coauthors and figure out what content feeds into the current draft, which of the remaining code blocks and scripts should be removed, and which should be migrated to another branch.

Despite researchers' reluctance to reorganize and rewrite code, this task is essential for reproducible research.

## Clean Code
Clean code helps others and your later self to make sense of code. Use intelligible variable, function, and file names. Adhere to a consistent style. Indent based on scope. Split code into multiple not overly long files. Use comments.

There are many more clean coding recommendations. Write your code so that someone who is not part of the project can easily understand it.

## Replication Package
Once your paper has been conditionally accepted for publication, you commonly have to hand in a replication package.

As mentioned above, it tends to be inefficient to adhere to the journal replication package format from the start of your project. Instead, you can assemble the required documents in no time, if you stick to the recommendations of this SoDa Replicator template.

You have the information on input data in the documentation in the `data/raw` directory. Your virtual environment configuration file tells you which package versions you utilize. And your code documentation details how your analysis data set variables are defined.

Some journals' data editors are not overly technical. To avoid various rounds of replication package resubmission, you should stick to simple wording in your instructions.

Though requirements are not identical across journals, they tend to be similar. There are various guides on how to craft replication packages more broadly. Cynthia has written fantastic [slides](https://cynthiahqy.github.io/monash-quarto-aea/02a-template/) on replication packages in Quarto. And the [Data and Code Availability Standard](https://datacodestandard.org/) lists rules that a number of journals agree on.

## AI Code Review Setup

This template includes GitHub workflows for AI-powered code review. The workflows live at `.github/workflows/` inside your `code/` and `paper/` repositories. Two tools are supported: **Claude** (Anthropic) and **Codex** (OpenAI). Activate whichever you have access to — or both.

---

### Claude Assistant

The workflow file is already included at `.github/workflows/claude.yml`. Claude reviews code and paper drafts against your `checklist.md` when you tag `@claude` in an issue or pull request.

Choose one option — you do not need both.

#### Option A — Claude subscription (no API key needed)

Requires a Claude **Pro, Max, Team, or Enterprise** subscription. Free accounts are not supported.

**Via Claude Code (if you have it installed):**
1. Open a terminal inside your `code/` or `paper/` directory
2. Run `claude` to open Claude Code
3. Run `/install-github-app` and follow the prompts
4. Close any pull request it opens — the workflow file is already included in this template

**Via browser:**
1. Go to [github.com/apps/claude](https://github.com/apps/claude)
2. Click **Install** (or **Configure** if you have previously installed it)
3. GitHub will show the permissions Claude requests:
   - Read access to actions, checks, and metadata
   - Read and write access to code, discussions, issues, pull requests, and workflows
4. Under **Repository access**, select **Only select repositories** (recommended — avoid granting access to all repos)
5. Use the dropdown to find and select your `code` repository (e.g. `your-project_code`). If you also want Claude to review the paper repo, add that too
6. Click **Install** (or **Save** if reconfiguring)
7. You will be redirected to a confirmation page — no further action needed there. The app automatically sets the `CLAUDE_CODE_OAUTH_TOKEN` secret in your repository

#### Option B — Anthropic API key

1. Get an API key from [console.anthropic.com](https://console.anthropic.com/) → **API Keys** → **Create Key**
2. Add it to your repository secrets:

   **Via terminal (recommended):**
   ```bash
   gh secret set ANTHROPIC_API_KEY --repo your-github-name/your-project_code
   ```
   Paste your key when prompted.

   **Via browser:** In your repository go to **Settings → Secrets and variables → Actions → New repository secret**, set name to `ANTHROPIC_API_KEY`, paste your key, click **Add secret**

The workflow file is already at `.github/workflows/claude.yml` — no further changes needed.

#### Using Claude

- Open an issue or pull request in your repository
- Add a comment mentioning `@claude` (e.g., `@claude please review against the checklist`)
- Claude responds within a few minutes, checking only the `[x]` items in `checklist.md`

#### Notes
- Ensure your API key has sufficient usage limits (Option B only)
- Monitor the **Actions** tab in your repository to track usage and spot any errors

---

### Codex Assistant

The workflow file is already included at `.github/workflows/codex.yml`. Codex works similarly to Claude — tag `@codex` in pull request comments.

#### Option A — ChatGPT subscription (no API key needed)

Requires a ChatGPT **Plus, Pro, Team, Edu, or Enterprise** subscription. Free accounts have limited-time access only.

1. Go to [chatgpt.com/codex](https://chatgpt.com/codex)
2. Click **Connect GitHub** and authorise access to your repository
3. Go to [chatgpt.com/codex/settings/environments](https://chatgpt.com/codex/settings/environments) — use the two dropdowns to select your **organisation** and then your **repository**, then click **Create environment**. If your repository does not appear in the dropdown, wait 5 minutes and refresh — newly connected repos can take a moment to appear. Wait for the environment to finish building before continuing
4. Click **Settings** in the top-right corner of the Codex interface
5. Under **Code Review**, toggle on **Enable code review**
6. Optionally toggle on **Automatic reviews** to have Codex review every new pull request without tagging

> **Troubleshooting:** If you see a comment from the `chatgpt-codex-connector` bot on a pull request saying *"To use Codex here, create an environment for this repo"*, the environment in step 3 has not been created. Return to [chatgpt.com/codex](https://chatgpt.com/codex), select your repository, and click **Create environment**.

#### Option B — OpenAI API key

1. Get an API key from [platform.openai.com](https://platform.openai.com/) → **API Keys** → **Create new secret key**
2. Add it to your repository secrets:

   **Via terminal (recommended):**
   ```bash
   gh secret set OPENAI_API_KEY --repo your-github-name/your-project_code
   ```
   Paste your key when prompted.

   **Via browser:** In your repository go to **Settings → Secrets and variables → Actions → New repository secret**, set name to `OPENAI_API_KEY`, paste your key, click **Add secret**

The workflow file is already at `.github/workflows/codex.yml` — no further changes needed.

#### Using Codex

- Add a comment `@codex review` in any pull request
- Codex reads `AGENTS.md` automatically for project conventions — no extra instructions needed
- Or ask in plain language: *"check this against our replication standards"*

Codex will react to your comment with a 👀 emoji to confirm it has seen the request — this is normal. The full review will appear as a follow-up comment once it finishes, which can take a few minutes. If you want to check progress or see if there was an error, go to [chatgpt.com/codex](https://chatgpt.com/codex) and look for the task in the left sidebar under your repository.

---

### Replication Compliance Skill

A DCAS compliance audit skill is bundled at `code/.github/skills/replication-compliance/` and works with Claude Code, Codex, Cursor, and Gemini. To install it globally across all your projects:

```bash
curl -fsSL https://raw.githubusercontent.com/cdueben/soda_replicator/main/code/.github/skills/replication-compliance/install.sh | bash
```

> **Note:** This installs files into your AI tool's global configuration directory. Read [`code/.github/skills/replication-compliance/README.md`](code/.github/skills/replication-compliance/README.md) before running.
