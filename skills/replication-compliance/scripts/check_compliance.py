#!/usr/bin/env python3
"""
DCAS Compliance Checker

Scans a research repository and evaluates compliance with the
Data and Code Availability Standard (DCAS) v1.0.

Usage:
    python check_compliance.py /path/to/repo
    python check_compliance.py /path/to/repo --json     # JSON output
    python check_compliance.py /path/to/repo --save     # Save report
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

# Severity levels
ERROR = "ERROR"      # Will almost certainly cause replication failure
WARNING = "WARNING"  # Risk to reproducibility or violates best practices
INFO = "INFO"        # Informational note

# Display indicators
PASS = "✅"
WARN = "⚠️"
FAIL = "❌"
NA = "N/A"


@dataclass
class CodeIssue:
    """Represents a code-level issue found in a file."""
    file: str
    line: int
    severity: str
    check_id: str
    message: str
    code: str = ""
    suggestion: str = ""


def find_files(root: Path, patterns: List[str]) -> List[Path]:
    """Find files matching any of the given patterns."""
    matches = []
    for pattern in patterns:
        matches.extend(root.rglob(pattern))
    return matches


def check_file_exists(root: Path, patterns: List[str]) -> Tuple[str, str]:
    """Check if any file matching patterns exists."""
    files = find_files(root, patterns)
    if files:
        return PASS, f"Found: {files[0].name}"
    return FAIL, "Not found"


def check_readme_section(readme_path: Path, keywords: List[str]) -> Tuple[str, str]:
    """Check if README contains a section with given keywords."""
    if not readme_path.exists():
        return FAIL, "README not found"

    content = readme_path.read_text(errors='ignore').lower()
    for keyword in keywords:
        if keyword.lower() in content:
            return PASS, f"Found '{keyword}' section"
    return FAIL, f"Missing section with keywords: {keywords}"


def detect_language(root: Path) -> str:
    """Detect primary programming language."""
    counts = {
        'stata': len(find_files(root, ['*.do'])),
        'r': len(find_files(root, ['*.R', '*.r', '*.Rmd', '*.qmd'])),
        'python': len(find_files(root, ['*.py'])),
        'matlab': len(find_files(root, ['*.m'])),
        'julia': len(find_files(root, ['*.jl'])),
    }
    if max(counts.values()) == 0:
        return 'unknown'
    return max(counts, key=counts.get)


def detect_all_languages(root: Path) -> List[str]:
    """Detect all programming languages used."""
    languages = []
    if find_files(root, ['*.do']):
        languages.append('stata')
    if find_files(root, ['*.R', '*.r', '*.Rmd', '*.qmd']):
        languages.append('r')
    if find_files(root, ['*.py']):
        languages.append('python')
    if find_files(root, ['*.m']):
        languages.append('matlab')
    if find_files(root, ['*.jl']):
        languages.append('julia')
    return languages if languages else ['unknown']


# =============================================================================
# CODE-LEVEL CHECKS (Based on AEA/Social Science Data Editors research)
# These detect issues that cause 75% of replication failures
# =============================================================================

# Regex patterns for detecting issues
ABSOLUTE_PATH_PATTERNS = [
    (r'["\'][A-Za-z]:\\[^"\']+["\']', 'Windows absolute path'),  # C:\Users\...
    (r'["\']\/Users\/[^"\']+["\']', 'macOS absolute path'),       # /Users/...
    (r'["\']\/home\/[^"\']+["\']', 'Linux absolute path'),        # /home/...
    (r'["\']~\/[^"\']+["\']', 'Home directory path'),              # ~/...
]

SEED_PATTERNS = {
    'stata': [
        (r'^\s*set\s+seed\s+\d+', 'set seed'),
    ],
    'r': [
        (r'set\.seed\s*\(', 'set.seed()'),
    ],
    'python': [
        (r'random\.seed\s*\(', 'random.seed()'),
        (r'np\.random\.seed\s*\(', 'np.random.seed()'),
        (r'numpy\.random\.seed\s*\(', 'numpy.random.seed()'),
        (r'torch\.manual_seed\s*\(', 'torch.manual_seed()'),
        (r'tf\.random\.set_seed\s*\(', 'tf.random.set_seed()'),
    ],
    'matlab': [
        (r'rng\s*\(', 'rng()'),
    ],
    'julia': [
        (r'Random\.seed!\s*\(', 'Random.seed!()'),
    ],
}

RANDOMIZATION_INDICATORS = {
    'stata': ['sample', 'bootstrap', 'permute', 'simulate', 'shuffle', 'random'],
    'r': ['sample', 'rnorm', 'runif', 'rbinom', 'boot', 'shuffle', 'random'],
    'python': ['random', 'shuffle', 'sample', 'choice', 'randint', 'randn', 'normal'],
    'matlab': ['rand', 'randn', 'randi', 'randperm', 'datasample'],
    'julia': ['rand', 'randn', 'shuffle', 'sample'],
}


def check_absolute_paths(root: Path) -> List[CodeIssue]:
    """Check for hardcoded absolute paths (ERROR: causes replication failure)."""
    issues = []
    code_extensions = ['*.do', '*.R', '*.r', '*.Rmd', '*.py', '*.m', '*.jl']

    for ext in code_extensions:
        for file_path in root.rglob(ext):
            if '.git' in str(file_path):
                continue
            try:
                content = file_path.read_text(errors='ignore')
                lines = content.split('\n')
                for line_num, line in enumerate(lines, 1):
                    # Skip comments
                    stripped = line.strip()
                    if stripped.startswith(('#', '*', '//', '%', '--')):
                        continue

                    for pattern, desc in ABSOLUTE_PATH_PATTERNS:
                        matches = re.findall(pattern, line, re.IGNORECASE)
                        for match in matches:
                            issues.append(CodeIssue(
                                file=str(file_path.relative_to(root)),
                                line=line_num,
                                severity=ERROR,
                                check_id='absolute-path',
                                message=f'{desc} detected',
                                code=line.strip()[:100],
                                suggestion='Use relative paths or global/environment variables for portability'
                            ))
            except (OSError, UnicodeDecodeError):
                pass

    return issues


def check_random_seeds(root: Path, language: str) -> List[CodeIssue]:
    """Check for missing random seeds (WARNING: 70% of instability)."""
    issues = []

    ext_map = {
        'stata': ['*.do'],
        'r': ['*.R', '*.r', '*.Rmd'],
        'python': ['*.py'],
        'matlab': ['*.m'],
        'julia': ['*.jl'],
    }

    if language not in ext_map:
        return issues

    seed_patterns = SEED_PATTERNS.get(language, [])
    random_indicators = RANDOMIZATION_INDICATORS.get(language, [])

    for ext in ext_map[language]:
        for file_path in root.rglob(ext):
            if '.git' in str(file_path):
                continue
            try:
                content = file_path.read_text(errors='ignore')
                content_lower = content.lower()

                # Check if file uses randomization
                uses_random = any(ind in content_lower for ind in random_indicators)
                if not uses_random:
                    continue

                # Check if seed is set
                has_seed = any(re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
                              for pattern, _ in seed_patterns)

                if not has_seed:
                    issues.append(CodeIssue(
                        file=str(file_path.relative_to(root)),
                        line=0,
                        severity=WARNING,
                        check_id='missing-seed',
                        message='File uses randomization but no seed is set',
                        suggestion=f'Add seed setting at top of file for reproducibility'
                    ))
            except (OSError, UnicodeDecodeError):
                pass

    return issues


def check_stata_specific(root: Path) -> List[CodeIssue]:
    """Stata-specific checks for reproducibility."""
    issues = []

    for file_path in root.rglob('*.do'):
        if '.git' in str(file_path):
            continue
        try:
            content = file_path.read_text(errors='ignore')
            lines = content.split('\n')
            rel_path = str(file_path.relative_to(root))

            # Check for version statement (should be near top)
            has_version = bool(re.search(r'^\s*version\s+\d+', content, re.MULTILINE | re.IGNORECASE))
            if not has_version and len(content) > 100:  # Skip tiny files
                issues.append(CodeIssue(
                    file=rel_path,
                    line=1,
                    severity=WARNING,
                    check_id='stata-no-version',
                    message="'version' statement not found",
                    suggestion="Add 'version 17' (or appropriate version) at top for compatibility"
                ))

            # Check for set varabbrev off
            has_varabbrev = bool(re.search(r'^\s*set\s+varabbrev\s+off', content, re.MULTILINE | re.IGNORECASE))
            if not has_varabbrev and len(content) > 500:  # Only check substantial files
                issues.append(CodeIssue(
                    file=rel_path,
                    line=1,
                    severity=WARNING,
                    check_id='stata-no-varabbrev',
                    message="'set varabbrev off' not found",
                    suggestion="Add 'set varabbrev off' to prevent variable abbreviation errors"
                ))

            # Check for sort without isid
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip().lower()
                if stripped.startswith('*') or stripped.startswith('//'):
                    continue

                # Look for sort commands
                if re.match(r'^\s*sort\s+\w', line, re.IGNORECASE):
                    # Check previous 10 lines for isid
                    start = max(0, line_num - 11)
                    prev_lines = '\n'.join(lines[start:line_num-1])
                    if not re.search(r'\bisid\b', prev_lines, re.IGNORECASE):
                        issues.append(CodeIssue(
                            file=rel_path,
                            line=line_num,
                            severity=WARNING,
                            check_id='stata-sort-no-isid',
                            message="'sort' without prior 'isid' check",
                            code=line.strip()[:80],
                            suggestion="Run 'isid varlist' before sorting to ensure unique identifiers"
                        ))

        except (OSError, UnicodeDecodeError):
            pass

    return issues


def check_python_requirements(root: Path) -> List[CodeIssue]:
    """Check Python requirements.txt for unpinned versions."""
    issues = []

    req_files = find_files(root, ['requirements.txt'])
    for req_path in req_files:
        try:
            content = req_path.read_text(errors='ignore')
            lines = content.split('\n')
            rel_path = str(req_path.relative_to(root))

            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith('#') or stripped.startswith('-'):
                    continue

                # Check for unpinned versions (no ==)
                if '==' not in stripped and re.match(r'^[a-zA-Z0-9\-_]+', stripped):
                    # Ignore lines with >= or other specifiers (they're partially pinned)
                    if not any(op in stripped for op in ['>=', '<=', '~=', '!=']):
                        issues.append(CodeIssue(
                            file=rel_path,
                            line=line_num,
                            severity=WARNING,
                            check_id='unpinned-dependency',
                            message='Unpinned dependency',
                            code=stripped,
                            suggestion='Pin version with == (e.g., pandas==2.1.4) for reproducibility'
                        ))
        except (OSError, UnicodeDecodeError):
            pass

    return issues


def run_code_level_checks(root: Path) -> List[CodeIssue]:
    """Run all code-level checks and return issues."""
    all_issues = []
    languages = detect_all_languages(root)

    # Absolute paths (highest priority - ERROR)
    all_issues.extend(check_absolute_paths(root))

    # Random seeds (WARNING)
    for lang in languages:
        all_issues.extend(check_random_seeds(root, lang))

    # Stata-specific
    if 'stata' in languages:
        all_issues.extend(check_stata_specific(root))

    # Python requirements
    if 'python' in languages:
        all_issues.extend(check_python_requirements(root))

    return all_issues


def check_data_availability(root: Path) -> Dict:
    """Check DCAS Rules 1-6: Data Availability."""
    results = {}
    readme = root / 'README.md'
    if not readme.exists():
        readme = root / 'code' / 'README.md'

    # Rule 1: Data Availability Statement
    status, note = check_readme_section(readme, ['data availability', 'data access'])
    results['rule_1'] = {'name': 'Data Availability Statement', 'status': status, 'note': note}

    # Rule 2: Raw data
    data_dirs = ['data/raw', 'data', 'raw_data', '_data', 'Data', 'DATA']
    found = any((root / d).exists() for d in data_dirs)
    results['rule_2'] = {
        'name': 'Raw data',
        'status': PASS if found else WARN,
        'note': 'Data directory found' if found else 'No data directory found'
    }

    # Rule 3: Analysis data
    analysis_dirs = ['data/analysis', 'data/processed', 'analysis_data']
    found = any((root / d).exists() for d in analysis_dirs)
    results['rule_3'] = {
        'name': 'Analysis data',
        'status': PASS if found else WARN,
        'note': 'Analysis data found' if found else 'Check if generated by scripts'
    }

    # Rule 4: Data format
    data_files = find_files(root, ['*.csv', '*.dta', '*.rds', '*.parquet', '*.xlsx'])
    results['rule_4'] = {
        'name': 'Data format',
        'status': PASS if data_files else WARN,
        'note': f"Found {len(data_files)} data files" if data_files else 'No standard data files'
    }

    # Rule 5: Metadata
    codebook = find_files(root, ['*codebook*', '*variables*', '*dictionary*'])
    results['rule_5'] = {
        'name': 'Metadata',
        'status': PASS if codebook else WARN,
        'note': f"Found: {codebook[0].name}" if codebook else 'No codebook found'
    }

    # Rule 6: Citations
    status, note = check_readme_section(readme, ['citation', 'reference', 'source'])
    results['rule_6'] = {'name': 'Data citations', 'status': status, 'note': note}

    return results


def check_code(root: Path) -> Dict:
    """Check DCAS Rules 7-9: Code."""
    results = {}

    # Rule 7: Data transformation
    dataprep = find_files(root, ['*clean*.do', '*clean*.R', '*clean*.py',
                                  '*prep*.do', '*prep*.R', '*prep*.py'])
    dataprep_dir = any((root / d).exists() for d in ['code/dataprep', 'dataprep', 'scripts/prep'])
    results['rule_7'] = {
        'name': 'Data transformation',
        'status': PASS if (dataprep or dataprep_dir) else WARN,
        'note': f"Found {len(dataprep)} prep scripts" if dataprep else 'Check for data prep scripts'
    }

    # Rule 8: Analysis programs
    analysis = find_files(root, ['*regress*.do', '*regress*.R', '*analysis*.py',
                                  '*estimate*.do', '*estimate*.R', '*estim*.m',
                                  '*simul*.m', '*plot*.m', '*run*.m'])
    analysis_dir = any((root / d).exists() for d in ['code/analysis', 'analysis', 'scripts/analysis',
                                                       '_estim', 'simulations', 'analytics'])
    results['rule_8'] = {
        'name': 'Analysis programs',
        'status': PASS if (analysis or analysis_dir) else WARN,
        'note': f"Found {len(analysis)} analysis scripts" if analysis else 'Check for analysis scripts'
    }

    # Rule 9: Source format
    scripts = find_files(root, ['*.do', '*.R', '*.py', '*.jl', '*.m', '*.r', '*.Rmd', '*.qmd'])
    binaries = find_files(root, ['*.exe', '*.dll', '*.so', '*.pyc', '*.mex*'])
    if binaries:
        status, note = WARN, f"Found {len(binaries)} binary files"
    elif scripts:
        status, note = PASS, f"Found {len(scripts)} source files"
    else:
        status, note = FAIL, "No source code found"
    results['rule_9'] = {'name': 'Source format', 'status': status, 'note': note}

    return results


def check_supporting(root: Path) -> Dict:
    """Check DCAS Rules 10-12: Supporting Materials."""
    results = {}
    readme = root / 'README.md'

    # Rule 10: Instruments
    instruments = find_files(root, ['*survey*', '*questionnaire*', '*instrument*'])
    docs_dir = (root / 'documents').exists() or (root / 'docs').exists()
    results['rule_10'] = {
        'name': 'Instruments',
        'status': PASS if instruments else (WARN if docs_dir else NA),
        'note': 'Found instruments' if instruments else ('Check if applicable' if not docs_dir else 'N/A')
    }

    # Rule 11: Ethics
    status, note = check_readme_section(readme, ['irb', 'ethics', 'approval'])
    if status == FAIL:
        status, note = NA, 'Check if applicable'
    results['rule_11'] = {'name': 'Ethics approval', 'status': status, 'note': note}

    # Rule 12: Pre-registration
    status, note = check_readme_section(readme, ['pre-registration', 'registered', 'registry'])
    if status == FAIL:
        status, note = NA, 'Check if applicable'
    results['rule_12'] = {'name': 'Pre-registration', 'status': status, 'note': note}

    return results


def check_documentation(root: Path) -> Dict:
    """Check DCAS Rule 13: Documentation."""
    results = {}
    readme = root / 'README.md'
    if not readme.exists():
        readme = root / 'code' / 'README.md'

    # README exists
    results['readme'] = {
        'name': 'README exists',
        'status': PASS if readme.exists() else FAIL,
        'note': str(readme) if readme.exists() else 'Missing'
    }

    if readme.exists():
        content = readme.read_text(errors='ignore').lower()

        # Software requirements
        sw_keywords = ['stata', 'r version', 'python', 'software', 'requirements']
        found = any(kw in content for kw in sw_keywords)
        results['software'] = {
            'name': 'Software requirements',
            'status': PASS if found else WARN,
            'note': 'Documented' if found else 'Not documented'
        }

        # Hardware requirements
        hw_keywords = ['memory', 'ram', 'runtime', 'hours', 'minutes', 'hardware']
        found = any(kw in content for kw in hw_keywords)
        results['hardware'] = {
            'name': 'Hardware/runtime',
            'status': PASS if found else WARN,
            'note': 'Documented' if found else 'Not documented'
        }

        # Instructions
        instr_keywords = ['instruction', 'how to', 'run the', 'execute', 'replicate']
        found = any(kw in content for kw in instr_keywords)
        results['instructions'] = {
            'name': 'Instructions',
            'status': PASS if found else WARN,
            'note': 'Found' if found else 'Not documented'
        }

    return results


def check_sharing(root: Path) -> Dict:
    """Check DCAS Rules 14-16: Sharing."""
    results = {}
    readme = root / 'README.md'

    # Rule 14: Archive
    status, note = check_readme_section(readme, ['doi', 'zenodo', 'icpsr', 'dataverse', 'archive'])
    results['rule_14'] = {'name': 'Archive location', 'status': status, 'note': note}

    # Rule 15: License
    license_files = find_files(root, ['LICENSE*', 'LICENCE*'])
    results['rule_15'] = {
        'name': 'License',
        'status': PASS if license_files else FAIL,
        'note': f"Found: {license_files[0].name}" if license_files else 'Missing LICENSE file'
    }

    # Rule 16: Omissions
    status, note = check_readme_section(readme, ['omission', 'not included', 'restricted', 'confidential'])
    if status == FAIL:
        status, note = NA, 'Check if any omissions exist'
    results['rule_16'] = {'name': 'Omissions', 'status': status, 'note': note}

    return results


def check_large_files(root: Path, threshold_mb: int = 50) -> Dict:
    """Check for large files that may need git-lfs."""
    results = {}
    threshold_bytes = threshold_mb * 1024 * 1024

    # Check for git-lfs
    gitattributes = root / '.gitattributes'
    has_lfs = False
    if gitattributes.exists():
        content = gitattributes.read_text(errors='ignore')
        has_lfs = 'lfs' in content.lower()

    results['git_lfs'] = {
        'name': 'Git LFS configured',
        'status': PASS if has_lfs else NA,
        'note': 'LFS configured' if has_lfs else 'Not using git-lfs (may be OK)'
    }

    # Find large files
    large_files = []
    for f in root.rglob('*'):
        if f.is_file() and '.git' not in str(f):
            try:
                if f.stat().st_size > threshold_bytes:
                    large_files.append(f)
            except (OSError, PermissionError):
                pass

    if large_files:
        results['large_files'] = {
            'name': f'Large files (>{threshold_mb}MB)',
            'status': WARN if not has_lfs else PASS,
            'note': f"Found {len(large_files)} large files" + (" - consider git-lfs" if not has_lfs else "")
        }

    return results


def check_confidential_data(root: Path) -> Dict:
    """Check for confidential data handling."""
    results = {}
    readme = root / 'README.md'

    if readme.exists():
        content = readme.read_text(errors='ignore').lower()

        # Check for confidential data indicators
        confidential_keywords = ['confidential', 'restricted', 'proprietary',
                                  'cannot be shared', 'not publicly available',
                                  'apply for access', 'data use agreement']
        has_confidential = any(kw in content for kw in confidential_keywords)

        if has_confidential:
            # Check for access instructions
            access_keywords = ['apply', 'request', 'contact', 'access at', 'available from']
            has_access_info = any(kw in content for kw in access_keywords)

            results['confidential_data'] = {
                'name': 'Confidential data handling',
                'status': PASS if has_access_info else WARN,
                'note': 'Access instructions provided' if has_access_info else 'Add access instructions for restricted data'
            }

            # Check for simulated/synthetic data
            sim_data = find_files(root, ['*simulated*', '*synthetic*', '*fake*', '*test*'])
            sim_dir = any((root / d).exists() for d in ['data/simulated', 'data/synthetic', 'data/test'])
            results['simulated_data'] = {
                'name': 'Simulated data for testing',
                'status': PASS if (sim_data or sim_dir) else WARN,
                'note': 'Found simulated data' if (sim_data or sim_dir) else 'Consider providing simulated data for code testing'
            }

    return results


def check_language_specific(root: Path, language: str) -> Dict:
    """Check language-specific requirements."""
    results = {}

    if language == 'stata':
        # Master script
        master = find_files(root, ['run.do', 'master.do', 'main.do'])
        results['master'] = {
            'name': 'Master script',
            'status': PASS if master else WARN,
            'note': f"Found: {master[0].name}" if master else 'No master script'
        }

        # Package management
        libs = (root / 'code' / 'libraries' / 'stata').exists() or \
               (root / 'libraries' / 'stata').exists()
        results['packages'] = {
            'name': 'Package management',
            'status': PASS if libs else WARN,
            'note': 'Local libraries found' if libs else 'Document packages in README'
        }

    elif language == 'r':
        # renv
        renv = find_files(root, ['renv.lock'])
        results['renv'] = {
            'name': 'renv.lock',
            'status': PASS if renv else WARN,
            'note': 'Found' if renv else 'Consider using renv'
        }

        # Master script
        master = find_files(root, ['run.R', 'main.R', 'master.R'])
        results['master'] = {
            'name': 'Master script',
            'status': PASS if master else WARN,
            'note': f"Found: {master[0].name}" if master else 'No master script'
        }

    elif language == 'python':
        # requirements.txt
        reqs = find_files(root, ['requirements.txt', 'environment.yml', 'pyproject.toml'])
        results['requirements'] = {
            'name': 'Requirements file',
            'status': PASS if reqs else WARN,
            'note': f"Found: {reqs[0].name}" if reqs else 'Missing requirements.txt'
        }

        # Check if requirements are pinned
        if reqs:
            req_content = reqs[0].read_text(errors='ignore')
            if '==' in req_content:
                results['pinned'] = {
                    'name': 'Pinned versions',
                    'status': PASS,
                    'note': 'Package versions are pinned'
                }
            else:
                results['pinned'] = {
                    'name': 'Pinned versions',
                    'status': WARN,
                    'note': 'Versions not pinned (use package==1.2.3)'
                }

        # Master script
        master = find_files(root, ['run.py', 'main.py'])
        results['master'] = {
            'name': 'Master script',
            'status': PASS if master else WARN,
            'note': f"Found: {master[0].name}" if master else 'No master script'
        }

    elif language == 'matlab':
        # Check for main/master script
        master = find_files(root, ['main.m', 'run.m', 'master.m', 'run_all.m'])
        results['master'] = {
            'name': 'Master script',
            'status': PASS if master else WARN,
            'note': f"Found: {master[0].name}" if master else 'No master script (main.m)'
        }

        # Check for startup.m
        startup = find_files(root, ['startup.m'])
        results['startup'] = {
            'name': 'startup.m',
            'status': PASS if startup else WARN,
            'note': 'Found' if startup else 'Consider adding startup.m for path setup'
        }

        # Check for toolbox documentation
        readme = root / 'README.md'
        if readme.exists():
            content = readme.read_text(errors='ignore').lower()
            has_toolbox = 'toolbox' in content
            results['toolboxes'] = {
                'name': 'Toolbox documentation',
                'status': PASS if has_toolbox else WARN,
                'note': 'Toolboxes documented' if has_toolbox else 'Document required MATLAB toolboxes in README'
            }

    elif language == 'julia':
        # Check for Project.toml
        project = find_files(root, ['Project.toml'])
        manifest = find_files(root, ['Manifest.toml'])
        results['project'] = {
            'name': 'Project.toml',
            'status': PASS if project else WARN,
            'note': 'Found' if project else 'Missing Project.toml'
        }
        results['manifest'] = {
            'name': 'Manifest.toml',
            'status': PASS if manifest else WARN,
            'note': 'Found (versions locked)' if manifest else 'Missing Manifest.toml for version locking'
        }

        # Master script
        master = find_files(root, ['run.jl', 'main.jl'])
        results['master'] = {
            'name': 'Master script',
            'status': PASS if master else WARN,
            'note': f"Found: {master[0].name}" if master else 'No master script'
        }

    return results


def calculate_score(results: Dict) -> Tuple[int, int]:
    """Calculate pass/total score from results."""
    passed = sum(1 for r in results.values() if r.get('status') == PASS)
    total = sum(1 for r in results.values() if r.get('status') != NA)
    return passed, total


def generate_report(root: Path, include_json: bool = False) -> str:
    """Generate full compliance report."""
    language = detect_language(root)
    all_languages = detect_all_languages(root)

    data_results = check_data_availability(root)
    code_results = check_code(root)
    support_results = check_supporting(root)
    doc_results = check_documentation(root)
    share_results = check_sharing(root)
    lang_results = check_language_specific(root, language)
    large_file_results = check_large_files(root)
    confidential_results = check_confidential_data(root)

    # Run code-level checks
    code_issues = run_code_level_checks(root)
    errors = [i for i in code_issues if i.severity == ERROR]
    warnings = [i for i in code_issues if i.severity == WARNING]

    # Calculate scores
    data_score = calculate_score(data_results)
    code_score = calculate_score(code_results)
    support_score = calculate_score(support_results)
    doc_score = calculate_score(doc_results)
    share_score = calculate_score(share_results)

    total_passed = sum(s[0] for s in [data_score, code_score, support_score, doc_score, share_score])
    total_possible = sum(s[1] for s in [data_score, code_score, support_score, doc_score, share_score])
    percent = int(100 * total_passed / total_possible) if total_possible > 0 else 0

    # Build report
    report = []
    report.append("# Replication Compliance Report\n")
    report.append(f"**Repository:** {root.name}")
    report.append(f"**Path:** {root.absolute()}")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**Languages Detected:** {', '.join(lang.title() for lang in all_languages)}")
    report.append(f"**Primary Language:** {language.title()}")
    report.append(f"**Standard:** DCAS v1.0\n")

    report.append("## Summary\n")
    report.append("| Category | Score | Status |")
    report.append("|----------|-------|--------|")

    def status_icon(passed, total):
        if total == 0:
            return NA
        ratio = passed / total
        if ratio >= 0.8:
            return PASS
        elif ratio >= 0.5:
            return WARN
        return FAIL

    report.append(f"| Data Availability (1-6) | {data_score[0]}/{data_score[1]} | {status_icon(*data_score)} |")
    report.append(f"| Code (7-9) | {code_score[0]}/{code_score[1]} | {status_icon(*code_score)} |")
    report.append(f"| Supporting (10-12) | {support_score[0]}/{support_score[1]} | {status_icon(*support_score)} |")
    report.append(f"| Documentation (13) | {doc_score[0]}/{doc_score[1]} | {status_icon(*doc_score)} |")
    report.append(f"| Sharing (14-16) | {share_score[0]}/{share_score[1]} | {status_icon(*share_score)} |")
    report.append(f"| **Overall** | **{total_passed}/{total_possible}** | **{status_icon(total_passed, total_possible)} ({percent}%)** |\n")

    # Detailed findings
    all_results = {
        'Data Availability': data_results,
        'Code': code_results,
        'Supporting Materials': support_results,
        'Documentation': doc_results,
        'Sharing': share_results,
        f'{language.title()} Specific': lang_results,
    }

    # Add optional checks if they have results
    if large_file_results:
        all_results['Large Files'] = large_file_results
    if confidential_results:
        all_results['Confidential Data'] = confidential_results

    report.append("## Detailed Findings\n")
    for category, results in all_results.items():
        if not results:
            continue
        report.append(f"### {category}\n")
        report.append("| Check | Status | Notes |")
        report.append("|-------|--------|-------|")
        for key, r in results.items():
            report.append(f"| {r['name']} | {r['status']} | {r['note']} |")
        report.append("")

    # Recommendations
    report.append("## Recommendations\n")

    critical = []
    important = []

    for category, results in all_results.items():
        for key, r in results.items():
            if r['status'] == FAIL:
                critical.append(f"{r['name']}: {r['note']}")
            elif r['status'] == WARN:
                important.append(f"{r['name']}: {r['note']}")

    if critical:
        report.append("### Critical (Required)\n")
        for i, item in enumerate(critical, 1):
            report.append(f"{i}. {item}")
        report.append("")

    if important:
        report.append("### Important (Recommended)\n")
        for i, item in enumerate(important, 1):
            report.append(f"{i}. {item}")
        report.append("")

    if not critical and not important:
        report.append("No critical issues found. Review warnings above.\n")

    # Code-Level Issues Section
    if code_issues:
        report.append("## Code-Level Issues\n")
        report.append(f"Found **{len(errors)} errors** and **{len(warnings)} warnings** in source code.\n")

        if errors:
            report.append("### ❌ Errors (Will cause replication failure)\n")
            for issue in errors:
                report.append(f"**{issue.file}:{issue.line}** - {issue.message}")
                if issue.code:
                    report.append(f"```\n{issue.code}\n```")
                report.append(f"*Fix:* {issue.suggestion}\n")

        if warnings:
            report.append("### ⚠️ Warnings (Risk to reproducibility)\n")
            for issue in warnings[:10]:  # Limit to first 10
                report.append(f"**{issue.file}:{issue.line}** - {issue.message}")
                if issue.code:
                    report.append(f"  - Code: `{issue.code}`")
                report.append(f"  - *Fix:* {issue.suggestion}\n")

            if len(warnings) > 10:
                report.append(f"*...and {len(warnings) - 10} more warnings*\n")

    return '\n'.join(report)


def generate_json_report(root: Path) -> Dict:
    """Generate machine-readable JSON report."""
    language = detect_language(root)
    all_languages = detect_all_languages(root)

    data_results = check_data_availability(root)
    code_results = check_code(root)
    support_results = check_supporting(root)
    doc_results = check_documentation(root)
    share_results = check_sharing(root)
    lang_results = check_language_specific(root, language)

    code_issues = run_code_level_checks(root)
    errors = [i for i in code_issues if i.severity == ERROR]
    warnings = [i for i in code_issues if i.severity == WARNING]

    # Calculate scores
    data_score = calculate_score(data_results)
    code_score = calculate_score(code_results)
    support_score = calculate_score(support_results)
    doc_score = calculate_score(doc_results)
    share_score = calculate_score(share_results)

    total_passed = sum(s[0] for s in [data_score, code_score, support_score, doc_score, share_score])
    total_possible = sum(s[1] for s in [data_score, code_score, support_score, doc_score, share_score])
    percent = int(100 * total_passed / total_possible) if total_possible > 0 else 0

    return {
        "repository": root.name,
        "path": str(root.absolute()),
        "date": datetime.now().isoformat(),
        "languages": all_languages,
        "primary_language": language,
        "standard": "DCAS v1.0",
        "summary": {
            "score": f"{total_passed}/{total_possible}",
            "percent": percent,
            "errors": len(errors),
            "warnings": len(warnings),
            "categories": {
                "data_availability": {"score": f"{data_score[0]}/{data_score[1]}"},
                "code": {"score": f"{code_score[0]}/{code_score[1]}"},
                "supporting": {"score": f"{support_score[0]}/{support_score[1]}"},
                "documentation": {"score": f"{doc_score[0]}/{doc_score[1]}"},
                "sharing": {"score": f"{share_score[0]}/{share_score[1]}"},
            }
        },
        "code_issues": [asdict(i) for i in code_issues],
        "dcas_checks": {
            "data_availability": data_results,
            "code": code_results,
            "supporting": support_results,
            "documentation": doc_results,
            "sharing": share_results,
            f"{language}_specific": lang_results,
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='Check research repository compliance with DCAS v1.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_compliance.py /path/to/repo
  python check_compliance.py . --json
  python check_compliance.py ./project --save
  python check_compliance.py ./project --json --save
        """
    )
    parser.add_argument('repo_path', help='Path to repository to check')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--save', action='store_true', help='Save report to file')
    parser.add_argument('--code-only', action='store_true', help='Only run code-level checks')

    args = parser.parse_args()

    repo_path = Path(args.repo_path).resolve()
    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}", file=sys.stderr)
        sys.exit(1)

    if args.code_only:
        # Quick code-level scan only
        issues = run_code_level_checks(repo_path)
        if args.json:
            output = json.dumps([asdict(i) for i in issues], indent=2)
            print(output)
        else:
            errors = [i for i in issues if i.severity == ERROR]
            warnings = [i for i in issues if i.severity == WARNING]
            print(f"Code-Level Scan: {len(errors)} errors, {len(warnings)} warnings\n")
            for issue in issues:
                icon = FAIL if issue.severity == ERROR else WARN
                print(f"{icon} {issue.file}:{issue.line} [{issue.check_id}]")
                print(f"   {issue.message}")
                if issue.code:
                    print(f"   Code: {issue.code}")
                print(f"   Fix: {issue.suggestion}\n")
        sys.exit(1 if errors else 0)

    if args.json:
        report_data = generate_json_report(repo_path)
        output = json.dumps(report_data, indent=2, default=str)
        print(output)
        if args.save:
            output_path = repo_path / 'compliance_report.json'
            output_path.write_text(output)
            print(f"Report saved to: {output_path}", file=sys.stderr)
    else:
        report = generate_report(repo_path)
        print(report)
        if args.save:
            output_path = repo_path / 'compliance_report.md'
            output_path.write_text(report)
            print(f"\nReport saved to: {output_path}")


if __name__ == '__main__':
    main()
