# ============================================================
# reports.py
# ============================================================

from db_connection import get_connection, close_connection


# ── 1. TONG QUAN KHOA HOC ─────────────────────────────────────
def report_active_courses():
    """
    Thong ke tong quan tat ca khoa hoc:
    ten, giang vien, so bai giang, so hoc vien.
    Su dung View: vw_CourseSummary
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM vw_CourseSummary
            ORDER BY TotalLearners DESC
        """)
        rows = cursor.fetchall()
        if not rows:
            print("  Chua co du lieu khoa hoc.")
            return
        print("\n" + "="*72)
        print(f"{'TONG QUAN KHOA HOC':^72}")
        print("="*72)
        print(f"  {'#':<4} {'Ten Khoa Hoc':<28} {'Giang Vien':<20} "
              f"{'Bai Giang':>9} {'Hoc Vien':>8}")
        print("  " + "-"*68)
        for i, r in enumerate(rows, 1):
            print(f"  {i:<4} {r['CourseName']:<28} {r['InstructorName']:<20} "
                  f"{r['TotalLectures']:>9} {r['TotalLearners']:>8}")
        print("="*72)
        print(f"  Tong cong: {len(rows)} khoa hoc")
    except Exception as e:
        print(f"  [LOI] {e}")
    finally:
        close_connection(conn, cursor)


# ── 2. KHOI LUONG GIANG VIEN ──────────────────────────────────
def report_instructor_workload():
    """
    Bao cao khoi luong giang day:
    ten giang vien, chuyen mon, so khoa, tong hoc vien.
    Su dung View: vw_InstructorWorkload
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM vw_InstructorWorkload
            ORDER BY TotalCourses DESC, TotalStudentsEnrolled DESC
        """)
        rows = cursor.fetchall()
        if not rows:
            print("  Chua co du lieu giang vien.")
            return
        print("\n" + "="*72)
        print(f"{'KHOI LUONG GIANG DAY THEO GIANG VIEN':^72}")
        print("="*72)
        print(f"  {'Ten Giang Vien':<22} {'Chuyen Mon':<22} "
              f"{'So Khoa':>7} {'Hoc Vien':>8}")
        print("  " + "-"*62)
        for r in rows:
            print(f"  {r['InstructorName']:<22} {r['Expertise'] or 'N/A':<22} "
                  f"{r['TotalCourses']:>7} {r['TotalStudentsEnrolled']:>8}")
        print("="*72)
    except Exception as e:
        print(f"  [LOI] {e}")
    finally:
        close_connection(conn, cursor)


