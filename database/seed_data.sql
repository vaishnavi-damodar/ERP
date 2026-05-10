-- ============================================
-- EDUSYNC SAMPLE DUMMY DATA
-- ============================================

-- ============================================
-- 1. INSERT DEPARTMENTS
-- ============================================
INSERT INTO departments (department_name, department_code, hod_name, contact_email) VALUES
('Computer Science', 'CS', 'Dr. John Smith', 'cs@edusync.edu'),
('Electronics and Communication', 'ECE', 'Dr. Sarah Johnson', 'ece@edusync.edu'),
('Mechanical Engineering', 'ME', 'Dr. Michael Chen', 'me@edusync.edu'),
('Civil Engineering', 'CE', 'Dr. Emily Williams', 'ce@edusync.edu'),
('Information Technology', 'IT', 'Dr. James Brown', 'it@edusync.edu')
ON CONFLICT DO NOTHING;

-- ============================================
-- 2. INSERT USERS (Admin)
-- ============================================
INSERT INTO users (email, name, role, is_active) VALUES
('admin@edusync.edu', 'Admin User', 'admin', TRUE),
('admin2@edusync.edu', 'Admin Two', 'admin', TRUE)
ON CONFLICT DO NOTHING;

-- ============================================
-- 3. INSERT USERS (Faculty)
-- ============================================
INSERT INTO users (email, name, phone, role, is_active) VALUES
('dr.patel@edusync.edu', 'Dr. Rajesh Patel', '9876543210', 'faculty', TRUE),
('dr.sharma@edusync.edu', 'Dr. Priya Sharma', '9876543211', 'faculty', TRUE),
('dr.verma@edusync.edu', 'Dr. Amit Verma', '9876543212', 'faculty', TRUE),
('dr.gupta@edusync.edu', 'Dr. Neha Gupta', '9876543213', 'faculty', TRUE),
('dr.khan@edusync.edu', 'Dr. Ali Khan', '9876543214', 'faculty', TRUE),
('dr.mishra@edusync.edu', 'Dr. Rakesh Mishra', '9876543215', 'faculty', TRUE),
('dr.desai@edusync.edu', 'Dr. Pooja Desai', '9876543216', 'faculty', TRUE),
('dr.singh@edusync.edu', 'Dr. Vikram Singh', '9876543217', 'faculty', TRUE)
ON CONFLICT DO NOTHING;

-- ============================================
-- 4. INSERT USERS (Students)
-- ============================================
INSERT INTO users (email, name, phone, role, is_active) VALUES
('student1@edusync.edu', 'Arjun Kumar', '9000000001', 'student', TRUE),
('student2@edusync.edu', 'Sneha Patel', '9000000002', 'student', TRUE),
('student3@edusync.edu', 'Rohan Sharma', '9000000003', 'student', TRUE),
('student4@edusync.edu', 'Priya Singh', '9000000004', 'student', TRUE),
('student5@edusync.edu', 'Ananya Desai', '9000000005', 'student', TRUE),
('student6@edusync.edu', 'Vihaan Gupta', '9000000006', 'student', TRUE),
('student7@edusync.edu', 'Diya Verma', '9000000007', 'student', TRUE),
('student8@edusync.edu', 'Karan Mishra', '9000000008', 'student', TRUE),
('student9@edusync.edu', 'Zara Khan', '9000000009', 'student', TRUE),
('student10@edusync.edu', 'Nikhil Chopra', '9000000010', 'student', TRUE)
ON CONFLICT DO NOTHING;

-- ============================================
-- 5. INSERT FACULTY DETAILS
-- ============================================
INSERT INTO faculty (user_id, department_id, designation, employee_id, specialization, experience_years) 
SELECT u.id, d.id, 'Associate Professor', 'EMP001', 'Data Structures', 12
FROM users u, departments d WHERE u.email = 'dr.patel@edusync.edu' AND d.department_code = 'CS'
ON CONFLICT DO NOTHING;

INSERT INTO faculty (user_id, department_id, designation, employee_id, specialization, experience_years) 
SELECT u.id, d.id, 'Assistant Professor', 'EMP002', 'Database Systems', 8
FROM users u, departments d WHERE u.email = 'dr.sharma@edusync.edu' AND d.department_code = 'CS'
ON CONFLICT DO NOTHING;

INSERT INTO faculty (user_id, department_id, designation, employee_id, specialization, experience_years) 
SELECT u.id, d.id, 'Associate Professor', 'EMP003', 'VLSI Design', 10
FROM users u, departments d WHERE u.email = 'dr.verma@edusync.edu' AND d.department_code = 'ECE'
ON CONFLICT DO NOTHING;

INSERT INTO faculty (user_id, department_id, designation, employee_id, specialization, experience_years) 
SELECT u.id, d.id, 'Assistant Professor', 'EMP004', 'Thermodynamics', 6
FROM users u, departments d WHERE u.email = 'dr.gupta@edusync.edu' AND d.department_code = 'ME'
ON CONFLICT DO NOTHING;

