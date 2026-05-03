# ============================================================
# course_management.py
# ============================================================

from db_connection import get_connection, close_connection


# ══════════════════════════════════════════════════════════════
#  INSTRUCTOR (GIANG VIEN)
# ══════════════════════════════════════════════════════════════

def add_instructor(name: str, expertise: str, email: str):
    """Them giang vien moi."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO Instructors (InstructorName, Expertise, Email)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (name, expertise, email))
        conn.commit()
        print(f"  [OK] Da them giang vien: {name} (ID={cursor.lastrowid})")
        return True
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)


def get_all_instructors() -> list:
    """Lay toan bo danh sach giang vien."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Instructors ORDER BY InstructorID")
        return cursor.fetchall()
    except Exception as e:
        print(f"  [LOI] {e}")
        return []
    finally:
        close_connection(conn, cursor)


def get_instructor_by_id(instructor_id: int) -> dict | None:
    """Lay thong tin mot giang vien theo ID."""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM Instructors WHERE InstructorID = %s", (instructor_id,)
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"  [LOI] {e}")
        return None
    finally:
        close_connection(conn, cursor)


def update_instructor(instructor_id: int, name: str = None,
                       expertise: str = None, email: str = None):
    """[DA THEM] Cap nhat thong tin giang vien."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        updates, values = [], []
        if name:
            updates.append("InstructorName = %s"); values.append(name)
        if expertise:
            updates.append("Expertise = %s");      values.append(expertise)
        if email:
            updates.append("Email = %s");           values.append(email)
        if not updates:
            print("  [!] Khong co truong nao de cap nhat.")
            return False
        values.append(instructor_id)
        sql = f"UPDATE Instructors SET {', '.join(updates)} WHERE InstructorID = %s"
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount:
            print(f"  [OK] Cap nhat giang vien ID={instructor_id} thanh cong.")
            return True
        else:
            print(f"  [!] Khong tim thay giang vien ID={instructor_id}.")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)


def delete_instructor(instructor_id: int):
    """[DA THEM] Xoa giang vien (chi xoa duoc neu khong con day khoa nao)."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Instructors WHERE InstructorID = %s", (instructor_id,)
        )
        conn.commit()
        if cursor.rowcount:
            print(f"  [OK] Da xoa giang vien ID={instructor_id}.")
            return True
        else:
            print(f"  [!] Khong tim thay giang vien ID={instructor_id}.")
            return False
    except Exception as e:
        conn.rollback()
        # Loi khoa ngoai: giang vien dang day khoa hoc
        print(f"  [LOI] Khong the xoa - giang vien dang day khoa hoc. Chi tiet: {e}")
        return False
    finally:
        close_connection(conn, cursor)


# ══════════════════════════════════════════════════════════════
#  COURSE (KHOA HOC)
# ══════════════════════════════════════════════════════════════

def add_course(name: str, description: str, instructor_id: int):
    """Them khoa hoc moi."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO Courses (CourseName, Description, InstructorID)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (name, description, instructor_id))
        conn.commit()
        print(f"  [OK] Da them khoa hoc: {name} (ID={cursor.lastrowid})")
        return True
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)


def get_all_courses() -> list:
    """Lay toan bo danh sach khoa hoc kem ten giang vien."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.CourseID, c.CourseName, c.Description,
                   i.InstructorID, i.InstructorName
            FROM Courses c
            JOIN Instructors i ON c.InstructorID = i.InstructorID
            ORDER BY c.CourseID
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"  [LOI] {e}")
        return []
    finally:
        close_connection(conn, cursor)