# ── 3. TIEN DO HOC VIEN ───────────────────────────────────────
def report_learner_progress(learner_id: int):
    """
    Bao cao tien do hoc tap chi tiet cua mot hoc vien.
    Su dung Function: fn_LearnerCompletionPct()
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        # Lay thong tin hoc vien
        cursor.execute(
            "SELECT LearnerName, Email FROM Learners WHERE LearnerID = %s",
            (learner_id,)
        )
        learner = cursor.fetchone()
        if not learner:
            print(f"  [!] Khong tim thay hoc vien ID={learner_id}.")
            return

        # Lay chi tiet dang ky + % hoan thanh
        cursor.execute("""
            SELECT
                c.CourseID,
                c.CourseName,
                i.InstructorName,
                e.EnrollmentDate,
                e.Status,
                fn_LearnerCompletionPct(e.LearnerID, e.CourseID) AS CompletionPct
            FROM Enrollments e
            JOIN Courses     c ON e.CourseID     = c.CourseID
            JOIN Instructors i ON c.InstructorID = i.InstructorID
            WHERE e.LearnerID = %s
            ORDER BY e.EnrollmentDate
        """, (learner_id,))
        rows = cursor.fetchall()

        print("\n" + "="*70)
        print(f"  HOC VIEN : {learner['LearnerName']}")
        print(f"  EMAIL    : {learner['Email']}")
        print(f"  TONG KHOA: {len(rows)}")
        print("="*70)
        if not rows:
            print("  Hoc vien chua dang ky khoa hoc nao.")
            return
        print(f"  {'Ten Khoa Hoc':<28} {'Giang Vien':<18} "
              f"{'Ngay DK':<12} {'TT':<11} {'%HT':>5}")
        print("  " + "-"*75)
        for r in rows:
            # Thanh tien do truc quan
            pct   = float(r['CompletionPct'])
            bar   = '█' * int(pct / 10) + '░' * (10 - int(pct / 10))
            print(f"  {r['CourseName']:<28} {r['InstructorName']:<18} "
                  f"{str(r['EnrollmentDate']):<12} {r['Status']:<11} "
                  f"{pct:>4.0f}%")
            print(f"  {'':28} [{bar}]")
        print("="*70)

        # Tong ket
        total     = len(rows)
        completed = sum(1 for r in rows if r['Status'] == 'Completed')
        active    = sum(1 for r in rows if r['Status'] == 'Active')
        dropped   = sum(1 for r in rows if r['Status'] == 'Dropped')
        avg_pct   = sum(float(r['CompletionPct']) for r in rows) / total if total else 0
        print(f"  Hoan thanh: {completed}  |  Dang hoc: {active}  "
              f"|  Bo hoc: {dropped}  |  TB hoan thanh: {avg_pct:.1f}%")
    except Exception as e:
        print(f"  [LOI] {e}")
    finally:
        close_connection(conn, cursor)


# ── 4. THONG KE DANG KY [DA THEM] ────────────────────────────
def report_enrollment_statistics():
    """
    [DA THEM] Thong ke so luong dang ky theo trang thai
    (Active / Completed / Dropped) va ty le phan tram.
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                Status,
                COUNT(*) AS SoLuong,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Enrollments), 1) AS TyLe
            FROM Enrollments
            GROUP BY Status
            ORDER BY SoLuong DESC
        """)
        rows = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS Total FROM Enrollments")
        total = cursor.fetchone()['Total']

        print("\n" + "="*48)
        print(f"{'THONG KE DANG KY HOC':^48}")
        print("="*48)
        print(f"  {'Trang Thai':<15} {'So Luong':>10} {'Ty Le':>10}  {'Bieu Do':}")
        print("  " + "-"*44)
        for r in rows:
            bar = '█' * int(float(r['TyLe']) / 5)
            print(f"  {r['Status']:<15} {r['SoLuong']:>10} "
                  f"{str(r['TyLe'])+'%':>10}  {bar}")
        print("  " + "-"*44)
        print(f"  {'TONG CONG':<15} {total:>10}")
        print("="*48)
    except Exception as e:
        print(f"  [LOI] {e}")
    finally:
        close_connection(conn, cursor)


# ── 5. TOP KHOA HOC [DA THEM] ─────────────────────────────────
def report_top_courses():
    """
    [DA THEM] Top 5 khoa hoc co nhieu hoc vien dang ky nhat.
    Hien thi so hoan thanh, dang hoc, ty le hoan thanh.
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                c.CourseID,
                c.CourseName,
                i.InstructorName,
                COUNT(e.LearnerID)                                  AS TotalLearners,
                COALESCE(SUM(e.Status = 'Completed'), 0)            AS Completed,
                COALESCE(SUM(e.Status = 'Active'),    0)            AS Active,
                COALESCE(SUM(e.Status = 'Dropped'),   0)            AS Dropped,
                ROUND(
                    COALESCE(SUM(e.Status = 'Completed'), 0)
                    * 100.0 / NULLIF(COUNT(e.LearnerID), 0), 1
                ) AS CompletionRate
            FROM Courses c
            LEFT JOIN Enrollments e  ON c.CourseID     = e.CourseID
            LEFT JOIN Instructors i  ON c.InstructorID = i.InstructorID
            GROUP BY c.CourseID, c.CourseName, i.InstructorName
            ORDER BY TotalLearners DESC
            LIMIT 5
        """)
        rows = cursor.fetchall()
        print("\n" + "="*72)
        print(f"{'TOP 5 KHOA HOC NHIEU HOC VIEN NHAT':^72}")
        print("="*72)
        print(f"  {'#':<3} {'Ten Khoa Hoc':<26} {'Giang Vien':<18} "
              f"{'Tong':>5} {'HT':>5} {'DH':>5} {'BH':>5} {'TL%':>6}")
        print("  " + "-"*70)
        for i, r in enumerate(rows, 1):
            rate = r['CompletionRate'] if r['CompletionRate'] else 0
            print(f"  {i:<3} {r['CourseName']:<26} {r['InstructorName']:<18} "
                  f"{r['TotalLearners']:>5} {r['Completed']:>5} "
                  f"{r['Active']:>5} {r['Dropped']:>5} {rate:>5.1f}%")
        print("="*72)
        print("  HT=Hoan Thanh | DH=Dang Hoc | BH=Bo Hoc | TL%=Ty Le HT")
    except Exception as e:
        print(f"  [LOI] {e}")
    finally:
        close_connection(conn, cursor)