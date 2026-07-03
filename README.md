# NetBox Manager

NetBox Manager is a command-line tool for synchronising data from an Excel workbook into NetBox via the NetBox API.

The aim of this project is to maintain a single Excel workbook as the source of truth and automatically create or update objects in NetBox.

---

# Features

## Current

- ✅ Connect to the NetBox API
- ✅ Read an Excel workbook
- ✅ Import Wall Plates
- ✅ Create new devices
- ✅ Update existing devices
- ✅ Dry-run mode (preview changes without writing)

## Planned

- ⏳ Locations
- ⏳ Patch Panels
- ⏳ Switches
- ⏳ Interfaces
- ⏳ Cables
- ⏳ Racks
- ⏳ Printers
- ⏳ Wireless Access Points
- ⏳ Cameras
- ⏳ Full workbook synchronisation
- ⏳ Validation and reporting

---

# Project Structure

```
netbox-manager/
│
├── data/
│   └── FIX8 Network.xlsx
│
├── netbox_manager/
│   ├── client.py
│   ├── devices.py
│   ├── locations.py
│   ├── main.py
│   └── util.py
│
├── requirements.txt
├── README.md
└── .env
```

---

# Source of Truth

The only source of truth is:

```
data/FIX8 Network.xlsx
```

Each worksheet represents a different NetBox object type.

Current worksheets:

- wallplates

Future worksheets:

- locations
- patchpanels
- switches
- interfaces
- cables
- printers
- wireless
- cameras
- racks

---

# Wall Plates Worksheet

Sheet name:

```
wallplates
```

## Required Columns

| Column |
|---------|
| name |
| device_type |
| location |

## Optional Columns

| Column |
|---------|
| role |
| manufacturer |
| status |
| site |
| description |

If optional fields are left blank the following defaults are used:

| Field | Default |
|-------|---------|
| site | FIX8Group Denton |
| manufacturer | Generic |
| role | Wall Outlet (Network) |
| status | active |

Example:

| name | device_type | location |
|------|-------------|----------|
| TEST/1/G/01 | 2Way-RJ45-Faceplate | Workshop (LL) |

---

# Installation

Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it

```bash
source .venv/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

---

# Configuration

Copy:

```bash
cp .env.example .env
```

Example:

```env
NETBOX_URL=http://192.168.x.x
NETBOX_TOKEN=your_token_here
VERIFY_SSL=false
```

---

# Commands

## Test API

```bash
python -m netbox_manager.main test
```

## Dry Run

```bash
python -m netbox_manager.main sync wallplates --dry-run
```

Shows what would change without modifying NetBox.

## Import

```bash
python -m netbox_manager.main sync wallplates
```

Creates new wall plates and updates existing ones.

---

# Typical Workflow

1. Open **FIX8 Network.xlsx**
2. Edit the Wall Plates worksheet.
3. Save the workbook.
4. Run a Dry Run.
5. Check the output.
6. Run the import.
7. Commit both workbook and code changes to Git.

---

# Development Roadmap

## Milestone 1 ✅

- NetBox API connection
- CLI framework
- Excel workbook support
- Wall Plate synchronisation

## Milestone 2

- Location synchronisation
- Patch Panel synchronisation
- Switch synchronisation

## Milestone 3

- Interfaces
- Cable creation
- Automatic cable routing

## Milestone 4

- IP Addresses
- Prefixes
- VLANs
- Services
- Wireless

---

# Philosophy

This project deliberately avoids NetBox CSV imports.

Instead:

```
Excel Workbook
        ↓
 NetBox Manager
        ↓
   NetBox API
        ↓
    NetBox
```

The workbook is the only data that needs to be maintained.

NetBox Manager handles validation, lookups, defaults and synchronisation automatically.

---

# License

Personal project for managing and synchronising NetBox infrastructure using a workbook-driven workflow.