# 📚 PROJECT 04: Online Course Management System

> **Course:** Introduction to Database
> **University:** National Economics University – College of Technology
> **DBMS:** MySQL | **Language:** Python 3
> **Tools:** MySQL Workbench · VS Code

---

## 📋 Table of Contents

1. [Overview](#1-overview)
2. [Project Structure](#2-project-structure)
3. [Requirements](#3-requirements)
4. [Getting Started](#4-getting-started)
5. [Database Design](#5-database-design)
6. [Python Application](#6-python-application)
7. [Advanced SQL Features](#7-advanced-sql-features)
8. [Demo Output](#8-demo-output)
9. [References](#9-references)

---

## 1. Overview

A database-driven online course management system that supports efficient organization of courses, instructors, students, and learning materials, enabling flexible and interactive digital learning.

**Key capabilities:**

- Full CRUD management for **learners**, **instructors**, **courses**, and **lectures**
- Course **enrollment** with duplicate-check via Stored Procedure
- **Progress tracking** per learner with visual completion bars
- Statistics and reporting: course overview, instructor workload, enrollment trends, top courses

---

## 2. Project Structure

```
project04/
│
├── sql/
│   ├── 01_schema.sql              # Create database and all tables
│   ├── 02_sample_data.sql         # Sample data (5–10 rows per table)
│   ├── 03_indexes.sql             # Indexes for query optimization
│   ├── 04_views.sql               # Views for quick data access
│   ├── 05_stored_procedures.sql   # Stored Procedures
│   ├── 06_functions.sql           # User-Defined Functions
│   ├── 07_triggers.sql            # Triggers + Audit Log
│   └── 08_security.sql            # User accounts & access control
│
├── python/
│   ├── db_connection.py           # MySQL connection manager
│   ├── learner_management.py      # Learner CRUD operations
│   ├── course_management.py       # Instructor, Course & Lecture CRUD
│   ├── enrollment_management.py   # Enrollment & progress tracking
│   ├── reports.py                 # Statistics and reporting
│   └── main.py                    # Main CLI interface
│
└── README.md
```

---

## 3. Requirements

### 3.1 Software

| Software | Version | Download |
|---|---|---|
| Python | >= 3.10 | https://python.org |
| MySQL Server | >= 8.0 | https://dev.mysql.com |
| MySQL Workbench | >= 8.0 | https://dev.mysql.com/downloads/workbench |
| VS Code | Latest | https://code.visualstudio.com |

### 3.2 Python Library

Open the VS Code terminal and run:

```bash
pip install mysql-connector-python
```

---

## 4. Getting Started

### Step 1 — Set Up the Database (MySQL Workbench)

Open MySQL Workbench, connect to `root@localhost:3306`, then execute each SQL file **in order**:

```
01_schema.sql  ->  02_sample_data.sql  ->  03_indexes.sql
->  04_views.sql  ->  05_stored_procedures.sql
->  06_functions.sql  ->  07_triggers.sql  ->  08_security.sql
```

> **Warning:** Order matters — later files depend on objects created by earlier ones.

### Step 2 — Verify Connection Settings in `db_connection.py`

```python
DB_CONFIG = {
    'host':     'localhost',
    'port':     3306,
    'database': 'OnlineCourseDB',
    'user':     'root',
    'password': '123456',   # change if your password is different
}
```

### Step 3 — Run the Application

```bash
cd python
python main.py
```

The main menu will appear:

```
╔══════════════════════════════════════════════════╗
║     ONLINE COURSE MANAGEMENT SYSTEM              ║
╠══════════════════════════════════════════════════╣
║   [1]  Learner Management                        ║
║   [2]  Instructor Management                     ║
║   [3]  Course Management                         ║
║   [4]  Lecture Management                        ║
║   [5]  Enrollment & Learning Progress            ║
║   [6]  Reports & Statistics                      ║
║   [0]  Exit                                      ║
╚══════════════════════════════════════════════════╝
```

---

## 5. Database Design

### Entity-Relationship Overview

```
Instructors --(1:N)-- Courses --(1:N)-- Lectures
                          |
                        (N:M)
                          |
                     Enrollments --(N:1)-- Learners
                          |
                  EnrollmentAuditLog  <- (written by Triggers)
```

### Tables

| Table | Description | Primary Key |
|---|---|---|
| `Learners` | Learner profiles | LearnerID |
| `Instructors` | Instructor profiles | InstructorID |
| `Courses` | Course information | CourseID |
| `Lectures` | Lecture content within a course | LectureID |
| `Enrollments` | Learner-course registration | EnrollmentID |
| `EnrollmentAuditLog` | Audit trail for enrollment changes | LogID |

### Relationships

| Relationship | Type | Description |
|---|---|---|
| Instructor -> Courses | 1 : N | One instructor teaches many courses |
| Course -> Lectures | 1 : N | One course contains many lectures |
| Learner <-> Courses | N : M | Resolved through the Enrollments table |

---

## 6. Python Application

### `db_connection.py`

| Function | Description |
|---|---|
| `get_connection()` | Establishes a MySQL connection using mysql-connector-python |
| `close_connection()` | Safely closes cursor and connection |

### `learner_management.py`

| Function | Description |
|---|---|
| `add_learner()` | Add a new learner |
| `get_all_learners()` | Retrieve all learners |
| `get_learner_by_id()` | Get a single learner by ID |
| `search_learner_by_name()` | [NEW] Search learners by name keyword |
| `update_learner()` | Update learner information |
| `delete_learner()` | Delete a learner (cascades to enrollments) |

### `course_management.py`

| Function | Description |
|---|---|
| `add_instructor()` | Add a new instructor |
| `get_all_instructors()` | Retrieve all instructors |
| `get_instructor_by_id()` | Get a single instructor by ID |
| `update_instructor()` | [NEW] Update instructor information |
| `delete_instructor()` | [NEW] Delete an instructor |
| `add_course()` | Add a new course |
| `get_all_courses()` | Retrieve all courses with instructor name |
| `get_course_by_id()` | [NEW] Get a single course by ID |
| `search_course_by_name()` | [NEW] Search courses by name keyword |
| `update_course()` | Update course information |
| `delete_course()` | [NEW] Delete a course (cascades to lectures & enrollments) |
| `add_lecture()` | Add a new lecture to a course |
| `get_lectures_by_course()` | Retrieve all lectures for a course |
| `update_lecture()` | [NEW] Update lecture title or content |
| `delete_lecture()` | [NEW] Delete a lecture |

### `enrollment_management.py`

| Function | Description |
|---|---|
| `enroll_learner()` | Enroll a learner via Stored Procedure (checks duplicates) |
| `get_all_enrollments()` | [NEW] Retrieve all enrollments with learner and course names |
| `get_learner_courses()` | Get all courses a learner is enrolled in |
| `get_learners_by_course()` | [NEW] Get all learners enrolled in a course |
| `update_enrollment_status()` | Update enrollment status via Stored Procedure |
| `delete_enrollment()` | [NEW] Cancel an enrollment |

### `reports.py`

| Function | Description |
|---|---|
| `report_active_courses()` | Overview of all courses: lecture count, learner count |
| `report_instructor_workload()` | Teaching load and student count per instructor |
| `report_learner_progress()` | Detailed progress for one learner with visual bar |
| `report_enrollment_statistics()` | [NEW] Enrollment counts by status with percentage chart |
| `report_top_courses()` | [NEW] Top 5 courses by number of enrolled learners |

---

## 7. Advanced SQL Features

### Indexes

| Name | Table | Purpose |
|---|---|---|
| `idx_course_name` | Courses | Speed up course name searches |
| `idx_enrollment_learner` | Enrollments | Speed up queries by learner |
| `idx_enrollment_course` | Enrollments | Speed up queries by course |
| `idx_lecture_course` | Lectures | Speed up lecture lookups by course |
| `idx_instructor_email` | Instructors | Speed up instructor email lookups |

### Views

| Name | Description |
|---|---|
| `vw_LearnerEnrollments` | Enrolled courses per learner with enrollment date and status |
| `vw_InstructorWorkload` | Course count and total enrolled students per instructor |
| `vw_CourseSummary` | Lecture count and learner count per course |

### Stored Procedures

| Name | Description |
|---|---|
| `sp_EnrollLearner` | Enroll a learner; returns message if already enrolled |
| `sp_CourseCompletionSummary` | Completion summary (total, completed, active, dropped, rate%) |
| `sp_UpdateEnrollmentStatus` | Safely update enrollment status |

### User-Defined Functions

| Name | Returns | Description |
|---|---|---|
| `fn_LearnerCompletionPct` | DECIMAL(5,2) | Completion percentage for a learner in a specific course |
| `fn_TotalLectures` | INT | Total number of lectures in a given course |

### Triggers

| Name | Event | Description |
|---|---|---|
| `trg_AfterEnrollInsert` | AFTER INSERT on Enrollments | Writes an INSERT record to EnrollmentAuditLog |
| `trg_AfterEnrollUpdate` | AFTER UPDATE on Enrollments | Logs status changes (old -> new) |
| `trg_BeforeEnrollDelete` | BEFORE DELETE on Enrollments | Logs deletion before it occurs |

### Security and Access Control

| User | Permissions | Purpose |
|---|---|---|
| `admin_user` | ALL PRIVILEGES | Full database administration |
| `instructor_user` | SELECT on courses, lectures, enrollments | Read-only access for instructors |
| `learner_user` | SELECT on courses, lectures, enrollment view | Read-only access for learners |

---

## 8. Demo Output

### Learner Progress Report

```
======================================================================
  LEARNER  : Tran Minh Anh
  EMAIL    : anh.tran@student.vn
  COURSES  : 2
======================================================================
  Course Name              Instructor       Enrolled    Status       %
  ----------------------------------------------------------------------
  Introduction to Database Nguyen Van An    2024-01-10  Active      50%
                           [|||||.....]
  Python for Beginners     Tran Thi Bich    2024-01-12  Completed  100%
                           [||||||||||]
======================================================================
  Completed: 1  |  Active: 1  |  Dropped: 0  |  Avg. Completion: 75.0%
```

### Enrollment Statistics

```
================================================
       ENROLLMENT STATUS STATISTICS
================================================
  Status           Count      Rate    Chart
  --------------------------------------------
  Completed            4     40.0%    ########
  Active               4     40.0%    ########
  Dropped              2     20.0%    ####
  --------------------------------------------
  TOTAL               10
================================================
```

### Top 5 Courses

```
=======================================================================
            TOP 5 COURSES BY ENROLLMENT
=======================================================================
  #   Course Name              Instructor         Total Done Act Drop Rate%
  -----------------------------------------------------------------------
  1   Introduction to Database Nguyen Van An          2    1   1    0  50.0%
  2   Python for Beginners     Tran Thi Bich           2    2   0    0 100.0%
  ...
=======================================================================
  Done=Completed | Act=Active | Drop=Dropped | Rate%=Completion Rate
```

---

## 9. References

```
[1] MySQL Documentation (2024). MySQL 8.0 Reference Manual.
    https://dev.mysql.com/doc/refman/8.0/en/

[2] Python Software Foundation (2024). Python 3 Documentation.
    https://docs.python.org/3/

[3] MySQL Connector/Python Developer Guide (2024).
    https://dev.mysql.com/doc/connector-python/en/

[4] Ramakrishnan, R., & Gehrke, J. (2002).
    Database Management Systems (3rd ed.). McGraw-Hill.

[5] Silberschatz, A., Korth, H. F., & Sudarshan, S. (2019).
    Database System Concepts (7th ed.). McGraw-Hill.

[6] W3Schools SQL Tutorial (2024).
    https://www.w3schools.com/sql/

[7] MySQL Workbench Manual (2024).
    https://dev.mysql.com/doc/workbench/en/
```

---

> [NEW] = Function added beyond the minimum project requirements