def get_course_by_id(course_id: int) -> dict | None:
    """[DA THEM] Lay thong tin mot khoa hoc theo ID."""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.*, i.InstructorName
            FROM Courses c
            JOIN Instructors i ON c.InstructorID = i.InstructorID
            WHERE c.CourseID = %s
        """, (course_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"  [LOI] {e}")
        return None
    finally:
        close_connection(conn, cursor)


def search_course_by_name(keyword: str) -> list:
    """[DA THEM] Tim kiem khoa hoc theo ten."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.CourseID, c.CourseName, c.Description, i.InstructorName
            FROM Courses c
            JOIN Instructors i ON c.InstructorID = i.InstructorID
            WHERE c.CourseName LIKE %s
            ORDER BY c.CourseName
        """, (f"%{keyword}%",))
        return cursor.fetchall()
    except Exception as e:
        print(f"  [LOI] {e}")
        return []
    finally:
        close_connection(conn, cursor)


def update_course(course_id: int, name: str = None,
                   description: str = None, instructor_id: int = None):
    """Cap nhat thong tin khoa hoc."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        updates, values = [], []
        if name:
            updates.append("CourseName = %s");   values.append(name)
        if description:
            updates.append("Description = %s");  values.append(description)
        if instructor_id:
            updates.append("InstructorID = %s"); values.append(instructor_id)
        if not updates:
            print("  [!] Khong co truong nao de cap nhat.")
            return False
        values.append(course_id)
        sql = f"UPDATE Courses SET {', '.join(updates)} WHERE CourseID = %s"
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount:
            print(f"  [OK] Cap nhat khoa hoc ID={course_id} thanh cong.")
            return True
        else:
            print(f"  [!] Khong tim thay khoa hoc ID={course_id}.")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)


def delete_course(course_id: int):
    """[DA THEM] Xoa khoa hoc (bai giang va enrollment se tu dong xoa do CASCADE)."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Courses WHERE CourseID = %s", (course_id,))
        conn.commit()
        if cursor.rowcount:
            print(f"  [OK] Da xoa khoa hoc ID={course_id} (kem bai giang & dang ky).")
            return True
        else:
            print(f"  [!] Khong tim thay khoa hoc ID={course_id}.")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)


# ══════════════════════════════════════════════════════════════
#  LECTURE (BAI GIANG)
# ══════════════════════════════════════════════════════════════

def add_lecture(course_id: int, title: str, content: str):
    """Them bai giang moi vao khoa hoc."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO Lectures (CourseID, Title, Content)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (course_id, title, content))
        conn.commit()
        print(f"  [OK] Da them bai giang: '{title}' (ID={cursor.lastrowid})")
        return True
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)


def get_lectures_by_course(course_id: int) -> list:
    """Lay danh sach bai giang cua mot khoa hoc."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT l.LectureID, l.Title, l.Content, c.CourseName
            FROM Lectures l
            JOIN Courses c ON l.CourseID = c.CourseID
            WHERE l.CourseID = %s
            ORDER BY l.LectureID
        """, (course_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"  [LOI] {e}")
        return []
    finally:
        close_connection(conn, cursor)


def update_lecture(lecture_id: int, title: str = None, content: str = None):
    """[DA THEM] Cap nhat tieu de hoac noi dung bai giang."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        updates, values = [], []
        if title:
            updates.append("Title = %s");   values.append(title)
        if content:
            updates.append("Content = %s"); values.append(content)
        if not updates:
            print("  [!] Khong co truong nao de cap nhat.")
            return False
        values.append(lecture_id)
        sql = f"UPDATE Lectures SET {', '.join(updates)} WHERE LectureID = %s"
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount:
            print(f"  [OK] Cap nhat bai giang ID={lecture_id} thanh cong.")
            return True
        else:
            print(f"  [!] Khong tim thay bai giang ID={lecture_id}.")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)


def delete_lecture(lecture_id: int):
    """[DA THEM] Xoa mot bai giang."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Lectures WHERE LectureID = %s", (lecture_id,))
        conn.commit()
        if cursor.rowcount:
            print(f"  [OK] Da xoa bai giang ID={lecture_id}.")
            return True
        else:
            print(f"  [!] Khong tim thay bai giang ID={lecture_id}.")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [LOI] {e}")
        return False
    finally:
        close_connection(conn, cursor)