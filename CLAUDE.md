# CLAUDE.md — RandomTelecomPayments

This file provides context and guidance for Claude and other AI coding agents working in this repository.

## Project Overview

**RandomTelecomPayments** is a Python application that generates synthetic telecommunication payments data using random number generation. It simulates realistic transaction-level relationships and behaviours among user, device, IP address, card, and application entities.

The generated data is intended for:
- Prototyping fraud detection and analytics solutions without exposing real customer data
- Educational use as a realistic, privacy-safe telecom payments dataset

A stable master version of the dataset is published on Kaggle:
- https://www.kaggle.com/datasets/oislen/randomtelecompayments

The Docker image is published on Docker Hub:
- https://hub.docker.com/repository/docker/oislen/randomtelecompayments/general

---

## Repository Structure

```
RandomTelecomPayments/
├── .creds/                        # AWS credentials — NOT committed to version control
├── .github/
│   └── workflows/
│       ├── deploy-main-push.yml   # CI/CD: tag, scan, test, build and push Docker image on main push
│       └── dev-pull-requests.yml  # CI: Trivy security scan + unit tests on pull requests
├── aws/                           # AWS EC2 automation scripts and config
├── config/
│   ├── conda/                     # Conda environment setup script
│   └── uv/                        # uv dependency install script
├── data/
│   ├── RandomTelecomPayments.csv  # Main generated transaction-level output
│   ├── RandomTelecomUsers.parquet # Intermediate user-level output
│   ├── arch/                      # Archived prior dataset versions (V0.0–V0.3)
│   ├── ref/                       # Reference data (countries, names, emails, smartphones, crime index)
│   ├── report/                    # Analytical outputs (anomaly scores, model files, feature data)
│   ├── temp/                      # Per-country AI-generated temporary CSVs
│   └── unittest/                  # Parquet fixtures used by unit tests
├── doc/
│   ├── data_dictionary.csv        # Column-level data dictionary for the output dataset
│   ├── entity_relationship_diagram.jpg / .drawio
│   ├── new_hire_tasks.md          # Suggested analysis tasks for new contributors
│   ├── RandomTelecomPayments.postman_collection.json
│   └── issues/                    # Implementation plans for GitHub issues
├── generator/
│   ├── main.py                    # CLI entry point
│   ├── api.py                     # FastAPI application (GET + POST /api)
│   ├── cons.py                    # Global constants: paths, defaults, data model parameters
│   ├── app/
│   │   ├── ProgrammeParams.py     # Parameter validation and transaction_timescale computation
│   │   ├── gen_random_telecom_data.py  # Top-level orchestration function
│   │   ├── gen_user_data.py       # User-level DataFrame construction
│   │   └── gen_trans_data.py      # Transaction-level DataFrame construction
│   ├── batch/
│   │   └── gen_bedrock_data.py    # AWS Bedrock batch script to generate reference name/email data
│   ├── objects/
│   │   ├── Application.py         # Application entity (hashes, payment channels)
│   │   ├── Card.py                # Card entity (hashes, types, country codes, shared mappings)
│   │   ├── Device.py              # Device entity (hashes, types, shared mappings)
│   │   ├── Ip.py                  # IP entity (hashes, country codes, shared mappings)
│   │   ├── Transaction.py         # Transaction entity (hashes, dates, amounts, statuses)
│   │   └── User.py                # User entity (IDs, names, country codes, email domains, dates)
│   ├── qa/
│   │   ├── Cards.py               # QA: card hash → type and country code cardinality
│   │   ├── Ips.py                 # QA: IP hash → country code cardinality
│   │   ├── Transactions.py        # QA: transaction-level field consistency and business rules
│   │   └── Uids.py                # QA: user-level entity counts and date ordering
│   ├── unittests/
│   │   ├── app/                   # Tests for ProgrammeParams, gen_user_data, gen_trans_data, gen_random_telecom_data
│   │   ├── objects/               # Tests for each entity class
│   │   └── utilities/             # Tests for each utility function
│   └── utilities/
│       ├── align_country_codes.py
│       ├── Bedrock.py
│       ├── cnt2prop_dict.py
│       ├── commandline_interface.py
│       ├── gen_country_codes_dict.py
│       ├── gen_country_codes_map.py
│       ├── gen_dates_dict.py
│       ├── gen_idhash_cnt_dict.py
│       ├── gen_obj_idhash_series.py
│       ├── gen_random_entity_counts.py
│       ├── gen_random_hash.py
│       ├── gen_random_id.py
│       ├── gen_random_poisson_power.py
│       ├── gen_shared_idhashes.py
│       ├── gen_trans_rejection_rates.py
│       ├── gen_trans_status.py
│       ├── input_error_handling.py
│       ├── join_idhashes_dict.py
│       ├── JsonEncoder.py
│       ├── multiprocess.py
│       └── remove_duplicate_idhashes.py
├── Dockerfile
├── pyproject.toml                 # Project metadata and dependencies (uv)
├── requirements.txt               # Pip-compatible dependency list
└── uv.lock                        # Locked dependency manifest
```

