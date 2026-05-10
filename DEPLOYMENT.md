# EduSync Deployment Guide

## Pre-Deployment Checklist

- [ ] Backend tested locally
- [ ] Frontend tested locally
- [ ] Environment variables configured
- [ ] Database schema migrated
- [ ] SSL certificates ready
- [ ] Domain registered
- [ ] CDN configured (optional)
- [ ] Email service configured
- [ ] Backup strategy implemented
- [ ] Monitoring set up
- [ ] Load testing completed

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        EDUSYNC DEPLOYMENT                    │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────┐              ┌─────────────┐               │
│  │  Frontend  │◄────────────►│   Backend   │               │
│  │  (Vercel)  │              │   (Heroku/  │               │
│  │  Next.js   │              │   Railway)  │               │
│  └────────────┘              │   FastAPI   │               │
│       │                       └──────┬──────┘               │
│       │                              │                      │
│       └──────────────┬───────────────┘                      │
│                      │                                       │
│                      ▼                                       │
│              ┌────────────────┐                             │
│              │    Supabase    │                             │
│              │  PostgreSQL +  │                             │
│              │   Auth +       │                             │
│              │   Storage      │                             │
│              └────────────────┘                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Backend Deployment

### Option 1: Deploy to Heroku (Recommended for beginners)

#### Step 1: Install Heroku CLI
```bash
# Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Initialize Git Repository
```bash
cd backend
git init
git add .
git commit -m "Initial commit"
```

#### Step 3: Create Heroku App
```bash
heroku login
heroku create edusync-backend
```

#### Step 4: Set Environment Variables
```bash
heroku config:set SUPABASE_URL=your_supabase_url
heroku config:set SUPABASE_KEY=your_supabase_key
heroku config:set SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
heroku config:set JWT_SECRET=$(openssl rand -hex 32)
heroku config:set DATABASE_URL=your_database_url
```

#### Step 5: Create Procfile
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### Step 6: Deploy
```bash
git push heroku main
```

#### Step 7: Monitor
```bash
heroku logs --tail
heroku open
```

---

### Option 2: Deploy to Railway.app (Modern Alternative)

#### Step 1: Create Railway Account
Visit: https://railway.app

#### Step 2: Create PostgreSQL Service
1. Go to "New Project"
2. Add PostgreSQL
3. Configure database

#### Step 3: Deploy Backend
```bash
npm install -g @railway/cli
railway up
```

#### Step 4: Set Environment Variables
In Railway Dashboard:
- Go to your Python service
- Add environment variables
- Set all required .env values

#### Step 5: Connect Database
```bash
railway link
```

---

### Option 3: Deploy to AWS with ECS

#### Step 1: Build Docker Image
```bash
# Create Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 2: Push to ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker build -t edusync-backend .

docker tag edusync-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/edusync-backend:latest

docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/edusync-backend:latest
```

#### Step 3: Create ECS Service
1. Create task definition
2. Create service
3. Configure load balancer
4. Set auto-scaling

---

## Frontend Deployment

### Deploy to Vercel (Recommended)

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Deploy
```bash
cd frontend
vercel
```

#### Step 3: Configure Environment
In Vercel Dashboard:
1. Go to Settings → Environment Variables
2. Add `NEXT_PUBLIC_API_URL` = your backend URL
3. Add Supabase keys if using

#### Step 4: Set Production Domain
1. Add custom domain
2. Configure DNS
3. Enable auto-HTTPS

#### Step 5: Monitor
Vercel dashboard provides:
- Build logs
- Performance metrics
- Error tracking

---

### Deploy to Netlify

#### Step 1: Connect Repository
1. Go to netlify.com
2. Connect your GitHub/GitLab account
3. Select repository

#### Step 2: Configure Build Settings
- Build command: `npm run build`
- Publish directory: `.next`
- Node version: 18

#### Step 3: Set Environment Variables
Go to Site Settings → Build & Deploy → Environment
- `NEXT_PUBLIC_API_URL`: your backend URL

#### Step 4: Deploy
```bash
netlify deploy --prod
```

---

### Deploy to AWS CloudFront + S3

#### Step 1: Build Static Export
```bash
# Modify next.config.js
const nextConfig = {
  output: 'export',
  // ... rest of config
}

npm run build
```

#### Step 2: Upload to S3
```bash
aws s3 sync out/ s3://edusync-frontend/ --delete
```

#### Step 3: Create CloudFront Distribution
1. Create distribution
2. Set S3 as origin
3. Configure caching behavior
4. Enable gzip compression

#### Step 4: Set Custom Domain
1. Add CNAME record
2. Configure SSL certificate
3. Enable redirect from HTTP to HTTPS

---

## Database Deployment

### Supabase (Already Hosted)

#### Step 1: Create Supabase Account
Visit: https://supabase.com

#### Step 2: Create New Project
1. Choose region (for better latency)
2. Set strong database password
3. Note the connection details

#### Step 3: Run Migrations
1. Go to SQL Editor
2. Execute `database/schema.sql`
3. Execute `database/rls_policies.sql`
4. Execute `database/seed_data.sql`

#### Step 4: Configure Authentication
1. Go to Authentication → Providers
2. Enable Email/Password (if needed)
3. Configure redirect URLs
4. Set up SMTP for emails

#### Step 5: Monitor
Use Supabase Dashboard:
- Query performance
- Storage usage
- API requests
- Backups

---

## SSL/TLS Certificates

### Automatic with Vercel/Netlify
- Already includes SSL
- Auto-renewal
- No configuration needed

### Manual with Let's Encrypt + Heroku
```bash
# Add Heroku SSL add-on
heroku addons:create ssl:endpoint
heroku certs:add /path/to/cert /path/to/key
```

### AWS Certificate Manager
1. Request certificate
2. Validate domain
3. Deploy with CloudFront

---

## Monitoring & Logging

### Backend Monitoring

#### Heroku Logs
```bash
heroku logs --tail
heroku logs --source app --tail
heroku logs --source heroku --tail
```

#### Error Tracking
```bash
# Add error tracking service
# Example: Sentry
pip install sentry-sdk
```

#### Performance Monitoring
- Use Heroku metrics
- Monitor dyno CPU/RAM
- Track API response times

### Frontend Monitoring

#### Vercel Analytics
- Build performance
- Web vitals
- Error tracking

#### Custom Analytics
```typescript
// Add analytics to frontend
import { useEffect } from 'react';