-- ============================================
-- 6. INSERT STUDENT DETAILS
-- ============================================
INSERT INTO students (user_id, usn, department_id, semester, phone, address, enrollment_year)
SELECT u.id, 'CS21001', d.id, 4, '9000000001', '123 Main St, City', 2021
FROM users u, departments d WHERE u.email = 'student1@edusync.edu' AND d.department_code = 'CS'
ON CONFLICT DO NOTHING;

INSERT INTO students (user_id, usn, department_id, semester, phone, address, enrollment_year)
SELECT u.id, 'CS21002', d.id, 4, '9000000002', '456 Park Ave, City', 2021
FROM users u, departments d WHERE u.email = 'student2@edusync.edu' AND d.department_code = 'CS'
ON CONFLICT DO NOTHING;

INSERT INTO students (user_id, usn, department_id, semester, phone, address, enrollment_year)
SELECT u.id, 'CS21003', d.id, 4, '9000000003', '789 Oak Rd, City', 2021
FROM users u, departments d WHERE u.email = 'student3@edusync.edu' AND d.department_code = 'CS'
ON CONFLICT DO NOTHING;

INSERT INTO students (user_id, usn, department_id, semester, phone, address, enrollment_year)
SELECT u.id, 'IT21001', d.id, 4, '9000000004', '321 Pine St, City', 2021
FROM users u, departments d WHERE u.email = 'student4@edusync.edu' AND d.department_code = 'IT'
ON CONFLICT DO NOTHING;

INSERT INTO students (user_id, usn, department_id, semester, phone, address, enrollment_year)
SELECT u.id, 'IT21002', d.id, 4, '9000000005', '654 Cedar Lane, City', 2021
FROM users u, departments d WHERE u.email = 'student5@edusync.edu' AND d.department_code = 'IT'
ON CONFLICT DO NOTHING;

-- ============================================
-- 7. INSERT COURSES
-- ============================================
INSERT INTO courses (course_name, course_code, department_id, faculty_id, semester, credits, description)
SELECT 'Database Management Systems', 'CS301', d.id, f.id, 4, 4, 'Comprehensive study of DBMS concepts'
FROM departments d, faculty f 
WHERE d.department_code = 'CS' AND f.employee_id = 'EMP002'
ON CONFLICT DO NOTHING;

INSERT INTO courses (course_name, course_code, department_id, faculty_id, semester, credits, description)
SELECT 'Data Structures and Algorithms', 'CS302', d.id, f.id, 4, 4, 'Advanced concepts in DSA'
FROM departments d, faculty f 
WHERE d.department_code = 'CS' AND f.employee_id = 'EMP001'
ON CONFLICT DO NOTHING;

INSERT INTO courses (course_name, course_code, department_id, faculty_id, semester, credits, description)
SELECT 'Web Technologies', 'IT303', d.id, NULL, 4, 3, 'Modern web development frameworks'
FROM departments d 
WHERE d.department_code = 'IT'
ON CONFLICT DO NOTHING;

-- ============================================
-- 8. INSERT COURSE ENROLLMENTS
-- ============================================
INSERT INTO course_enrollments (student_id, course_id, status)
SELECT s.id, c.id, 'enrolled'
FROM students s, courses c
WHERE s.usn IN ('CS21001', 'CS21002', 'CS21003') AND c.course_code = 'CS301'
ON CONFLICT DO NOTHING;

INSERT INTO course_enrollments (student_id, course_id, status)
SELECT s.id, c.id, 'enrolled'
FROM students s, courses c
WHERE s.usn IN ('IT21001', 'IT21002') AND c.course_code = 'IT303'
ON CONFLICT DO NOTHING;

-- ============================================
-- 9. INSERT ATTENDANCE
-- ============================================
INSERT INTO attendance (student_id, course_id, attendance_date, status, marked_by)
SELECT s.id, c.id, CURRENT_DATE - INTERVAL '5 days', 'present', f.id
FROM students s, courses c, faculty f
WHERE s.usn = 'CS21001' AND c.course_code = 'CS301' AND f.employee_id = 'EMP002'
ON CONFLICT DO NOTHING;

INSERT INTO attendance (student_id, course_id, attendance_date, status)
SELECT s.id, c.id, CURRENT_DATE - INTERVAL '4 days', 'absent'
FROM students s, courses c
WHERE s.usn = 'CS21002' AND c.course_code = 'CS301'
ON CONFLICT DO NOTHING;

-- ============================================
-- 10. INSERT MARKS
-- ============================================
INSERT INTO marks (student_id, course_id, internal_marks, assignment_marks, practical_marks, semester_exam_marks, submitted_by)
SELECT s.id, c.id, 18, 9, 8, 55, f.id
FROM students s, courses c, faculty f
WHERE s.usn = 'CS21001' AND c.course_code = 'CS301' AND f.employee_id = 'EMP002'
ON CONFLICT DO NOTHING;

INSERT INTO marks (student_id, course_id, internal_marks, assignment_marks, practical_marks, semester_exam_marks)
SELECT s.id, c.id, 15, 7, 6, 48
FROM students s, courses c
WHERE s.usn = 'CS21002' AND c.course_code = 'CS301'
ON CONFLICT DO NOTHING;

