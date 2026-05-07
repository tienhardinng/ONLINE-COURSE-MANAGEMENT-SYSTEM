# ============================================================
#  backup_recovery.py
#  Backup & Recovery tool for OnlineCourseDB
#  Compatible with Windows, macOS, Linux
#
#  Usage:
#    python backup_recovery.py backup    -> create a new backup
#    python backup_recovery.py restore   -> restore latest backup
#    python backup_recovery.py list      -> list all backups
# ============================================================

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# ── CONFIG ───────────────────────────────────────────────────
DB_USER    = "root"
DB_PASS    = "123456"
DB_NAME    = "OnlineCourseDB"
BACKUP_DIR = Path("./backups")
MAX_KEEP   = 30   # keep only the 30 most recent backups

# Adjust these paths if mysqldump/mysql are not on PATH
MYSQLDUMP  = "mysqldump"
MYSQL      = "mysql"

# ── HELPERS ──────────────────────────────────────────────────
def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

def separator(title=""):
    width = 60
    if title:
        pad = (width - len(title) - 2) // 2
        print("=" * pad + f" {title} " + "=" * pad)
    else:
        print("=" * width)

# ── BACKUP ───────────────────────────────────────────────────
def do_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{DB_NAME}_{ts}.sql"
    filepath = BACKUP_DIR / filename

    log(f"Starting backup -> {filepath}")

    cmd = [
        MYSQLDUMP,
        f"-u{DB_USER}",
        f"-p{DB_PASS}",
        "--single-transaction",
        "--routines",
        "--triggers",
        "--events",
        DB_NAME,
    ]

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            log(f"ERROR: {result.stderr.strip()}")
            filepath.unlink(missing_ok=True)
            return

        size_kb = filepath.stat().st_size // 1024
        log(f"Backup completed: {filename}  ({size_kb} KB)")

        # Prune old backups
        backups = sorted(BACKUP_DIR.glob("backup_*.sql"), key=os.path.getmtime, reverse=True)
        for old in backups[MAX_KEEP:]:
            old.unlink()
            log(f"Pruned old backup: {old.name}")

    except FileNotFoundError:
        log("ERROR: 'mysqldump' not found. Make sure MySQL bin folder is on PATH.")
        log("  Windows tip: Add  C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin  to PATH")

# ── RESTORE ──────────────────────────────────────────────────
def do_restore():
    backups = sorted(BACKUP_DIR.glob("backup_*.sql"), key=os.path.getmtime, reverse=True)

    if not backups:
        log(f"ERROR: No backup files found in '{BACKUP_DIR}'")
        return

    latest = backups[0]
    log(f"Latest backup found: {latest.name}")

    confirm = input("  Are you sure? This will OVERWRITE the current database. (yes/no): ")
    if confirm.strip().lower() != "yes":
        log("Restore cancelled.")
        return

    log(f"Restoring from: {latest}")

    cmd = [
        MYSQL,
        f"-u{DB_USER}",
        f"-p{DB_PASS}",
        DB_NAME,
    ]

    try:
        with open(latest, "r", encoding="utf-8") as f:
            result = subprocess.run(cmd, stdin=f, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            log(f"ERROR: {result.stderr.strip()}")
        else:
            log(f"Restore completed successfully from {latest.name}")

    except FileNotFoundError:
        log("ERROR: 'mysql' not found. Make sure MySQL bin folder is on PATH.")

# ── LIST ─────────────────────────────────────────────────────
def do_list():
    backups = sorted(BACKUP_DIR.glob("backup_*.sql"), key=os.path.getmtime, reverse=True)

    separator("AVAILABLE BACKUPS")
    if not backups:
        print(f"  (no backups found in '{BACKUP_DIR}')")
    else:
        print(f"  {'#':<4} {'Filename':<45} {'Size':>8}")
        print("  " + "-" * 58)
        for i, f in enumerate(backups, 1):
            size_kb = f.stat().st_size // 1024
            print(f"  {i:<4} {f.name:<45} {size_kb:>5} KB")
    separator()

# ── MAIN ─────────────────────────────────────────────────────
def main():
    commands = {
        "backup":  do_backup,
        "restore": do_restore,
        "list":    do_list,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print()
        separator("OnlineCourseDB Backup & Recovery Tool")
        print("  Usage:")
        print("    python backup_recovery.py backup    # create new backup")
        print("    python backup_recovery.py restore   # restore latest backup")
        print("    python backup_recovery.py list      # list all backups")
        separator()
        return

    commands[sys.argv[1]]()

if __name__ == "__main__":
    main()