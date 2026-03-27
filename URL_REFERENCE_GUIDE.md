# PreSchool Application - URL Reference & Feature Map

## 🗺️ Complete URL Map

### Authentication URLs
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Login | `/authentication/login/` | POST | No | None |
| Signup | `/authentication/signup/` | POST | No | None |
| Logout | `/authentication/logout/` | GET | Yes | Any |
| Forgot Password | `/authentication/forgot-password/` | GET/POST | No | None |

### Home & Dashboard
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Home/Index | `/` | GET | No | None |
| Admin Dashboard | `/dashboard/` | GET | Yes | Admin |
| Student Dashboard | `/student/dashboard/` | GET | Yes | Student |
| Teacher Dashboard | `/dashboard/` | GET | Yes | Teacher |

### Students Module
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Student List | `/student/` | GET | Yes | Any |
| Add Student | `/student/add/` | GET/POST | Yes | Admin |
| View Student | `/student/students/<student_id>/` | GET | Yes | Any |
| Edit Student | `/student/edit/<student_id>/` | GET/POST | Yes | Admin or Owner |
| Delete Student | `/student/delete/<student_id>/` | GET | Yes | Admin |
| My Profile | `/student/my-profile/` | GET | Yes | Student |

### Staff/Teachers Module
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Teacher List | `/staff/teachers/` | GET | Yes | Any |
| Add Teacher | `/staff/teachers/add/` | GET/POST | Yes | Admin |
| Edit Teacher | `/staff/teachers/<teacher_id>/edit/` | GET/POST | Yes | Admin |
| Delete Teacher | `/staff/teachers/<teacher_id>/delete/` | GET | Yes | Admin |

### Academic - Departments
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Department List | `/academic/departments/` | GET | Yes | Any |
| Add Department | `/academic/departments/add/` | GET/POST | Yes | Admin |
| Edit Department | `/academic/departments/<dept_id>/edit/` | GET/POST | Yes | Admin |

### Academic - Subjects
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Subject List | `/academic/subjects/` | GET | Yes | Any |
| Add Subject | `/academic/subjects/add/` | GET/POST | Yes | Admin/Teacher |
| Subject Edit | `/academic/subjects/<subject_id>/edit/` | GET/POST | Yes | Admin/Teacher |

### Academic - Exams
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Exam List | `/academic/exams/` | GET | Yes | Any |
| Add Exam | `/academic/exams/add/` | GET/POST | Yes | Admin |
| Grade List | `/academic/grades/` | GET | Yes | Any |
| Add Grade | `/academic/grades/add/` | GET/POST | Yes | Admin/Teacher |

### Academic - Holidays
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Holiday List | `/academic/holidays/` | GET | Yes | Any |
| Add Holiday | `/academic/holidays/add/` | GET/POST | Yes | Admin |

### Academic - Subject Proposals
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Proposal List | `/academic/proposals/` | GET | Yes | Any |
| Add Proposal | `/academic/proposals/add/` | GET/POST | Yes | Student |
| Approve Proposal | `/academic/proposals/<id>/approve/` | POST | Yes | Admin/Teacher |
| Reject Proposal | `/academic/proposals/<id>/reject/` | POST | Yes | Admin/Teacher |

### Timetable Module  
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Timetable List | `/timetable/` | GET | Yes | Any |
| Add Timetable | `/timetable/add/` | GET/POST | Yes | Admin |
| Visual Tool | `/timetable/visual-tool/` | GET | Yes | Any |
| Export JSON | `/timetable/export-json/` | GET | Yes | Any |

### Admin Panel
| Feature | URL | Method | Auth Required | Role Required |
|---------|-----|--------|---------------|---------------|
| Admin Home | `/admin/` | GET | Yes | Admin |
| Users | `/admin/home_auth/customuser/` | GET | Yes | Admin |
| Teachers | `/admin/staff/teacher/` | GET | Yes | Admin |
| Students | `/admin/student/student/` | GET | Yes | Admin |
| Parents | `/admin/student/parent/` | GET | Yes | Admin |
| Departments | `/admin/academic/department/` | GET | Yes | Admin |
| Subjects | `/admin/academic/subject/` | GET | Yes | Admin |
| Exams | `/admin/academic/exam/` | GET | Yes | Admin |
| Grades | `/admin/academic/grade/` | GET | Yes | Admin |
| Holidays | `/admin/academic/holiday/` | GET | Yes | Admin |
| Proposals | `/admin/academic/subjectproposal/` | GET | Yes | Admin |

---

## 🔐 Access Control Matrix

### By Role

#### 👨‍💼 Admin
```
Can Access:
✅ All modules
✅ All CRUD operations
✅ Admin panel
✅ User management
✅ Data validation/approval
✅ All reports

Cannot:
❌ (No restrictions)
```

#### 👨‍🏫 Teacher
```
Can Access:
✅ Student list
✅ Subject creation
✅ Exam management
✅ Grade entry
✅ Proposal review
✅ Timetable view

Cannot:
❌ Delete any data
❌ Add students
❌ Add holidays
❌ Manage departments
❌ Add teachers
```

