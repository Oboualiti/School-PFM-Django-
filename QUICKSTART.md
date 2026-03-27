# PreSkool Application - Quick Start Guide

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 3. Create Admin Account
```bash
python manage.py createsuperuser
```
Fill in the prompts:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (change in production!)

### 4. Run Development Server
```bash
python manage.py runserver
```

Access at: `http://localhost:8000`

---

## Testing Different User Roles

### Admin Account
**Login:** 
- Email: `admin@example.com`
- Password: `admin123`

**Access:**
- Dashboard: Admin dashboard
- Teachers: Full CRUD
- Departments: Full CRUD
- All other modules: Full access

### Teacher Account (Create via Admin Panel)

1. Go to Django admin: `http://localhost:8000/admin`
2. Login with admin account
3. Go to "Custom Users" section
4. Click "Add Custom User"
5. Fill in details and check `is_teacher` checkbox
6. Save

**Then go back to admin to create Teacher profile:**
1. Go to "Teachers" section
2. Click "Add Teacher"
3. Select the user you just created
4. Fill in teacher details

### Student Account
Similar process but check `is_student` checkbox instead.

---

## Testing Each Module

### 1. Teachers Module
- Go to: `http://localhost:8000/staff/teachers/`
- Click "+" button to add new teacher
- Fill in form and submit
- Verify teacher appears in list
- Edit and delete buttons should work

### 2. Departments Module
- Go to: `http://localhost:8000/academic/departments/`
- Add new department
- Assign a department head (teacher)
- Edit departments
- Only admin should see add button

### 3. Subjects Module
- Go to: `http://localhost:8000/academic/subjects/`
- Must have departments and teachers first
- Add subject with department and teacher
- List shows all subjects organized by department

### 4. Exams Module
- Go to: `http://localhost:8000/academic/exams/`
- Need subjects to create exams
- Add exam with subject and date
- View grades: `/academic/grades/`

### 5. Holidays Module
- Go to: `http://localhost:8000/academic/holidays/`
- Add holidays with date
- Type: Public or School

### 6. Timetable
- Go to: `http://localhost:8000/timetable/`
- View existing schedules
- Add timetable entries
- Visual tool: `/timetable/visual-tool/`

### 7. Students
- Go to: `http://localhost:8000/student/`
- Full student management
- Students can view own profile at: `/student/my-profile/`

---

## Key Features to Verify

### Performance
- Open sidebar - animations should be smooth
- Click menu items - no lag
- Expand/collapse submenus - fast response

### Security  
- Try accessing admin features as teacher - should get "Access denied"
- Try accessing teacher routes as student - should be forbidden
- Logout and try accessing pages - should redirect to login

### Data Validation
- Try adding teacher without required fields - should show error
- Try adding subject without department - should not allow
- Image uploads should work for students

### Admin Interface
- Go to: `http://localhost:8000/admin`
- All models should be visible and manageable
- Filtering and search should work
- Can add/edit/delete via admin

---

## Troubleshooting

### Issue: "Page not found" on teacher/department pages

**Solution:** Make sure migrations are applied:
```bash
python manage.py migrate
python manage.py runserver
```

### Issue: Add/Edit forms show errors

**Solution:** Check that all required fields are filled

### Issue: Images not displaying

**Solution:** 
1. Create media folder: `mkdir media`
2. Update settings.py if needed
3. Restart server

### Issue: Permission denied errors

**Solution:** Verify user has correct role:
- Admin: `is_admin = True`
- Teacher: `is_teacher = True`
- Student: `is_student = True`

---

## Admin Panel Access

**URL:** `http://localhost:8000/admin/`

**Available Models:**
- Custom Users (manage accounts)
- Teachers (manage teacher profiles)
- Students (manage students)
- Parents (manage parent info)
- Departments (manage departments)
- Subjects (manage subjects)
- Exams (manage exams)
- Grades (manage grades)
- Holidays (manage holidays)
- Subject Proposals (review proposals)

---

## File Structure

```
School-PFM-Django-/
├── manage.py              # Main management script
├── db.sqlite3            # Database (auto-created)
├── requirements.txt      # Python dependencies
├── FIXES_IMPLEMENTATION.md  # Detailed changes
├── README.md             # This file
│
├── school/               # Project settings
│   ├── settings.py       # Configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI config
│
├── home_auth/           # Authentication module
│   ├── models.py        # CustomUser model
│   ├── views.py         # Auth views
│   ├── urls.py          # Auth routes
│   └── decorators.py    # Role-based decorators
│
├── student/             # Student management
│   ├── models.py        # Student, Parent models
│   ├── views.py         # Student CRUD
│   └── urls.py          # Student routes
│
├── staff/               # Teacher management
│   ├── models.py        # Teacher model
│   ├── views.py         # Teacher CRUD
│   └── urls.py          # Staff routes
│
├── academic/            # Academic modules
│   ├── models.py        # Department, Subject, Exam, etc.
│   ├── views.py         # Academic views
│   ├── urls.py          # Academic routes
│   └── admin.py         # Admin configurations
│
├── timetable/          # Timetable management
│   ├── models.py       # TimeTable model
│   ├── views.py        # Timetable views
│   └── urls.py         # Timetable routes
│
├── faculty/            # Home/Dashboard
│   ├── views.py        # Dashboard views
│   └── urls.py         # Home routes
│
├── static/             # Static files
│   └── assets/         # CSS, JS, Images
│
└── templates/          # HTML templates
    ├── Home/           # Base templates
    ├── academic/       # Academic templates
    ├── staff/          # Staff templates
    ├── students/       # Student templates
    ├── authentication/ # Auth templates
    └── timetable/      # Timetable templates
```

---

## Important Notes

1. **In Production:**
   - Change `DEBUG = False` in settings.py
   - Set a unique `SECRET_KEY`
   - Use environment variables for passwords
   - Enable HTTPS/SSL
   - Use PostgreSQL instead of SQLite

2. **Database:**
   - SQLite is fine for development/testing
   - For production, migrate to PostgreSQL or MySQL

3. **Static Files:**
   - For production: `python manage.py collectstatic`
   - Serve with Nginx or Apache

4. **Email (Optional):**
   - Configure email backend in settings.py
   - Set email credentials for password reset

---

## Contact & Support

**Issues Found:**
- Check `FIXES_IMPLEMENTATION.md` for detailed information
- Review error messages carefully  
- Check browser console for JavaScript errors

**Common Commands:**
```bash
# Run tests
python manage.py test

# Create new app
python manage.py startapp appname

# Shell access
python manage.py shell

# Dump database
python manage.py dumpdata > backup.json

# Load database
python manage.py loaddata backup.json

# Clear cache
python manage.py cache_clear
```

---

## Success Checklist

- [ ] Server runs without errors: `python manage.py runserver`
- [ ] Can login as admin
- [ ] Can access admin panel
- [ ] Teachers module works (add/edit/delete)
- [ ] Departments module works
- [ ] Can add subjects with department
- [ ] Can add exams and grades
- [ ] Sidebar animations are smooth
- [ ] Role-based access control working
- [ ] All URLs accessible and working

---

**Version:** 1.0
**Last Updated:** March 27, 2026
**Status:** Ready for Testing ✅
