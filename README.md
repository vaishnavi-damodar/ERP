# EduSync - Smart College ERP System

A complete college management system built with modern full-stack technologies.

## 🎯 Project Overview

EduSync is a comprehensive College Enterprise Resource Planning (ERP) system designed to streamline academic operations. It provides role-based access for Admins, Faculty, and Students with features for attendance, marks management, timetable, fee management, and more.

## 📋 Features

### 🔐 Authentication & Security
- JWT-based authentication
- Role-based access control (Admin, Faculty, Student)
- Secure password reset
- Protected API routes with middleware

### 👨‍💼 Admin Module
- Dashboard with analytics
- CRUD operations for students, faculty, departments, courses
- Timetable management
- Attendance and marks analytics
- Fee management system
- Leave request approvals
- System reports with PDF export
- Search and filter capabilities

### 👨‍🏫 Faculty Module
- Dashboard with assigned courses
- Mark attendance
- Upload internal marks
- Manage assignments
- Student performance analysis
- Leave request management
- Timetable view

### 👨‍🎓 Student Module
- Personal dashboard
- View attendance and marks
- Assignment downloads
- Fee payment status
- Timetable view
- Apply for leave
- Profile management

## 🏗️ Project Structure

```
EduSync/
├── frontend/          # Next.js 15 frontend application
│   ├── app/          # App Router
│   ├── components/   # Reusable components
│   ├── lib/          # Utilities and helpers
│   ├── styles/       # Global styles
│   └── ...
├── backend/          # FastAPI backend
│   ├── app/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   └── ...
└── database/         # Database schema and RLS policies
    ├── schema.sql
    └── rls_policies.sql
```

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: ShadCN UI
- **Animations**: Framer Motion
- **State Management**: React Hooks + Context API
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.10+
- **Authentication**: JWT
- **Database**: Supabase PostgreSQL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

### Database
- **Primary DB**: Supabase PostgreSQL
- **Auth**: Supabase Auth
- **Storage**: Supabase Storage
- **Row-Level Security**: RLS Policies

## 📦 Database Schema

### Core Tables
- `users` - User authentication and profiles
- `students` - Student information
- `faculty` - Faculty information
- `departments` - Department details
- `courses` - Course information
- `attendance` - Attendance records
- `marks` - Student marks
- `fees` - Fee management
- `assignments` - Course assignments
- `leave_requests` - Leave applications
- `timetable` - Class schedule

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL (or Supabase account)
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install

# Create .env.local file
cp .env.example .env.local

# Start development server
npm run dev
```

## 🔧 Environment Variables

### Backend (.env)
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION=24
DATABASE_URL=postgresql://...
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

## 📱 Database Relationships (ER Diagram)

```
users (1) ──── (1) students
         └──── (1) faculty

departments (1) ──── (M) students
            └────── (M) faculty
            └────── (M) courses

courses (1) ──── (M) attendance
        └───── (M) marks
        └───── (M) assignments
        └───── (1) timetable

students (1) ──── (M) attendance
         └─────── (M) marks
         └─────── (M) fees
         └─────── (M) leave_requests

faculty (1) ──── (M) courses
        └──────── (M) assignments

timetable (M) ──── (1) departments
          └────── (M) courses
```

## 🔒 Row-Level Security (RLS)

The Supabase database implements comprehensive RLS policies:
- Students can only view their own data
- Faculty can manage only their assigned courses
- Admins have full access
- Automatic user_id filtering based on JWT claims

## 📊 Key APIs

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - Logout

### Admin APIs
- `GET/POST /api/admin/students` - Manage students
- `GET/POST /api/admin/faculty` - Manage faculty
- `GET/POST /api/admin/departments` - Manage departments
- `GET/POST /api/admin/courses` - Manage courses
- `GET /api/admin/analytics` - System analytics

### Faculty APIs
- `POST /api/faculty/attendance` - Mark attendance
- `POST /api/faculty/marks` - Upload marks
- `GET/POST /api/faculty/assignments` - Manage assignments

### Student APIs
- `GET /api/student/attendance` - View attendance
- `GET /api/student/marks` - View marks
- `GET /api/student/assignments` - View assignments
- `POST /api/student/leave` - Apply for leave

## 🎨 UI Components

All UI components are built with ShadCN and Tailwind CSS:
- Dashboard cards with glassmorphism
- Data tables with sorting/filtering
- Charts for analytics
- Forms with validation
- Navigation sidebar
- Theme toggle (dark/light)
- Loading states and skeletons
- Toast notifications

## 🔄 Database Normalization

The schema follows 3NF (Third Normal Form):
- Elimination of duplicate data
- Dependency on primary keys
- No transitive dependencies
- Proper foreign key relationships

## 🚀 Deployment

### Backend Deployment (Heroku/Railway)
```bash
pip freeze > requirements.txt
git push heroku main
```

### Frontend Deployment (Vercel)
```bash
npm run build
vercel --prod
```

### Database Migration
Database schema is managed through Supabase Console or migrations.

## 📚 Documentation

- API Documentation: Available at `/docs` (Swagger UI)
- Component Storybook: Coming soon
- Deployment Guide: See `DEPLOYMENT.md`

## 📝 Database Concepts Covered

1. **Normalization**: 3NF applied throughout
2. **Relationships**: One-to-Many, Many-to-One properly implemented
3. **Constraints**: PK, FK, NOT NULL, UNIQUE
4. **Indexes**: On frequently queried columns
5. **Transactions**: ACID compliance
6. **Views**: For complex queries
7. **Triggers**: For automated updates
8. **RLS**: For row-level security

## 👨‍💻 Development Team

This project is suitable for:
- College DBMS final project
- Portfolio showcase
- Learning full-stack development
- Understanding real-world ERP systems

## 📄 License

MIT License - Feel free to use this project for educational purposes.

## 🆘 Support

For issues and questions, please open an issue on GitHub or contact the development team.

---

**Last Updated**: May 2026
**Version**: 1.0.0
