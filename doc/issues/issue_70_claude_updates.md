# Issue #70 - Claude Updates

## Overview

**Issue:** [#70 Claude Updates](https://github.com/oislen/RandomTelecomPayments/issues/70)  
**Label:** documentation  
**Milestone:** RandomTelecomPayments Version 1  

### Scope

1. Add `CLAUDE.md` file to the repository root
2. Update README
3. Update docs
4. Update unittests

---

## Implementation Plan

### 1. Add `CLAUDE.md`

**Status: Complete**

`CLAUDE.md` was created at the repository root. It provides a single authoritative reference for Claude and other AI coding agents working in this repository. The following sections were included:

#### 1.1 Project Overview
- Purpose of the RandomTelecomPayments project (synthetic telecom payments data generator)
- Links to the Kaggle master dataset and Docker Hub image

#### 1.2 Repository Structure
A full annotated directory tree covering every top-level folder and key file with inline descriptions, matching the tree published in `README.md`.

#### 1.3 Development Environment Setup
- `uv sync` (recommended)
- conda alternative (`conda create` + `pip install -r requirements.txt`)

#### 1.4 Running the Application
- Local CLI via `exeMain.cmd` / `exeMain.sh` and direct `uv run python generator/main.py` invocation
- Output file locations (`data/RandomTelecomPayments.csv`, `data/RandomTelecomUsers.parquet`)
- Local FastAPI server via `exeApi.cmd` / `exeApi.sh`, with endpoint table (GET and POST `/api`)
- Docker pull, CLI run, data extraction, and FastAPI-via-Docker commands

#### 1.5 Application Parameters
Full parameter table (name, type, default, description) for all 8 CLI parameters, with a note that all defaults are defined in `generator/cons.py`.

#### 1.6 Running Unit Tests
Convenience scripts (`exeUnittests.cmd` / `exeUnittests.sh`) and equivalent `uv run python -m unittest discover` commands for all three suites, plus a note on GitHub Actions integration.

#### 1.7 Data Model
- Entity list and output column groups table (User, Device, Card, IP, Application, Transaction, Iteration)
- Links to `doc/entity_relationship_diagram.jpg` and `doc/data_dictionary.csv`

#### 1.8 Key Modules and Entry Points
Table mapping every key file to its purpose, covering `main.py`, `api.py`, `cons.py`, `ProgrammeParams.py`, `gen_random_telecom_data.py`, `gen_user_data.py`, `gen_trans_data.py`, `objects/`, `utilities/`, `qa/`, and `batch/gen_bedrock_data.py`.

#### 1.9 Coding Conventions
- `beartype` runtime type enforcement on all public functions and `__init__` methods
- Constants centralised in `generator/cons.py`
- Entity class pattern, utility function pattern
- NumPy docstring style
- Test coverage requirements and constants policy
- Required column order from `cons.py` column lists

#### 1.10 Common Tasks for AI Agents
Step-by-step instructions for:
- Adding a new output column (5-step checklist: objects, cons.py, app, data dictionary, tests)
- Changing a default parameter (cons.py, README.md, CLAUDE.md)
- Adding a new utility function (create, import, test)
- Regenerating reference data via the Bedrock batch script
- Rebuilding the Docker image
- Running QA checks manually

#### 1.11 CI/CD
Summary table of both GitHub Actions workflows (triggers and jobs).

---

### 2. Update README

**Status: Complete**

The `README.md` was fully reviewed and expanded. The following changes were made:

#### 2.1 Repository Structure section added
A full annotated directory tree was added covering every top-level folder and key file with inline descriptions. This gives contributors and AI agents immediate orientation without having to browse the repo manually.

#### 2.2 Development Setup section added
A new **Development Setup** section documents both the recommended `uv sync` path and the conda alternative (`conda create` + `pip install -r requirements.txt`).

#### 2.3 Application Parameters converted to table
The bulleted parameter list was replaced with a structured Markdown table including parameter name, type, default, and description for all 8 CLI parameters. The `is_release` flag is internal to `main.py` and intentionally omitted from the public-facing README.

#### 2.4 Running the Application expanded
The original Docker-only section was expanded into a full **Running the Application** section covering:
- Local CLI run with `uv` and the convenience `exeMain.cmd` / `exeMain.sh` scripts
- Output file locations
- Local FastAPI server startup with `exeApi.cmd` / `exeApi.sh`
- API endpoint table (GET and POST `/api`)
- Docker pull, CLI run, data extraction, and FastAPI-via-Docker commands

#### 2.5 Running Unit Tests section added
A new **Running Unit Tests** section documents the `exeUnittests.cmd` / `exeUnittests.sh` convenience scripts and the equivalent `uv run python -m unittest discover` commands for all three suites, plus a note that tests run automatically via GitHub Actions.

#### 2.6 CI/CD section added
A new **CI/CD** section summarises both GitHub Actions workflows (`dev-pull-requests.yml` and `deploy-main-push.yml`) in a table showing triggers and jobs.

#### 2.7 Reference Data section added
A new **Reference Data** section documents all files in `data/ref/` and their purpose, plus instructions for regenerating AI-generated name/email reference data via the Bedrock batch script.

#### 2.8 Images and links verified
All existing image references (`doc/entity_relationship_diagram.jpg`, `doc/fastapi_endpoint.jpg`) and external links (Kaggle, Docker Hub) were retained verbatim.

---

### 3. Update Docs

**Status: Complete**

#### 3.1 `doc/data_dictionary.csv` — audited and updated

All column names were verified against the column lists in `generator/cons.py` (`user_cols`, `device_cols`, `card_cols`, `ip_cols`, `app_cols`, `trans_cols`, `itr_cols`). The following changes were made:

| Change | Detail |
|---|---|
| Added `itr_hash` row | Was missing from the dictionary entirely; added with type String, Nullable FALSE, example value, and description explaining its purpose as a per-iteration batch identifier |
| Fixed `card_payment_channel` enum value | `'Worldpay'` corrected to `'WorldPay'` to match the value in `cons.data_model_payment_channels` |

All other 22 columns were already present with accurate descriptions and examples. No columns were removed.

#### 3.2 `doc/new_hire_tasks.md` — onboarding section added

A new **Section 0: Onboarding** was prepended to the document with links to `CLAUDE.md`, `README.md`, `doc/data_dictionary.csv`, and `doc/entity_relationship_diagram.jpg`, so new contributors have a clear starting point before beginning the analytical tasks.

The table of contents was updated to include the new section.

#### 3.3 `doc/issues/` — this implementation plan

This document (`doc/issues/issue_70_claude_updates.md`) serves as the complete record of all work done for issue #70.

---

### 4. Update Unit Tests

**Status: Complete**

#### 4.1 Existing test files fixed

| File | Change |
|---|---|
| `unittests/utilities/test_commandline_interface.py` | Rewrote entirely — removed dead `if False and __name__ == "__main__":` guard; replaced with a proper `unittest.TestCase` using `unittest.mock.patch` to inject `sys.argv`, covering defaults, all overrides, return type, and expected keys |
| `unittests/utilities/test_gen_obj_idhash_series.py` | Renamed misnamed class `TestGenIdhashCntDict` → `TestGenObjIdhashSeries` |

#### 4.2 New test files created

##### `unittests/utilities/`

| File | Coverage |
|---|---|
| `test_input_error_handling.py` | Valid minimum/full inputs raise no exception; zero/negative/non-integer values for `n_users`, `use_random_seed`, `n_itr`, `n_applications` each raise `ValueError`; error messages contain the offending parameter name |
| `test_join_idhashes_dict.py` | Return type is DataFrame; row count unchanged; new value column added; correct values mapped; NaN for missing keys; original columns unchanged; integer-key variant |
| `test_JsonEncoder.py` | `np.datetime64` and `pd.Timestamp` serialise to non-empty strings; `np.int64`/`int32` serialise to `int`; `np.float64`/`float32` serialise to `float`; native Python types pass through unchanged; mixed-type dict round-trip; unknown type raises `TypeError` |
| `test_gen_trans_rejection_rates.py` | Return type is dict; all 8 top-level keys present; inner values are floats; country-code and email-domain rates sum to 1.0 and are non-negative; entity-hash and userid keys match the input DataFrame |
| `test_gen_trans_status.py` | Card-absent path: status in {Successful, Pending}, error code is NaN; card-present low-rates path: status in {Successful, Pending}, error code is NaN; card-present high-rates path: status is Rejected, error code in valid set; status always in valid universe across multiple seeds; Rejected status always has a non-null error code |

##### `unittests/app/`

| File | Coverage |
|---|---|
| `test_ProgrammeParams.py` | All attribute types correct; values stored verbatim; `transaction_timescale` computed correctly for 1-year and half-year spans; `random_seed=None` accepted; default `n_users=100` and `n_applications=20000` |
| `test_gen_random_telecom_data.py` | Return type is dict with keys `user_data`/`trans_data`; user DataFrame has n_users rows, all expected columns, unique uids, non-null userids; trans DataFrame is non-empty, has all expected columns, is sorted by date, all userids traceable to user_data; status/error-code business rule invariants |
| `test_gen_user_data.py` | Return type; row count = n_users; all expected columns present; count columns dropped; key columns (userid, uid, first_name, last_name, itr_hash) are non-null; uid uniqueness; single itr_hash value per run; hash columns contain lists; registration dates within configured window |
| `test_gen_trans_data.py` | Return type; non-empty; all expected columns; no list-valued columns remain; transaction_hash/userid/transaction_date non-null; sorted ascending by date; status in valid set; Rejected ↔ non-null error code; Successful/Pending ↔ null error code; error codes in valid universe; payment methods, card types, channels all in valid sets; null card_hash ↔ null card_type; amounts ≥ 0; userid referential integrity against user_data |

#### 4.3 Docstrings updated

All existing test classes that had an empty `""""""` docstring were updated with a meaningful multi-line description explaining what the class tests and why. Files updated:

- `unittests/objects/`: `test_Application.py`, `test_Card.py`, `test_Device.py`, `test_Ip.py`, `test_Transaction.py`, `test_User.py`
- `unittests/app/`: `test_gen_user_trans_data.py`
- `unittests/utilities/`: `test_align_country_codes.py`, `test_cnt2prop_dict.py`, `test_gen_country_codes_dict.py`, `test_gen_country_codes_map.py`, `test_gen_dates_dict.py`, `test_gen_idhash_cnt_dict.py`, `test_gen_random_entity_counts.py`, `test_gen_random_hash.py`, `test_gen_random_id.py`, `test_gen_random_poisson_power.py`, `test_gen_shared_idhashes.py`, `test_remove_duplicate_idhashes.py`, `test_round_trans_amount.py`

#### 4.4 Test fixtures and constants

All new tests use constants from `generator/cons.py` (`unittest_seed`, `unittest_n_users`, `unittest_n_entities`, `unittest_registration_start_date`, etc.) rather than hardcoded values.

#### 4.5 CI integration

- Verify that `.github/` workflows execute the unit tests on push/PR and that the test command matches `exeUnittests.sh`

---

## Acceptance Criteria

| # | Criterion | Status |
|---|---|---|
| 1 | `CLAUDE.md` exists at the repository root and contains all sections listed in §1 above | Complete |
| 2 | `README.md` includes a unit test run section and development setup section | Complete |
| 3 | `doc/data_dictionary.csv` columns match those defined in `generator/cons.py` | Complete |
| 4 | All unit tests pass: `uv run python -m pytest generator/unittests/` | Pending |
| 5 | No new source files are introduced without corresponding unit tests | Complete |

---

## File Change Summary

| File | Action | Status |
|---|---|---|
| `CLAUDE.md` | Create | Complete |
| `README.md` | Update | Complete |
| `doc/data_dictionary.csv` | Update (audit columns) | Complete |
| `doc/new_hire_tasks.md` | Add onboarding section (§0) with links to CLAUDE.md | Complete |
| `generator/unittests/utilities/test_commandline_interface.py` | Rewrite (remove dead guard, add mock-based tests) | Complete |
| `generator/unittests/utilities/test_gen_obj_idhash_series.py` | Fix class name | Complete |
| `generator/unittests/utilities/test_input_error_handling.py` | Create | Complete |
| `generator/unittests/utilities/test_join_idhashes_dict.py` | Create | Complete |
| `generator/unittests/utilities/test_JsonEncoder.py` | Create | Complete |
| `generator/unittests/utilities/test_gen_trans_rejection_rates.py` | Create | Complete |
| `generator/unittests/utilities/test_gen_trans_status.py` | Create | Complete |
| `generator/unittests/app/test_ProgrammeParams.py` | Create | Complete |
| `generator/unittests/app/test_gen_random_telecom_data.py` | Create | Complete |
| `generator/unittests/app/test_gen_user_data.py` | Create | Complete |
| `generator/unittests/app/test_gen_trans_data.py` | Create | Complete |
| All existing test files with empty `""""""` docstrings | Update class docstrings | Complete |
