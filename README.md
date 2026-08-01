A modular CLI Security & Hardware Operations Toolkit
# VaultOps

A modular CLI Security & Hardware Operations Toolkit.

VaultOps is a simple command-line password manager that securely stores credentials in an encrypted JSON file using **Fernet** encryption.

---

## Features

* Store credentials securely
* Encrypt passwords with `cryptography`
* List saved credentials
* Filter credentials by service
* Delete credentials
* Simple command-line interface
* Logging support
* Fully tested with `pytest`

---

## Requirements

* Python 3.13+
* pip

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd vaultops
```

### Install the project

```bash
pip install -e .
```

---

## Usage

### Add a credential

```bash
vaultops add \
    --entry-id cred-001 \
    --service-name github \
    --username alice \
    --password mypassword
```

Example:

```bash
vaultops add \
    --entry-id cred-001 \
    --service-name github \
    --username ali \
    --password hunter22
```

---

### List all credentials

```bash
vaultops list
```

Example output:

```text
2026-07-24 12:00:00 [INFO] vaultops: [cred-001] github (ali)
```

---

### Filter by service

```bash
vaultops list --service github
```

---

### Delete a credential

```bash
vaultops delete --entry-id cred-001
```

Example output:

```text
2026-07-24 12:00:00 [INFO] vaultops: Deleted credential: cred-001
```

---

## Project Structure

```text
vaultops/
├── src/
│   └── vaultops/
│       ├── cli.py
│       ├── config.py
│       ├── exceptions.py
│       ├── logging_config.py
│       ├── models/
│       ├── security/
│       └── storage/
├── tests/
├── pyproject.toml
└── README.md
```

---

## Running Tests

```bash
pytest
```

or

```bash
pytest -v
```

---

## Technologies

* Python
* argparse
* dataclasses
* logging
* pytest
* cryptography
* JSON

---

## License

This project is intended for educational and learning purposes.

You can also improve it later by adding:

* Screenshots or terminal GIFs
* Architecture diagram
* Development roadmap
* Future features (export/import, update command, search, master password, etc.)

