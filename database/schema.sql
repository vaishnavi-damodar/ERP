-- ============================================
-- EDUSYNC DATABASE SCHEMA
-- College ERP System with Supabase PostgreSQL
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. DEPARTMENTS TABLE
-- ============================================
CREATE TABLE departments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    department_name VARCHAR(100) NOT NULL UNIQUE,
    department_code VARCHAR(10) NOT NULL UNIQUE,
    hod_name VARCHAR(100),
    contact_email VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_departments_code ON departments(department_code);

-- ============================================
-- 2. USERS TABLE (Base for all roles)
-- ============================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'faculty', 'student')),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

-- ============================================
-- 3. STUDENTS TABLE
-- ============================================
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    usn VARCHAR(20) NOT NULL UNIQUE,
    department_id UUID NOT NULL REFERENCES departments(id),
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    phone VARCHAR(20),
    date_of_birth DATE,
    address TEXT,
    parent_contact VARCHAR(20),
    enrollment_year INTEGER,
    cgpa DECIMAL(4, 2) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_students_usn ON students(usn);
CREATE INDEX idx_students_department ON students(department_id);
CREATE INDEX idx_students_semester ON students(semester);
CREATE INDEX idx_students_user_id ON students(user_id);

-- ============================================
-- 4. FACULTY TABLE
-- ============================================
CREATE TABLE faculty (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    department_id UUID NOT NULL REFERENCES departments(id),
    designation VARCHAR(100) NOT NULL,
    employee_id VARCHAR(50) NOT NULL UNIQUE,
    specialization VARCHAR(200),
    phone VARCHAR(20),
    office_location VARCHAR(100),
    qualification VARCHAR(200),
    experience_years INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_faculty_department ON faculty(department_id);
CREATE INDEX idx_faculty_employee_id ON faculty(employee_id);
CREATE INDEX idx_faculty_user_id ON faculty(user_id);

-- ============================================
-- 5. COURSES TABLE
-- ============================================
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_name VARCHAR(200) NOT NULL,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    department_id UUID NOT NULL REFERENCES departments(id),
    faculty_id UUID REFERENCES faculty(id) ON DELETE SET NULL,
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    credits INTEGER NOT NULL DEFAULT 4,
    description TEXT,
    total_lectures INTEGER DEFAULT 45,
    total_practicals INTEGER DEFAULT 0,
    total_tutorials INTEGER DEFAULT 15,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_courses_code ON courses(course_code);
CREATE INDEX idx_courses_department ON courses(department_id);
CREATE INDEX idx_courses_faculty ON courses(faculty_id);
CREATE INDEX idx_courses_semester ON courses(semester);

-- ============================================
-- 6. ATTENDANCE TABLE
-- ============================================
CREATE TABLE attendance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    attendance_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'absent', 'late', 'excused')),
    remarks TEXT,
    marked_by UUID REFERENCES faculty(id),
    marked_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_attendance_student ON attendance(student_id);
CREATE INDEX idx_attendance_course ON attendance(course_id);
CREATE INDEX idx_attendance_date ON attendance(attendance_date);
CREATE INDEX idx_attendance_unique ON attendance(student_id, course_id, attendance_date);

-- ============================================
-- 7. MARKS TABLE
-- ============================================
CREATE TABLE marks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    internal_marks DECIMAL(5, 2) CHECK (internal_marks BETWEEN 0 AND 20),
    assignment_marks DECIMAL(5, 2) CHECK (assignment_marks BETWEEN 0 AND 10),
    practical_marks DECIMAL(5, 2) CHECK (practical_marks BETWEEN 0 AND 10),
    semester_exam_marks DECIMAL(5, 2) CHECK (semester_exam_marks BETWEEN 0 AND 60),
    total_marks DECIMAL(6, 2),
    grade VARCHAR(2),
    submitted_by UUID REFERENCES faculty(id),
    submitted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_marks_student ON marks(student_id);
CREATE INDEX idx_marks_course ON marks(course_id);
CREATE INDEX idx_marks_unique ON marks(student_id, course_id);

