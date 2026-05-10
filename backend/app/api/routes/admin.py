"""
Admin API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.schemas import (
    StudentResponse, StudentCreate, StudentUpdate,
    FacultyResponse, FacultyCreate, FacultyUpdate,
    DepartmentResponse, DepartmentCreate, DepartmentUpdate,
    CourseResponse, CourseCreate, CourseUpdate,
    UserCreate, UserResponse
)
from app.core.security import get_current_admin
from app.core.database import get_db, SupabaseDB

router = APIRouter(prefix="/admin", tags=["Admin"])

# ============================================
# Student Management
# ============================================

@router.get("/students", response_model=List[StudentResponse])
async def get_students(
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    department_id: str = None,
    semester: int = None
):
    """Get all students with optional filters"""
    query = db.query("students").select("*, user:users(*)")
    
    if department_id:
        query = query.eq("department_id", department_id)
    if semester:
        query = query.eq("semester", semester)
    
    result = query.range(skip, skip + limit - 1).execute()
    return [StudentResponse(**student) for student in result.data]

@router.post("/students", response_model=StudentResponse)
async def create_student(
    student: StudentCreate,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Create a new student"""
    result = db.insert("students", student.dict())
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create student"
        )
    return StudentResponse(**result.data[0])

@router.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: str,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Get student by ID"""
    result = db.query("students").select("*, user:users(*)").eq("id", student_id).execute()
    student = result.data[0] if result.data else None
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return StudentResponse(**student)

@router.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: str,
    student_update: StudentUpdate,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Update student information"""
    update_data = student_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    result = db.update("students", update_data, student_id)
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return StudentResponse(**result.data[0])

@router.delete("/students/{student_id}")
async def delete_student(
    student_id: str,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Delete a student"""
    result = db.delete("students", student_id)
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return {"message": "Student deleted successfully"}

# ============================================
# Faculty Management
# ============================================

@router.get("/faculty", response_model=List[FacultyResponse])
async def get_faculty(
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    department_id: str = None
):
    """Get all faculty with optional filters"""
    query = db.query("faculty").select("*, user:users(*)")
    
    if department_id:
        query = query.eq("department_id", department_id)
    
    result = query.range(skip, skip + limit - 1).execute()
    return [FacultyResponse(**faculty) for faculty in result.data]

@router.post("/faculty", response_model=FacultyResponse)
async def create_faculty(
    faculty: FacultyCreate,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Create a new faculty member"""
    result = db.insert("faculty", faculty.dict())
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create faculty"
        )
    return FacultyResponse(**result.data[0])

@router.put("/faculty/{faculty_id}", response_model=FacultyResponse)
async def update_faculty(
    faculty_id: str,
    faculty_update: FacultyUpdate,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Update faculty information"""
    update_data = faculty_update.dict(exclude_unset=True)
    result = db.update("faculty", update_data, faculty_id)
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )
    
    return FacultyResponse(**result.data[0])

# ============================================
# Department Management
# ============================================

@router.get("/departments", response_model=List[DepartmentResponse])
async def get_departments(
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Get all departments"""
    result = db.query("departments").select("*").execute()
    return [DepartmentResponse(**dept) for dept in result.data]

@router.post("/departments", response_model=DepartmentResponse)
async def create_department(
    department: DepartmentCreate,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Create a new department"""
    result = db.insert("departments", department.dict())
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create department"
        )
    return DepartmentResponse(**result.data[0])

@router.put("/departments/{dept_id}", response_model=DepartmentResponse)
async def update_department(
    dept_id: str,
    department_update: DepartmentUpdate,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Update department information"""
    update_data = department_update.dict(exclude_unset=True)
    result = db.update("departments", update_data, dept_id)
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    return DepartmentResponse(**result.data[0])

# ============================================
# Course Management
# ============================================

@router.get("/courses", response_model=List[CourseResponse])
async def get_courses(
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db),
    department_id: str = None,
    semester: int = None
):
    """Get all courses with optional filters"""
    query = db.query("courses").select("*")
    
    if department_id:
        query = query.eq("department_id", department_id)
    if semester:
        query = query.eq("semester", semester)
    
    result = query.execute()
    return [CourseResponse(**course) for course in result.data]

@router.post("/courses", response_model=CourseResponse)
async def create_course(
    course: CourseCreate,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Create a new course"""
    result = db.insert("courses", course.dict())
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create course"
        )
    return CourseResponse(**result.data[0])

@router.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course_update: CourseUpdate,
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Update course information"""
    update_data = course_update.dict(exclude_unset=True)
    result = db.update("courses", update_data, course_id)
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return CourseResponse(**result.data[0])

# ============================================
# Analytics
# ============================================

@router.get("/analytics/overview")
async def get_analytics_overview(
    current_admin: dict = Depends(get_current_admin),
    db: SupabaseDB = Depends(get_db)
):
    """Get system analytics overview"""
    # Get statistics from views
    try:
        dept_stats = db.query("department_statistics").select("*").execute()
        faculty_workload = db.query("faculty_workload").select("*").execute()
        
        return {
            "total_students": len(db.query("students").select("id").execute().data),
            "total_faculty": len(db.query("faculty").select("id").execute().data),
            "total_departments": len(db.query("departments").select("id").execute().data),
            "total_courses": len(db.query("courses").select("id").execute().data),
            "department_stats": dept_stats.data,
            "faculty_workload": faculty_workload.data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching analytics: {str(e)}"
        )