---

## Development Environment Setup

**Prerequisites:** Python >= 3.12

**Using uv (recommended):**
```bash
uv sync
```

**Using conda:**
```bash
conda create --name RandomTelecomPayments python=3.12 --yes
conda activate RandomTelecomPayments
pip install -r requirements.txt
```

---

## Running the Application

All commands assume the working directory is the repository root.

### Local CLI
```bash
# Windows
generator\exeMain.cmd

# Linux / macOS
bash generator/exeMain.sh

# Direct
uv run python generator/main.py --n_users 100 --use_random_seed 1 --n_itr 1
```

Output is written to:
- `data/RandomTelecomPayments.csv` — transaction-level dataset
- `data/RandomTelecomUsers.parquet` — user-level intermediate dataset

### Local FastAPI Server
```bash
# Windows
generator\exeApi.cmd

# Linux / macOS
bash generator/exeApi.sh

# Direct
uv run fastapi run generator/api.py
```

Endpoints available at `http://localhost:8000/docs`:

| Method | Path | Description |
|---|---|---|
| GET | `/api` | Generate data via query string parameters |
| POST | `/api` | Generate data via JSON request body |

### Docker
```bash
# Pull latest image
docker pull oislen/randomtelecompayments:latest

# Run CLI
docker run --name rtp oislen/randomtelecompayments:latest --n_users 1000 --use_random_seed 1 --n_itr 2

# Extract generated CSV
docker cp rtp:/home/user/RandomTelecomPayments/data/RandomTelecomPayments.csv ~/Downloads/

# Run FastAPI server
docker run --name rtp --publish 8000:8000 --entrypoint uv --rm oislen/randomtelecompayments:latest run fastapi run generator/api.py
```

---

## Application Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `n_users` | int | 100 | Number of users to generate |
| `use_random_seed` | int (0/1) | 0 | Fixed random seed for reproducible results (1 = enabled) |
| `n_itr` | int | 1 | Number of parallel data generation batches |
| `n_applications` | int | 20000 | Number of applications to generate |
| `registration_start_date` | str (YYYY-MM-DD) | 2 years ago | Start date for user registrations |
| `registration_end_date` | str (YYYY-MM-DD) | 1 year ago | End date for user registrations |
| `transaction_start_date` | str (YYYY-MM-DD) | 1 year ago | Start date for transactions |
| `transaction_end_date` | str (YYYY-MM-DD) | today | End date for transactions |

All defaults are defined in `generator/cons.py`.

---

## Running Unit Tests

```bash
# Windows
generator\exeUnittests.cmd

# Linux / macOS
bash generator/exeUnittests.sh

# Direct (from repository root)
uv run python -m unittest discover generator/unittests/utilities
uv run python -m unittest discover generator/unittests/objects
uv run python -m unittest discover generator/unittests/app
```

Unit tests run automatically on every pull request and push to `main` via GitHub Actions.

---

## Data Model

**Entities:** `User`, `Device`, `IP`, `Card`, `Application`, `Transaction`

**Entity relationship diagram:** `doc/entity_relationship_diagram.jpg`

**Data dictionary:** `doc/data_dictionary.csv`

**Output columns (in order):**

| Group | Columns |
|---|---|
| User | `userid`, `first_name`, `last_name`, `registration_date`, `registration_country_code`, `uid`, `email_domain` |
| Device | `device_hash`, `device_type` |
| Card | `card_hash`, `card_type`, `card_country_code` |
| IP | `ip_hash`, `ip_country_code` |
| Application | `application_hash` |
| Transaction | `transaction_hash`, `transaction_date`, `transaction_amount`, `transaction_payment_method`, `card_payment_channel`, `transaction_status`, `transaction_error_code` |
| Iteration | `itr_hash` |

---

## Key Modules and Entry Points

