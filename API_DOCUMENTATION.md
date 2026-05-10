# EduSync API Documentation

**Base URL**: `http://localhost:8000/api/v1`  
**Documentation**: `http://localhost:8000/docs` (Swagger UI)  
**ReDoc**: `http://localhost:8000/redoc`

---

## Authentication Endpoints

### 1. User Signup
**Endpoint**: `POST /auth/signup`

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "securepassword123",
  "role": "student"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Error Responses**:
- `400 Bad Request`: Email already registered, validation error
- `422 Unprocessable Entity`: Invalid input

---

### 2. User Login
**Endpoint**: `POST /auth/login`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid credentials

---

### 3. Refresh Token
**Endpoint**: `POST /auth/refresh`

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### 4. Get Current User
**Endpoint**: `GET /auth/me`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200):
```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "user@example.com",
  "phone": "9876543210",
  "role": "student",
  "is_active": true,
  "last_login": "2024-05-09T10:30:00",
  "created_at": "2024-01-15T08:00:00",
  "updated_at": "2024-05-09T10:30:00"
}
```

---

## Admin Endpoints

All admin endpoints require `Authorization: Bearer {access_token}` header with admin role.

### Students Management

#### Get All Students
**Endpoint**: `GET /admin/students`

**Query Parameters**:
- `skip` (integer, default: 0) - Pagination offset
- `limit` (integer, default: 10) - Pagination limit
- `department_id` (string, optional) - Filter by department
- `semester` (integer, optional) - Filter by semester

**Response** (200):
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "usn": "CS21001",
    "department_id": "uuid",
    "semester": 4,
    "phone": "9876543210",
    "cgpa": 7.8,
    "is_active": true,
    "user": {
      "id": "uuid",
      "name": "Arjun Kumar",
      "email": "arjun@example.com",
      "role": "student"
    }
  }
]
```

---

#### Create Student
**Endpoint**: `POST /admin/students`

**Request Body**:
```json
{
  "user_id": "uuid",
  "usn": "CS21001",
  "department_id": "uuid",
  "semester": 4,
  "phone": "9876543210",
  "address": "123 Main St, City"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "usn": "CS21001",
  "department_id": "uuid",
  "semester": 4,
  "cgpa": 0.0,
  "is_active": true
}
```

---

#### Get Student
**Endpoint**: `GET /admin/students/{student_id}`

**Response** (200):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "usn": "CS21001",
  "department_id": "uuid",
  "semester": 4,
  "phone": "9876543210",
  "cgpa": 7.8,
  "is_active": true
}
```

---

#### Update Student
**Endpoint**: `PUT /admin/students/{student_id}`

**Request Body** (all fields optional):
```json
{
  "semester": 5,
  "phone": "9876543211",
  "address": "456 Park Ave, City"
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "usn": "CS21001",
  "semester": 5,
  "phone": "9876543211",
  "address": "456 Park Ave, City"
}
```

---

#### Delete Student
**Endpoint**: `DELETE /admin/students/{student_id}`

**Response** (200):
```json
{
  "message": "Student deleted successfully"
}
```

---

### Faculty Management

#### Get All Faculty
**Endpoint**: `GET /admin/faculty`

**Query Parameters**:
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)
- `department_id` (string, optional)

