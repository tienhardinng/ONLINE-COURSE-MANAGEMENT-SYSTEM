# 📚 Online Course Management System — Project 04

> **Course:** Introduction to Database · National Economics University – College of Technology
> **DBMS:** MySQL 8.0 · **Language:** Python 3 · **Tools:** MySQL Workbench, VS Code

---

## 🔗 Quick Links

| Resource | Link |
|---|---|
| GitHub Repository | https://github.com/tienhardinng/ONLINE-COURSE-MANAGEMENT-SYSTEM |
| Demo Video | *(YouTube link)* |

---

## 📋 Table of Contents

1. [Project Structure](#1-project-structure)
2. [Requirements & Setup](#2-requirements--setup)
3. [How to Run](#3-how-to-run)
4. [Backup & Recovery](#4-backup--recovery)
5. [Query Optimization (EXPLAIN)](#5-query-optimization-explain)
6. [Database Design](#6-database-design)
7. [Advanced SQL Features](#7-advanced-sql-features)
8. [Python Modules](#8-python-modules)

---

## 1. Project Structure

```
ONLINE_COURSE_PROJECT/
│
├── sql/
│   ├── 01_schema.sql              # Tables & constraints
│   ├── 02_sample_data.sql         # 10 rows per table
│   ├── 03_indexes.sql             # Performance indexes
│   ├── 04_views.sql               # 3 views
│   ├── 05_stored_procedures.sql   # 3 stored procedures
│   ├── 06_functions.sql           # 2 user-defined functions
│   ├── 07_triggers.sql            # 3 triggers + audit log
│   └── 08_security.sql            # User accounts & GRANT
│
├── python/
│   ├── db_connection.py
│   ├── learner_management.py
│   ├── course_management.py
│   ├── enrollment_management.py
│   ├── reports.py
│   ├── main.py
│   ├── backup_recovery.py         # ← Backup & Recovery tool
│   └── query_optimization.py     # ← EXPLAIN demo
│
└── README.md
```

---

## 2. Requirements & Setup

**Software:** Python >= 3.10, MySQL Server >= 8.0, MySQL Workbench, VS Code

**Python library:**
```bash
pip install mysql-connector-python
```

**Add MySQL to PATH** (Windows — run once in PowerShell):
```powershell
$env:PATH += ";C:\Program Files\MySQL\MySQL Server 8.0\bin"
```

Verify:
```powershell
mysqldump --version
mysql --version
```

---

## 3. How to Run

### Step 1 — Set up database (MySQL Workbench)

Execute SQL files **in order**:
```
01_schema.sql → 02_sample_data.sql → 03_indexes.sql → 04_views.sql
→ 05_stored_procedures.sql → 06_functions.sql → 07_triggers.sql → 08_security.sql
```

### Step 2 — Configure connection

Edit `db_connection.py`:
```python
DB_CONFIG = {
    'host':     'localhost',
    'port':     3306,
    'database': 'OnlineCourseDB',
    'user':     'root',
    'password': '123456',   # ← change if needed
}
```

### Step 3 — Run the application
```bash
cd python
python main.py
```

---

## 4. Backup & Recovery

File: `python/backup_recovery.py`

This tool uses `mysqldump` to export the entire database to a timestamped `.sql` file,
and can restore from the latest backup with a single command.

### Commands

```powershell
# Create a new backup  →  saved to ./backups/backup_OnlineCourseDB_YYYYMMDD_HHMMSS.sql
python backup_recovery.py backup

# List all available backups
python backup_recovery.py list

# Restore from the most recent backup  (will prompt for confirmation)
python backup_recovery.py restore
```

### How it works

| Operation | Tool used | What it does |
|---|---|---|
| `backup` | `mysqldump` | Exports all tables, routines, triggers to a `.sql` file |
| `restore` | `mysql` | Re-runs the `.sql` file to rebuild the database |
| Auto-prune | Python `pathlib` | Keeps only the 30 most recent backups |

### Example output

```
[2026-05-08 03:00:00] Starting backup -> ./backups/backup_OnlineCourseDB_20260508_030000.sql
[2026-05-08 03:00:01] Backup completed: backup_OnlineCourseDB_20260508_030000.sql  (48 KB)
```

### Production recommendation

Schedule automatic daily backups using Windows Task Scheduler:
```
Action: python C:\path\to\backup_recovery.py backup
Trigger: Daily at 02:00 AM
```

---

## 5. Query Optimization (EXPLAIN)

File: `python/query_optimization.py`

Runs `EXPLAIN` on all high-frequency queries in the system to verify that MySQL
is using indexes rather than performing full table scans.

### Run

```powershell
cd python
python query_optimization.py
```

### What it checks

| Query | Index verified |
|---|---|
| Search courses by name | `idx_course_name` |
| Get enrollments by learner | `idx_enrollment_learner` |
| Get learners in a course | `idx_enrollment_course` |
| Find instructor by email | `idx_instructor_email` |
| Query `vw_CourseSummary` | composite join |
| `fn_LearnerCompletionPct` across all enrollments | UDF + index |

### How to read the output

```
  table        type    key                      rows
  Enrollments  ref     idx_enrollment_learner   3      ← index used ✓
  Courses      eq_ref  PRIMARY                  1      ← index used ✓
```

- **`type = ref` or `eq_ref`** → index is being used efficiently
- **`type = ALL`** → full table scan, no index → needs attention
- **`key = NULL`** → no index used on that table

---

## 6. Database Design

### Entity-Relationship Overview

```
Instructors ──(1:N)── Courses ──(1:N)── Lectures
                          │
                        (N:M)
                          │
                     Enrollments ──(N:1)── Learners
                          │
                  EnrollmentAuditLog  ← written by Triggers
```

> `EnrollmentAuditLog` has no foreign keys by design — audit logs must survive
> even after the original enrollment is deleted.

### Tables

| Table | Primary Key | Description |
|---|---|---|
| `Learners` | LearnerID | Learner profiles |
| `Instructors` | InstructorID | Instructor profiles |
| `Courses` | CourseID | Course information |
| `Lectures` | LectureID | Lecture content |
| `Enrollments` | EnrollmentID | Learner–course registration |
| `EnrollmentAuditLog` | LogID | Audit trail |

---

## 7. Advanced SQL Features

### Indexes (03_indexes.sql)

| Index | Table | Purpose |
|---|---|---|
| `idx_course_name` | Courses | Name search |
| `idx_enrollment_learner` | Enrollments | Queries by learner |
| `idx_enrollment_course` | Enrollments | Queries by course |
| `idx_lecture_course` | Lectures | Lecture lookups |
| `idx_instructor_email` | Instructors | Email lookups |

### Views (04_views.sql)

| View | Description |
|---|---|
| `vw_LearnerEnrollments` | Enrolled courses per learner with status |
| `vw_InstructorWorkload` | Course count and student count per instructor |
| `vw_CourseSummary` | Lecture count and learner count per course |

### Stored Procedures (05_stored_procedures.sql)

| Procedure | Description |
|---|---|
| `sp_EnrollLearner` | Enroll learner; blocks duplicate via OUT message |
| `sp_CourseCompletionSummary` | Completion stats for a given course |
| `sp_UpdateEnrollmentStatus` | Safe status update with validation |

### User-Defined Functions (06_functions.sql)

| Function | Returns | Description |
|---|---|---|
| `fn_LearnerCompletionPct` | DECIMAL(5,2) | Completion % for a learner in a course |
| `fn_TotalLectures` | INT | Total lectures in a course |

### Triggers (07_triggers.sql)

| Trigger | Event | Description |
|---|---|---|
| `trg_AfterEnrollInsert` | AFTER INSERT | Logs new enrollment |
| `trg_AfterEnrollUpdate` | AFTER UPDATE | Logs status change |
| `trg_BeforeEnrollDelete` | BEFORE DELETE | Logs deletion before it happens |

### Security (08_security.sql)

| User | Permissions | Purpose |
|---|---|---|
| `admin_user` | ALL PRIVILEGES | Full administration |
| `instructor_user` | SELECT on courses, lectures, enrollments | Read-only |
| `learner_user` | SELECT on courses, lectures, enrollment view | Read-only |

---

## 8. Python Modules

| Module | Key functions |
|---|---|
| `db_connection.py` | `get_connection()`, `close_connection()` |
| `learner_management.py` | `add_learner()`, `get_all_learners()`, `search_learner_by_name()`, `update_learner()`, `delete_learner()` |
| `course_management.py` | Full CRUD for instructors, courses, and lectures |
| `enrollment_management.py` | `enroll_learner()`, `get_all_enrollments()`, `update_enrollment_status()`, `delete_enrollment()` |
| `reports.py` | `report_active_courses()`, `report_instructor_workload()`, `report_learner_progress()`, `report_enrollment_statistics()`, `report_top_courses()` |
| `main.py` | CLI menu — entry point |
| `backup_recovery.py` | `backup` / `restore` / `list` commands |
| `query_optimization.py` | EXPLAIN analysis for all key queries |

---

> \[NEW\] marks functions added beyond the minimum project requirements