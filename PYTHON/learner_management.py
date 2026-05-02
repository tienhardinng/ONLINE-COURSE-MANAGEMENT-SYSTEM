# ============================================================
# learner_management.py
# Quan ly Hoc Vien - CRUD day du
# [DA THEM] search_learner_by_name()
# [DA THEM] get_learner_by_id()
# ============================================================

from db_connection import get_connection, close_connection


# ── CREATE ────────────────────────────────────────────────────
def add_learner(name: str, email: str, phone: str):
    """Them hoc vien moi vao bang Learners."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO Learners (LearnerName, Email, PhoneNumber)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (name, email, phone))
        conn.commit()
        print(f"  [OK] Da them hoc vien: {name} (ID={cursor.lastrowid})")
        return True
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] Them hoc vien that bai: {e}")
        return False
    finally:
        close_connection(conn, cursor)


# ── READ ──────────────────────────────────────────────────────
def get_all_learners() -> list:
    """Lay toan bo danh sach hoc vien, sap xep theo ID."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Learners ORDER BY LearnerID")
        return cursor.fetchall()
    except Exception as e:
        print(f"  [LOI] {e}")
        return []
    finally:
        close_connection(conn, cursor)


def get_learner_by_id(learner_id: int) -> dict | None:
    """[DA THEM] Lay thong tin mot hoc vien theo ID."""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Learners WHERE LearnerID = %s", (learner_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"  [LOI] {e}")
        return None
    finally:
        close_connection(conn, cursor)


def search_learner_by_name(keyword: str) -> list:
    """[DA THEM] Tim kiem hoc vien theo ten (khong phan biet hoa thuong)."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM Learners WHERE LearnerName LIKE %s ORDER BY LearnerName",
            (f"%{keyword}%",)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"  [LOI] {e}")
        return []
    finally:
        close_connection(conn, cursor)


# ── UPDATE ────────────────────────────────────────────────────
def update_learner(learner_id: int, name: str = None,
                   email: str = None, phone: str = None):
    """Cap nhat thong tin hoc vien (chi update truong duoc truyen vao)."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        updates, values = [], []
        if name:
            updates.append("LearnerName = %s")
            values.append(name)
        if email:
            updates.append("Email = %s")
            values.append(email)
        if phone:
            updates.append("PhoneNumber = %s")
            values.append(phone)
        if not updates:
            print("  [!] Khong co truong nao de cap nhat.")
            return False
        values.append(learner_id)
        sql = f"UPDATE Learners SET {', '.join(updates)} WHERE LearnerID = %s"
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount:
            print(f"  [OK] Cap nhat hoc vien ID={learner_id} thanh cong.")
            return True
        else:
            print(f"  [!] Khong tim thay hoc vien ID={learner_id}.")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)


# ── DELETE ────────────────────────────────────────────────────
def delete_learner(learner_id: int):
    """Xoa hoc vien (cac enrollment lien quan se tu dong xoa do CASCADE)."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Learners WHERE LearnerID = %s", (learner_id,))
        conn.commit()
        if cursor.rowcount:
            print(f"  [OK] Da xoa hoc vien ID={learner_id}.")
            return True
        else:
            print(f"  [!] Khong tim thay hoc vien ID={learner_id}.")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)