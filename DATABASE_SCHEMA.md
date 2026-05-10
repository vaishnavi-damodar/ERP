# EduSync Database Documentation

## Database Overview

EduSync uses a normalized PostgreSQL database (hosted on Supabase) with 15 core tables designed for a college management system. The schema follows 3NF (Third Normal Form) with proper primary keys, foreign keys, and indexes for optimal performance.

## Entity Relationship Diagram (ER Diagram)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        EDUSYNC DATABASE STRUCTURE                               │
└─────────────────────────────────────────────────────────────────────────────────┘

                                    USERS (Central)
                                    ┌──────────────┐
                                    │ • id (PK)    │
                                    │ • email      │
                                    │ • name       │
                                    │ • role       │
                                    └──────┬───────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
            ┌─────────────────┐   ┌─────────────────┐   ┌──────────────┐
            │    STUDENTS     │   │    FACULTY      │   │ DEPARTMENTS  │
            │ • id (PK)       │   │ • id (PK)       │   │ • id (PK)    │
            │ • user_id (FK)  │   │ • user_id (FK)  │   │ • name       │
            │ • usn (UNIQUE)  │   │ • emp_id        │   │ • code       │
            │ • dept_id (FK)  │   │ • dept_id (FK)  │   │ • hod_name   │
            │ • semester      │   │ • designation   │   └──────────────┘
            │ • cgpa          │   │ • specialization│        ▲
            └────────┬────────┘   └────────┬────────┘        │
                     │                     │                 │
                     └──────────┬──────────┘                 │
                                │                            │
                                ▼                            │
                        ┌──────────────────┐                 │
                        │    COURSES       │◄────────────────┘
                        │ • id (PK)        │
                        │ • code (UNIQUE)  │
                        │ • name           │
                        │ • faculty_id(FK) │
                        │ • dept_id (FK)   │
                        │ • semester       │
                        └────────┬─────────┘
                                 │
                    ┌────────────┼────────────────┐
                    │            │                │
                    ▼            ▼                ▼
            ┌─────────────┐ ┌──────────┐ ┌──────────────────┐
            │ ATTENDANCE  │ │  MARKS   │ │ ASSIGNMENTS      │
            │ • id (PK)   │ │• id (PK) │ │• id (PK)         │
            │ • stud_id   │ │• stud_id │ │• course_id (FK)  │
            │ • course_id │ │• course_ │ │• faculty_id (FK) │
            │ • date      │ │  id (FK) │ │• due_date        │
            │ • status    │ │• marks   │ │• total_marks     │
            └─────────────┘ │• grade   │ └──────────────────┘
                            └──────────┘          │
                                                  ▼
                                    ┌──────────────────────────┐
                                    │ ASSIGNMENT_SUBMISSIONS   │
                                    │ • id (PK)                │
                                    │ • assign_id (FK)         │
                                    │ • stud_id (FK)           │
                                    │ • submit_date            │
                                    │ • marks_obtained         │
                                    └──────────────────────────┘

            ┌─────────────────────────┐      ┌──────────────┐
            │   LEAVE_REQUESTS        │      │  TIMETABLE   │
            │ • id (PK)               │      │ • id (PK)    │
            │ • student_id (FK)       │      │ • dept_id    │
            │ • start_date            │      │ • course_id  │
            │ • end_date              │      │ • faculty_id │
            │ • reason                │      │ • day        │
            │ • status                │      │ • time_slot  │
            │ • approved_by (FK)      │      └──────────────┘
            └─────────────────────────┘

                    ┌──────────┐         ┌─────────────┐
                    │  FEES    │         │NOTIFICATIONS│
                    │ • id (PK)│         │ • id (PK)   │
                    │ • stud_id│         │ • user_id   │
                    │ • semester        │ • message   │
                    │ • total  │         │ • read      │
                    │ • paid   │         └─────────────┘
                    │ • status │
                    └──────────┘

                    ┌───────────────┐
                    │  AUDIT_LOGS   │
                    │ • id (PK)     │
                    │ • user_id (FK)│
                    │ • action      │
                    │ • entity_type │
                    │ • timestamp   │
                    └───────────────┘
