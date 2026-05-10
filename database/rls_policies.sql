-- ============================================
-- SUPABASE ROW-LEVEL SECURITY (RLS) POLICIES
-- College ERP System
-- ============================================

-- Enable RLS for all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE faculty ENABLE ROW LEVEL SECURITY;
ALTER TABLE departments ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE marks ENABLE ROW LEVEL SECURITY;
ALTER TABLE fees ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignment_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE leave_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE timetable ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_enrollments ENABLE ROW LEVEL SECURITY;

-- ============================================
-- USERS TABLE POLICIES
-- ============================================

-- Admins can view all users
CREATE POLICY "Admins can view all users" ON users
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- Users can view their own profile
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT
    USING (id = auth.uid());

-- Admins can update user information
CREATE POLICY "Admins can update users" ON users
    FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE
    USING (id = auth.uid())
    WITH CHECK (id = auth.uid());

-- ============================================
-- STUDENTS TABLE POLICIES
-- ============================================

-- Students can view their own profile
CREATE POLICY "Students can view own profile" ON students
    FOR SELECT
    USING (user_id = auth.uid());

-- Faculty can view students in their department/courses
CREATE POLICY "Faculty can view students in their department" ON students
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM faculty f
            WHERE f.user_id = auth.uid() 
            AND f.department_id = students.department_id
        )
    );

-- Admins can view all students
CREATE POLICY "Admins can view all students" ON students
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- Admins can manage students
CREATE POLICY "Admins can manage students" ON students
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- FACULTY TABLE POLICIES
-- ============================================

-- Faculty can view their own profile
CREATE POLICY "Faculty can view own profile" ON faculty
    FOR SELECT
    USING (user_id = auth.uid());

-- Faculty can view other faculty in same department
CREATE POLICY "Faculty can view department faculty" ON faculty
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM faculty f
            WHERE f.user_id = auth.uid()
            AND f.department_id = faculty.department_id
        )
    );

-- Admins can view all faculty
CREATE POLICY "Admins can view all faculty" ON faculty
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- Admins can manage faculty
CREATE POLICY "Admins can manage faculty" ON faculty
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- DEPARTMENTS TABLE POLICIES
-- ============================================

-- All authenticated users can view departments
CREATE POLICY "All users can view departments" ON departments
    FOR SELECT
    USING (auth.role() = 'authenticated');

-- Only admins can manage departments
CREATE POLICY "Admins can manage departments" ON departments
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- COURSES TABLE POLICIES
-- ============================================

-- All authenticated users can view courses
CREATE POLICY "All users can view courses" ON courses
    FOR SELECT
    USING (auth.role() = 'authenticated');

-- Faculty can view courses they teach
CREATE POLICY "Faculty can view their courses" ON courses
    FOR SELECT
    USING (
        faculty_id = (
            SELECT id FROM faculty WHERE user_id = auth.uid()
        )
    );

-- Faculty can update their courses
CREATE POLICY "Faculty can update their courses" ON courses
    FOR UPDATE
    USING (
        faculty_id = (
            SELECT id FROM faculty WHERE user_id = auth.uid()
        )
    );

-- Admins can manage all courses
CREATE POLICY "Admins can manage courses" ON courses
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- ATTENDANCE TABLE POLICIES
-- ============================================

-- Students can view their own attendance
CREATE POLICY "Students can view own attendance" ON attendance
    FOR SELECT
    USING (
        student_id = (
            SELECT id FROM students WHERE user_id = auth.uid()
        )
    );

-- Faculty can view attendance for their courses
CREATE POLICY "Faculty can view course attendance" ON attendance
    FOR SELECT
    USING (
        course_id IN (
            SELECT c.id FROM courses c
            WHERE c.faculty_id = (
                SELECT id FROM faculty WHERE user_id = auth.uid()
            )
        )
    );

-- Faculty can insert/update attendance for their courses
CREATE POLICY "Faculty can manage attendance" ON attendance
    FOR ALL
    USING (
        course_id IN (
            SELECT c.id FROM courses c
            WHERE c.faculty_id = (
                SELECT id FROM faculty WHERE user_id = auth.uid()
            )
        )
    );

-- Admins can view all attendance
CREATE POLICY "Admins can view all attendance" ON attendance
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- Admins can manage attendance
CREATE POLICY "Admins can manage attendance" ON attendance
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- MARKS TABLE POLICIES
-- ============================================

-- Students can view their own marks
CREATE POLICY "Students can view own marks" ON marks
    FOR SELECT
    USING (
        student_id = (
            SELECT id FROM students WHERE user_id = auth.uid()
        )
    );

-- Faculty can view marks for their courses
CREATE POLICY "Faculty can view course marks" ON marks
    FOR SELECT
    USING (
        course_id IN (
            SELECT c.id FROM courses c
            WHERE c.faculty_id = (
                SELECT id FROM faculty WHERE user_id = auth.uid()
            )
        )
    );

-- Faculty can insert/update marks for their courses
CREATE POLICY "Faculty can manage marks" ON marks
    FOR ALL
    USING (
        course_id IN (
            SELECT c.id FROM courses c
            WHERE c.faculty_id = (
                SELECT id FROM faculty WHERE user_id = auth.uid()
            )
        )
    );

-- Admins can view and manage all marks
CREATE POLICY "Admins can manage marks" ON marks
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- FEES TABLE POLICIES
-- ============================================

-- Students can view their own fees
CREATE POLICY "Students can view own fees" ON fees
    FOR SELECT
    USING (
        student_id = (
            SELECT id FROM students WHERE user_id = auth.uid()
        )
    );

