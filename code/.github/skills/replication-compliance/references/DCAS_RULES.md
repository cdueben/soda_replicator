# Data and Code Availability Standard (DCAS) v1.0

Source: [datacodestandard.org](https://datacodestandard.org)

---

## Data Rules

### Rule 1: Data Availability Statement

> A Data Availability Statement is provided with detailed enough information such that an independent researcher can replicate the steps needed to access the original data, including any limitations and the expected monetary and time cost of data access.

**Requirements:**
- Location of data (URL, repository, archive)
- Access procedure (direct download, application, purchase)
- Time required to obtain access
- Monetary costs (if any)
- Any restrictions on use

**Example:**
```markdown
## Data Availability

The CPS data are publicly available from the Census Bureau at
https://www.census.gov/cps. No registration required.

The proprietary firm data are available from XYZ Corporation.
Researchers must apply at https://xyz.com/research. Approval
typically takes 4-6 weeks. Access fee: $500.
```

### Rule 2: Raw Data

> Raw data used in the research (primary data collected by the author and secondary data not otherwise available) is made publicly accessible. Exceptions are explained under Rule 1.

**Requirements:**
- Include raw data files in package
- If restricted, explain in Data Availability Statement
- Primary data (surveys, experiments) must be shared unless legally prohibited

### Rule 3: Analysis Data

> Analysis data is provided as part of the replication package unless they can be fully reproduced from accessible data within a reasonable time frame. Exceptions are explained under Rule 1.

**Requirements:**
- Include final analysis datasets
- OR provide scripts to generate them from raw data
- "Reasonable time" = typically under 24 hours

### Rule 4: Data Format

> The data files are provided in any format compatible with commonly used statistical package or software. Some journals require data files in open, non-proprietary formats.

**Acceptable Formats:**
- Open: CSV, Parquet, JSON, SQLite
- Statistical: DTA (Stata), RDS (R), SAS7BDAT (SAS)
- Spreadsheet: XLSX (prefer CSV for reproducibility)

**Avoid:**
- Proprietary formats without open readers
- Binary formats without documentation

### Rule 5: Metadata

> Description of variables and their allowed values are publicly accessible.

**Requirements:**
- Variable names and descriptions
- Value labels and coding schemes
- Units of measurement
- Missing value codes
- Data type (string, numeric, date)

**Formats:**
- Codebook (PDF, MD, XLSX)
- Variable labels in data files
- Separate data dictionary

### Rule 6: Data Citation

> All data used in the paper are cited.

**Requirements:**
- Full bibliographic citation for each data source
- Include: Author/Organization, Title, Year, Publisher, URL, Access Date
- Follow journal citation style

**Example:**
```
Bureau of Labor Statistics. 2023. "Current Population Survey,
Annual Social and Economic Supplement." U.S. Census Bureau.
https://www.census.gov/programs-surveys/cps.html.
Accessed: January 15, 2024.
```

---

## Code Rules

### Rule 7: Data Transformation

> Programs used to create any final and analysis data sets from raw data are included.

**Requirements:**
- Scripts that clean raw data
- Scripts that merge/combine data sources
- Scripts that construct analysis variables
- Complete pipeline from raw → analysis

### Rule 8: Analysis Programs

> Programs producing the computational results (estimation, simulation, model solution, visualization) are included.

**Requirements:**
- All estimation/regression scripts
- Simulation code
- Scripts generating tables
- Scripts generating figures
- Any post-estimation analysis

### Rule 9: Code Format

> Code is provided in source format that can be directly interpreted or compiled by appropriate software.

**Requirements:**
- Plain text source files (.do, .R, .py, .jl)
- NOT compiled binaries
- NOT encrypted or obfuscated code
- Human-readable

---

## Supporting Materials Rules

### Rule 10: Instruments

> If collecting original data through surveys or experiments, survey instruments or experiment instructions as well as details on subject selection are included.

**Requirements (if applicable):**
- Survey questionnaires
- Experiment protocols and instructions
- Subject recruitment criteria
- Randomization procedures

### Rule 11: Ethics

> If applicable, details are shared about ethics approval.

**Requirements (if applicable):**
- IRB/Ethics committee name
- Approval number
- Date of approval
- Any conditions of approval

### Rule 12: Pre-Registration

> If applicable, pre-registration of the research is identified and cited.

**Requirements (if applicable):**
- Registry name (AEA RCT Registry, OSF, EGAP)
- Registration number
- URL to registration
- Registration date

---

## Documentation Rule

### Rule 13: README Documentation

> A README document is included, containing a Data Availability Statement, listing all software and hardware dependencies and requirements (including the expected run time), and explaining how to reproduce the research results. The README follows the schema provided by the Social Science Data Editors' template README.

**Required README Sections:**
1. Title and authors
2. Data Availability Statement
3. Software requirements (with versions)
4. Hardware requirements
5. Expected runtime
6. Instructions for replication
7. List of tables/figures and producing scripts

**Template:** [Social Science Data Editors README](https://social-science-data-editors.github.io/template_README/)

---

## Sharing Rules

### Rule 14: Archive Location

> Data and programs are archived by the authors in the repositories deemed acceptable by the journal.

**Common Repositories:**
- ICPSR (https://www.icpsr.umich.edu/)
- Zenodo (https://zenodo.org/)
- Harvard Dataverse (https://dataverse.harvard.edu/)
- OSF (https://osf.io/)
- Journal-specific repositories

**Requirements:**
- Persistent identifier (DOI)
- Long-term preservation
- Public accessibility

### Rule 15: License

> A license specifies the terms of use of code and data in the replication package. The license allows for replication by researchers unconnected to the original parties.

**Recommended Licenses:**
- Code: MIT, BSD-3, Apache 2.0
- Data: CC-BY 4.0, CC0
- Mixed: [AEA template](https://github.com/AEADataEditor/aea-de-guidance/blob/master/template-LICENSE.md)

**Requirements:**
- Must permit replication
- Must permit academic use
- Should be machine-readable

### Rule 16: Omissions

> The README clearly indicates any omission of the required parts of the package due to legal requirements or limitations or other approved agreements.

**Requirements:**
- Explicitly state what is missing
- Explain why (legal, proprietary, ethical)
- Provide alternative access paths if possible
- Document any agreements with data providers