```

## Detailed Table Schema

### 1. USERS
**Base table for all role types**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| name | VARCHAR(255) | NOT NULL | User name |
| phone | VARCHAR(20) | | Phone number |
| role | VARCHAR(50) | CHECK, NOT NULL | admin/faculty/student |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| last_login | TIMESTAMP | | Last login time |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |

**Indexes:**
- `idx_users_email` (email) - Fast login lookups
- `idx_users_role` (role) - Filter by role
- `idx_users_is_active` (is_active) - Active users

---

### 2. DEPARTMENTS
**Organization structure**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Department ID |
| department_name | VARCHAR(100) | UNIQUE, NOT NULL | Department name |
| department_code | VARCHAR(10) | UNIQUE, NOT NULL | Code (e.g., CS, ECE) |
| hod_name | VARCHAR(100) | | Head of Department |
| contact_email | VARCHAR(100) | | Department email |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Relationships:**
- One-to-Many with STUDENTS
- One-to-Many with FACULTY
- One-to-Many with COURSES
- One-to-Many with TIMETABLE

---

### 3. STUDENTS
**Student information**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Student ID |
| user_id | UUID | FK(users), UNIQUE | User reference |
| usn | VARCHAR(20) | UNIQUE, NOT NULL | University Serial Number |
| department_id | UUID | FK(departments) | Department |
| semester | INTEGER | NOT NULL, CHECK (1-8) | Current semester |
| phone | VARCHAR(20) | | Student phone |
| date_of_birth | DATE | | DOB |
| address | TEXT | | Address |
| parent_contact | VARCHAR(20) | | Parent contact |
| enrollment_year | INTEGER | | Year of enrollment |
| cgpa | DECIMAL(4,2) | DEFAULT 0.0 | Cumulative GPA |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_students_usn` (usn) - Unique identifier
- `idx_students_department` (department_id) - Department queries
- `idx_students_semester` (semester) - Semester filter
- `idx_students_user_id` (user_id) - User mapping

**Relationships:**
- Many-to-One with USERS
- Many-to-One with DEPARTMENTS
- One-to-Many with ATTENDANCE
- One-to-Many with MARKS
- One-to-Many with FEES
- One-to-Many with LEAVE_REQUESTS
- Many-to-Many with COURSES (via COURSE_ENROLLMENTS)

---

### 4. FACULTY
**Faculty member information**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Faculty ID |
| user_id | UUID | FK(users), UNIQUE | User reference |
| department_id | UUID | FK(departments) | Department |
| designation | VARCHAR(100) | NOT NULL | Position/Title |
| employee_id | VARCHAR(50) | UNIQUE, NOT NULL | Employee ID |
| specialization | VARCHAR(200) | | Specialization |
| phone | VARCHAR(20) | | Office phone |
| office_location | VARCHAR(100) | | Office room |
| qualification | VARCHAR(200) | | Academic qualification |
| experience_years | INTEGER | DEFAULT 0 | Years of experience |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Relationships:**
- Many-to-One with DEPARTMENTS
- One-to-Many with COURSES
- One-to-Many with ASSIGNMENTS

---

### 5. COURSES
**Course catalog**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Course ID |
| course_name | VARCHAR(200) | NOT NULL | Course title |
| course_code | VARCHAR(20) | UNIQUE, NOT NULL | Code (e.g., CS301) |
| department_id | UUID | FK(departments) | Offering department |
| faculty_id | UUID | FK(faculty) | Assigned faculty |
| semester | INTEGER | NOT NULL, CHECK (1-8) | Semester offered |
| credits | INTEGER | DEFAULT 4 | Credit hours |
| description | TEXT | | Course description |
| total_lectures | INTEGER | DEFAULT 45 | Lecture hours |
| total_practicals | INTEGER | DEFAULT 0 | Practical hours |
| total_tutorials | INTEGER | DEFAULT 15 | Tutorial hours |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_courses_code` (course_code)
- `idx_courses_department` (department_id)
- `idx_courses_faculty` (faculty_id)
- `idx_courses_semester` (semester)

**Relationships:**
- Many-to-One with DEPARTMENTS
- Many-to-One with FACULTY
- One-to-Many with ATTENDANCE
- One-to-Many with MARKS
- One-to-Many with ASSIGNMENTS
- One-to-Many with TIMETABLE

---

### 6. ATTENDANCE
**Attendance records**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Record ID |
| student_id | UUID | FK(students) | Student |
| course_id | UUID | FK(courses) | Course |
| attendance_date | DATE | NOT NULL | Date |
| status | VARCHAR(20) | CHECK (present/absent/late/excused) | Status |
| remarks | TEXT | | Additional remarks |
| marked_by | UUID | FK(faculty) | Faculty who marked |
| marked_at | TIMESTAMP | DEFAULT NOW() | Marked time |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_attendance_student` (student_id)
- `idx_attendance_course` (course_id)
- `idx_attendance_date` (attendance_date)
- `idx_attendance_composite` (student_id, course_id, attendance_date) UNIQUE

