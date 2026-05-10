"""
Student API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas import (
    AttendanceResponse,
    MarksResponse,
    AssignmentResponse,
    FeesResponse,
    LeaveRequestResponse, LeaveRequestCreate,
    TimetableResponse,
    StudentResponse
)
from app.core.security import get_current_student
from app.core.database import get_db, SupabaseDB

router = APIRouter(prefix="/student", tags=["Student"])

# ============================================
# Student Dashboard
# ============================================

@router.get("/profile", response_model=StudentResponse)
async def get_student_profile(
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Get current student's profile"""
    # Get student ID from user ID
    student_result = db.query("students").select("*, user:users(*)").eq("user_id", current_student["user_id"]).execute()
    student = student_result.data[0] if student_result.data else None
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    return StudentResponse(**student)

@router.get("/dashboard")
async def get_student_dashboard(
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Get student dashboard overview"""
    # Get student ID
    student_result = db.query("students").select("id").eq("user_id", current_student["user_id"]).execute()
    student_id = student_result.data[0]["id"] if student_result.data else None
    
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    try:
        # Get attendance percentage
        attendance = db.query("attendance").select("*").eq("student_id", student_id).execute()
        total_attendance = len(attendance.data) if attendance.data else 0
        present_count = len([a for a in attendance.data if a.get("status") in ["present", "late"]]) if attendance.data else 0
        attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
        
        # Get marks
        marks = db.query("marks").select("*").eq("student_id", student_id).execute()
        avg_marks = sum([m.get("total_marks", 0) for m in marks.data]) / len(marks.data) if marks.data else 0
        
        # Get fees
        fees = db.query("fees").select("*").eq("student_id", student_id).execute()
        total_fees = sum([f.get("total_fee", 0) for f in fees.data]) if fees.data else 0
        paid_fees = sum([f.get("paid_fee", 0) for f in fees.data]) if fees.data else 0
        
        # Get leave requests
        leave_requests = db.query("leave_requests").select("*").eq("student_id", student_id).execute()
        
        return {
            "attendance_percentage": round(attendance_percentage, 2),
            "average_marks": round(avg_marks, 2),
            "total_courses": len(marks.data) if marks.data else 0,
            "fees_paid": round(paid_fees, 2),
            "total_fees": round(total_fees, 2),
            "pending_leave_requests": len([lr for lr in leave_requests.data if lr.get("status") == "pending"]) if leave_requests.data else 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching dashboard: {str(e)}"
        )

# ============================================
# Attendance
# ============================================

@router.get("/attendance", response_model=List[AttendanceResponse])
async def get_student_attendance(
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Get student's attendance records"""
    # Get student ID
    student_result = db.query("students").select("id").eq("user_id", current_student["user_id"]).execute()
    student_id = student_result.data[0]["id"] if student_result.data else None
    
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    result = db.query("attendance").select("*").eq("student_id", student_id).execute()
    return [AttendanceResponse(**att) for att in result.data]

# ============================================
# Marks
# ============================================

@router.get("/marks", response_model=List[MarksResponse])
async def get_student_marks(
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Get student's marks"""
    # Get student ID
    student_result = db.query("students").select("id").eq("user_id", current_student["user_id"]).execute()
    student_id = student_result.data[0]["id"] if student_result.data else None
    
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    result = db.query("marks").select("*").eq("student_id", student_id).execute()
    return [MarksResponse(**mark) for mark in result.data]

# ============================================
# Assignments
# ============================================

@router.get("/assignments", response_model=List[AssignmentResponse])
async def get_student_assignments(
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Get student's assignments for enrolled courses"""
    # Get student ID
    student_result = db.query("students").select("id").eq("user_id", current_student["user_id"]).execute()
    student_id = student_result.data[0]["id"] if student_result.data else None
    
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    try:
        # Get enrolled courses
        enrollments = db.query("course_enrollments").select("course_id").eq("student_id", student_id).execute()
        course_ids = [e.get("course_id") for e in enrollments.data] if enrollments.data else []
        
        # Get assignments for those courses
        if course_ids:
            result = db.query("assignments").select("*").in_("course_id", course_ids).eq("is_published", True).execute()
            return [AssignmentResponse(**assignment) for assignment in result.data]
        
        return []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching assignments: {str(e)}"
        )

# ============================================
# Fees
# ============================================

@router.get("/fees", response_model=List[FeesResponse])
async def get_student_fees(
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Get student's fee status"""
    # Get student ID
    student_result = db.query("students").select("id").eq("user_id", current_student["user_id"]).execute()
    student_id = student_result.data[0]["id"] if student_result.data else None
    
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    result = db.query("fees").select("*").eq("student_id", student_id).execute()
    return [FeesResponse(**fee) for fee in result.data]

# ============================================
# Timetable
# ============================================

@router.get("/timetable", response_model=List[TimetableResponse])
async def get_student_timetable(
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Get student's timetable"""
    # Get student details
    student_result = db.query("students").select("department_id, semester").eq("user_id", current_student["user_id"]).execute()
    student = student_result.data[0] if student_result.data else None
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Get timetable for student's department and semester
    result = db.query("timetable").select("*").eq("department_id", student["department_id"]).eq("semester", student["semester"]).execute()
    return [TimetableResponse(**tt) for tt in result.data]

# ============================================
# Leave Requests
# ============================================

@router.get("/leave-requests", response_model=List[LeaveRequestResponse])
async def get_student_leave_requests(
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Get student's leave requests"""
    # Get student ID
    student_result = db.query("students").select("id").eq("user_id", current_student["user_id"]).execute()
    student_id = student_result.data[0]["id"] if student_result.data else None
    
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    result = db.query("leave_requests").select("*").eq("student_id", student_id).execute()
    return [LeaveRequestResponse(**lr) for lr in result.data]

@router.post("/leave-requests", response_model=LeaveRequestResponse)
async def apply_leave(
    leave_request: LeaveRequestCreate,
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Apply for leave"""
    # Get student ID
    student_result = db.query("students").select("id").eq("user_id", current_student["user_id"]).execute()
    student_id = student_result.data[0]["id"] if student_result.data else None
    
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    leave_data = leave_request.dict()
    leave_data["student_id"] = student_id
    leave_data["status"] = "pending"
    leave_data["applied_at"] = "now()"
    
    result = db.insert("leave_requests", leave_data)
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to apply for leave"
        )
    
    return LeaveRequestResponse(**result.data[0])

# ============================================
# Profile Management
# ============================================

@router.put("/profile")
async def update_student_profile(
    profile_data: dict,
    current_student: dict = Depends(get_current_student),
    db: SupabaseDB = Depends(get_db)
):
    """Update student profile"""
    # Get student ID
    student_result = db.query("students").select("id").eq("user_id", current_student["user_id"]).execute()
    student_id = student_result.data[0]["id"] if student_result.data else None
    
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    result = db.update("students", profile_data, student_id)
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update profile"
        )
    
    return {"message": "Profile updated successfully"}
