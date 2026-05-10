"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

# ============================================
# Enums
# ============================================

class RoleEnum(str, Enum):
    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"

class AttendanceStatusEnum(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"

class LeaveTypeEnum(str, Enum):
    MEDICAL = "medical"
    PERSONAL = "personal"
    CASUAL = "casual"
    OTHERS = "others"

class LeaveStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class PaymentStatusEnum(str, Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"

# ============================================
# Auth Schemas
# ============================================

class SignupRequest(BaseModel):
    """User signup request"""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: RoleEnum

class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str

class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: EmailStr

class NewPasswordRequest(BaseModel):
    """New password request"""
    token: str
    new_password: str = Field(..., min_length=6)

# ============================================
# User Schemas
# ============================================

class UserBase(BaseModel):
    """Base user schema"""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: RoleEnum

class UserCreate(UserBase):
    """User creation schema"""
    password: str

class UserUpdate(BaseModel):
    """User update schema"""
    name: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(UserBase):
    """User response schema"""
    id: str
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# Department Schemas
# ============================================

class DepartmentBase(BaseModel):
    """Base department schema"""
    department_name: str
    department_code: str
    hod_name: Optional[str] = None
    contact_email: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    """Department creation schema"""
    pass

class DepartmentUpdate(BaseModel):
    """Department update schema"""
    department_name: Optional[str] = None
    hod_name: Optional[str] = None
    contact_email: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    """Department response schema"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# Student Schemas
# ============================================

class StudentBase(BaseModel):
    """Base student schema"""
    usn: str
    department_id: str
    semester: int = Field(..., ge=1, le=8)
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    parent_contact: Optional[str] = None

class StudentCreate(StudentBase):
    """Student creation schema"""
    user_id: str

class StudentUpdate(BaseModel):
    """Student update schema"""
    semester: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_contact: Optional[str] = None

class StudentResponse(StudentBase):
    """Student response schema"""
    id: str
    user_id: str
    cgpa: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# ============================================
# Faculty Schemas
# ============================================

class FacultyBase(BaseModel):
    """Base faculty schema"""
    department_id: str
    designation: str
    employee_id: str
    specialization: Optional[str] = None
    phone: Optional[str] = None
    office_location: Optional[str] = None

class FacultyCreate(FacultyBase):
    """Faculty creation schema"""
    user_id: str

class FacultyUpdate(BaseModel):
    """Faculty update schema"""
    designation: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    office_location: Optional[str] = None

class FacultyResponse(FacultyBase):
    """Faculty response schema"""
    id: str
    user_id: str
    qualification: Optional[str] = None
    experience_years: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# ============================================
# Course Schemas
# ============================================

class CourseBase(BaseModel):
    """Base course schema"""
    course_name: str
    course_code: str
    department_id: str
    faculty_id: Optional[str] = None
    semester: int = Field(..., ge=1, le=8)
    credits: int = 4
    description: Optional[str] = None

class CourseCreate(CourseBase):
    """Course creation schema"""
    pass

class CourseUpdate(BaseModel):
    """Course update schema"""
    course_name: Optional[str] = None
    faculty_id: Optional[str] = None
    credits: Optional[int] = None
    description: Optional[str] = None

class CourseResponse(CourseBase):
    """Course response schema"""
    id: str
    total_lectures: int
    total_practicals: int
    total_tutorials: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# Attendance Schemas
# ============================================

class AttendanceBase(BaseModel):
    """Base attendance schema"""
    student_id: str
    course_id: str
    attendance_date: date
    status: AttendanceStatusEnum
    remarks: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    """Attendance creation schema"""
    pass

class AttendanceUpdate(BaseModel):
    """Attendance update schema"""
    status: AttendanceStatusEnum
    remarks: Optional[str] = None

class AttendanceResponse(AttendanceBase):
    """Attendance response schema"""
    id: str
    marked_by: Optional[str] = None
    marked_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# Marks Schemas
# ============================================

class MarksBase(BaseModel):
    """Base marks schema"""
    student_id: str
    course_id: str
    internal_marks: Optional[float] = None
    assignment_marks: Optional[float] = None
    practical_marks: Optional[float] = None
    semester_exam_marks: Optional[float] = None

class MarksCreate(MarksBase):
    """Marks creation schema"""
    pass

class MarksUpdate(BaseModel):
    """Marks update schema"""
    internal_marks: Optional[float] = None
    assignment_marks: Optional[float] = None
    practical_marks: Optional[float] = None
    semester_exam_marks: Optional[float] = None

class MarksResponse(MarksBase):
    """Marks response schema"""
    id: str
    total_marks: float
    grade: str
    submitted_by: Optional[str] = None
    submitted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# Fees Schemas
# ============================================

class FeesBase(BaseModel):
    """Base fees schema"""
    student_id: str
    semester: int
    total_fee: float
    due_date: Optional[date] = None

class FeesCreate(FeesBase):
    """Fees creation schema"""
    pass

class FeesUpdate(BaseModel):
    """Fees update schema"""
    paid_fee: Optional[float] = None
    payment_date: Optional[date] = None
    transaction_id: Optional[str] = None
    payment_method: Optional[str] = None

class FeesResponse(FeesBase):
    """Fees response schema"""
    id: str
    paid_fee: float
    due_fee: float
    payment_status: PaymentStatusEnum
    payment_date: Optional[date] = None
    transaction_id: Optional[str] = None
    payment_method: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# Assignment Schemas
# ============================================

class AssignmentBase(BaseModel):
    """Base assignment schema"""
    course_id: str
    faculty_id: str
    title: str
    description: Optional[str] = None
    due_date: datetime
    assignment_type: str = "homework"
    total_marks: int = 10

class AssignmentCreate(AssignmentBase):
    """Assignment creation schema"""
    pass

class AssignmentUpdate(BaseModel):
    """Assignment update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_published: Optional[bool] = None

class AssignmentResponse(AssignmentBase):
    """Assignment response schema"""
    id: str
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    is_published: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# Leave Request Schemas
# ============================================

class LeaveRequestBase(BaseModel):
    """Base leave request schema"""
    student_id: str
    start_date: date
    end_date: date
    reason: str
    leave_type: LeaveTypeEnum

class LeaveRequestCreate(LeaveRequestBase):
    """Leave request creation schema"""
    pass

class LeaveRequestUpdate(BaseModel):
    """Leave request update schema"""
    status: LeaveStatusEnum
    approval_remarks: Optional[str] = None

class LeaveRequestResponse(LeaveRequestBase):
    """Leave request response schema"""
    id: str
    status: LeaveStatusEnum
    attachment_url: Optional[str] = None
    approved_by: Optional[str] = None
    approval_remarks: Optional[str] = None
    approved_at: Optional[datetime] = None
    applied_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# Timetable Schemas
# ============================================

class TimetableBase(BaseModel):
    """Base timetable schema"""
    department_id: str
    semester: int
    course_id: str
    faculty_id: Optional[str] = None
    day_of_week: str
    start_time: str
    end_time: str
    room_number: Optional[str] = None
    session_type: str = "lecture"

class TimetableCreate(TimetableBase):
    """Timetable creation schema"""
    pass

class TimetableResponse(TimetableBase):
    """Timetable response schema"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# Response Schemas
# ============================================

class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    total: int
    page: int
    limit: int
    data: List[dict]

class MessageResponse(BaseModel):
    """Simple message response"""
    message: str
    status: str = "success"

class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