---

### 7. MARKS
**Student marks and grades**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Record ID |
| student_id | UUID | FK(students) | Student |
| course_id | UUID | FK(courses) | Course |
| internal_marks | DECIMAL(5,2) | CHECK (0-20) | Internal assessment |
| assignment_marks | DECIMAL(5,2) | CHECK (0-10) | Assignment marks |
| practical_marks | DECIMAL(5,2) | CHECK (0-10) | Lab/Practical marks |
| semester_exam_marks | DECIMAL(5,2) | CHECK (0-60) | Final exam marks |
| total_marks | DECIMAL(6,2) | GENERATED | Auto-calculated |
| grade | VARCHAR(2) | | Letter grade |
| submitted_by | UUID | FK(faculty) | Faculty who submitted |
| submitted_at | TIMESTAMP | | Submission time |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Automatic Calculations:**
- `total_marks` = internal + assignment + practical + semester_exam
- `grade` based on total_marks:
  - A+ (90-100), A (80-89), B (70-79), C (60-69), D (50-59), F (<50)

**Indexes:**
- `idx_marks_student` (student_id)
- `idx_marks_course` (course_id)
- `idx_marks_composite` (student_id, course_id) UNIQUE

---

### 8. FEES
**Fee management**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Record ID |
| student_id | UUID | FK(students) | Student |
| semester | INTEGER | NOT NULL | Semester |
| total_fee | DECIMAL(10,2) | NOT NULL | Total amount |
| paid_fee | DECIMAL(10,2) | DEFAULT 0.0 | Paid amount |
| due_fee | DECIMAL(10,2) | GENERATED | total - paid |
| payment_status | VARCHAR(50) | CHECK (pending/partial/paid/overdue) | Status |
| due_date | DATE | | Payment deadline |
| payment_date | DATE | | Actual payment date |
| transaction_id | VARCHAR(100) | | Transaction reference |
| payment_method | VARCHAR(50) | | Online/Cash/Cheque |
| remarks | TEXT | | Comments |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Automatic Status Updates:**
- `paid_fee >= total_fee` → "paid"
- `paid_fee > 0` → "partial"
- `today > due_date AND paid_fee < total_fee` → "overdue"

---

### 9. ASSIGNMENTS
**Course assignments**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Assignment ID |
| course_id | UUID | FK(courses) | Course |
| faculty_id | UUID | FK(faculty) | Faculty creator |
| title | VARCHAR(255) | NOT NULL | Assignment title |
| description | TEXT | | Detailed description |
| file_url | VARCHAR(500) | | Document URL |
| file_name | VARCHAR(255) | | Original filename |
| due_date | TIMESTAMP | NOT NULL | Submission deadline |
| assignment_type | VARCHAR(50) | DEFAULT 'homework' | Type |
| total_marks | INTEGER | DEFAULT 10 | Max marks |
| is_published | BOOLEAN | DEFAULT FALSE | Published status |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_assignments_course` (course_id)
- `idx_assignments_faculty` (faculty_id)
- `idx_assignments_due_date` (due_date)

---

### 10. ASSIGNMENT_SUBMISSIONS
**Student submissions for assignments**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Submission ID |
| assignment_id | UUID | FK(assignments) | Assignment |
| student_id | UUID | FK(students) | Student |
| file_url | VARCHAR(500) | | Submitted file |
| file_name | VARCHAR(255) | | Filename |
| submission_date | TIMESTAMP | NOT NULL | Submission time |
| status | VARCHAR(50) | DEFAULT 'submitted' | Submission status |
| marks_obtained | DECIMAL(5,2) | | Marks awarded |
| feedback | TEXT | | Faculty feedback |
| graded_by | UUID | FK(faculty) | Grading faculty |
| graded_at | TIMESTAMP | | Grading time |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_submissions_assignment` (assignment_id)
- `idx_submissions_student` (student_id)
- `idx_submissions_composite` (assignment_id, student_id) UNIQUE

---