| File | Purpose |
|---|---|
| `generator/main.py` | CLI entry point; calls `input_error_handling` then `main()` |
| `generator/api.py` | FastAPI app; GET and POST `/api` both delegate to `main()` |
| `generator/cons.py` | Single source of truth for all file paths, defaults, and data model constants |
| `generator/app/ProgrammeParams.py` | Validates and stores all programme parameters; computes `transaction_timescale` |
| `generator/app/gen_random_telecom_data.py` | Seeds RNG, instantiates all entity objects, calls `gen_user_data` and `gen_trans_data` |
| `generator/app/gen_user_data.py` | Builds user-level DataFrame by joining entity attribute dicts |
| `generator/app/gen_trans_data.py` | Explodes user data to transaction level; applies country alignment, QA, status/error generation |
| `generator/objects/` | One class per entity type; each generates hashes, counts, and attribute mappings |
| `generator/utilities/` | Stateless helper functions; imported by app and objects |
| `generator/qa/` | Post-generation assertion checks; called at end of `main()` |
| `generator/batch/gen_bedrock_data.py` | Standalone script to regenerate AI reference data via AWS Bedrock |

---

## Coding Conventions

- **Runtime type checking:** `beartype` decorators on all public functions and `__init__` methods — never remove these
- **Constants:** all file paths, model parameters, and defaults live in `generator/cons.py`; do not hardcode paths or magic numbers in source files
- **Entity pattern:** new entity types follow the pattern in `generator/objects/` — a class with `__init__` generating hash dicts, a `gen_*` method for each attribute, and `beartype` annotations
- **Utilities:** new helper functions go in `generator/utilities/`; they must be stateless and independently testable
- **Docstrings:** NumPy style with `Parameters` and `Returns` sections on all public functions and classes
- **Test coverage:** every new function or class requires a corresponding test file under `generator/unittests/` mirroring the source directory (`app/`, `objects/`, `utilities/`)
- **Test constants:** use `cons.unittest_seed`, `cons.unittest_n_users`, `cons.unittest_n_entities`, and the `cons.unittest_*_date` constants — never hardcode seed values or counts in test files
- **Column order:** output DataFrames must follow the column order defined by `cons.user_cols + cons.device_cols + cons.card_cols + cons.ip_cols + cons.app_cols + cons.trans_cols + cons.itr_cols`

---

## Common Tasks for AI Agents

### Adding a new output column
1. Update the relevant entity class in `generator/objects/` to generate the new attribute
2. Add the column name to the appropriate list in `generator/cons.py` (`user_cols`, `device_cols`, etc.)
3. Update `generator/app/gen_user_data.py` or `generator/app/gen_trans_data.py` to join the new attribute
4. Update `doc/data_dictionary.csv` with the new column definition
5. Update the corresponding unit test file in `generator/unittests/objects/` and `generator/unittests/app/`

### Changing a default parameter
1. Edit the `default_*` constant in `generator/cons.py`
2. Update the Application Parameters table in `README.md`
3. Update the Application Parameters table in `CLAUDE.md`

### Adding a new utility function
1. Create the function in `generator/utilities/` with a `beartype` decorator and NumPy docstring
2. Import it in the consuming module
3. Create a test file `generator/unittests/utilities/test_<function_name>.py`

### Regenerating reference data (names, email domains)
```bash
uv run python generator/batch/gen_bedrock_data.py --data_point first_names --run_bedrock
uv run python generator/batch/gen_bedrock_data.py --data_point last_names --run_bedrock
uv run python generator/batch/gen_bedrock_data.py --data_point email_domains --run_bedrock
```
Requires AWS credentials in `.creds/sessionToken.json`.

### Rebuilding the Docker image
```bash
docker build -t oislen/randomtelecompayments:latest .
```

### Running QA checks manually
QA checks run automatically at the end of `main()`. To run them standalone:
```python
import qa
qa.Uids(data=trans_data).run_all()
qa.Transactions(data=trans_data).run_all()
qa.Cards(data=trans_data).run_all()
qa.Ips(data=trans_data).run_all()
```

---

## CI/CD

| Workflow | Trigger | Jobs |
|---|---|---|
| `dev-pull-requests.yml` | Pull request → `dev` or `main` | Trivy filesystem security scan; Python unit tests |
| `deploy-main-push.yml` | Push → `main` | Release tag; Trivy filesystem scan; Python unit tests; Docker Hub image build and push; Trivy image scan |
