# Complete DCAS Compliance Checklist

Use this checklist to systematically verify compliance with each DCAS rule.

---

## Data Availability [Rules 1-6]

### Rule 1: Data Availability Statement

- [ ] README contains "Data Availability" section
- [ ] Each data source is listed
- [ ] Access procedure described for each source
- [ ] URL/location provided for each source
- [ ] Access costs documented (or noted as free)
- [ ] Expected time to obtain access documented
- [ ] Any restrictions on use noted

### Rule 2: Raw Data

- [ ] Raw data files included in package
- [ ] OR: Explanation provided for why data cannot be shared
- [ ] Each data source has its own directory
- [ ] Original filenames preserved (or documented)
- [ ] Download date/version recorded
- [ ] No personal/confidential data exposed

### Rule 3: Analysis Data

- [ ] Final analysis datasets included
- [ ] OR: Scripts generate them from raw data in < 24 hours
- [ ] Analysis data is complete (all observations used in paper)
- [ ] No intermediate files required from outside package

### Rule 4: Data Format

- [ ] All data files in standard formats
- [ ] Formats listed: ___________________
- [ ] No proprietary formats without open readers
- [ ] Character encoding documented (UTF-8 preferred)

### Rule 5: Metadata

For each dataset:

| Dataset | Codebook | Variable Labels | Value Labels | Units | Missing Codes |
|---------|----------|-----------------|--------------|-------|---------------|
| | [ ] | [ ] | [ ] | [ ] | [ ] |
| | [ ] | [ ] | [ ] | [ ] | [ ] |
| | [ ] | [ ] | [ ] | [ ] | [ ] |

### Rule 6: Data Citations

For each data source:

| Source | Cited in README | Cited in Paper | Complete Citation |
|--------|-----------------|----------------|-------------------|
| | [ ] | [ ] | [ ] |
| | [ ] | [ ] | [ ] |
| | [ ] | [ ] | [ ] |

---

## Code [Rules 7-9]

### Rule 7: Data Transformation Programs

- [ ] Scripts exist to process each raw data source
- [ ] Scripts create all interim datasets
- [ ] Scripts create final analysis datasets
- [ ] No manual steps required between scripts
- [ ] Order of execution documented

| Raw Source | Processing Script | Output |
|------------|-------------------|--------|
| | | |
| | | |

### Rule 8: Analysis Programs

- [ ] All regressions/estimations have producing scripts
- [ ] All simulations have producing scripts
- [ ] All tables have producing scripts
- [ ] All figures have producing scripts
- [ ] No manual copy-paste of results

| Output | Producing Script | Line Numbers |
|--------|------------------|--------------|
| Table 1 | | |
| Table 2 | | |
| Figure 1 | | |

### Rule 9: Code Format

- [ ] All code in plain text source format
- [ ] No compiled binaries
- [ ] No encrypted/obfuscated code
- [ ] Character encoding is UTF-8

---

## Supporting Materials [Rules 10-12]

### Rule 10: Instruments (if applicable)

- [ ] N/A - No original data collection
- [ ] Survey instrument included
- [ ] Experiment instructions included
- [ ] Subject selection criteria documented
- [ ] Randomization procedure documented

### Rule 11: Ethics (if applicable)

- [ ] N/A - No human subjects research
- [ ] IRB/Ethics board name: _________________
- [ ] Approval number: _________________
- [ ] Approval date: _________________
- [ ] Approval documentation included

### Rule 12: Pre-Registration (if applicable)

- [ ] N/A - Not pre-registered
- [ ] Registry name: _________________
- [ ] Registration number: _________________
- [ ] Registration URL: _________________
- [ ] Registration date: _________________

---

## Documentation [Rule 13]

### README Requirements

- [ ] README.md file exists
- [ ] Paper title and authors listed
- [ ] Overview of package contents

### Data Availability Statement

- [ ] Included in README
- [ ] All sources covered
- [ ] Access instructions complete

### Software Requirements

| Software | Version | Required | Documented |
|----------|---------|----------|------------|
| Stata | | [ ] | [ ] |
| R | | [ ] | [ ] |
| Python | | [ ] | [ ] |
| Other: | | [ ] | [ ] |

### Package Requirements

| Language | Lock File | Documented |
|----------|-----------|------------|
| Stata | libraries/stata/ | [ ] |
| R | renv.lock | [ ] |
| Python | requirements.txt | [ ] |

### Hardware Requirements

- [ ] Operating system(s) tested
- [ ] Memory (RAM) requirement
- [ ] Storage requirement
- [ ] CPU/cores requirement (if parallel)

### Runtime

- [ ] Expected total runtime documented
- [ ] Runtime per script documented
- [ ] Hardware for timing documented

### Instructions

- [ ] Clear step-by-step instructions
- [ ] Numbered steps
- [ ] Commands provided verbatim
- [ ] Output locations specified
- [ ] Verification steps included

---

## Sharing [Rules 14-16]

### Rule 14: Archive Location

- [ ] Package archived in repository
- [ ] Repository: _________________
- [ ] DOI: _________________
- [ ] Permanent URL: _________________

### Rule 15: License

- [ ] LICENSE file exists
- [ ] License type: _________________
- [ ] Permits replication
- [ ] Permits academic use
- [ ] Machine-readable format

### Rule 16: Omissions

- [ ] No omissions required
- [ ] Omissions clearly listed in README
- [ ] Legal/contractual reasons explained
- [ ] Alternative access paths provided

---

## Language-Specific Checks

### Stata

- [ ] `version` statement in master script
- [ ] `set varabbrev off`
- [ ] `set seed` for reproducibility
- [ ] Forward slashes in paths
- [ ] Packages bundled or documented
- [ ] No absolute paths

### R

- [ ] `renv.lock` file present
- [ ] `set.seed()` used
- [ ] Session info logged
- [ ] No absolute paths

### Python

- [ ] `requirements.txt` with versions
- [ ] Random seeds set
- [ ] Virtual environment documented
- [ ] No absolute paths

---

## Final Verification

### Pre-Submission Test

1. [ ] Make fresh copy of package
2. [ ] Delete all generated files (analysis data, results)
3. [ ] Run master script from scratch
4. [ ] Compare output to manuscript
5. [ ] All numbers match exactly

### Quality Checks

- [ ] No sensitive information (passwords, API keys)
- [ ] No personal paths in code
- [ ] No debugging code left in
- [ ] Comments are accurate
- [ ] No dead code/unused files

---

## Scoring

| Category | Possible | Achieved |
|----------|----------|----------|
| Data Availability (1-6) | 6 | |
| Code (7-9) | 3 | |
| Supporting Materials (10-12) | 3* | |
| Documentation (13) | 5 | |
| Sharing (14-16) | 3 | |
| **Total** | **20** | |

*Adjust for N/A items

**Compliance Level:**
- 20/20: Full compliance
- 16-19: Minor issues
- 12-15: Significant gaps
- <12: Major revision needed