### 11. LEAVE_REQUESTS
**Leave/absence management**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Request ID |
| student_id | UUID | FK(students) | Student |
| start_date | DATE | NOT NULL | Leave from |
| end_date | DATE | NOT NULL | Leave until |
| reason | TEXT | NOT NULL | Reason |
| leave_type | VARCHAR(50) | CHECK (medical/personal/casual/others) | Type |
| attachment_url | VARCHAR(500) | | Supporting document |
| status | VARCHAR(50) | DEFAULT 'pending' CHECK | Request status |
| approved_by | UUID | FK(faculty) | Approving faculty |
| approval_remarks | TEXT | | Approval comments |
| approved_at | TIMESTAMP | | Approval time |
| applied_at | TIMESTAMP | DEFAULT NOW() | Application time |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_leave_student` (student_id)
- `idx_leave_status` (status)
- `idx_leave_date_range` (start_date, end_date)

---

### 12. TIMETABLE
**Class schedule**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Timetable ID |
| department_id | UUID | FK(departments) | Department |
| semester | INTEGER | NOT NULL | Semester |
| course_id | UUID | FK(courses) | Course |
| faculty_id | UUID | FK(faculty) | Faculty |
| day_of_week | VARCHAR(20) | CHECK (Monday-Saturday) | Day |
| start_time | TIME | NOT NULL | Start time |
| end_time | TIME | NOT NULL | End time |
| room_number | VARCHAR(50) | | Classroom/Lab |
| session_type | VARCHAR(50) | DEFAULT 'lecture' | lecture/practical/tutorial |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_timetable_department` (department_id)
- `idx_timetable_course` (course_id)
- `idx_timetable_faculty` (faculty_id)
- `idx_timetable_day` (day_of_week)

---

### 13. NOTIFICATIONS
**User notifications**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Notification ID |
| user_id | UUID | FK(users) | User |
| title | VARCHAR(255) | NOT NULL | Title |
| message | TEXT | | Message content |
| notification_type | VARCHAR(50) | | Type (info/alert/deadline) |
| is_read | BOOLEAN | DEFAULT FALSE | Read status |
| related_entity_id | UUID | | Related record ID |
| related_entity_type | VARCHAR(50) | | Entity type |
| action_url | VARCHAR(500) | | Link to action |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| read_at | TIMESTAMP | | Read time |

**Indexes:**
- `idx_notifications_user` (user_id)
- `idx_notifications_read` (is_read)
- `idx_notifications_created` (created_at)

---

### 14. AUDIT_LOGS
**Action audit trail**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Log ID |
| user_id | UUID | FK(users) | User who made change |
| action | VARCHAR(255) | NOT NULL | Action performed |
| entity_type | VARCHAR(100) | | Table/Entity |
| entity_id | UUID | | Record ID |
| old_values | JSONB | | Previous values |
| new_values | JSONB | | Updated values |
| ip_address | VARCHAR(45) | | IP address |
| user_agent | TEXT | | Browser info |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_audit_user` (user_id)
- `idx_audit_entity` (entity_type, entity_id)
- `idx_audit_created` (created_at)

---

### 15. COURSE_ENROLLMENTS
**Student-Course many-to-many mapping**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Enrollment ID |
| student_id | UUID | FK(students) | Student |
| course_id | UUID | FK(courses) | Course |
| enrollment_date | TIMESTAMP | DEFAULT NOW() | Enrollment date |
| status | VARCHAR(50) | DEFAULT 'enrolled' | enrolled/dropped/completed |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_enrollments_student` (student_id)
- `idx_enrollments_course` (course_id)
- `idx_enrollments_composite` (student_id, course_id) UNIQUE

---

## Database Views

### 1. student_performance
Analytics for student performance tracking

```sql
SELECT 
    s.id,
    s.usn,
    u.name,
    AVG(m.total_marks) as avg_marks,
    COUNT(DISTINCT m.course_id) as courses_completed,
    AVG(CAST(m.grade AS FLOAT)) as avg_grade,
    (attendance_percentage) -- calculated
FROM students, marks, attendance...
```

### 2. faculty_workload
Faculty productivity metrics

```sql
SELECT 
    f.id,
    u.name,
    COUNT(DISTINCT c.id) as courses_assigned,
    COUNT(DISTINCT a.id) as assignments_given,
    COUNT(DISTINCT m.id) as marks_submitted
FROM faculty...
```

### 3. department_statistics
Department-level analytics