-- Admins can view and manage all fees
CREATE POLICY "Admins can manage fees" ON fees
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- ASSIGNMENTS TABLE POLICIES
-- ============================================

-- Students can view published assignments for enrolled courses
CREATE POLICY "Students can view course assignments" ON assignments
    FOR SELECT
    USING (
        course_id IN (
            SELECT ce.course_id FROM course_enrollments ce
            JOIN students s ON ce.student_id = s.id
            WHERE s.user_id = auth.uid()
        )
        AND is_published = TRUE
    );

-- Faculty can view/manage their assignments
CREATE POLICY "Faculty can manage their assignments" ON assignments
    FOR ALL
    USING (
        faculty_id = (
            SELECT id FROM faculty WHERE user_id = auth.uid()
        )
    );

-- Admins can view all assignments
CREATE POLICY "Admins can view assignments" ON assignments
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- Admins can manage assignments
CREATE POLICY "Admins can manage assignments" ON assignments
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- ASSIGNMENT SUBMISSIONS TABLE POLICIES
-- ============================================

-- Students can view and submit their submissions
CREATE POLICY "Students can manage own submissions" ON assignment_submissions
    FOR ALL
    USING (
        student_id = (
            SELECT id FROM students WHERE user_id = auth.uid()
        )
    );

-- Faculty can view submissions for their assignments
CREATE POLICY "Faculty can view submissions" ON assignment_submissions
    FOR SELECT
    USING (
        assignment_id IN (
            SELECT id FROM assignments
            WHERE faculty_id = (
                SELECT id FROM faculty WHERE user_id = auth.uid()
            )
        )
    );

-- Faculty can grade submissions
CREATE POLICY "Faculty can grade submissions" ON assignment_submissions
    FOR UPDATE
    USING (
        assignment_id IN (
            SELECT id FROM assignments
            WHERE faculty_id = (
                SELECT id FROM faculty WHERE user_id = auth.uid()
            )
        )
    );

-- Admins can view all submissions
CREATE POLICY "Admins can view submissions" ON assignment_submissions
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- LEAVE REQUESTS TABLE POLICIES
-- ============================================

-- Students can view their own leave requests
CREATE POLICY "Students can manage own leave requests" ON leave_requests
    FOR ALL
    USING (
        student_id = (
            SELECT id FROM students WHERE user_id = auth.uid()
        )
    );

-- Faculty can view leave requests for their students
CREATE POLICY "Faculty can view leave requests" ON leave_requests
    FOR SELECT
    USING (
        student_id IN (
            SELECT s.id FROM students s
            WHERE s.department_id IN (
                SELECT department_id FROM faculty
                WHERE user_id = auth.uid()
            )
        )
    );

-- Faculty can approve/reject leave requests
CREATE POLICY "Faculty can approve leave requests" ON leave_requests
    FOR UPDATE
    USING (
        student_id IN (
            SELECT s.id FROM students s
            WHERE s.department_id IN (
                SELECT department_id FROM faculty
                WHERE user_id = auth.uid()
            )
        )
    );

-- Admins can view and manage all leave requests
CREATE POLICY "Admins can manage leave requests" ON leave_requests
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- TIMETABLE TABLE POLICIES
-- ============================================

-- All authenticated users can view timetable
CREATE POLICY "All users can view timetable" ON timetable
    FOR SELECT
    USING (auth.role() = 'authenticated');

-- Faculty can view their timetable
CREATE POLICY "Faculty can view their timetable" ON timetable
    FOR SELECT
    USING (
        faculty_id = (
            SELECT id FROM faculty WHERE user_id = auth.uid()
        )
    );

-- Admins can manage timetable
CREATE POLICY "Admins can manage timetable" ON timetable
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- NOTIFICATIONS TABLE POLICIES
-- ============================================

-- Users can view their own notifications
CREATE POLICY "Users can view own notifications" ON notifications
    FOR SELECT
    USING (user_id = auth.uid());

-- Users can update their own notifications
CREATE POLICY "Users can update own notifications" ON notifications
    FOR UPDATE
    USING (user_id = auth.uid());

-- ============================================
-- AUDIT LOGS TABLE POLICIES
-- ============================================

-- Admins can view audit logs
CREATE POLICY "Admins can view audit logs" ON audit_logs
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- COURSE ENROLLMENTS TABLE POLICIES
-- ============================================

-- Students can view their enrollments
CREATE POLICY "Students can view own enrollments" ON course_enrollments
    FOR SELECT
    USING (
        student_id = (
            SELECT id FROM students WHERE user_id = auth.uid()
        )
    );

-- Faculty can view student enrollments for their courses
CREATE POLICY "Faculty can view enrollments" ON course_enrollments
    FOR SELECT
    USING (
        course_id IN (
            SELECT c.id FROM courses c
            WHERE c.faculty_id = (
                SELECT id FROM faculty WHERE user_id = auth.uid()
            )
        )
    );

-- Admins can manage enrollments
CREATE POLICY "Admins can manage enrollments" ON course_enrollments
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid() AND u.role = 'admin'
        )
    );

-- ============================================
-- DEFAULT DENY POLICIES (Security Best Practice)
-- ============================================

-- Add restrictive DELETE policies
CREATE POLICY "No delete by default" ON users
    FOR DELETE
    USING (FALSE);

CREATE POLICY "No delete by default" ON students
    FOR DELETE
    USING (FALSE);

CREATE POLICY "No delete by default" ON faculty
    FOR DELETE
    USING (FALSE);
