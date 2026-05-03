# ============================================================
# main.py
# Online Course Management System
# ============================================================

import os

from learner_management import (
    add_learner, get_all_learners, get_learner_by_id,
    update_learner, delete_learner, search_learner_by_name
)
from course_management import (
    add_instructor, get_all_instructors, get_instructor_by_id,
    update_instructor, delete_instructor,
    add_course, get_all_courses, get_course_by_id,
    update_course, delete_course, search_course_by_name,
    add_lecture, get_lectures_by_course,
    update_lecture, delete_lecture
)
from enrollment_management import (
    enroll_learner, get_all_enrollments, get_learner_courses,
    get_learners_by_course, update_enrollment_status,
    delete_enrollment
)
from reports import (
    report_active_courses, report_instructor_workload,
    report_learner_progress, report_enrollment_statistics,
    report_top_courses
)


# ── TIEN ICH ──────────────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\n  Nhan [Enter] de tiep tuc...")

def input_int(prompt: str) -> int | None:
    """Nhap so nguyen, tra None neu khong hop le."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("  [!] Gia tri phai la so nguyen!")
        return None

def header(title: str):
    print("\n" + "─"*52)
    print(f"  {title}")
    print("─"*52)


# ══════════════════════════════════════════════════════════════
#  MENU CHINH
# ══════════════════════════════════════════════════════════════
def main_menu():
    while True:
        clear()
        print("╔══════════════════════════════════════════════════╗")
        print("║     ONLINE COURSE MANAGEMENT SYSTEM              ║")
        print("║     He Thong Quan Ly Khoa Hoc Truc Tuyen         ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║   [1]  Quan Ly Hoc Vien                          ║")
        print("║   [2]  Quan Ly Giang Vien                        ║")
        print("║   [3]  Quan Ly Khoa Hoc                          ║")
        print("║   [4]  Quan Ly Bai Giang                         ║")
        print("║   [5]  Dang Ky & Tien Do Hoc Tap                 ║")
        print("║   [6]  Bao Cao & Thong Ke                        ║")
        print("║   [0]  Thoat Chuong Trinh                        ║")
        print("╚══════════════════════════════════════════════════╝")
        choice = input("  >> Lua chon: ").strip()

        if   choice == '1': menu_learner()
        elif choice == '2': menu_instructor()
        elif choice == '3': menu_course()
        elif choice == '4': menu_lecture()
        elif choice == '5': menu_enrollment()
        elif choice == '6': menu_report()
        elif choice == '0':
            print("\n  Cam on ban da su dung he thong. Tam biet!\n")
            break
        else:
            print("  [!] Lua chon khong hop le, vui long thu lai.")
            pause()


# ══════════════════════════════════════════════════════════════
#  1. QUAN LY HOC VIEN
# ══════════════════════════════════════════════════════════════
def menu_learner():
    while True:
        clear()
        print("╔══════════════════════════════════════════════════╗")
        print("║            QUAN LY HOC VIEN                      ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║  [1]  Xem danh sach hoc vien                     ║")
        print("║  [2]  Tim kiem hoc vien theo ten                  ║")
        print("║  [3]  Xem thong tin mot hoc vien                  ║")
        print("║  [4]  Them hoc vien moi                           ║")
        print("║  [5]  Cap nhat thong tin hoc vien                 ║")
        print("║  [6]  Xoa hoc vien                                ║")
        print("║  [0]  Quay lai menu chinh                         ║")
        print("╚══════════════════════════════════════════════════╝")
        c = input("  >> Lua chon: ").strip()

        if c == '1':
            header("DANH SACH HOC VIEN")
            rows = get_all_learners()
            if not rows:
                print("  Chua co hoc vien nao trong he thong.")
            else:
                print(f"  {'ID':<6} {'Ho Ten':<25} {'Email':<30} {'So DT':<13}")
                print("  " + "-"*74)
                for r in rows:
                    print(f"  {r['LearnerID']:<6} {r['LearnerName']:<25} "
                          f"{r['Email']:<30} {r['PhoneNumber'] or 'N/A':<13}")
                print(f"\n  Tong: {len(rows)} hoc vien")
            pause()

        elif c == '2':
            header("TIM KIEM HOC VIEN")
            kw = input("  Nhap tu khoa ten: ").strip()
            if kw:
                rows = search_learner_by_name(kw)
                if not rows:
                    print(f"  Khong tim thay hoc vien nao voi tu khoa '{kw}'.")
                else:
                    print(f"  {'ID':<6} {'Ho Ten':<25} {'Email':<30} {'So DT':<13}")
                    print("  " + "-"*74)
                    for r in rows:
                        print(f"  {r['LearnerID']:<6} {r['LearnerName']:<25} "
                              f"{r['Email']:<30} {r['PhoneNumber'] or 'N/A':<13}")
            pause()

        elif c == '3':
            header("THONG TIN HOC VIEN")
            lid = input_int("  Nhap LearnerID: ")
            if lid:
                r = get_learner_by_id(lid)
                if r:
                    print(f"  ID       : {r['LearnerID']}")
                    print(f"  Ho Ten   : {r['LearnerName']}")
                    print(f"  Email    : {r['Email']}")
                    print(f"  So DT    : {r['PhoneNumber'] or 'N/A'}")
                else:
                    print(f"  [!] Khong tim thay hoc vien ID={lid}.")
            pause()

        elif c == '4':
            header("THEM HOC VIEN MOI")
            name  = input("  Ho ten        : ").strip()
            email = input("  Email          : ").strip()
            phone = input("  So dien thoai  : ").strip()
            if name and email:
                add_learner(name, email, phone)
            else:
                print("  [!] Ho ten va Email khong duoc de trong!")
            pause()

        elif c == '5':
            header("CAP NHAT HOC VIEN")
            lid = input_int("  Nhap LearnerID can sua: ")
            if lid:
                r = get_learner_by_id(lid)
                if not r:
                    print(f"  [!] Khong tim thay ID={lid}.")
                else:
                    print(f"  Dang sua: {r['LearnerName']} | {r['Email']}")
                    name  = input("  Ten moi   (Enter giu nguyen): ").strip() or None
                    email = input("  Email moi (Enter giu nguyen): ").strip() or None
                    phone = input("  SDT moi   (Enter giu nguyen): ").strip() or None
                    update_learner(lid, name, email, phone)
            pause()

        elif c == '6':
            header("XOA HOC VIEN")
            lid = input_int("  Nhap LearnerID can xoa: ")
            if lid:
                r = get_learner_by_id(lid)
                if not r:
                    print(f"  [!] Khong tim thay ID={lid}.")
                else:
                    print(f"  Se xoa: {r['LearnerName']} ({r['Email']})")
                    print("  [!] Cac dang ky cua hoc vien nay cung se bi xoa!")
                    cf = input("  Xac nhan xoa? (y/n): ").strip().lower()
                    if cf == 'y':
                        delete_learner(lid)
                    else:
                        print("  Da huy thao tac.")
            pause()

        elif c == '0':
            break


# ══════════════════════════════════════════════════════════════
#  2. QUAN LY GIANG VIEN
# ══════════════════════════════════════════════════════════════
def menu_instructor():
    while True:
        clear()
        print("╔══════════════════════════════════════════════════╗")
        print("║           QUAN LY GIANG VIEN                     ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║  [1]  Xem danh sach giang vien                   ║")
        print("║  [2]  Xem thong tin mot giang vien                ║")
        print("║  [3]  Them giang vien moi                         ║")
        print("║  [4]  Cap nhat thong tin giang vien               ║")
        print("║  [5]  Xoa giang vien                              ║")
        print("║  [0]  Quay lai menu chinh                         ║")
        print("╚══════════════════════════════════════════════════╝")
        c = input("  >> Lua chon: ").strip()

        if c == '1':
            header("DANH SACH GIANG VIEN")
            rows = get_all_instructors()
            if not rows:
                print("  Chua co giang vien nao.")
            else:
                print(f"  {'ID':<6} {'Ho Ten':<24} {'Chuyen Mon':<25} {'Email':<25}")
                print("  " + "-"*80)
                for r in rows:
                    print(f"  {r['InstructorID']:<6} {r['InstructorName']:<24} "
                          f"{r['Expertise'] or 'N/A':<25} {r['Email']:<25}")
                print(f"\n  Tong: {len(rows)} giang vien")
            pause()

        elif c == '2':
            header("THONG TIN GIANG VIEN")
            iid = input_int("  Nhap InstructorID: ")
            if iid:
                r = get_instructor_by_id(iid)
                if r:
                    print(f"  ID         : {r['InstructorID']}")
                    print(f"  Ho Ten     : {r['InstructorName']}")
                    print(f"  Chuyen Mon : {r['Expertise'] or 'N/A'}")
                    print(f"  Email      : {r['Email']}")
                else:
                    print(f"  [!] Khong tim thay giang vien ID={iid}.")
            pause()

        elif c == '3':
            header("THEM GIANG VIEN MOI")
            name  = input("  Ho ten     : ").strip()
            exp   = input("  Chuyen mon : ").strip()
            email = input("  Email      : ").strip()
            if name and email:
                add_instructor(name, exp, email)
            else:
                print("  [!] Ho ten va Email khong duoc de trong!")
            pause()

        elif c == '4':
            header("CAP NHAT GIANG VIEN")
            iid = input_int("  Nhap InstructorID can sua: ")
            if iid:
                r = get_instructor_by_id(iid)
                if not r:
                    print(f"  [!] Khong tim thay ID={iid}.")
                else:
                    print(f"  Dang sua: {r['InstructorName']}")
                    name  = input("  Ten moi       (Enter giu nguyen): ").strip() or None
                    exp   = input("  Chuyen mon moi(Enter giu nguyen): ").strip() or None
                    email = input("  Email moi     (Enter giu nguyen): ").strip() or None
                    update_instructor(iid, name, exp, email)
            pause()

        elif c == '5':
            header("XOA GIANG VIEN")
            iid = input_int("  Nhap InstructorID can xoa: ")
            if iid:
                r = get_instructor_by_id(iid)
                if not r:
                    print(f"  [!] Khong tim thay ID={iid}.")
                else:
                    print(f"  Se xoa: {r['InstructorName']}")
                    print("  [!] Chi xoa duoc neu giang vien khong day khoa hoc nao!")
                    cf = input("  Xac nhan xoa? (y/n): ").strip().lower()
                    if cf == 'y':
                        delete_instructor(iid)
                    else:
                        print("  Da huy thao tac.")
            pause()

        elif c == '0':
            break


# ══════════════════════════════════════════════════════════════
#  3. QUAN LY KHOA HOC
# ══════════════════════════════════════════════════════════════
def menu_course():
    while True:
        clear()
        print("╔══════════════════════════════════════════════════╗")
        print("║            QUAN LY KHOA HOC                      ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║  [1]  Xem danh sach khoa hoc                     ║")
        print("║  [2]  Tim kiem khoa hoc theo ten                  ║")
        print("║  [3]  Xem chi tiet mot khoa hoc                   ║")
        print("║  [4]  Them khoa hoc moi                           ║")
        print("║  [5]  Cap nhat khoa hoc                           ║")
        print("║  [6]  Xoa khoa hoc                                ║")
        print("║  [0]  Quay lai menu chinh                         ║")
        print("╚══════════════════════════════════════════════════╝")
        c = input("  >> Lua chon: ").strip()

        if c == '1':
            header("DANH SACH KHOA HOC")
            rows = get_all_courses()
            if not rows:
                print("  Chua co khoa hoc nao.")
            else:
                print(f"  {'ID':<6} {'Ten Khoa Hoc':<28} {'Giang Vien':<22} {'Mo Ta':<18}")
                print("  " + "-"*74)
                for r in rows:
                    desc = (r['Description'] or '')
                    desc = desc[:16] + '..' if len(desc) > 18 else desc
                    print(f"  {r['CourseID']:<6} {r['CourseName']:<28} "
                          f"{r['InstructorName']:<22} {desc:<18}")
                print(f"\n  Tong: {len(rows)} khoa hoc")
            pause()

        elif c == '2':
            header("TIM KIEM KHOA HOC")
            kw = input("  Nhap tu khoa ten khoa hoc: ").strip()
            if kw:
                rows = search_course_by_name(kw)
                if not rows:
                    print(f"  Khong tim thay khoa hoc nao voi tu khoa '{kw}'.")
                else:
                    for r in rows:
                        print(f"  [{r['CourseID']}] {r['CourseName']} "
                              f"- GV: {r['InstructorName']}")
            pause()

        elif c == '3':
            header("CHI TIET KHOA HOC")
            cid = input_int("  Nhap CourseID: ")
            if cid:
                r = get_course_by_id(cid)
                if r:
                    print(f"  ID          : {r['CourseID']}")
                    print(f"  Ten         : {r['CourseName']}")
                    print(f"  Giang Vien  : {r['InstructorName']}")
                    print(f"  Mo Ta       : {r['Description'] or 'N/A'}")
                    # Hien thi so bai giang
                    lecs = get_lectures_by_course(cid)
                    print(f"  So Bai Giang: {len(lecs)}")
                else:
                    print(f"  [!] Khong tim thay khoa hoc ID={cid}.")
            pause()

        elif c == '4':
            header("THEM KHOA HOC MOI")
            # Hien thi giang vien de chon
            instructors = get_all_instructors()
            if not instructors:
                print("  [!] Chua co giang vien. Hay them giang vien truoc!")
                pause(); continue
            print("  Danh sach giang vien:")
            for i in instructors:
                print(f"    [{i['InstructorID']}] {i['InstructorName']} - {i['Expertise']}")
            name  = input("  Ten khoa hoc     : ").strip()
            desc  = input("  Mo ta            : ").strip()
            iid   = input_int("  InstructorID     : ")
            if name and iid:
                add_course(name, desc, iid)
            else:
                print("  [!] Ten va InstructorID khong duoc de trong!")
            pause()

        elif c == '5':
            header("CAP NHAT KHOA HOC")
            cid = input_int("  Nhap CourseID can sua: ")
            if cid:
                r = get_course_by_id(cid)
                if not r:
                    print(f"  [!] Khong tim thay ID={cid}.")
                else:
                    print(f"  Dang sua: {r['CourseName']}")
                    name  = input("  Ten moi   (Enter giu nguyen): ").strip() or None
                    desc  = input("  Mo ta moi (Enter giu nguyen): ").strip() or None
                    iid_s = input("  InstructorID moi (Enter bo qua): ").strip()
                    iid   = int(iid_s) if iid_s.isdigit() else None
                    update_course(cid, name, desc, iid)
            pause()

        elif c == '6':
            header("XOA KHOA HOC")
            cid = input_int("  Nhap CourseID can xoa: ")
            if cid:
                r = get_course_by_id(cid)
                if not r:
                    print(f"  [!] Khong tim thay ID={cid}.")
                else:
                    print(f"  Se xoa: {r['CourseName']}")
                    print("  [!] Tat ca bai giang va dang ky cua khoa nay cung se bi xoa!")
                    cf = input("  Xac nhan xoa? (y/n): ").strip().lower()
                    if cf == 'y':
                        delete_course(cid)
                    else:
                        print("  Da huy thao tac.")
            pause()

        elif c == '0':
            break


# ══════════════════════════════════════════════════════════════
#  4. QUAN LY BAI GIANG
# ══════════════════════════════════════════════════════════════
def menu_lecture():
    while True:
        clear()
        print("╔══════════════════════════════════════════════════╗")
        print("║            QUAN LY BAI GIANG                     ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║  [1]  Xem bai giang theo khoa hoc                ║")
        print("║  [2]  Them bai giang moi                          ║")
        print("║  [3]  Cap nhat bai giang                          ║")
        print("║  [4]  Xoa bai giang                               ║")
        print("║  [0]  Quay lai menu chinh                         ║")
        print("╚══════════════════════════════════════════════════╝")
        c = input("  >> Lua chon: ").strip()

        if c == '1':
            header("BAI GIANG THEO KHOA HOC")
            cid = input_int("  Nhap CourseID: ")
            if cid:
                rows = get_lectures_by_course(cid)
                if not rows:
                    print("  Khoa hoc nay chua co bai giang nao.")
                else:
                    print(f"\n  Khoa hoc: {rows[0]['CourseName']}")
                    print(f"  {'LID':<6} {'Tieu De':<35} {'Noi Dung (tom tat)'}")
                    print("  " + "-"*70)
                    for r in rows:
                        cont = (r['Content'] or '')
                        cont = cont[:28] + '..' if len(cont) > 30 else cont
                        print(f"  {r['LectureID']:<6} {r['Title']:<35} {cont}")
                    print(f"\n  Tong: {len(rows)} bai giang")
            pause()

        elif c == '2':
            header("THEM BAI GIANG MOI")
            # Hien thi danh sach khoa hoc
            courses = get_all_courses()
            if not courses:
                print("  [!] Chua co khoa hoc nao.")
                pause(); continue
            print("  Danh sach khoa hoc:")
            for co in courses:
                print(f"    [{co['CourseID']}] {co['CourseName']}")
            cid   = input_int("  Chon CourseID : ")
            title = input("  Tieu de       : ").strip()
            cont  = input("  Noi dung      : ").strip()
            if cid and title:
                add_lecture(cid, title, cont)
            else:
                print("  [!] CourseID va Tieu de khong duoc de trong!")
            pause()

        elif c == '3':
            header("CAP NHAT BAI GIANG")
            lid   = input_int("  Nhap LectureID can sua: ")
            if lid:
                title = input("  Tieu de moi   (Enter giu nguyen): ").strip() or None
                cont  = input("  Noi dung moi  (Enter giu nguyen): ").strip() or None
                update_lecture(lid, title, cont)
            pause()

        elif c == '4':
            header("XOA BAI GIANG")
            lid = input_int("  Nhap LectureID can xoa: ")
            if lid:
                cf = input(f"  Xac nhan xoa bai giang ID={lid}? (y/n): ").strip().lower()
                if cf == 'y':
                    delete_lecture(lid)
                else:
                    print("  Da huy thao tac.")
            pause()

        elif c == '0':
            break


# ══════════════════════════════════════════════════════════════
#  5. DANG KY & TIEN DO HOC TAP
# ══════════════════════════════════════════════════════════════
def menu_enrollment():
    while True:
        clear()
        print("╔══════════════════════════════════════════════════╗")
        print("║       DANG KY & TIEN DO HOC TAP                  ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║  [1]  Xem tat ca dang ky hoc                     ║")
        print("║  [2]  Xem khoa hoc cua mot hoc vien               ║")
        print("║  [3]  Xem hoc vien cua mot khoa hoc               ║")
        print("║  [4]  Dang ky hoc vien vao khoa hoc               ║")
        print("║  [5]  Cap nhat trang thai hoc tap                 ║")
        print("║  [6]  Huy dang ky hoc                             ║")
        print("║  [7]  Xem tien do chi tiet mot hoc vien           ║")
        print("║  [0]  Quay lai menu chinh                         ║")
        print("╚══════════════════════════════════════════════════╝")
        c = input("  >> Lua chon: ").strip()

        if c == '1':
            header("DANH SACH TAT CA DANG KY")
            rows = get_all_enrollments()
            if not rows:
                print("  Chua co dang ky nao.")
            else:
                print(f"  {'EID':<5} {'Hoc Vien':<22} {'Khoa Hoc':<26} "
                      f"{'Ngay DK':<12} {'TT':<10}")
                print("  " + "-"*76)
                for r in rows:
                    print(f"  {r['EnrollmentID']:<5} {r['LearnerName']:<22} "
                          f"{r['CourseName']:<26} "
                          f"{str(r['EnrollmentDate']):<12} {r['Status']:<10}")
                print(f"\n  Tong: {len(rows)} dang ky")
            pause()

        elif c == '2':
            header("KHOA HOC CUA HOC VIEN")
            lid = input_int("  Nhap LearnerID: ")
            if lid:
                rows = get_learner_courses(lid)
                if not rows:
                    print("  Hoc vien nay chua dang ky khoa hoc nao.")
                else:
                    print(f"  {'Ten Khoa Hoc':<28} {'Giang Vien':<20} "
                          f"{'Ngay DK':<12} {'Trang Thai':<12}")
                    print("  " + "-"*72)
                    for r in rows:
                        print(f"  {r['CourseName']:<28} {r['InstructorName']:<20} "
                              f"{str(r['EnrollmentDate']):<12} {r['Status']:<12}")
            pause()

        elif c == '3':
            header("HOC VIEN CUA KHOA HOC")
            cid = input_int("  Nhap CourseID: ")
            if cid:
                rows = get_learners_by_course(cid)
                if not rows:
                    print("  Khoa hoc nay chua co hoc vien nao.")
                else:
                    print(f"  {'ID':<6} {'Ho Ten':<25} {'Email':<28} "
                          f"{'Ngay DK':<12} {'TT':<10}")
                    print("  " + "-"*80)
                    for r in rows:
                        print(f"  {r['LearnerID']:<6} {r['LearnerName']:<25} "
                              f"{r['Email']:<28} "
                              f"{str(r['EnrollmentDate']):<12} {r['Status']:<10}")
                    print(f"\n  Tong: {len(rows)} hoc vien")
            pause()

        elif c == '4':
            header("DANG KY HOC VIEN VAO KHOA HOC")
            # Hien thi danh sach nhanh
            print("  --- Danh sach hoc vien ---")
            for r in get_all_learners():
                print(f"    [{r['LearnerID']}] {r['LearnerName']}")
            lid = input_int("  Nhap LearnerID : ")
            print("  --- Danh sach khoa hoc ---")
            for r in get_all_courses():
                print(f"    [{r['CourseID']}] {r['CourseName']}")
            cid = input_int("  Nhap CourseID  : ")
            if lid and cid:
                enroll_learner(lid, cid)
            pause()

        elif c == '5':
            header("CAP NHAT TRANG THAI HOC")
            print("  Trang thai: Active | Completed | Dropped")
            lid    = input_int("  LearnerID    : ")
            cid    = input_int("  CourseID     : ")
            status = input("  Trang thai moi: ").strip()
            if lid and cid:
                update_enrollment_status(lid, cid, status)
            pause()

        elif c == '6':
            header("HUY DANG KY HOC")
            lid = input_int("  LearnerID: ")
            cid = input_int("  CourseID : ")
            if lid and cid:
                cf = input("  Xac nhan huy dang ky? (y/n): ").strip().lower()
                if cf == 'y':
                    delete_enrollment(lid, cid)
                else:
                    print("  Da huy thao tac.")
            pause()

        elif c == '7':
            header("TIEN DO CHI TIET HOC VIEN")
            # Hien thi danh sach hoc vien de chon
            for r in get_all_learners():
                print(f"    [{r['LearnerID']}] {r['LearnerName']}")
            lid = input_int("  Nhap LearnerID: ")
            if lid:
                report_learner_progress(lid)
            pause()

        elif c == '0':
            break


# ══════════════════════════════════════════════════════════════
#  6. BAO CAO & THONG KE
# ══════════════════════════════════════════════════════════════
def menu_report():
    while True:
        clear()
        print("╔══════════════════════════════════════════════════╗")
        print("║           BAO CAO & THONG KE                     ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║  [1]  Tong quan tat ca khoa hoc                  ║")
        print("║  [2]  Khoi luong giang day cua giang vien        ║")
        print("║  [3]  Tien do hoc tap cua mot hoc vien           ║")
        print("║  [4]  Thong ke dang ky (Active/Completed/Dropped)║")
        print("║  [5]  Top 5 khoa hoc nhieu hoc vien nhat         ║")
        print("║  [0]  Quay lai menu chinh                         ║")
        print("╚══════════════════════════════════════════════════╝")
        c = input("  >> Lua chon: ").strip()

        if c == '1':
            report_active_courses()
            pause()
        elif c == '2':
            report_instructor_workload()
            pause()
        elif c == '3':
            header("TIEN DO HOC VIEN")
            for r in get_all_learners():
                print(f"    [{r['LearnerID']}] {r['LearnerName']}")
            lid = input_int("  Nhap LearnerID: ")
            if lid:
                report_learner_progress(lid)
            pause()
        elif c == '4':
            report_enrollment_statistics()
            pause()
        elif c == '5':
            report_top_courses()
            pause()
        elif c == '0':
            break


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    main_menu()