```sql
SELECT 
    d.id,
    d.department_name,
    COUNT(DISTINCT s.id) as total_students,
    COUNT(DISTINCT f.id) as total_faculty,
    AVG(m.total_marks) as avg_marks
FROM departments...
```

---

## Key Database Constraints & Rules

### Primary Key Constraints
- Every table has a UUID primary key
- Ensures uniqueness and referential integrity

### Foreign Key Constraints
- `ON DELETE CASCADE` for dependent records
- `ON DELETE SET NULL` for optional references
- Maintains referential integrity

### CHECK Constraints
- `semester` BETWEEN 1 AND 8
- `role` IN ('admin', 'faculty', 'student')
- Attendance status validation
- Mark range validation (0-100)

### UNIQUE Constraints
- `users.email` - No duplicate emails
- `students.usn` - Unique student number
- `faculty.employee_id` - Unique employee ID
- `courses.course_code` - Unique course codes
- `departments.department_code` - Unique codes

### Default Values
- `is_active` defaults to TRUE
- `created_at` and `updated_at` default to NOW()
- Automatic timestamp updates via triggers

---

## Normalization

The schema follows **3NF (Third Normal Form)**:

✓ **1NF (First Normal Form)**
- Atomic values only
- No repeating groups
- Single value per cell

✓ **2NF (Second Normal Form)**
- 1NF compliance
- No partial dependencies
- All non-key attributes dependent on entire primary key

✓ **3NF (Third Normal Form)**
- 2NF compliance
- No transitive dependencies
- Non-key attributes not dependent on other non-key attributes

---

## Performance Optimization

### Indexes Strategy
- Foreign keys indexed for faster joins
- Email indexed for login queries
- Date columns indexed for range queries
- Composite indexes for common query combinations

### Query Optimization
- Use appropriate indexes
- Avoid full table scans
- Use views for complex aggregations
- Implement pagination for large result sets

### Connection Pooling
- Supabase handles connection pooling
- Max connections: 10 (free tier)
- Use connection pooling for backend

---

## Security Features

### Row-Level Security (RLS)
Enabled on all tables with policies:
- Students can only see their own data
- Faculty can see assigned courses/students
- Admins have full access

### Data Encryption
- Passwords hashed with bcrypt
- Sensitive data encrypted at rest (Supabase)
- HTTPS for all connections

### Audit Logging
- All modifications logged in `audit_logs`
- User tracking for accountability
- Timestamp and IP recording

---

## Data Relationships Summary

| Relationship | Type | Table 1 | Table 2 |
|--------------|------|---------|---------|
| User-Student | 1:1 | users | students |
| User-Faculty | 1:1 | users | faculty |
| Dept-Student | 1:M | departments | students |
| Dept-Faculty | 1:M | departments | faculty |
| Dept-Course | 1:M | departments | courses |
| Faculty-Course | 1:M | faculty | courses |
| Course-Attendance | 1:M | courses | attendance |
| Course-Marks | 1:M | courses | marks |
| Course-Assignment | 1:M | courses | assignments |
| Student-Attendance | 1:M | students | attendance |
| Student-Marks | 1:M | students | marks |
| Student-Fees | 1:M | students | fees |
| Student-Leave | 1:M | students | leave_requests |
| Student-Course | M:M | students | courses |
| Faculty-Assignment | 1:M | faculty | assignments |

---

## Backup & Recovery

**Supabase Backup Strategy:**
- Automatic daily backups
- 7-day retention (free tier)
- 30-day retention (paid tier)
- Point-in-time recovery available

**Manual Backup:**
```bash
pg_dump -h <supabase-host> -U postgres -d postgres > backup.sql
```

**Restore:**
```bash
psql -h <supabase-host> -U postgres -d postgres < backup.sql
```

---

## Database Maintenance

### Regular Tasks
- Monitor table sizes
- Analyze query performance
- Update statistics
- Vacuum and analyze tables

### Supabase Maintenance
- Monitor API usage
- Review RLS policies
- Check storage usage
- Review logs

---

## Additional Notes

- All timestamps are in UTC
- Timezone handling in application layer
- Phone numbers stored as strings (international support)
- Addresses stored as text for flexibility
- JSONB used for flexible logging
- Enum-like CHECK constraints for fixed options

---

**Database Last Updated**: May 2026
**Version**: 1.0.0
**Schema Status**: Production Ready
