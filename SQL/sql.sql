-- ============================================================
-- PROJECT 04: ONLINE COURSE MANAGEMENT SYSTEM
-- File: 01_schema.sql - Tao co so du lieu va cac bang
-- ============================================================

CREATE DATABASE IF NOT EXISTS OnlineCourseDB
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE OnlineCourseDB;

-- Bang Instructors (Giang vien)
CREATE TABLE Instructors (
    InstructorID    INT             AUTO_INCREMENT PRIMARY KEY,
    InstructorName  VARCHAR(100)    NOT NULL,
    Expertise       VARCHAR(150),
    Email           VARCHAR(100)    UNIQUE NOT NULL
);

-- Bang Learners (Hoc vien)
CREATE TABLE Learners (
    LearnerID    INT           AUTO_INCREMENT PRIMARY KEY,
    LearnerName  VARCHAR(100)  NOT NULL,
    Email        VARCHAR(100)  UNIQUE NOT NULL,
    PhoneNumber  VARCHAR(15)
);

-- Bang Courses (Khoa hoc)
CREATE TABLE Courses (
    CourseID      INT           AUTO_INCREMENT PRIMARY KEY,
    CourseName    VARCHAR(150)  NOT NULL,
    Description   TEXT,
    InstructorID  INT           NOT NULL,
    CONSTRAINT fk_course_instructor
        FOREIGN KEY (InstructorID) REFERENCES Instructors(InstructorID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Bang Lectures (Bai giang)
CREATE TABLE Lectures (
    LectureID  INT           AUTO_INCREMENT PRIMARY KEY,
    CourseID   INT           NOT NULL,
    Title      VARCHAR(200)  NOT NULL,
    Content    TEXT,
    CONSTRAINT fk_lecture_course
        FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Bang Enrollments (Dang ky hoc)
CREATE TABLE Enrollments (
    EnrollmentID    INT   AUTO_INCREMENT PRIMARY KEY,
    LearnerID       INT   NOT NULL,
    CourseID        INT   NOT NULL,
    EnrollmentDate  DATE  NOT NULL DEFAULT (CURRENT_DATE),
    Status          ENUM('Active','Completed','Dropped') DEFAULT 'Active',
    CONSTRAINT fk_enrollment_learner
        FOREIGN KEY (LearnerID) REFERENCES Learners(LearnerID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_enrollment_course
        FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_enrollment UNIQUE (LearnerID, CourseID)
);

-- Bang AuditLog (phuc vu Trigger)
CREATE TABLE EnrollmentAuditLog (
    LogID       INT           AUTO_INCREMENT PRIMARY KEY,
    Action      VARCHAR(50)   NOT NULL,
    LearnerID   INT,
    CourseID    INT,
    ChangedAt   DATETIME      DEFAULT CURRENT_TIMESTAMP,
    Note        VARCHAR(255)
);

-- ============================================================
-- File: 02_sample_data.sql - Du lieu mau
-- ============================================================
USE OnlineCourseDB;

-- Du lieu Instructors (10 giang vien)
INSERT INTO Instructors (InstructorName, Expertise, Email) VALUES
('Nguyen Van An',    'Database Systems',         'an.nguyen@edu.vn'),
('Tran Thi Bich',    'Python Programming',       'bich.tran@edu.vn'),
('Le Hoang Cuong',   'Web Development',          'cuong.le@edu.vn'),
('Pham Thi Dung',    'Machine Learning',         'dung.pham@edu.vn'),
('Hoang Van Em',     'Network Security',         'em.hoang@edu.vn'),
('Vu Thi Phuong',    'Data Structures',          'phuong.vu@edu.vn'),
('Do Van Giang',     'Software Engineering',     'giang.do@edu.vn'),
('Bui Thi Hoa',      'Cloud Computing',          'hoa.bui@edu.vn'),
('Dang Van Hung',    'Mobile Development',       'hung.dang@edu.vn'),
('Ngo Thi Lan',      'Artificial Intelligence',  'lan.ngo@edu.vn');

-- Du lieu Learners (10 hoc vien)
INSERT INTO Learners (LearnerName, Email, PhoneNumber) VALUES
('Tran Minh Anh',    'anh.tran@student.vn',   '0901234567'),
('Nguyen Thu Ba',    'ba.nguyen@student.vn',  '0912345678'),
('Le Van Chi',       'chi.le@student.vn',     '0923456789'),
('Pham Ngoc Diem',   'diem.pham@student.vn',  '0934567890'),
('Hoang Van Duc',    'duc.hoang@student.vn',  '0945678901'),
('Vu Thi Giang',     'giang.vu@student.vn',   '0956789012'),
('Do Minh Ha',       'ha.do@student.vn',      '0967890123'),
('Bui Van Hieu',     'hieu.bui@student.vn',   '0978901234'),
('Dang Thi Lan',     'lan.dang@student.vn',   '0989012345'),
('Ngo Van Minh',     'minh.ngo@student.vn',   '0990123456');

-- Du lieu Courses (10 khoa hoc)
INSERT INTO Courses (CourseName, Description, InstructorID) VALUES
('Introduction to Database',  'Co so du lieu co ban',              1),
('Python for Beginners',       'Lap trinh Python tu dau',          2),
('Web Development Basics',     'HTML, CSS, JavaScript',            3),
('Machine Learning 101',       'Nhap mon Machine Learning',        4),
('Network Security Essentials','Bao mat mang may tinh',            5),
('Data Structures & Algorithms','Cau truc du lieu va giai thuat',  6),
('Software Engineering',       'Quy trinh phat trien phan mem',    7),
('Cloud Computing Intro',      'Dien toan dam may co ban',         8),
('Mobile App Development',     'Phat trien ung dung di dong',      9),
('AI Fundamentals',            'Nen tang tri tue nhan tao',        10);

-- Du lieu Lectures (10 bai giang - 1 bai/khoa cho don gian, em co the them)
INSERT INTO Lectures (CourseID, Title, Content) VALUES
(1, 'Bai 1: CSDL la gi?',       'Gioi thieu khai niem co so du lieu, DBMS'),
(1, 'Bai 2: Mo hinh quan he',   'Relational model, bang, khoa chinh, khoa ngoai'),
(2, 'Bai 1: Bien va kieu du lieu','Khai bao bien, int, str, float trong Python'),
(2, 'Bai 2: Vong lap',          'for, while loop trong Python'),
(3, 'Bai 1: HTML co ban',       'The div, p, h1, a, img trong HTML'),
(4, 'Bai 1: Hoi quy tuyen tinh','Linear regression, gradient descent'),
(5, 'Bai 1: Firewall',          'Tuong lua, cac loai firewall'),
(6, 'Bai 1: Array va Linked List','Mang, danh sach lien ket'),
(7, 'Bai 1: SDLC',              'Vong doi phat trien phan mem'),
(8, 'Bai 1: Cloud la gi?',      'IaaS, PaaS, SaaS');

-- Du lieu Enrollments (10 dang ky)
INSERT INTO Enrollments (LearnerID, CourseID, EnrollmentDate, Status) VALUES
(1, 1, '2024-01-10', 'Active'),
(1, 2, '2024-01-12', 'Completed'),
(2, 1, '2024-01-11', 'Active'),
(3, 3, '2024-01-15', 'Active'),
(4, 4, '2024-02-01', 'Dropped'),
(5, 2, '2024-02-05', 'Completed'),
(6, 5, '2024-02-10', 'Active'),
(7, 6, '2024-02-12', 'Active'),
(8, 7, '2024-03-01', 'Active'),
(9, 8, '2024-03-05', 'Completed');

-- ============================================================
-- File: 03_indexes.sql - Chi muc tang toc do truy van
-- ============================================================
USE OnlineCourseDB;

-- Index tim kiem khoa hoc theo ten
CREATE INDEX idx_course_name
    ON Courses(CourseName);

-- Index tim kiem dang ky theo hoc vien
CREATE INDEX idx_enrollment_learner
    ON Enrollments(LearnerID);

-- Index tim kiem dang ky theo khoa hoc
CREATE INDEX idx_enrollment_course
    ON Enrollments(CourseID);

-- Index tim kiem bai giang theo khoa hoc
CREATE INDEX idx_lecture_course
    ON Lectures(CourseID);

-- Index tim kiem giang vien theo email
CREATE INDEX idx_instructor_email
    ON Instructors(Email);
    
-- ============================================================
-- File: 04_views.sql - View truy cap nhanh du lieu
-- ============================================================
USE OnlineCourseDB;

-- View 1: Cac khoa hoc hoc vien da dang ky (kem trang thai)
CREATE OR REPLACE VIEW vw_LearnerEnrollments AS
SELECT
    l.LearnerID,
    l.LearnerName,
    c.CourseName,
    e.EnrollmentDate,
    e.Status
FROM Enrollments e
JOIN Learners l ON e.LearnerID = l.LearnerID
JOIN Courses  c ON e.CourseID  = c.CourseID;

-- View 2: Khoi luong giang day cua moi giang vien
CREATE OR REPLACE VIEW vw_InstructorWorkload AS
SELECT
    i.InstructorID,
    i.InstructorName,
    i.Expertise,
    COUNT(c.CourseID)      AS TotalCourses,
    COUNT(e.EnrollmentID)  AS TotalStudentsEnrolled
FROM Instructors i
LEFT JOIN Courses     c ON i.InstructorID = c.InstructorID
LEFT JOIN Enrollments e ON c.CourseID     = e.CourseID
GROUP BY i.InstructorID, i.InstructorName, i.Expertise;

-- View 3: Tong quan khoa hoc (so bai giang, so hoc vien)
CREATE OR REPLACE VIEW vw_CourseSummary AS
SELECT
    c.CourseID,
    c.CourseName,
    i.InstructorName,
    COUNT(DISTINCT lec.LectureID)  AS TotalLectures,
    COUNT(DISTINCT e.LearnerID)    AS TotalLearners
FROM Courses c
LEFT JOIN Instructors i   ON c.InstructorID = i.InstructorID
LEFT JOIN Lectures    lec ON c.CourseID     = lec.CourseID
LEFT JOIN Enrollments e   ON c.CourseID     = e.CourseID
GROUP BY c.CourseID, c.CourseName, i.InstructorName;

-- Kiem tra views
SELECT * FROM vw_LearnerEnrollments;
SELECT * FROM vw_InstructorWorkload;
SELECT * FROM vw_CourseSummary;


-- ============================================================
-- File: 05_stored_procedures.sql
-- ============================================================
USE OnlineCourseDB;

DELIMITER $$

-- SP 1: Dang ky hoc vien vao khoa hoc (co kiem tra trung lap)
CREATE PROCEDURE sp_EnrollLearner(
    IN  p_LearnerID     INT,
    IN  p_CourseID      INT,
    OUT p_Message       VARCHAR(200)
)
BEGIN
    DECLARE v_exists INT DEFAULT 0;
    
    -- Kiem tra da dang ky chua
    SELECT COUNT(*) INTO v_exists
    FROM Enrollments
    WHERE LearnerID = p_LearnerID AND CourseID = p_CourseID;
    
    IF v_exists > 0 THEN
        SET p_Message = 'Hoc vien da dang ky khoa hoc nay roi!';
    ELSE
        INSERT INTO Enrollments (LearnerID, CourseID, EnrollmentDate, Status)
        VALUES (p_LearnerID, p_CourseID, CURRENT_DATE, 'Active');
        SET p_Message = 'Dang ky thanh cong!';
    END IF;
END$$

-- SP 2: Tong ket hoan thanh khoa hoc
CREATE PROCEDURE sp_CourseCompletionSummary(
    IN p_CourseID INT
)
BEGIN
    SELECT
        c.CourseName,
        COUNT(e.EnrollmentID)                                       AS TotalEnrolled,
        SUM(e.Status = 'Completed')                                 AS Completed,
        SUM(e.Status = 'Active')                                    AS Active,
        SUM(e.Status = 'Dropped')                                   AS Dropped,
        ROUND(SUM(e.Status = 'Completed') * 100.0 /
              COUNT(e.EnrollmentID), 2)                             AS CompletionRate
    FROM Courses c
    LEFT JOIN Enrollments e ON c.CourseID = e.CourseID
    WHERE c.CourseID = p_CourseID
    GROUP BY c.CourseName;
END$$

-- SP 3: Cap nhat trang thai dang ky
CREATE PROCEDURE sp_UpdateEnrollmentStatus(
    IN p_LearnerID  INT,
    IN p_CourseID   INT,
    IN p_NewStatus  ENUM('Active','Completed','Dropped')
)
BEGIN
    UPDATE Enrollments
    SET Status = p_NewStatus
    WHERE LearnerID = p_LearnerID AND CourseID = p_CourseID;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

DELIMITER ;

-- === Kiem tra Stored Procedures ===
-- Dang ky hoc vien so 10 vao khoa 3
CALL sp_EnrollLearner(10, 3, @msg);
SELECT @msg AS KetQua;

-- Xem tong ket khoa hoc so 1
CALL sp_CourseCompletionSummary(1);

-- Cap nhat trang thai
CALL sp_UpdateEnrollmentStatus(1, 1, 'Completed');


-- ============================================================
-- File: 06_functions.sql - Ham nguoi dung tu dinh nghia
-- ============================================================
USE OnlineCourseDB;

DELIMITER $$

-- Ham 1: Tinh % hoan thanh cua hoc vien trong mot khoa hoc
-- (so lectures da xem / tong lectures)
-- De don gian: neu Status = Completed => 100%, Active => 50%, Dropped => 0%
CREATE FUNCTION fn_LearnerCompletionPct(
    p_LearnerID INT,
    p_CourseID  INT
)
RETURNS DECIMAL(5,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_status  VARCHAR(20);
    DECLARE v_pct     DECIMAL(5,2) DEFAULT 0.00;
    
    SELECT Status INTO v_status
    FROM Enrollments
    WHERE LearnerID = p_LearnerID AND CourseID = p_CourseID
    LIMIT 1;
    
    CASE v_status
        WHEN 'Completed' THEN SET v_pct = 100.00;
        WHEN 'Active'    THEN SET v_pct = 50.00;
        WHEN 'Dropped'   THEN SET v_pct = 0.00;
        ELSE SET v_pct = 0.00;
    END CASE;
    
    RETURN v_pct;
END$$

-- Ham 2: Dem tong so lectures cua mot khoa hoc
CREATE FUNCTION fn_TotalLectures(p_CourseID INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total INT;
    SELECT COUNT(*) INTO v_total
    FROM Lectures WHERE CourseID = p_CourseID;
    RETURN v_total;
END$$

DELIMITER ;

-- === Kiem tra Functions ===
SELECT fn_LearnerCompletionPct(1, 1) AS CompletionPct;
SELECT fn_TotalLectures(1)           AS TotalLectures;

-- Dung trong query lon hon
SELECT
    l.LearnerName,
    c.CourseName,
    fn_LearnerCompletionPct(e.LearnerID, e.CourseID) AS CompletionPct
FROM Enrollments e
JOIN Learners l ON e.LearnerID = l.LearnerID
JOIN Courses  c ON e.CourseID  = c.CourseID;

-- ============================================================
-- File: 07_triggers.sql - Trigger tu dong
-- ============================================================
USE OnlineCourseDB;

DELIMITER $$

-- Trigger 1: Ghi audit log khi them enrollment moi
CREATE TRIGGER trg_AfterEnrollInsert
AFTER INSERT ON Enrollments
FOR EACH ROW
BEGIN
    INSERT INTO EnrollmentAuditLog (Action, LearnerID, CourseID, Note)
    VALUES (
        'INSERT',
        NEW.LearnerID,
        NEW.CourseID,
        CONCAT('Dang ky moi - Status: ', NEW.Status)
    );
END$$

-- Trigger 2: Ghi audit log khi cap nhat enrollment
CREATE TRIGGER trg_AfterEnrollUpdate
AFTER UPDATE ON Enrollments
FOR EACH ROW
BEGIN
    IF OLD.Status <> NEW.Status THEN
        INSERT INTO EnrollmentAuditLog (Action, LearnerID, CourseID, Note)
        VALUES (
            'UPDATE',
            NEW.LearnerID,
            NEW.CourseID,
            CONCAT('Doi trang thai: ', OLD.Status, ' -> ', NEW.Status)
        );
    END IF;
END$$

-- Trigger 3: Ngan xoa instructor con dang day khoa hoc
-- (MySQL da xu ly qua FOREIGN KEY RESTRICT, nhung ta co the them thong bao ro hon)
CREATE TRIGGER trg_BeforeEnrollDelete
BEFORE DELETE ON Enrollments
FOR EACH ROW
BEGIN
    INSERT INTO EnrollmentAuditLog (Action, LearnerID, CourseID, Note)
    VALUES (
        'DELETE',
        OLD.LearnerID,
        OLD.CourseID,
        'Xoa dang ky'
    );
END$$

DELIMITER ;

-- === Kiem tra Triggers ===
-- Them moi de trigger chay
INSERT INTO Enrollments (LearnerID, CourseID, EnrollmentDate)
VALUES (10, 5, CURRENT_DATE);

-- Cap nhat de trigger UPDATE chay
UPDATE Enrollments SET Status = 'Completed'
WHERE LearnerID = 10 AND CourseID = 5;

-- Xem audit log
SELECT * FROM EnrollmentAuditLog;

-- ============================================================
-- File: 08_security.sql - Bao mat va phan quyen
-- ============================================================

-- Tao user cho giang vien (chi doc du lieu)
CREATE USER IF NOT EXISTS 'instructor_user'@'localhost'
    IDENTIFIED BY 'Instructor@2024';

GRANT SELECT ON OnlineCourseDB.Courses        TO 'instructor_user'@'localhost';
GRANT SELECT ON OnlineCourseDB.Lectures       TO 'instructor_user'@'localhost';
GRANT SELECT ON OnlineCourseDB.Enrollments    TO 'instructor_user'@'localhost';
GRANT SELECT ON OnlineCourseDB.vw_InstructorWorkload TO 'instructor_user'@'localhost';

-- Tao user cho admin (toan quyen)
CREATE USER IF NOT EXISTS 'admin_user'@'localhost'
    IDENTIFIED BY 'Admin@2024Strong';

GRANT ALL PRIVILEGES ON OnlineCourseDB.* TO 'admin_user'@'localhost';

-- Tao user cho hoc vien (chi doc)
CREATE USER IF NOT EXISTS 'learner_user'@'localhost'
    IDENTIFIED BY 'Learner@2024';

GRANT SELECT ON OnlineCourseDB.Courses     TO 'learner_user'@'localhost';
GRANT SELECT ON OnlineCourseDB.Lectures    TO 'learner_user'@'localhost';
GRANT SELECT ON OnlineCourseDB.vw_LearnerEnrollments TO 'learner_user'@'localhost';

FLUSH PRIVILEGES;

-- Xem phan quyen
SHOW GRANTS FOR 'instructor_user'@'localhost';
SHOW GRANTS FOR 'learner_user'@'localhost';