#### 👨‍🎓 Student
```
Can Access:
✅ Own profile
✅ Dashboard
✅ Subject proposals
✅ View timetable
✅ View exam results
✅ View holidays

Cannot:
❌ Add/edit/delete anything
❌ View other students' data
❌ Add subjects
❌ Manage grades
❌ Add holidays
```

---

## 🎯 Common User Workflows

### Workflow 1: Adding a New Teacher
```
1. Login as Admin
2. Go to: /staff/teachers/add/
3. Fill form:
   - First Name
   - Last Name
   - Email (becomes username)
   - Password
   - Gender
   - Qualification
   - Experience
   - Mobile Number
   - Department (optional)
   - Joining Date
   - Address
4. Click Submit
5. Teacher appears in list and can now login
```

### Workflow 2: Creating a Department with Head
```
1. Login as Admin
2. Go to: /academic/departments/add/
3. Fill form:
   - Department Name (e.g., "Computer Science")
   - Select Head of Department (choose from existing teachers)
4. Click Submit
5. Department is created and assigned head
```

### Workflow 3: Student Proposing a Subject
```
1. Login as Student
2. Go to: /academic/proposals/add/
3. Fill form:
   - Subject Name
   - Choose Department
   - Description
4. Click Submit
5. Proposal sent for review
6. Admin/Teacher reviews at: /academic/proposals/
7. If approved, becomes official subject
```

### Workflow 4: Teacher Recording Exam Grades
```
1. Login as Teacher
2. Go to: /academic/exams/
3. View available exams
4. Go to: /academic/grades/add/
5. Fill form:
   - Select Student
   - Select Exam
   - Enter Mark/Grade
6. Click Submit
7. Grade is recorded and visible to student
```

---

## 📊 Data Models Relationship

```
CustomUser (from django.contrib.auth)
    ├─→ Teacher (1-to-1 relationship via user field)
    ├─→ Student (1-to-1 relationship via user field)
    └─→ SubjectProposal (proposer field)

Department
    ├─→ head_of_dept (FK to Teacher)
    └─→ Subject (many-to-one)
        ├─→ teacher (FK to Teacher)
        └─→ Exam (many-to-one)
            ├─→ Grade (many-to-one)
            │   └─→ student (FK to Student)
            └─→ TimeTable (many-to-one)

Student (1-to-1 with Parent)
    ├─→ parent (OneToOne to Parent)
    ├─→ Grade (many relationship via Exam)
    └─→ user (OneToOne to CustomUser)

Parent
    └─→ Student (1-to-1 relationship)

TimeTable
    ├─→ subject (FK to Subject)
    ├─→ teacher (FK to Teacher)
    └─→ day (CharField choice)
```

---

## 🔍 Important Query Examples

### For Testing/Management

**Get all teachers:**
```python
# In Django shell: python manage.py shell
from staff.models import Teacher
teachers = Teacher.objects.all()
```

**Get all students:**
```python
from student.models import Student
students = Student.objects.all()
```

**Get departments with heads:**
```python
from academic.models import Department
depts = Department.objects.select_related('head_of_dept')
```

**Get exam results:**
```python
from academic.models import Grade
grades = Grade.objects.select_related('student', 'exam')
```

---

## 🆘 Common Issues & Quick Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| 404 on teacher page | Migration not applied | `python manage.py migrate` |
| Permission denied | Wrong user role | Check `is_admin`/`is_teacher`/`is_student` |
| Forms not submitting | CSRF token missing | Ensure `{% csrf_token %}` in forms |
| Images not showing | Static files issue | `python manage.py collectstatic` |
| Sidebar flicking | JavaScript error | Check browser console for errors |
| Slow animations | Old script.js | Verify script.js is updated |

---

## 📱 API Ready Endpoints

These endpoints can be extended for API/REST usage:

```
GET  /staff/teachers/              # List all teachers
POST /staff/teachers/add/          # Create teacher
GET  /staff/teachers/<id>/edit/    # Retrieve teacher
POST /staff/teachers/<id>/edit/    # Update teacher
GET  /staff/teachers/<id>/delete/  # Delete teacher

GET  /academic/departments/        # List departments
POST /academic/departments/add/    # Create department
... (similar pattern for all modules)
```

---

## 🔄 Testing Credentials

**Default Admin Account:**
```
Username: admin
Email: admin@example.com
Password: (whatever you set during createsuperuser)
```

**To create test accounts:**
1. Go to `/admin/`
2. Login with admin
3. Go to "Custom Users"
4. Click "Add Custom User"
5. Set credentials and roles
6. Save and logout
7. Login with new account to test

---

## 📚 Quick Reference Commands

```bash
# Server management
python manage.py runserver          # Start server
python manage.py runserver 8080     # Use different port

# Database management
python manage.py makemigrations     # Create migrations
python manage.py migrate             # Apply migrations
python manage.py createsuperuser    # Create admin user

# Admin & Utilities
python manage.py shell              # Interactive Python
python manage.py test               # Run tests
python manage.py collectstatic      # Collect static files

# Debugging
python manage.py dbshell            # Database shell
python manage.py dumpdata > backup.json  # Backup
python manage.py loaddata backup.json    # Restore
```

---

**Last Updated:** March 27, 2026  
**Version:** 1.0  
**Status:** Complete & Ready ✅
