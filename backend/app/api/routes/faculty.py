"""
Faculty API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from datetime import date
from app.schemas import (
    AttendanceResponse, AttendanceCreate, AttendanceUpdate,
    MarksResponse, MarksCreate, MarksUpdate,
    AssignmentResponse, AssignmentCreate, AssignmentUpdate,
    CourseResponse
)
from app.core.security import get_current_faculty
from app.core.database import get_db, SupabaseDB

router = APIRouter(prefix="/faculty", tags=["Faculty"])

# ============================================
# Attendance Management
# ============================================

@router.get("/attendance", response_model=List[AttendanceResponse])
async def get_attendance(
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db),
    course_id: str = None,
    start_date: date = None,
    end_date: date = None
):
    """Get attendance records for faculty's courses"""
    # Get faculty ID
    faculty_result = db.query("faculty").select("id").eq("user_id", current_faculty["user_id"]).execute()
    faculty_id = faculty_result.data[0]["id"] if faculty_result.data else None
    
    if not faculty_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty record not found"
        )
    
    # Build query
    query = db.query("attendance").select("*")
    
    if course_id:
        query = query.eq("course_id", course_id)
    if start_date:
        query = query.gte("attendance_date", start_date)
    if end_date:
        query = query.lte("attendance_date", end_date)
    
    result = query.execute()
    return [AttendanceResponse(**att) for att in result.data]

@router.post("/attendance", response_model=AttendanceResponse)
async def mark_attendance(
    attendance: AttendanceCreate,
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db)
):
    """Mark attendance for students"""
    # Get faculty ID
    faculty_result = db.query("faculty").select("id").eq("user_id", current_faculty["user_id"]).execute()
    faculty_id = faculty_result.data[0]["id"] if faculty_result.data else None
    
    attendance_data = attendance.dict()
    attendance_data["marked_by"] = faculty_id
    attendance_data["marked_at"] = "now()"
    
    result = db.insert("attendance", attendance_data)
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to mark attendance"
        )
    return AttendanceResponse(**result.data[0])

@router.put("/attendance/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
    attendance_id: str,
    attendance_update: AttendanceUpdate,
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db)
):
    """Update attendance record"""
    update_data = attendance_update.dict(exclude_unset=True)
    result = db.update("attendance", update_data, attendance_id)
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    return AttendanceResponse(**result.data[0])

# ============================================
# Marks Management
# ============================================

@router.get("/marks", response_model=List[MarksResponse])
async def get_marks(
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db),
    course_id: str = None
):
    """Get marks for faculty's courses"""
    query = db.query("marks").select("*")
    
    if course_id:
        query = query.eq("course_id", course_id)
    
    result = query.execute()
    return [MarksResponse(**mark) for mark in result.data]

@router.post("/marks", response_model=MarksResponse)
async def upload_marks(
    marks: MarksCreate,
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db)
):
    """Upload marks for students"""
    # Get faculty ID
    faculty_result = db.query("faculty").select("id").eq("user_id", current_faculty["user_id"]).execute()
    faculty_id = faculty_result.data[0]["id"] if faculty_result.data else None
    
    marks_data = marks.dict()
    marks_data["submitted_by"] = faculty_id
    marks_data["submitted_at"] = "now()"
    
    result = db.insert("marks", marks_data)
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to upload marks"
        )
    return MarksResponse(**result.data[0])

@router.put("/marks/{marks_id}", response_model=MarksResponse)
async def update_marks(
    marks_id: str,
    marks_update: MarksUpdate,
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db)
):
    """Update marks"""
    update_data = marks_update.dict(exclude_unset=True)
    result = db.update("marks", update_data, marks_id)
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marks record not found"
        )
    
    return MarksResponse(**result.data[0])

# ============================================
# Assignments
# ============================================

@router.get("/assignments", response_model=List[AssignmentResponse])
async def get_assignments(
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db)
):
    """Get faculty's assignments"""
    # Get faculty ID
    faculty_result = db.query("faculty").select("id").eq("user_id", current_faculty["user_id"]).execute()
    faculty_id = faculty_result.data[0]["id"] if faculty_result.data else None
    
    result = db.query("assignments").select("*").eq("faculty_id", faculty_id).execute()
    return [AssignmentResponse(**assignment) for assignment in result.data]

@router.post("/assignments", response_model=AssignmentResponse)
async def create_assignment(
    assignment: AssignmentCreate,
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db)
):
    """Create a new assignment"""
    # Get faculty ID
    faculty_result = db.query("faculty").select("id").eq("user_id", current_faculty["user_id"]).execute()
    faculty_id = faculty_result.data[0]["id"] if faculty_result.data else None
    
    assignment_data = assignment.dict()
    assignment_data["faculty_id"] = faculty_id
    
    result = db.insert("assignments", assignment_data)
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create assignment"
        )
    return AssignmentResponse(**result.data[0])

@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: str,
    assignment_update: AssignmentUpdate,
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db)
):
    """Update assignment"""
    update_data = assignment_update.dict(exclude_unset=True)
    result = db.update("assignments", update_data, assignment_id)
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    return AssignmentResponse(**result.data[0])

# ============================================
# Courses
# ============================================

@router.get("/courses", response_model=List[CourseResponse])
async def get_faculty_courses(
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db)
):
    """Get faculty's assigned courses"""
    # Get faculty ID
    faculty_result = db.query("faculty").select("id").eq("user_id", current_faculty["user_id"]).execute()
    faculty_id = faculty_result.data[0]["id"] if faculty_result.data else None
    
    result = db.query("courses").select("*").eq("faculty_id", faculty_id).execute()
    return [CourseResponse(**course) for course in result.data]

# ============================================
# Analytics
# ============================================

@router.get("/analytics/performance")
async def get_performance_analytics(
    current_faculty: dict = Depends(get_current_faculty),
    db: SupabaseDB = Depends(get_db),
    course_id: str = None
):
    """Get student performance analytics"""
    try:
        # Get performance data
        query = db.query("student_performance").select("*")
        result = query.execute()
        
        return {
            "students": result.data,
            "average_performance": sum([s.get("avg_marks", 0) for s in result.data]) / len(result.data) if result.data else 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching analytics: {str(e)}"
        )
