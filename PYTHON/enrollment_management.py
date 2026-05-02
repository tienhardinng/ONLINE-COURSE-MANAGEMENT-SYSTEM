# ============================================================
# enrollment_management.py
# Quan ly Dang Ky Hoc & Tien Do
# [DA THEM] get_all_enrollments()
# [DA THEM] get_enrollment_by_id()
# [DA THEM] delete_enrollment()
# [DA THEM] get_learners_by_course()
# ============================================================

from db_connection import get_connection, close_connection


# ── CREATE ────────────────────────────────────────────────────
def enroll_learner(learner_id: int, course_id: int):
    """
    Dang ky hoc vien vao khoa hoc thong qua Stored Procedure.
    SP se kiem tra trung lap tu dong.
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        # Goi stored procedure sp_EnrollLearner
        args = (learner_id, course_id, '')
        result_args = cursor.callproc('sp_EnrollLearner', args)
        conn.commit()
        # Lay OUT parameter (vi tri thu 3)
        msg = result_args[2] if result_args[2] else 'Da xu ly.'
        print(f"  [KET QUA] {msg}")
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
    finally:
        close_connection(conn, cursor)


# ── READ ──────────────────────────────────────────────────────
def get_all_enrollments() -> list:
    """[DA THEM] Lay toan bo dang ky kem ten hoc vien va khoa hoc."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                e.EnrollmentID,
                l.LearnerID,
                l.LearnerName,
                c.CourseID,
                c.CourseName,
                e.EnrollmentDate,
                e.Status
            FROM Enrollments e
            JOIN Learners l ON e.LearnerID = l.LearnerID
            JOIN Courses  c ON e.CourseID  = c.CourseID
            ORDER BY e.EnrollmentDate DESC, e.EnrollmentID DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"  [LOI] {e}")
        return []
    finally:
        close_connection(conn, cursor)


def get_enrollment_by_id(enrollment_id: int) -> dict | None:
    """[DA THEM] Lay thong tin mot dong dang ky theo EnrollmentID."""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT e.*, l.LearnerName, c.CourseName
            FROM Enrollments e
            JOIN Learners l ON e.LearnerID = l.LearnerID
            JOIN Courses  c ON e.CourseID  = c.CourseID
            WHERE e.EnrollmentID = %s
        """, (enrollment_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"  [LOI] {e}")
        return None
    finally:
        close_connection(conn, cursor)


def get_learner_courses(learner_id: int) -> list:
    """Lay danh sach khoa hoc cua mot hoc vien."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                c.CourseID,
                c.CourseName,
                i.InstructorName,
                e.EnrollmentDate,
                e.Status
            FROM Enrollments e
            JOIN Courses     c ON e.CourseID     = c.CourseID
            JOIN Instructors i ON c.InstructorID = i.InstructorID
            WHERE e.LearnerID = %s
            ORDER BY e.EnrollmentDate DESC
        """, (learner_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"  [LOI] {e}")
        return []
    finally:
        close_connection(conn, cursor)


def get_learners_by_course(course_id: int) -> list:
    """[DA THEM] Lay danh sach hoc vien da dang ky mot khoa hoc."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                l.LearnerID,
                l.LearnerName,
                l.Email,
                e.EnrollmentDate,
                e.Status
            FROM Enrollments e
            JOIN Learners l ON e.LearnerID = l.LearnerID
            WHERE e.CourseID = %s
            ORDER BY e.EnrollmentDate
        """, (course_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"  [LOI] {e}")
        return []
    finally:
        close_connection(conn, cursor)


# ── UPDATE ────────────────────────────────────────────────────
def update_enrollment_status(learner_id: int, course_id: int,
                               new_status: str):
    """Cap nhat trang thai dang ky (Active / Completed / Dropped)."""
    valid = ('Active', 'Completed', 'Dropped')
    if new_status not in valid:
        print(f"  [!] Trang thai khong hop le. Chon: {valid}")
        return False
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.callproc('sp_UpdateEnrollmentStatus',
                        [learner_id, course_id, new_status])
        conn.commit()
        print(f"  [OK] Cap nhat trang thai -> '{new_status}' thanh cong.")
        return True
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)


# ── DELETE ────────────────────────────────────────────────────
def delete_enrollment(learner_id: int, course_id: int):
    """[DA THEM] Huy dang ky (xoa dong trong bang Enrollments)."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM Enrollments
            WHERE LearnerID = %s AND CourseID = %s
        """, (learner_id, course_id))
        conn.commit()
        if cursor.rowcount:
            print(f"  [OK] Da huy dang ky hoc vien {learner_id} khoi khoa {course_id}.")
            return True
        else:
            print("  [!] Khong tim thay dang ky tuong ung.")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)