**Response** (200):
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "department_id": "uuid",
    "designation": "Associate Professor",
    "employee_id": "EMP001",
    "specialization": "Data Structures",
    "experience_years": 12,
    "is_active": true
  }
]
```

---

#### Create Faculty
**Endpoint**: `POST /admin/faculty`

**Request Body**:
```json
{
  "user_id": "uuid",
  "department_id": "uuid",
  "designation": "Assistant Professor",
  "employee_id": "EMP002",
  "specialization": "Database Systems",
  "experience_years": 8
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "department_id": "uuid",
  "designation": "Assistant Professor",
  "employee_id": "EMP002",
  "experience_years": 8
}
```

---

### Departments Management

#### Get All Departments
**Endpoint**: `GET /admin/departments`

**Response** (200):
```json
[
  {
    "id": "uuid",
    "department_name": "Computer Science",
    "department_code": "CS",
    "hod_name": "Dr. John Smith",
    "contact_email": "cs@edusync.edu",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

#### Create Department
**Endpoint**: `POST /admin/departments`

**Request Body**:
```json
{
  "department_name": "Electronics",
  "department_code": "ECE",
  "hod_name": "Dr. Jane Doe",
  "contact_email": "ece@edusync.edu"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "department_name": "Electronics",
  "department_code": "ECE",
  "hod_name": "Dr. Jane Doe",
  "contact_email": "ece@edusync.edu"
}
```

---

#### Update Department
**Endpoint**: `PUT /admin/departments/{dept_id}`

**Request Body** (optional fields):
```json
{
  "department_name": "Electronics and Communication",
  "hod_name": "Dr. Jane Smith"
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "department_name": "Electronics and Communication",
  "department_code": "ECE",
  "hod_name": "Dr. Jane Smith"
}
```

---

### Courses Management

#### Get All Courses
**Endpoint**: `GET /admin/courses`

**Query Parameters**:
- `department_id` (string, optional)
- `semester` (integer, optional)

**Response** (200):
```json
[
  {
    "id": "uuid",
    "course_name": "Data Structures",
    "course_code": "CS301",
    "department_id": "uuid",
    "faculty_id": "uuid",
    "semester": 4,
    "credits": 4,
    "is_active": true
  }
]
```

---

#### Create Course
**Endpoint**: `POST /admin/courses`

**Request Body**:
```json
{
  "course_name": "Database Management",
  "course_code": "CS302",
  "department_id": "uuid",
  "faculty_id": "uuid",
  "semester": 4,
  "credits": 4,
  "description": "Comprehensive study of DBMS"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "course_name": "Database Management",
  "course_code": "CS302",
  "semester": 4,
  "credits": 4
}
```

---

#### Update Course
**Endpoint**: `PUT /admin/courses/{course_id}`

**Request Body** (optional fields):
```json
{
  "faculty_id": "uuid",
  "credits": 3
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "course_name": "Database Management",
  "course_code": "CS302",
  "credits": 3
}
```

---

### Analytics

#### Get System Analytics
**Endpoint**: `GET /admin/analytics/overview`

**Response** (200):
```json
{
  "total_students": 150,
  "total_faculty": 25,
  "total_departments": 5,
  "total_courses": 45,
  "department_stats": [
    {
      "id": "uuid",
      "department_name": "Computer Science",
      "total_students": 60,
      "total_faculty": 12,
      "total_courses": 20,
      "avg_department_marks": 75.5
    }
  ],
  "faculty_workload": [
    {
      "id": "uuid",
      "name": "Dr. Patel",
      "employee_id": "EMP001",
      "courses_assigned": 3,
      "total_assignments": 12,
      "marks_submitted": 150
    }
  ]
}
```

---

## Faculty Endpoints

All faculty endpoints require `Authorization: Bearer {access_token}` header with faculty role.

### Attendance Management

#### Get Attendance
**Endpoint**: `GET /faculty/attendance`

**Query Parameters**:
- `course_id` (string, optional)
- `start_date` (date, optional)
- `end_date` (date, optional)

**Response** (200):
```json
[
  {
    "id": "uuid",
    "student_id": "uuid",
    "course_id": "uuid",
    "attendance_date": "2024-05-09",
    "status": "present",
    "marked_by": "uuid",
    "marked_at": "2024-05-09T10:00:00"
  }
]
```

---

#### Mark Attendance
**Endpoint**: `POST /faculty/attendance`

**Request Body**:
```json
{
  "student_id": "uuid",
  "course_id": "uuid",
  "attendance_date": "2024-05-09",
  "status": "present",
  "remarks": "Present in class"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "student_id": "uuid",
  "course_id": "uuid",
  "attendance_date": "2024-05-09",
  "status": "present"
}
```

---

#### Update Attendance
**Endpoint**: `PUT /faculty/attendance/{attendance_id}`

**Request Body**:
```json
{
  "status": "late",
  "remarks": "Marked late entry"
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "status": "late",
  "remarks": "Marked late entry"
}
```

---

### Marks Management

#### Upload Marks
**Endpoint**: `POST /faculty/marks`

**Request Body**:
```json
{
  "student_id": "uuid",
  "course_id": "uuid",
  "internal_marks": 18,
  "assignment_marks": 9,
  "practical_marks": 8,
  "semester_exam_marks": 55
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "student_id": "uuid",
  "course_id": "uuid",
  "internal_marks": 18,
  "assignment_marks": 9,
  "practical_marks": 8,
  "semester_exam_marks": 55,
  "total_marks": 90,
  "grade": "A+"
}
```

---

#### Update Marks
**Endpoint**: `PUT /faculty/marks/{marks_id}`

**Request Body** (optional fields):
```json
{
  "internal_marks": 19,
  "semester_exam_marks": 58
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "total_marks": 94,
  "grade": "A+"
}
```

---

### Assignments

#### Get Faculty Assignments
**Endpoint**: `GET /faculty/assignments`

**Response** (200):
```json
[
  {
    "id": "uuid",
    "course_id": "uuid",
    "faculty_id": "uuid",
    "title": "Database Design Project",
    "description": "Design a relational database",
    "due_date": "2024-05-20T23:59:59",
    "total_marks": 10,
    "is_published": true
  }
]
```

---

#### Create Assignment
**Endpoint**: `POST /faculty/assignments`

**Request Body**:
```json
{
  "course_id": "uuid",
  "title": "SQL Query Optimization",
  "description": "Optimize complex SQL queries",
  "due_date": "2024-05-25T23:59:59",
  "assignment_type": "homework",
  "total_marks": 10
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "course_id": "uuid",
  "title": "SQL Query Optimization",
  "due_date": "2024-05-25T23:59:59",
  "total_marks": 10
}
```

---

#### Update Assignment
**Endpoint**: `PUT /faculty/assignments/{assignment_id}`

**Request Body** (optional fields):
```json
{
  "title": "SQL Query Optimization - Updated",
  "due_date": "2024-05-26T23:59:59",
  "is_published": true
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "title": "SQL Query Optimization - Updated",
  "due_date": "2024-05-26T23:59:59",
  "is_published": true
}
```

---

### Faculty Courses

#### Get Faculty Courses
**Endpoint**: `GET /faculty/courses`

**Response** (200):
```json
[
  {
    "id": "uuid",
    "course_name": "Data Structures",
    "course_code": "CS301",
    "semester": 4,
    "credits": 4,
    "department_id": "uuid",
    "faculty_id": "uuid",
    "is_active": true
  }
]
```

---

### Faculty Analytics

#### Get Performance Analytics
**Endpoint**: `GET /faculty/analytics/performance`

**Query Parameters**:
- `course_id` (string, optional)

**Response** (200):
```json
{
  "students": [
    {
      "id": "uuid",
      "usn": "CS21001",
      "name": "Arjun Kumar",
      "avg_marks": 82.5,
      "courses_completed": 5,
      "avg_grade": 4.0,
      "attendance_percentage": 95.5
    }
  ],
  "average_performance": 78.3
}
```

---

## Student Endpoints

All student endpoints require `Authorization: Bearer {access_token}` header with student role.

### Student Profile

#### Get Student Profile
**Endpoint**: `GET /student/profile`

**Response** (200):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "usn": "CS21001",
  "department_id": "uuid",
  "semester": 4,
  "phone": "9876543210",
  "cgpa": 8.2,
  "is_active": true,
  "user": {
    "name": "Arjun Kumar",
    "email": "arjun@example.com",
    "role": "student"
  }
}
```

---

#### Get Dashboard
**Endpoint**: `GET /student/dashboard`

**Response** (200):
```json
{
  "attendance_percentage": 92.5,
  "average_marks": 78.5,
  "total_courses": 6,
  "fees_paid": 25000,
  "total_fees": 50000,
  "pending_leave_requests": 1
}
```

---

#### Update Profile
**Endpoint**: `PUT /student/profile`

**Request Body** (optional fields):
```json
{
  "phone": "9876543211",
  "address": "New address"
}
```

**Response** (200):
```json
{
  "message": "Profile updated successfully"
}
```

---

### Student Attendance

#### Get Student Attendance
**Endpoint**: `GET /student/attendance`

**Response** (200):
```json
[
  {
    "id": "uuid",
    "student_id": "uuid",
    "course_id": "uuid",
    "attendance_date": "2024-05-09",
    "status": "present",
    "marked_at": "2024-05-09T10:00:00"
  }
]
```

---

### Student Marks

#### Get Student Marks
**Endpoint**: `GET /student/marks`

**Response** (200):
```json
[
  {
    "id": "uuid",
    "student_id": "uuid",
    "course_id": "uuid",
    "internal_marks": 18,
    "assignment_marks": 9,
    "practical_marks": 8,
    "semester_exam_marks": 55,
    "total_marks": 90,
    "grade": "A+"
  }
]
```

---

### Student Assignments

#### Get Student Assignments
**Endpoint**: `GET /student/assignments`

**Response** (200):
```json
[
  {
    "id": "uuid",
    "course_id": "uuid",
    "title": "Database Design Project",
    "description": "Design a database",
    "due_date": "2024-05-20T23:59:59",
    "total_marks": 10,
    "is_published": true
  }
]
```

---

### Student Fees

#### Get Student Fees
**Endpoint**: `GET /student/fees`

**Response** (200):
```json
[
  {
    "id": "uuid",
    "student_id": "uuid",
    "semester": 4,
    "total_fee": 50000,
    "paid_fee": 25000,
    "due_fee": 25000,
    "payment_status": "partial",
    "due_date": "2024-05-31",
    "transaction_id": "TRX123456"
  }
]
```

---

### Student Timetable

#### Get Student Timetable
**Endpoint**: `GET /student/timetable`

**Response** (200):
```json
[
  {
    "id": "uuid",
    "course_id": "uuid",
    "day_of_week": "Monday",
    "start_time": "09:00:00",
    "end_time": "10:30:00",
    "room_number": "A-101",
    "session_type": "lecture"
  }
]
```

---

### Student Leave Requests

#### Get Leave Requests
**Endpoint**: `GET /student/leave-requests`

**Response** (200):
```json
[
  {
    "id": "uuid",
    "student_id": "uuid",
    "start_date": "2024-05-15",
    "end_date": "2024-05-17",
    "reason": "Medical treatment",
    "leave_type": "medical",
    "status": "pending",
    "applied_at": "2024-05-09T10:00:00"
  }
]
```

---

#### Apply For Leave
**Endpoint**: `POST /student/leave-requests`

**Request Body**:
```json
{
  "start_date": "2024-05-15",
  "end_date": "2024-05-17",
  "reason": "Medical treatment",
  "leave_type": "medical"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "start_date": "2024-05-15",
  "end_date": "2024-05-17",
  "reason": "Medical treatment",
  "leave_type": "medical",
  "status": "pending"
}
```

---

## Error Handling

### Standard Error Response

```json
{
  "detail": "Error message",
  "status_code": 400,
  "timestamp": "2024-05-09T10:30:00"
}
```

### Common Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## Rate Limiting

- **Limit**: 100 requests per minute
- **Header**: `X-RateLimit-Remaining`
- **Reset Time**: `X-RateLimit-Reset`

---

## Authentication

All protected endpoints require:
```
Authorization: Bearer {access_token}
```

### Token Structure
```
{
  "sub": "user_id",
  "email": "user@example.com",
  "role": "admin|faculty|student",
  "exp": 1715000000,
  "iat": 1714913600
}
```

---

## Request/Response Examples

### Example: Complete Login Flow

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@edusync.edu",
    "password": "admin123"
  }'

# Response:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "token_type": "bearer"
# }

# 2. Use token to get students
curl -X GET "http://localhost:8000/api/v1/admin/students?skip=0&limit=10" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

**API Documentation Last Updated**: May 2026
**Version**: 1.0.0
**Status**: Production Ready
