# Installation Guide

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.10+ (for backend)
- PostgreSQL (or Supabase account)
- Git
- npm or yarn

## Step-by-Step Installation

### 1. Clone or Extract the Project

```bash
cd EduSync
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

#### Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Supabase credentials
nano .env
```

**Required Environment Variables:**
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Supabase anonymous key
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key (for admin operations)
- `JWT_SECRET`: Generate with: `openssl rand -hex 32`
- `DATABASE_URL`: PostgreSQL connection string

#### Setup Database

1. Go to Supabase Console
2. Create a new project or use existing
3. Run the SQL schema:
   - Copy content from `database/schema.sql`
   - Paste in Supabase SQL Editor
   - Execute

4. Apply RLS Policies:
   - Copy content from `database/rls_policies.sql`
   - Paste in Supabase SQL Editor
   - Execute

#### Run Backend

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

Backend will run on `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
# or
yarn install
```

#### Configure Environment

```bash
# Copy environment template
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

**Required Environment Variables:**
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000/api/v1)
- `NEXT_PUBLIC_SUPABASE_URL`: Supabase URL (optional)
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Supabase anon key (optional)

#### Run Frontend

```bash
npm run dev
# or
yarn dev
```

Frontend will run on `http://localhost:3000`

### 4. Test Default Credentials

The system includes seed data with these default users:

#### Admin Account
- Email: `admin@edusync.edu`
- Password: `admin123`

#### Faculty Account
- Email: `faculty@edusync.edu`
- Password: `faculty123`

#### Student Account
- Email: `student@edusync.edu`
- Password: `student123`

## Troubleshooting

### Backend Issues

#### ModuleNotFoundError

```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

#### Database Connection Error

- Verify Supabase URL and keys in `.env`
- Check PostgreSQL connection string
- Ensure Supabase project is running

#### CORS Issues

- Verify `CORS_ORIGINS` in `backend/.env` includes your frontend URL
- Default: `http://localhost:3000`

### Frontend Issues

#### Cannot fetch API

- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify backend CORS settings

#### Module not found

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Supabase Connection Issues

- Verify project is active in Supabase console
- Check credentials are correct
- Ensure RLS policies are enabled
- Test connection with SQL query directly in Supabase

## Quick Start Commands

### Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

### Full Stack (in separate terminals)
```bash
# Terminal 1 - Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

## Production Build

### Backend
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend
```bash
# Build static files
npm run build

# Start production server
npm run start
```

## Database Seeding

To populate test data:

1. In Supabase SQL Editor, run the provided seed script:
```sql
-- Run database/seed_data.sql
```

## Port Configuration

- **Frontend**: 3000
- **Backend**: 8000
- **Supabase**: 5432 (PostgreSQL)

Change ports if needed in environment variables.

## API Documentation

Access Swagger UI at: `http://localhost:8000/docs`

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## Support

For issues:
1. Check terminal error messages
2. Review environment variables
3. Verify database connection
4. Check console logs in browser (F12)

---

**Installation Complete!** 🎉

Your EduSync College ERP System is ready to use.