INSERT INTO marks (student_id, course_id, internal_marks, assignment_marks, practical_marks, semester_exam_marks)
SELECT s.id, c.id, 19, 10, 9, 58
FROM students s, courses c
WHERE s.usn = 'CS21003' AND c.course_code = 'CS301'
ON CONFLICT DO NOTHING;

-- ============================================
-- 11. INSERT FEES
-- ============================================
INSERT INTO fees (student_id, semester, total_fee, paid_fee, due_date, payment_status)
SELECT s.id, 4, 50000, 25000, CURRENT_DATE + INTERVAL '30 days', 'partial'
FROM students s WHERE s.usn = 'CS21001'
ON CONFLICT DO NOTHING;

INSERT INTO fees (student_id, semester, total_fee, paid_fee, payment_status)
SELECT s.id, 4, 50000, 50000, 'paid'
FROM students s WHERE s.usn = 'CS21002'
ON CONFLICT DO NOTHING;

INSERT INTO fees (student_id, semester, total_fee, paid_fee, due_date, payment_status)
SELECT s.id, 4, 50000, 0, CURRENT_DATE - INTERVAL '5 days', 'overdue'
FROM students s WHERE s.usn = 'IT21001'
ON CONFLICT DO NOTHING;

-- ============================================
-- 12. INSERT ASSIGNMENTS
-- ============================================
INSERT INTO assignments (course_id, faculty_id, title, description, due_date, total_marks, is_published)
SELECT c.id, f.id, 'Database Design Project', 'Design a relational database for e-commerce system', 
        CURRENT_TIMESTAMP + INTERVAL '7 days', 10, TRUE
FROM courses c, faculty f
WHERE c.course_code = 'CS301' AND f.employee_id = 'EMP002'
ON CONFLICT DO NOTHING;

-- ============================================
-- 13. INSERT LEAVE REQUESTS
-- ============================================
INSERT INTO leave_requests (student_id, start_date, end_date, reason, leave_type, status)
SELECT s.id, CURRENT_DATE + INTERVAL '5 days', CURRENT_DATE + INTERVAL '7 days', 
        'Medical treatment', 'medical', 'pending'
FROM students s WHERE s.usn = 'CS21001'
ON CONFLICT DO NOTHING;

INSERT INTO leave_requests (student_id, start_date, end_date, reason, leave_type, status, approved_by)
SELECT s.id, CURRENT_DATE - INTERVAL '10 days', CURRENT_DATE - INTERVAL '8 days', 
        'Family emergency', 'personal', 'approved', f.id
FROM students s, faculty f
WHERE s.usn = 'CS21002' AND f.employee_id = 'EMP002'
ON CONFLICT DO NOTHING;

-- ============================================
-- 14. INSERT TIMETABLE
-- ============================================
INSERT INTO timetable (department_id, semester, course_id, faculty_id, day_of_week, start_time, end_time, room_number, session_type)
SELECT d.id, 4, c.id, f.id, 'Monday', '09:00:00', '10:30:00', 'A-101', 'lecture'
FROM departments d, courses c, faculty f
WHERE d.department_code = 'CS' AND c.course_code = 'CS301' AND f.employee_id = 'EMP002'
ON CONFLICT DO NOTHING;

INSERT INTO timetable (department_id, semester, course_id, faculty_id, day_of_week, start_time, end_time, room_number, session_type)
SELECT d.id, 4, c.id, f.id, 'Wednesday', '11:00:00', '12:30:00', 'A-101', 'lecture'
FROM departments d, courses c, faculty f
WHERE d.department_code = 'CS' AND c.course_code = 'CS301' AND f.employee_id = 'EMP002'
ON CONFLICT DO NOTHING;

INSERT INTO timetable (department_id, semester, course_id, faculty_id, day_of_week, start_time, end_time, room_number, session_type)
SELECT d.id, 4, c.id, f.id, 'Friday', '14:00:00', '16:00:00', 'Lab-B2', 'practical'
FROM departments d, courses c, faculty f
WHERE d.department_code = 'CS' AND c.course_code = 'CS301' AND f.employee_id = 'EMP002'
ON CONFLICT DO NOTHING;

-- ============================================
-- 15. INSERT NOTIFICATIONS
-- ============================================
INSERT INTO notifications (user_id, title, message, notification_type, is_read)
SELECT u.id, 'Welcome to EduSync', 'Your account has been created successfully', 'info', FALSE
FROM users u WHERE u.email = 'student1@edusync.edu'
ON CONFLICT DO NOTHING;

-- ============================================
-- VIEWS AUTOMATICALLY UPDATED
-- ============================================

-- Note: Regular views are automatically updated with live data
-- No refresh needed for views created as CREATE VIEW

-- ============================================
-- DONE
-- ============================================

-- Data insertion complete!
-- You can now login with:
-- Admin: admin@edusync.edu / admin123
-- Faculty: dr.patel@edusync.edu / (set password)
-- Student: student1@edusync.edu / (set password)