export function useAnalytics() {
  useEffect(() => {
    // Track page views
    // Track errors
    // Track user actions
  }, []);
}
```

### Database Monitoring

#### Supabase Monitoring
1. Go to Project Settings
2. Monitor database size
3. Check connection count
4. Review slow queries
5. Monitor storage

---

## CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        run: |
          git push https://heroku:${{ secrets.HEROKU_API_KEY }}@git.heroku.com/${{ secrets.HEROKU_APP_NAME }}.git main

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

## Scaling Strategy

### Horizontal Scaling

**Backend:**
- Use Heroku Professional Dyno
- Add multiple dynos for load balancing
- Use Heroku's automatic scaling

**Frontend:**
- Vercel handles auto-scaling
- CDN caching automatic
- No manual scaling needed

### Vertical Scaling

**Database:**
- Upgrade Supabase plan
- Increase connection limits
- Upgrade compute instances

---

## Backup & Disaster Recovery

### Database Backups

**Supabase Automated:**
- Daily automatic backups
- 7-day retention (free)
- 30-day retention (paid)

**Manual Backup:**
```bash
pg_dump -h db.supabase.co -U postgres -d postgres > backup.sql
```

### Application Backups

**Backend:**
- Store code in GitHub
- Use git branches for versioning
- Tag releases

**Frontend:**
- Automatic with Vercel
- GitHub stores all code
- Rollback to previous deployments

### Disaster Recovery Plan

1. **Immediate Response** (0-30 min)
   - Check status page
   - Notify users
   - Begin investigation

2. **Short Term** (30 min - 4 hours)
   - Identify root cause
   - Implement hotfix
   - Deploy patch

3. **Long Term** (4+ hours)
   - Post-mortem analysis
   - Implement permanent fix
   - Update documentation

---

## Performance Optimization

### Backend Optimization
- Enable gzip compression
- Implement caching
- Use Redis for sessions
- Optimize database queries

### Frontend Optimization
- Enable Next.js caching
- Optimize images
- Code splitting
- Lazy loading

### Database Optimization
- Add appropriate indexes
- Analyze slow queries
- Archive old data
- Implement partitioning

---

## Security Best Practices

### Backend Security
- Enable HTTPS/TLS
- Use strong JWT secrets
- Implement rate limiting
- Add request validation
- Use CORS properly
- Keep dependencies updated

### Frontend Security
- Content Security Policy
- X-Frame-Options header
- X-Content-Type-Options header
- Secure HTTP headers

### Database Security
- Enable RLS policies
- Use strong passwords
- Backup regularly
- Monitor access logs
- Encrypt sensitive data

---

## Cost Optimization

### Estimated Monthly Costs

| Service | Free Tier | Paid |
|---------|-----------|------|
| Supabase PostgreSQL | 500 MB | $25+ |
| Heroku Backend | Ended | $7-500+ |
| Vercel Frontend | Included | $20+ |
| Custom Domain | - | $10-15 |
| **Total** | - | **$50-550+** |

### Cost Reduction Tips
1. Use free tiers during development
2. Optimize database queries
3. Enable CDN caching
4. Archive old data
5. Right-size instances

---

## Post-Deployment

### Health Checks
```bash
# Check backend health
curl https://backend.herokuapp.com/health

# Check frontend
curl https://edusync.vercel.app
```

### Smoke Testing
1. Test login flow
2. Test each role
3. Test API endpoints
4. Test database queries
5. Test file uploads

### Documentation
- Update API documentation
- Document deployment process
- Create runbooks for maintenance
- Set up incident response

---

## Maintenance Schedule

### Daily
- Monitor error logs
- Check uptime status
- Review user reports

### Weekly
- Review performance metrics
- Check backup status
- Security audit

### Monthly
- Database optimization
- Dependency updates
- Cost review
- Performance analysis

### Quarterly
- Security audit
- Capacity planning
- Disaster recovery test
- Load testing

---

## Deployment Checklist

- [ ] Backend deployed and running
- [ ] Frontend deployed and accessible
- [ ] Database migrations applied
- [ ] Environment variables set correctly
- [ ] SSL/TLS enabled
- [ ] Monitoring configured
- [ ] Backups automated
- [ ] Error tracking enabled
- [ ] Analytics configured
- [ ] Documentation updated
- [ ] Team trained on deployment
- [ ] Rollback procedure tested

---

## Support Resources

- **Heroku Docs**: https://devcenter.heroku.com
- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://railway.app/docs
- **Supabase Docs**: https://supabase.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

**Deployment Guide Last Updated**: May 2026
**Version**: 1.0.0