-- ============================================
-- 8. FEES TABLE
-- ============================================
CREATE TABLE fees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    semester INTEGER NOT NULL,
    total_fee DECIMAL(10, 2) NOT NULL,
    paid_fee DECIMAL(10, 2) DEFAULT 0.0,
    due_fee DECIMAL(10, 2),
    payment_status VARCHAR(50) NOT NULL CHECK (payment_status IN ('pending', 'partial', 'paid', 'overdue')),
    due_date DATE,
    payment_date DATE,
    transaction_id VARCHAR(100),
    payment_method VARCHAR(50),
    remarks TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_fees_student ON fees(student_id);
CREATE INDEX idx_fees_status ON fees(payment_status);
CREATE INDEX idx_fees_semester ON fees(semester);

-- ============================================
-- 9. ASSIGNMENTS TABLE
-- ============================================
CREATE TABLE assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    faculty_id UUID NOT NULL REFERENCES faculty(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_url VARCHAR(500),
    file_name VARCHAR(255),
    due_date TIMESTAMP NOT NULL,
    assignment_type VARCHAR(50) DEFAULT 'homework',
    total_marks INTEGER DEFAULT 10,
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_assignments_course ON assignments(course_id);
CREATE INDEX idx_assignments_faculty ON assignments(faculty_id);
CREATE INDEX idx_assignments_due_date ON assignments(due_date);

-- ============================================
-- 10. ASSIGNMENT SUBMISSIONS TABLE
-- ============================================
CREATE TABLE assignment_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assignment_id UUID NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    file_url VARCHAR(500),
    file_name VARCHAR(255),
    submission_date TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'submitted',
    marks_obtained DECIMAL(5, 2),
    feedback TEXT,
    graded_by UUID REFERENCES faculty(id),
    graded_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_submissions_assignment ON assignment_submissions(assignment_id);
CREATE INDEX idx_submissions_student ON assignment_submissions(student_id);
CREATE INDEX idx_submissions_unique ON assignment_submissions(assignment_id, student_id);

-- ============================================
-- 11. LEAVE REQUESTS TABLE
-- ============================================
CREATE TABLE leave_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    leave_type VARCHAR(50) NOT NULL CHECK (leave_type IN ('medical', 'personal', 'casual', 'others')),
    attachment_url VARCHAR(500),
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    approved_by UUID REFERENCES faculty(id),
    approval_remarks TEXT,
    approved_at TIMESTAMP,
    applied_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_leave_student ON leave_requests(student_id);
CREATE INDEX idx_leave_status ON leave_requests(status);
CREATE INDEX idx_leave_date_range ON leave_requests(start_date, end_date);

-- ============================================
-- 12. TIMETABLE TABLE
-- ============================================
CREATE TABLE timetable (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    department_id UUID NOT NULL REFERENCES departments(id),
    semester INTEGER NOT NULL,
    course_id UUID NOT NULL REFERENCES courses(id),
    faculty_id UUID REFERENCES faculty(id),
    day_of_week VARCHAR(20) NOT NULL CHECK (day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_number VARCHAR(50),
    session_type VARCHAR(50) DEFAULT 'lecture',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_timetable_department ON timetable(department_id);
CREATE INDEX idx_timetable_course ON timetable(course_id);
CREATE INDEX idx_timetable_faculty ON timetable(faculty_id);
CREATE INDEX idx_timetable_day ON timetable(day_of_week);

-- ============================================
-- 13. NOTIFICATIONS TABLE
-- ============================================
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    notification_type VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    related_entity_id UUID,
    related_entity_type VARCHAR(50),
    action_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    read_at TIMESTAMP
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);
CREATE INDEX idx_notifications_created ON notifications(created_at);

-- ============================================
-- 14. AUDIT LOGS TABLE
-- ============================================
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at);

-- ============================================
-- 15. COURSE ENROLLMENT TABLE
-- ============================================
CREATE TABLE course_enrollments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    enrollment_date TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'enrolled' CHECK (status IN ('enrolled', 'dropped', 'completed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_enrollments_student ON course_enrollments(student_id);
CREATE INDEX idx_enrollments_course ON course_enrollments(course_id);
CREATE INDEX idx_enrollments_unique ON course_enrollments(student_id, course_id);

-- ============================================
-- VIEWS FOR ANALYTICS
-- ============================================

-- Student Performance View
CREATE VIEW student_performance AS
SELECT 
    s.id,
    s.usn,
    u.name,
    ROUND(AVG(m.total_marks), 2) as avg_marks,
    COUNT(DISTINCT m.course_id) as courses_completed,
    ROUND(AVG(m.total_marks) / 25, 2) as avg_gpa,
    (SELECT ROUND(COUNT(*) * 100.0 / 
        NULLIF(COUNT(*), 0), 2)
     FROM attendance a 
     WHERE a.student_id = s.id AND a.status IN ('present', 'late')) as attendance_percentage
FROM students s
JOIN users u ON s.user_id = u.id
LEFT JOIN marks m ON s.id = m.student_id
GROUP BY s.id, s.usn, u.name;

-- Faculty Workload View
CREATE VIEW faculty_workload AS
SELECT 
    f.id,
    u.name,
    f.employee_id,
    COUNT(DISTINCT c.id) as courses_assigned,
    COUNT(DISTINCT a.id) as total_assignments,
    COUNT(DISTINCT m.id) as marks_submitted
FROM faculty f
JOIN users u ON f.user_id = u.id
LEFT JOIN courses c ON f.id = c.faculty_id
LEFT JOIN assignments a ON f.id = a.faculty_id
LEFT JOIN marks m ON f.id = m.submitted_by
GROUP BY f.id, u.name, f.employee_id;

-- Department Statistics View
CREATE VIEW department_statistics AS
SELECT 
    d.id,
    d.department_name,
    COUNT(DISTINCT s.id) as total_students,
    COUNT(DISTINCT f.id) as total_faculty,
    COUNT(DISTINCT c.id) as total_courses,
    ROUND(AVG(m.total_marks), 2) as avg_department_marks
FROM departments d
LEFT JOIN students s ON d.id = s.department_id
LEFT JOIN faculty f ON d.id = f.department_id
LEFT JOIN courses c ON d.id = c.department_id
LEFT JOIN marks m ON c.id = m.course_id
GROUP BY d.id, d.department_name;

-- ============================================
-- FUNCTIONS FOR CALCULATIONS
-- ============================================

-- Function to calculate total marks
CREATE OR REPLACE FUNCTION calculate_total_marks()
RETURNS TRIGGER AS $$
BEGIN
    NEW.total_marks := COALESCE(NEW.internal_marks, 0) + 
                       COALESCE(NEW.assignment_marks, 0) + 
                       COALESCE(NEW.practical_marks, 0) + 
                       COALESCE(NEW.semester_exam_marks, 0);
    
    -- Assign grade based on total marks
    IF NEW.total_marks >= 90 THEN
        NEW.grade := 'A+';
    ELSIF NEW.total_marks >= 80 THEN
        NEW.grade := 'A';
    ELSIF NEW.total_marks >= 70 THEN
        NEW.grade := 'B';
    ELSIF NEW.total_marks >= 60 THEN
        NEW.grade := 'C';
    ELSIF NEW.total_marks >= 50 THEN
        NEW.grade := 'D';
    ELSE
        NEW.grade := 'F';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for marks calculation
CREATE TRIGGER marks_calculation_trigger
BEFORE INSERT OR UPDATE ON marks
FOR EACH ROW
EXECUTE FUNCTION calculate_total_marks();

-- Function to update due_fee
CREATE OR REPLACE FUNCTION update_due_fee()
RETURNS TRIGGER AS $$
BEGIN
    NEW.due_fee := NEW.total_fee - NEW.paid_fee;
    
    -- Update payment status
    IF NEW.paid_fee >= NEW.total_fee THEN
        NEW.payment_status := 'paid';
    ELSIF NEW.paid_fee > 0 THEN
        NEW.payment_status := 'partial';
    ELSIF CURRENT_DATE > NEW.due_date THEN
        NEW.payment_status := 'overdue';
    ELSE
        NEW.payment_status := 'pending';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for fee calculation
CREATE TRIGGER fee_calculation_trigger
BEFORE INSERT OR UPDATE ON fees
FOR EACH ROW
EXECUTE FUNCTION update_due_fee();

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX idx_attendance_composite ON attendance(student_id, course_id, attendance_date);
CREATE INDEX idx_marks_composite ON marks(student_id, course_id);
CREATE INDEX idx_fees_composite ON fees(student_id, semester);
CREATE INDEX idx_assignments_composite ON assignments(course_id, due_date);

-- ============================================
-- GRANTS (For Supabase RLS)
-- ============================================

GRANT USAGE ON SCHEMA public TO authenticated;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO authenticated;
