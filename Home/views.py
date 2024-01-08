from datetime import datetime
from django.shortcuts import render
import csv
from io import StringIO
import json
from django.core.files.storage import FileSystemStorage
import random
import os
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import create_tables
from django.contrib import messages
from colorcode import Color, print_colored
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404


'''
Functions and Views:

1. print_colored(*args, color=Color.DEFAULT): Prints text to the console with specified color.
2. get_all_faculties(sort=None): Fetches all faculty records from the database, optionally sorted.
3. update_faculty(request, faculty_id): Renders and processes updates for faculty details.
4. update_faculty_in_database(updated_data, faculty_id): Updates faculty details in the database.
5. delete_faculty(request, faculty_id): Deletes a faculty record from the database.
6. update_faculty_idv(request, faculty_id): Renders and processes updates for individual faculty details.
7. Various functions for adding details (e.g., add_faculty_details, add_conference_details, add_education_details): Render pages for adding different details.
8. Various ID generators (e.g., exp_id_generator, patent_id_generator): Generate unique IDs for different entities.
9. Various update functions (e.g., update_certificate_idv, update_conference_idv): Update details based on individual IDs.
10. report_view_gender(request): Renders a page displaying gender-related reports.
11. gender_report(): Generates gender-related data for reporting.
12. department_join_report(request): Renders a page displaying department-related reports.
13. conference_join_report(request): Renders a page displaying conference-related reports.
14. report_generation(request): Renders a page for report generation.

'''

# -------------------------------------------------------------------------Some SELECT statements-----------------------------------------------------------------------------------------------------------
def return_admin():
    raw_sql_query = """
    SELECT * FROM adminuser;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                return data
    except Exception as e:
        print(f"Error executing |return_admin| SQL query: {e}")


def return_faculty_credential():
    raw_sql_query = """
    SELECT * FROM credential;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                return data
    except Exception as e:
        print(f"Error executing |return_faculty_credential| SQL query: {e}")


def get_faculty_id(username):
    raw_sql_query = f"""
    SELECT FacultyID FROM credential
    WHERE Username = '{username}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchone()
                return data
    except Exception as e:
        print(f"Error executing |get_faculty_id| SQL query: {e}")


def get_admin_id(username):
    raw_sql_query = f"""
    SELECT id FROM adminuser
    WHERE username = '{username}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchone()
                return data
    except Exception as e:
        print(f"Error executing |get_admin_id| SQL query: {e}")

# -------------------------------------------------------------------------ID generators-----------------------------------------------------------------------------------------------------------
def exp_id_generator():
    raw_sql_query = f"""
        SELECT expID FROM WorkExperience;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
            id = random.randint(1000, 9999)
            if not any(( id == int(x[0])) for x in data):
                return id
            id2 = random.randint(1000, 9999)
            return id2
        
    except Exception as e:
        print(e)
        id2 = random.randint(1000, 9999)
        return id2
        
    

def patent_id_generator():
    raw_sql_query = f"""
        SELECT PatentID FROM patent;"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
            id = random.randint(1000, 9999)
            if not any(( id == int(x[0])) for x in data):
                return id
            id2 = random.randint(1000, 9999)

            return id2

    except Exception as e:
        print(e)
        id2 = random.randint(1000, 9999)
        return id2


def cert_id_generator():
    raw_sql_query = """
        SELECT CertID FROM Certificate;"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
            id = random.randint(1000, 9999)
            if not any(( id == int(x[0])) for x in data):
                return id
            id2 = random.randint(1000, 9999)

            return id2

    except Exception as e:
        print(e)
        id2 = random.randint(1000, 9999)
        return id2

def edu_id_generator():
    raw_sql_query = """
        SELECT EduID FROM EducationDetails;"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
            id = random.randint(1000, 9999)
            if not any(( id == int(x[0])) for x in data):
                return id
            id2 = random.randint(1000, 9999)

            return id2

    except Exception as e:
        print(e)
        id2 = random.randint(1000, 9999)
        return id2


def faculty_id_generator():
    raw_sql_query = """
        SELECT FacultyID FROM Faculty;"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
            id = random.randint(1000, 9999)
            if not any(( id == int(x[0])) for x in data):
                return id
            id2 = random.randint(1000, 9999)

            return id2

    except Exception as e:
        print(e)
        id2 = random.randint(1000, 9999)
        return id2

def paper_id_generator():
    raw_sql_query = """
        SELECT PaperID FROM Paper;"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
            id = random.randint(1000, 9999)
            if not any(( id == int(x[0])) for x in data):
                return id
            id2 = random.randint(1000, 9999)

            return id2

    except Exception as e:
        print(e)
        id2 = random.randint(1000, 9999)
        return id2


def conference_id_generator():
    raw_sql_query = """
        SELECT ConferenceID FROM Conference;"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
            id = random.randint(1000, 9999)
            if not any(( id == int(x[0])) for x in data):
                return id
            id2 = random.randint(1000, 9999)

            return id2

    except Exception as e:
        print(e)
        id2 = random.randint(1000, 9999)
        return id2
def id_generator():
    faculty_id = random.randint(1000, 9999)
    return faculty_id

# -------------------------------------------------------------------------Login-----------------------------------------------------------------------------------------------------------
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        admin_credentials = return_admin()
        faculty_credentials = return_faculty_credential()

        print_colored(faculty_credentials, color=Color.GREEN)
        if any((username == admin_user[1] and password == admin_user[2]) for admin_user in admin_credentials):
            admin_id = get_admin_id(username)[0]
            request.session['admin_id'] = admin_id
            return redirect(f'adminfis/{admin_id}')

        
        elif any((username == faculty_user[1] and password == faculty_user[2]) for faculty_user in faculty_credentials):
            faculty_id = get_faculty_id(username)[0]
            request.session['faculty_id'] = faculty_id
            print_colored(faculty_id)
            return redirect(f'teacher/{faculty_id}')


        else:
            return render(request, 'login.html')

# -------------------------------------------------------------------------SELECT commands-----------------------------------------------------------------------------------------------------------
def get_teacher_details(teacher_id):
    raw_sql_query = f"""
    SELECT * FROM faculty
    WHERE FacultyId = '{teacher_id}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchone()
                context = {
                    'teacher_id' : data[0] , 
                    'first_name' : data[1], 
                    'last_name' : data[2], 
                    'dob' : data[3], 
                    'gender' : data[4], 
                    'phone' : data[5], 
                    'email' : data[6], 
                    'address' : data[7]
                    }
                return context
    except Exception as e:
        print(f"Error executing |get_teacher_details| SQL query: {e}")


def get_admin_details(admin_id):
    raw_sql_query = f"""
    SELECT * FROM adminuser
    WHERE id = '{admin_id}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchone()
                context = {
                    'admin_id': data[0],
                    'username': data[1]
                }
                return context
    except Exception as e:
        print(f"Error executing |get_admin_details| SQL query: {e}")

def get_certificate(teacher_id):
    certificate_query = f"""
    SELECT CertID, FacultyID, CertificateName, IssuingAuthority, IssueDate
    FROM CERTIFICATE
    WHERE FacultyID = '{teacher_id}'
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(certificate_query)
            if cursor.description:
                data = cursor.fetchall()
                context = []
                for datum in data:
                    dict_temp = {
                        'certID' : datum[0] , 
                        'facultyID' : datum[1], 
                        'name' : datum[2], 
                        'issueAuth' : datum[3], 
                        'issueDate' : datum[4]
                        }
                    context.append(dict_temp)
                certificate =  context
                return certificate
    except Exception as e:
        print(f"Error executing |get_certificate| SQL query: {e}")


def get_conference(teacher_id):
    conference_query = f"""
    SELECT ConferenceID, FacultyID, ConferenceName, Location, DateAttended
    FROM CONFERENCE
    WHERE FacultyID = '{teacher_id}'
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(conference_query)
            if cursor.description:
                data = cursor.fetchall()
                context = []
                for datum in data:
                    dict_temp = {
                        'conferenceID': datum[0],
                        'facultyID': datum[1],
                        'name': datum[2],
                        'location': datum[3],
                        'date': datum[4]
                    }
                    context.append(dict_temp)
                conference = context
                print_colored(conference)
                return conference
    except Exception as e:
        print(f"Error executing |get_conference| SQL query: {e}")


def get_education(teacher_id):
    education = f"""
    SELECT EduID,FacultyID,Degree,Major,University,YearOfPassing
    FROM EDUCATIONDETAILS
    WHERE FacultyId = '{teacher_id}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(education)
            if cursor.description:
                data = cursor.fetchall()
                context = []
                for datum in data:
                    dict_temp = {
                        'eduID': datum[0],
                        'facultyID': datum[1],
                        'degree': datum[2],
                        'major': datum[3],
                        'uni': datum[4],
                        'yearofpass': datum[5]
                    }
                    context.append(dict_temp)

                return context
    except Exception as e:
        print(f"Error executing |get_education| SQL query: {e}")
    
def get_paper(teacher_id):
    paper = f"""
    SELECT PaperID, FacultyID, Title, Journal, PublicationDate
    FROM paper
    WHERE FacultyId = '{teacher_id}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(paper)
            if cursor.description:
                data = cursor.fetchall()
                context = []
                for datum in data:
                    dict_temp = {
                        'paperID': datum[0],
                        'facultyID': datum[1],
                        'title': datum[2],
                        'journal': datum[3],
                        'date': datum[4]
                    }
                    context.append(dict_temp)

                return context
    except Exception as e:
        print(f"Error executing |get_paper| SQL query: {e}")


def get_patent(teacher_id):
    patent = f"""
    SELECT PatentID, FacultyID, Title, PatentNumber, DateIssued
    FROM patent
    WHERE FacultyId = '{teacher_id}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(patent)
            if cursor.description:
                data = cursor.fetchall()
                context = []
                for datum in data:
                    dict_temp = {
                        'patentID': datum[0],
                        'facultyID': datum[1],
                        'title': datum[2],
                        'patentnum': datum[3],
                        'date': datum[4]
                    }
                    context.append(dict_temp)

                return context
    except Exception as e:
        print(f"Error executing |get_patent| SQL query: {e}")

def get_workexp(teacher_id):
    WorkExperience = f"""
    SELECT ExpID,FacultyID,Organization,Position,Experience
    FROM WorkExperience
    WHERE FacultyId = '{teacher_id}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(WorkExperience)
            if cursor.description:
                data = cursor.fetchall()
                context = []
                for datum in data:
                    dict_temp = {
                        'expID': datum[0],
                        'facultyID': datum[1],
                        'ord': datum[2],
                        'position': datum[3],
                        'experience' : datum[4]
                    }
                    context.append(dict_temp)

                return context
    except Exception as e:
        print(f"Error executing |get_workexp| SQL query: {e}")

def get_salary(teacher_id):
    salary = f"""
    SELECT SalaryID,FacultyID,Amount,PaymentDate,Semester
    FROM Salary
    WHERE FacultyId = '{teacher_id}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(salary)
            if cursor.description:
                data = cursor.fetchall()
                context = []
                for datum in data:
                    dict_temp = {
                        'salaryID': datum[0],
                        'facultyID': datum[1],
                        'amt': datum[2],
                        'paydate': datum[3],
                        'sem': datum[4]
                    }
                    context.append(dict_temp)

                return context
    except Exception as e:
        print(f"Error executing |get_salary| SQL query: {e}")

def get_teaching(teacher_id):
    teaching = f"""
    SELECT CourseID,FacultyID,Semester,Year,Department,Position,LeavesTaken,LeavesAllotted
    FROM teaching
    WHERE FacultyId = '{teacher_id}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(teaching)
            if cursor.description:
                data = cursor.fetchall()
                context = []
                for datum in data:
                    dict_temp = {
                        'courseID': datum[0],
                        'facultyID': datum[1],
                        'sem': datum[2],
                        'year': datum[3],
                        'department': datum[4],
                        'position': datum[5],
                        'leavesTaken': datum[6],
                        'LeavesAlloted': datum[7],
                    }
                    context.append(dict_temp)
                print_colored(context, color=Color.RED)
                return context
    except Exception as e:
        print(f"Error executing |get_teaching| SQL query: {e}")
        
def get_faculty_by_gender(gender = 'Male', sort=None):
    raw_sql_query = f"""
    SELECT FacultyID, FirstName, LastName, DateOfBirth, Gender, ContactNumber, Email, Address 
    FROM faculty
    WHERE gender = '{gender}'
    """
    if sort is not None:
        raw_sql_query = f"{raw_sql_query}\nORDER BY {sort};"
    else:
        raw_sql_query += ";"
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                keys_tuple = ('FacultyID', 'FirstName', 'LastName',
                              'DateOfBirth', 'Gender', 'ContactNumber', 'Email', 'Address')
                context = []
                for datum in data:
                    faculty_dict = dict(zip(keys_tuple, datum))
                    context.append(faculty_dict)
                return context
    except Exception as e:
        print(f"Error executing |get_faculty_by_gender| SQL query: {e}")
        return []
    
def get_all_faculties(sort=None):
    # Fetch all faculties from the database
    raw_sql_query = """
    SELECT FacultyID, FirstName, LastName, DateOfBirth, Gender, ContactNumber, Email, Address 
    FROM faculty
    """
    if sort is not None:
        raw_sql_query = f"{raw_sql_query}\nORDER BY {sort};"
    else:
        raw_sql_query += ";"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                keys_tuple = ('FacultyID', 'FirstName', 'LastName',
                              'DateOfBirth', 'Gender', 'ContactNumber', 'Email', 'Address')
                context = []
                for datum in data:
                    faculty_dict = dict(zip(keys_tuple, datum))
                    context.append(faculty_dict)
                return context
    except Exception as e:
        print(f"Error executing |get_all_faculties| SQL query: {e}")
        return []

def selected_faculties(id, sort=None):
    raw_sql_query = f"""
    SELECT FacultyID, FirstName, LastName,DateOfBirth, Gender, ContactNumber, Email, Address FROM faculty
    WHERE facultyid = '{id}'
    """
    if sort is not None:
        raw_sql_query = f"{raw_sql_query}\nORDER BY {sort};"
    else:
        raw_sql_query += ";"
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchone()
                
                keys_tuple = ('FacultyID', 'FirstName', 'LastName',
                              'DateOfBirth', 'Gender', 'ContactNumber', 'Email', 'Address')
                context = dict(zip(keys_tuple, data))
                
                return context
    except Exception as e:
        print(f"Error executing |selected_faculties| SQL query: {e}")

def selected_faculties_by_name(name, sort=None):
    raw_sql_query = f"""
    SELECT FacultyID, FirstName, LastName,DateOfBirth, Gender, ContactNumber, Email, Address 
    FROM faculty
    WHERE FirstName LIKE '{name}%'
    """

    if sort is not None:
        raw_sql_query = f"{raw_sql_query}\nORDER BY {sort};"
    else:
        raw_sql_query += ";"

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                keys_tuple = ('FacultyID', 'FirstName', 'LastName',
                              'DateOfBirth', 'Gender', 'ContactNumber', 'Email', 'Address')
                context = []
                for datum in data:
                    context.append(dict(zip(keys_tuple, datum)))
                return context
    except Exception as e:
        print(f"Error executing |selected_faculties_by_name| SQL query: {e}")

# -------------------------------------------------------------------------teacher dashboard and view_teacher-----------------------------------------------------------------------------------------------------------
def teacher_dashboard(request, teacher_id):
    context = get_teacher_details(teacher_id)
    
    return render(request, 'teacher_dashboard.html', context)

def view_teacher(request, teacher_id):
    teacher = get_teacher_details(teacher_id)
    teaching = get_teaching(teacher_id)
    paper = get_paper(teacher_id)
    patent = get_patent(teacher_id)
    work_exp = get_workexp(teacher_id)
    certificate = get_certificate(teacher_id)
    conference = get_conference(teacher_id)
    education = get_education(teacher_id)
    salary = get_salary(teacher_id)

    return render(request, 'view_teacher.html', {
        'teacher': teacher,
        'teaching': teaching,
        'paper': paper,
        'patent': patent,
        'work_exp': work_exp,
        'certificate': certificate,
        'conference': conference,
        'education': education,
        'salary': salary,
        'teacher_id': teacher_id
    })
    

def update_teacher(request, teacher_id):
    pass

#-------------------------------------------------------------------------admin home and add faculty-----------------------------------------------------------------------------------------------------------
def admin_home(request, admin_id):
    context = get_admin_details(admin_id)
    admin_id_login = request.session.get('admin_id')
    print_colored(admin_id_login)
    return render(request, 'admin_home.html', context)


def add_faculty(request, admin_id):
    admin_id_login = request.session.get('admin_id')
    print_colored(admin_id_login)
    if request.method == "GET":
        return render(request, 'add_faculty.html', {'admin_id': admin_id, 'admin_id_login' : admin_id_login})
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        id = id_generator()
        with connection.cursor() as cursor:
            # Assuming your table is named 'faculty'
            cursor.execute("""INSERT INTO faculty (FacultyID, FirstName, LastName, DateOfBirth, Gender, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                           (id, first_name, last_name, date_of_birth, gender, contact_number, email, address))

        messages.success(request, 'Faculty has been added successfully!')
        return redirect('admin_home', admin_id=admin_id)

#-------------------------------------------------------------------------Manage_faculty - admin-----------------------------------------------------------------------------------------------------------
def manage_faculty(request):
    sort = None
    admin_id_login = request.session.get('admin_id')
    print_colored(admin_id_login)
    if request.method == "GET":
        faculties = get_all_faculties(sort)
        return render(request, 'manage_faculty.html', {'faculties': faculties, 'admin_id_login' : admin_id_login})
    if request.method == "POST":
        if request.POST.get('search_category') == 'id':
            id1 = request.POST.get('search')
            id2 = request.POST.get('search_id')
            if request.POST.get('sort') != "":
                sort = request.POST.get('sort')
            result_id = id1 if id1 is not None else id2
            faculties = (selected_faculties(result_id, sort),)
            if any(faculties) is False:
                
                if request.POST.get('filter') is None:
                    faculties = get_all_faculties(sort)
                else:
                    gender = request.POST.get('filter')
                    faculties = get_faculty_by_gender(gender, sort)
        if request.POST.get('search_category') == 'name':
            name = request.POST.get('search_name')
            if request.POST.get('sort') != "":
                sort = request.POST.get('sort')
            faculties = selected_faculties_by_name(name, sort)

            if faculties is None:
                if request.POST.get('filter') is None:
                    faculties = get_all_faculties(sort)
                else:
                    gender = request.POST.get('filter')
                    faculties = get_faculty_by_gender(gender, sort)
        return render(request, 'manage_faculty.html', {'faculties': faculties, 'admin_id_login': admin_id_login})


def update_faculty(request, faculty_id):
    context = get_teacher_details(faculty_id)

    if request.method == "GET":
        return render(request, 'update_faculty.html', context)

    if request.method == "POST":
        update_faculty_in_database(request.POST, faculty_id)
        return redirect('manage_faculty')


def update_faculty_in_database(updated_data, faculty_id):
    # Update faculty details in the database
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE faculty
            SET FirstName = %s, LastName = %s, DateOfBirth = %s, Gender = %s, ContactNumber = %s, Email = %s, Address = %s
            WHERE FacultyID = %s
        """, (
            updated_data['first_name'],
            updated_data['last_name'],
            updated_data['date_of_birth'],
            updated_data['gender'],
            updated_data['contact_number'],
            updated_data['email'],
            updated_data['address'],
            faculty_id
        ))



def update_faculty_idv(request, faculty_id):
    teacher = get_teacher_details(faculty_id)        
    teaching = get_teaching(faculty_id)
    paper = get_paper(faculty_id)                       
    patent = get_patent(faculty_id)
    work_exp = get_workexp(faculty_id)
    certificate = get_certificate(faculty_id)
    conference = get_conference(faculty_id)
    education = get_education(faculty_id)
    salary = get_salary(faculty_id)
    
    print(teacher)
    if request.method == "GET":
        
        return render(request, 'update_faculty_idv.html', {'teacher': teacher,
                                                       'teaching': teaching,
                                                       'paper': paper,
                                                       'patent': patent,
                                                       'work_exp': work_exp,
                                                       'certificate': certificate,
                                                       'conference': conference,
                                                       'education': education,
                                                       'salary': salary, })
    
    update_faculty_in_database(request.POST, faculty_id)
    return render(request, 'teacher_dashboard.html', {'first_name': teacher['first_name'], 'email': teacher['email'], 'teacher_id': teacher['teacher_id']})

def delete_faculty(request, faculty_id):
    raw_sql_query = f"""
    DELETE FROM Faculty 
    WHERE facultyId = '{faculty_id}'
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_sql_query)
    return redirect('manage_faculty')

#-------------------------------------------------------------------------add_idv_details-----------------------------------------------------------------------------------------------------------

def add_faculty_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher' : teacher})
    if request.method == "POST":
        for req, val in request.POST.items():
            pass
        return HttpResponse("POST REQUEST")

def add_conference_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})


def add_education_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    

def add_certificate_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})


def add_patent_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    

def add_paper_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    

def add_work_exp_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        organization = request.POST.get('organization')
        position = request.POST.get('position')
        experience = request.POST.get('experience')
        exp_id = exp_id_generator()

        raw_sql_query = f"""
        INSERT INTO WorkExperience (ExpID, FacultyID, Organization, Position, Experience)
        VALUES ('{exp_id}','{faculty_id}','{organization}','{position}','{experience}')"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_sql_query)
        except Exception as e:
            print(e)
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    
    
def add_education_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        degree = request.POST.get('degree')
        major = request.POST.get('major')
        university = request.POST.get('university')
        year_of_passing = request.POST.get('yearOfPassing')
        edu_id = edu_id_generator()

        raw_sql_query = f"""
        INSERT INTO EducationDetails (EduID, FacultyID, Degree, Major, University, YearOfPassing)
        VALUES ('{edu_id}', '{faculty_id}', '{degree}', '{major}', '{university}', '{year_of_passing}')"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_sql_query)
        except Exception as e:
            print(e)
        return render(request, 'add_faculty_details.html', {'teacher': teacher})


def add_certificate_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        certificate_name = request.POST.get('certificateName')
        issuing_authority = request.POST.get('issuingAuthority')
        issue_date = request.POST.get('issueDate')
        cert_id = cert_id_generator()


        raw_sql_query = f"""
        INSERT INTO Certificate (CertID, FacultyID, CertificateName, IssuingAuthority, IssueDate)
        VALUES ('{cert_id}', '{faculty_id}', '{certificate_name}', '{issuing_authority}', '{issue_date}')"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_sql_query)
        except Exception as e:
            print(e)
        return render(request, 'add_faculty_details.html', {'teacher': teacher})

def add_patent_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        title = request.POST.get('title')
        patent_number = request.POST.get('patentNumber')
        date_issued = request.POST.get('dateIssued')
        patent_id = patent_id_generator()

        raw_sql_query = f"""
        INSERT INTO Patent (PatentID, FacultyID, Title, PatentNumber, DateIssued)
        VALUES ('{patent_id}', '{faculty_id}', '{title}', '{patent_number}', '{date_issued}')"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_sql_query)
        except Exception as e:
            print(e)
        return render(request, 'add_faculty_details.html', {'teacher': teacher})

def add_paper_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        paper_title = request.POST.get('paperTitle')
        journal = request.POST.get('journal')
        publication_date = request.POST.get('publicationDate')
        paper_id = paper_id_generator()

        raw_sql_query = f"""
        INSERT INTO Paper (PaperID, FacultyID, Title, Journal, PublicationDate)
        VALUES ('{paper_id}', '{faculty_id}', '{paper_title}', '{journal}', '{publication_date}')"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_sql_query)
        except Exception as e:
            print(e)
        return render(request, 'add_faculty_details.html', {'teacher': teacher})


def add_conference_details(request, faculty_id):
    teacher = get_teacher_details(faculty_id)
    if request.method == "GET":
        return render(request, 'add_faculty_details.html', {'teacher': teacher})
    if request.method == "POST":
        conference_name = request.POST.get('conferenceName')
        location = request.POST.get('location')
        date_attended = request.POST.get('date')
        conference_id = conference_id_generator()

        raw_sql_query = f"""
        INSERT INTO Conference (ConferenceID, FacultyID, ConferenceName, Location, DateAttended)
        VALUES ('{conference_id}', '{faculty_id}', '{conference_name}', '{location}', '{date_attended}')"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_sql_query)
        except Exception as e:
            print(e)
        return render(request, 'add_faculty_details.html', {'teacher': teacher})

#---------------------------------------------------------------------------update_idv_details---------------------------------------------------------------------------------------------------------------
def update_certificate_idv(request, faculty_id, certificate_id):
    teacher = get_teacher_details(faculty_id)
    certificate = request.POST
    certificate_file = request.FILES.get('certificateFile')

    if certificate_file:
        # Save the file temporarily
        fs = FileSystemStorage()
        filename = fs.save(certificate_file.name, certificate_file)

        # Move the file to the specified folder
        upload_folder = 'C:/Users/HARI/Desktop/FIS/media'
        source = fs.path(filename)
        destination = os.path.join(upload_folder, filename)
        os.rename(source, destination)

        # Construct the file path
        path_file = f"{upload_folder}/{filename}"

    with connection.cursor() as cursor:
        cursor.execute(f"""
            UPDATE certificate
            SET CertificateName = '{certificate['title']}', IssuingAuthority = '{certificate['issuer']}',
            IssueDate = '{certificate['issue_date']}', FilePath = '{path_file}'
            WHERE FacultyID = '{faculty_id}' AND CertID = '{certificate_id}'
        """)

    return render(request, 'teacher_dashboard.html', {'first_name': teacher['first_name'], 'email': teacher['email'], 'teacher_id': teacher['teacher_id']})



def update_conference_idv(request, faculty_id, conference_id):
    teacher = get_teacher_details(faculty_id)
    conference = request.POST
    with connection.cursor() as cursor:
        cursor.execute(f"""
            UPDATE conference
            SET ConferenceName = '{conference['conferenceName']}', Location = '{conference['location']}', dateAttended = '{conference['dateAttended']}'
            WHERE FacultyID = '{faculty_id}' AND ConferenceID = '{conference_id}'
        """)

    return render(request, 'teacher_dashboard.html', {'first_name': teacher['first_name'], 'email': teacher['email'], 'teacher_id': teacher['teacher_id']})


def update_education_details_idv(request, faculty_id, education_details_id):
    teacher = get_teacher_details(faculty_id)
    education = request.POST
    with connection.cursor() as cursor:
        cursor.execute(f"""
            UPDATE educationdetails
            SET degree = '{education['degree']}', major = '{education['major']}', university = '{education['university']}', yearOfPassing = '{education['yearOfPassing']}'
            WHERE FacultyID = '{faculty_id}' AND eduID = '{education_details_id}'
        """)

    return render(request, 'teacher_dashboard.html', {'first_name': teacher['first_name'], 'email': teacher['email'], 'teacher_id': teacher['teacher_id']})



def update_paper_idv(request, faculty_id, paper_id):
    teacher = get_teacher_details(faculty_id)
    paper = request.POST
    with connection.cursor() as cursor:
        cursor.execute(f"""
            UPDATE paper
            SET title = '{paper['title']}', journal = '{paper['journal']}', publicationDate = '{paper['publication_date']}'
            WHERE FacultyID = '{faculty_id}' AND paperID = '{paper_id}'
        """)

    return render(request, 'teacher_dashboard.html', {'first_name': teacher['first_name'], 'email': teacher['email'], 'teacher_id': teacher['teacher_id']})

def update_patent_idv(request, faculty_id, patent_id):
    teacher = get_teacher_details(faculty_id)
    patent = request.POST
    with connection.cursor() as cursor:
        cursor.execute(f"""
            UPDATE patent
            SET title = '{patent['title']}', patentNumber = '{patent['patentNumber']}', dateIssued = '{patent['dateIssued']}'
            WHERE FacultyID = '{faculty_id}' AND patentID = '{patent_id}'
        """)

    return render(request, 'teacher_dashboard.html', {'first_name': teacher['first_name'], 'email': teacher['email'], 'teacher_id': teacher['teacher_id']})



def update_work_exp_idv(request, faculty_id, work_exp_id):
    teacher = get_teacher_details(faculty_id)
    work_exp = request.POST
    with connection.cursor() as cursor:
        cursor.execute(f"""
            UPDATE workexperience
            SET organization = '{work_exp['organization']}',  position = '{work_exp['position']}', experience = '{work_exp['experience']}'
            WHERE FacultyID = '{faculty_id}' AND ExpID = '{work_exp_id}'
        """)

    return render(request, 'teacher_dashboard.html', {'first_name': teacher['first_name'], 'email': teacher['email'], 'teacher_id': teacher['teacher_id']})

#-------------------------------------------------------------------------DELETE indv data-------------------------------------------------------------------------------------------------------------


def delete_work_exp_idv(request, faculty_id, work_exp_id):
    raw_sql_query = f"""
    DELETE FROM WorkExperience
    WHERE FacultyID = {faculty_id} AND ExpID = {work_exp_id};
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
    except Exception as e:
        return HttpResponse(e)
    return render(request, 'teacher_dashboard.html', {'teacher_id': faculty_id})


def delete_certificate_idv(request, faculty_id, certificate_id):
    raw_sql_query = f"""
    DELETE FROM Certificate
    WHERE FacultyID = {faculty_id} AND CertID = {certificate_id};
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
    except Exception as e:
        return HttpResponse(e)
    return render(request, 'teacher_dashboard.html', {'teacher_id': faculty_id})


def delete_education_details_idv(request, faculty_id, education_details_id):
    raw_sql_query = f"""
    DELETE FROM EducationDetails
    WHERE FacultyID = {faculty_id} AND EduID = {education_details_id};
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
    except Exception as e:
        return HttpResponse(e)
    return render(request, 'teacher_dashboard.html', {'teacher_id': faculty_id})


def delete_conference_idv(request, faculty_id, conference_id):
    raw_sql_query = f"""
    DELETE FROM Conference
    WHERE FacultyID = {faculty_id} AND ConferenceID = {conference_id};
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
    except Exception as e:
        return HttpResponse(e)
    return render(request, 'teacher_dashboard.html', {'teacher_id': faculty_id})


def delete_paper_idv(request, faculty_id, paper_id):
    raw_sql_query = f"""
    DELETE FROM Paper
    WHERE FacultyID = {faculty_id} AND PaperID = {paper_id};
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
    except Exception as e:
        return HttpResponse(e)
    return render(request, 'teacher_dashboard.html', {'teacher_id': faculty_id})


def delete_patent_idv(request, faculty_id, patent_id):
    raw_sql_query = f"""
    DELETE FROM Patent
    WHERE FacultyID = {faculty_id} AND PatentID = {patent_id};
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
    except Exception as e:
        return HttpResponse(e)
    return render(request, 'teacher_dashboard.html', {'teacher_id': faculty_id})

#-------------------------------------------------------------------------------------------REPORTS---------------------------------------------------------------------------------------------------------
'''
Report types :
    Gender Report
    Conference Report
    Department Report
    Avg Experience Report
'''


def report_generation(request):
    admin_id_login = request.session.get('admin_id')
    admin_id = admin_id_login
    return render(request, 'report_generation.html', {'admin_id' : admin_id, 'admin_id_login' : admin_id_login})

def report_view_gender(request):
    gender_data, male, female = gender_report()
    admin_id_login = request.session.get('admin_id')

    return render(request, 'report_gender.html', {'gender_data': gender_data, 'male':male, 'female':female , 'admin_id_login' : admin_id_login})

def gender_report():
    raw_sql_query = f"""
    SELECT gender, Count(*) as Faculty_Count
    FROM faculty
    GROUP BY gender;"""

    male_data_sql = """SELECT FacultyID, CONCAT(FirstName, ' ', LastName) AS FullName FROM faculty WHERE gender = 'Male';"""
    female_data_sql = """SELECT FacultyID, CONCAT(FirstName, ' ', LastName) AS FullName FROM faculty WHERE gender = 'Female';"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                context = {}
                for key, val in data:
                    context[key] = val

        with connection.cursor() as cursor:
            cursor.execute(male_data_sql)
            if cursor.description:
                data = cursor.fetchall()
                male_data = {}
                for id, name in data:
                    male_data[id] = name

        with connection.cursor() as cursor:
            cursor.execute(female_data_sql)
            if cursor.description:
                data = cursor.fetchall()
                female_data = {}
                for id, name in data:
                    female_data[id] = name
        print_colored(context, male_data, female_data)
        return (context, male_data, female_data)
            
    except Exception as e:
        print(f"Error executing |gender_report| SQL query: {e}")


def department_join_report(request):
    department_sql = """
    SELECT Department, Count(*) as Faculty_Count
    FROM teaching
    GROUP BY department;
    """

    avg_experience_sql = """
    SELECT
        Faculty.FacultyID,
        CONCAT(Faculty.FirstName, ' ', Faculty.LastName) AS FULL_NAME,
        ROUND(AVG(WorkExperience.Experience), 2) AS avg_experience
    FROM
        Faculty
    JOIN
        WorkExperience ON Faculty.FacultyID = WorkExperience.FacultyID
    GROUP BY
        Faculty.FacultyID, Faculty.FirstName, Faculty.LastName;
    """

    all_people_sql = """
    SELECT
        Faculty.FacultyID,
        CONCAT(Faculty.FirstName, ' ', Faculty.LastName) AS FULL_NAME,
        Teaching.Department
    FROM
        Faculty
    JOIN
        Teaching ON Faculty.FacultyID = Teaching.FacultyID
    """

    # Fetch department data
    try:
        with connection.cursor() as cursor:
            cursor.execute(department_sql)
            department_data = dict_fetchall(cursor)
    except Exception as e:
        print(f"Error executing |dept_report| SQL query: {e}")

    # Fetch average experience data
    try:
        with connection.cursor() as cursor:
            cursor.execute(avg_experience_sql)
            avg_experience_data = dict_fetchall(cursor)
    except Exception as e:
        print(f"Error executing |avg_exp| SQL query: {e}")

    # Fetch all people data
    try:
        with connection.cursor() as cursor:
            cursor.execute(all_people_sql)
            all_people_data = dict_fetchall(cursor)
    except Exception as e:
        print(f"Error executing |all_people_data=avg_exp+dept_data| SQL query: {e}")

    # Filter all people data based on the department if a department is specified
    if request.method == "POST":
        dept = request.POST.get('dept')
        if dept:
            all_people_data = [
                person for person in all_people_data if person['Department'] == dept]

    context = {
        'department_data': department_data,
        'avg_experience_data': avg_experience_data,
        'all_people_data': all_people_data,
    }

    return render(request, 'report_department.html', context)


def dict_fetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def conference_join_report(request):
    raw_sql_query = """
    SELECT
        Faculty.FacultyID,
        Faculty.FirstName,
        Faculty.LastName,
        COUNT(Conference.ConferenceID) AS ConferenceCount,
        GROUP_CONCAT(DISTINCT Conference.Location ORDER BY Conference.DateAttended) AS ConferenceLocations
    FROM
        Faculty
        INNER JOIN Conference ON Faculty.FacultyID = Conference.FacultyID
    GROUP BY
        Faculty.FacultyID, Faculty.FirstName, Faculty.LastName;"""

    with connection.cursor() as cursor:
        cursor.execute(raw_sql_query)
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    raw_sql_query = """SELECT ConferenceName, Location FROM Conference;"""
    with connection.cursor() as cursor:
        cursor.execute(raw_sql_query)
        columns = [col[0] for col in cursor.description]
        data2 = [dict(zip(columns, row)) for row in cursor.fetchall()]
    print_colored(data, color=Color.BLUE)
    print_colored(data2)

    conference_locations_json = json.dumps(data2)
    return render(request, 'conference_join_report.html', {'conference_report': data, 'conference_locations': conference_locations_json})

# -------------------------------------------------------------------CSV files reader and uploader-----------------------------------------------------------


def insert_faculty_data(file_content, file_format):
    try:
        if file_format.lower() != 'csv':
            print("Unsupported file format. Please provide a CSV file.")
            return

        # Convert bytes to string
        content_str = file_content.decode('utf-8')

        # Read data from CSV file
        csv_reader = csv.DictReader(StringIO(content_str))

        with connection.cursor() as cursor:
            # Prepare SQL query for insertion
            sql_query = "INSERT INTO Faculty (FacultyID, FirstName, LastName, DateOfBirth, Gender, ContactNumber, Email, Address) VALUES "

            # Iterate over rows in the data and append values to the SQL query
            for row in csv_reader:
                date_of_birth = datetime.strptime(
                    row['DateOfBirth'], '%d-%m-%Y').strftime('%Y-%m-%d')
                values = f"({row['FacultyID']}, '{row['FirstName']}', '{row['LastName']}', '{date_of_birth}', '{row['Gender']}', '{row['ContactNumber']}', '{row['Email']}', '{row['Address']}'),"
                sql_query += values

            # Remove the trailing comma
            sql_query = sql_query.rstrip(',')

            # Execute the SQL query
            cursor.execute(sql_query)

            # Commit the changes to the database
            connection.commit()

            print("Data inserted successfully.")

    except Exception as e:
        print(f"Error executing |csv_all_faculties_data_basic| SQL query: {e}")



def csv_data_collection(request):
    admin_id_login = request.session.get('admin_id')
    print_colored(admin_id_login)
    if request.method == 'POST':
        # Get the uploaded file from the request
        uploaded_file = request.FILES.get('file_upload')

        # Check if a file is provided
        if uploaded_file:
            # Read the content of the file
            file_content = uploaded_file.read()

            # Determine the file format based on the file extension
            file_format = uploaded_file.name.split('.')[-1]

            # Perform the data insertion
            insert_faculty_data(file_content, file_format)

            # Redirect or render a success page
            return render(request, 'csv_collect_give.html', {'admin_id_login': admin_id_login})

    # Render the upload form
    return render(request, 'csv_collect_give.html', {'admin_id_login': admin_id_login})



def return_faculty():
    raw_sql_query = """
    SELECT * FROM faculty;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                return data
    except Exception as e:
        print(f"Error executing |select * from faculty| SQL query: {e}")


def generate_csv(request):
    # Call the function to get faculty data
    faculty_data = return_faculty()

    # Create CSV content
    csv_content = "FacultyID,FirstName,LastName,DateOfBirth,Gender,ContactNumber,Email,Address\n"
    for row in faculty_data:
        csv_content += ",".join(map(str, row)) + "\n"

    # Create a response with CSV content
    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="faculty_data.csv"'

    return response


def download_csv_page(request):
    return render(request, 'download_csv_page.html')


def add_faculty_status_from_csv(request):
    admin_id_login = request.session.get('admin_id')
    admin_id_login = 1234
    print_colored(admin_id_login)

    if request.method == 'POST':
        # Get the uploaded file from the request
        uploaded_file = request.FILES.get('file_upload')

        # Check if a file is provided
        if uploaded_file:
            # Read the content of the file
            file_content = uploaded_file.read().decode('utf-8')

            # Create a CSV reader
            csv_reader = csv.DictReader(StringIO(file_content))

            # Iterate over rows in the CSV and add data to the database
            for row in csv_reader:
                try:
                    print_colored(row, color=Color.RED)
                    # Construct and execute raw SQL query
                    raw_sql_query = f"""
                        INSERT INTO FacultyStatus (FacultyId, AreaOfSpecialization, Designation, DateOfJoining,
                        DateDesignatedAsAssociate, DateDesignatedAsProfessor, CurrentlyAssociate, NatureOfAssociation, ContractType, DateOfLeaving)
                        VALUES (
                            '{row['faculty_id']}',
                            '{row['area_of_specialization']}',
                            '{row['designation']}',
                            '{row['date_of_joining']}',
                            '{row['date_of_associate']}',
                            {f'"{row["date_of_professor"]}"' if 'date_of_professor' in row and row['date_of_professor'] else 'NULL'},
                            {1 if row['currently_associate'] == 'Yes' else 0},
                            '{row['nature_of_association']}',
                            {f'"{row["contract_type"]}"' if 'contract_type' in row and row['contract_type'] else 'NULL'},
                            {f'"{row["date_of_leaving"]}"' if 'date_of_leaving' in row and row['date_of_leaving'] else 'NULL'}
                        );
                    """

                    with connection.cursor() as cursor:
                        cursor.execute(raw_sql_query)

                except Exception as e:
                    # Handle any exceptions or validation errors
                    print(f"Error adding data: {e}")

            # Redirect or render a success page
            return render(request, 'upload_csv.html', {'admin_id_login': admin_id_login})

    # Render the upload form
    return render(request, 'upload_csv.html', {'admin_id_login': admin_id_login})


def update_faculty_status(request):
    admin_id_login = request.session.get('admin_id')
    admin_id_login = 1234

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM FacultyStatus')
        faculty_statuses = dictfetchall(cursor)

    if request.method == 'POST':
        print_colored(request.POST, color=Color.BLUE)
        # Get the form data from the request
        faculty_id = request.POST.get('faculty_id')
        area_of_specialization = request.POST.get('area_of_specialization')
        designation = request.POST.get('designation')
        date_of_joining = request.POST.get('date_of_joining')
        date_of_associate = request.POST.get('date_of_associate')
        date_of_professor = request.POST.get('date_of_professor')
        currently_associate = request.POST.get('currently_associate')
        nature_of_association = request.POST.get('nature_of_association')
        contract_type = request.POST.get('contract_type')
        date_of_leaving = request.POST.get('date_of_leaving')

        # Convert date strings to date objects or set to None if empty or 'None'
        date_of_joining = datetime.strptime(date_of_joining, '%Y-%m-%d').date(
        ) if date_of_joining and date_of_joining.lower() != 'none' else None
        date_of_associate = datetime.strptime(date_of_associate, '%Y-%m-%d').date(
        ) if date_of_associate and date_of_associate.lower() != 'none' else None
        date_of_professor = datetime.strptime(date_of_professor, '%Y-%m-%d').date(
        ) if date_of_professor and date_of_professor.lower() != 'none' else None
        currently_associate = int(
            currently_associate) if currently_associate and currently_associate.lower() != 'none' else None
        date_of_leaving = datetime.strptime(date_of_leaving, '%Y-%m-%d').date(
        ) if date_of_leaving and date_of_leaving.lower() != 'none' else None

        # Update the FacultyStatus table using SQL queries
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE FacultyStatus
                SET AreaOfSpecialization = %s,
                    Designation = %s,
                    DateOfJoining = %s,
                    DateDesignatedAsAssociate = %s,
                    DateDesignatedAsProfessor = %s,
                    CurrentlyAssociate = %s,
                    NatureOfAssociation = %s,
                    ContractType = %s,
                    DateOfLeaving = %s
                WHERE FacultyId = %s
            ''', [area_of_specialization, designation, date_of_joining,
                  date_of_associate, date_of_professor, currently_associate,
                  nature_of_association, contract_type, date_of_leaving, faculty_id])

        # Redirect to the faculty details page or any other appropriate page
        return render(request, 'update_teacher_status.html', {'faculty_statuses': faculty_statuses, 'admin_id_login': admin_id_login})

    else:
        # Retrieve the current faculty status using SQL queries
        return render(request, 'update_teacher_status.html', {'faculty_statuses': faculty_statuses, 'admin_id_login': admin_id_login})

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def update_faculty_status_idv(request, faculty_id):
    admin_id_login = request.session.get('admin_id')
    admin_id_login = 1234


    print_colored(request.POST, color=Color.BLUE)
        # Get the form data from the request
    faculty_id_new = faculty_id
    print_colored(faculty_id_new)
    area_of_specialization = request.POST.get('area_of_specialization')
    designation = request.POST.get('designation')
    date_of_joining = request.POST.get('date_of_joining')
    date_of_associate = request.POST.get('date_of_associate')
    date_of_professor = request.POST.get('date_of_professor')
    currently_associate = request.POST.get('currently_associate')
    nature_of_association = request.POST.get('nature_of_association')
    contract_type = request.POST.get('contract_type')
    date_of_leaving = request.POST.get('date_of_leaving')


        # Convert date strings to date objects or set to None if empty or 'None'
    date_of_joining = datetime.strptime(date_of_joining, '%Y-%m-%d').date(
    ) if date_of_joining and date_of_joining.lower() != 'none' else None
    date_of_associate = datetime.strptime(date_of_associate, '%Y-%m-%d').date(
    ) if date_of_associate and date_of_associate.lower() != 'none' and date_of_associate != '' else None
    date_of_professor = datetime.strptime(date_of_professor, '%Y-%m-%d').date(
    ) if date_of_professor and date_of_professor.lower() != 'none' and date_of_professor != '' else None
    currently_associate = int(
        currently_associate) if currently_associate and currently_associate.lower() != 'none' else None
    date_of_leaving = datetime.strptime(date_of_leaving, '%Y-%m-%d').date(
    ) if date_of_leaving and date_of_leaving.lower() != 'none' else None

    print_colored(date_of_associate, date_of_joining, date_of_leaving,
                date_of_professor, currently_associate)

    # Update the FacultyStatus table using SQL queries
    with connection.cursor() as cursor:
        cursor.execute('''
            UPDATE FacultyStatus
            SET AreaOfSpecialization = %s,
                Designation = %s,
                DateOfJoining = %s,
                DateDesignatedAsAssociate = %s,
                DateDesignatedAsProfessor = %s,
                CurrentlyAssociate = %s,
                NatureOfAssociation = %s,
                ContractType = %s,
                DateOfLeaving = %s
            WHERE FacultyId = %s
        ''', [area_of_specialization, designation, date_of_joining,
            date_of_associate, date_of_professor, currently_associate,
            nature_of_association, contract_type, date_of_leaving, faculty_id_new])

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM FacultyStatus')
        faculty_statuses = dictfetchall(cursor)

    # Redirect to the faculty details page or any other appropriate page
    return render(request, 'update_teacher_status.html', {'faculty_statuses': faculty_statuses, 'admin_id_login': admin_id_login})


def delete_teacher_status_idv(request, faculty_id):
    admin_id_login = request.session.get('admin_id')
    admin_id_login = 1234

    raw_sql_query = f'''
    Delete From facultystatus
    Where FacultyID = {faculty_id};
    '''

    with connection.cursor() as cursor:
        cursor.execute(raw_sql_query)
    
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM FacultyStatus')
        faculty_statuses = dictfetchall(cursor)

    return render(request, 'update_teacher_status.html', {'faculty_statuses': faculty_statuses, 'admin_id_login': admin_id_login})


def faculty_stats_view(request):
    with connection.cursor() as cursor:
        # Get the number of associate professors
        cursor.execute(
            'SELECT COUNT(*) FROM FacultyStatus WHERE Designation = %s', ['Associate Professor'])
        num_associate_professors = cursor.fetchone()[0]
        cursor.execute(
            'SELECT COUNT(*) FROM FacultyStatus WHERE Designation = %s', ['Assistant Professor'])
        num_assistant_professors = cursor.fetchone()[0]
        # Get the number of professors
        cursor.execute(
            'SELECT COUNT(*) FROM FacultyStatus WHERE Designation = %s', ['Professor'])
        num_professors = cursor.fetchone()[0]

    start_date = end_date = None
    professors_present = []
    
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        # Check if start_date_str and end_date_str are not None
        if start_date_str is not None and end_date_str is not None:
            # Convert date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # Run SQL queries to get faculty statistics
            with connection.cursor() as cursor:
                # Get the list of professors present during the specified date range
                cursor.execute('''
                    SELECT Faculty.FacultyId, Faculty.FirstName, Faculty.LastName, FacultyStatus.Designation
                    FROM Faculty
                    INNER JOIN FacultyStatus ON Faculty.FacultyId = FacultyStatus.FacultyId
                    WHERE FacultyStatus.DateOfJoining >= %s
                        AND (FacultyStatus.DateOfLeaving IS NULL OR FacultyStatus.DateOfLeaving <= %s)
                ''', [start_date_str, end_date_str])
                professors_present = dictfetchall(cursor)
                print_colored(professors_present, color=Color.RED) 

        return render(request, 'faculty_stats_view.html', {'num_associate_professors': num_associate_professors, 'num_assistant_professors': num_assistant_professors,'num_professors': num_professors,'professors_present': professors_present
        })
    
    if request.method == "GET":
        return render(request, 'faculty_stats_view.html', {'num_associate_professors': num_associate_professors, 'num_assistant_professors': num_assistant_professors,'num_professors': num_professors,'professors_present': professors_present})



def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def view_profile(request, faculty_id):
    context = get_teacher_details(faculty_id)
    context['profile_img'] = get_profile_img(faculty_id)
    context['certificates'] = get_certificate_url(faculty_id)
    print_colored(context, color=Color.GREEN)
    return render(request, 'profile.html', context)

def certificate_list(request, faculty_id):
    context = get_teacher_details(faculty_id)
    context['profile_img'] = get_profile_img(faculty_id)
    context['certificates'] = get_certificate_url(faculty_id)
    return render(request, 'profile.html', context)


def update_faculty_profile(request, faculty_id):

    if request.method == "GET":
        context = get_teacher_details(faculty_id)
        context['profile_img'] = get_profile_img(faculty_id)
        context['certificates'] = get_certificate_url(faculty_id)
        return render(request, 'profile.html', context)

    if request.method == "POST":
        update_faculty_in_database(request.POST, faculty_id)
        context = get_teacher_details(faculty_id)
        context['profile_img'] = get_profile_img(faculty_id)
        context['certificates'] = get_certificate_url(faculty_id)
        return render(request, 'profile.html', context)


def update_profile_image(request, faculty_id):
    
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        print_colored(profile_image, color=Color.BLUE)
        # Save the image to the media folder
        if profile_image:
            media_path = os.path.abspath(f'static/img/{faculty_id}_{profile_image.name}')
            with open(media_path, 'wb+') as destination:
                for chunk in profile_image.chunks():
                    destination.write(chunk)
            
            # Update the database with the image URL
            with connection.cursor() as cursor:
                cursor.execute("UPDATE faculty SET profile_img = %s WHERE facultyid = %s", [
                            media_path, faculty_id])

            context = get_teacher_details(faculty_id)
            context['profile_img'] = get_profile_img(faculty_id)
            context['certificates'] = get_certificate_url(faculty_id)

            print_colored(context, color=Color.GREEN)
            return render(request, 'profile.html', context)

    context = get_teacher_details(faculty_id)
    context['profile_img'] = get_profile_img(faculty_id)
    context['certificates'] = get_certificate_url(faculty_id)

    print_colored(context, color=Color.RED)

    return render(request, 'profile.html', context)


def get_profile_img(faculty_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT profile_img FROM faculty WHERE facultyid = %s", [faculty_id])
        row = cursor.fetchone()
        print_colored(row)
        if row:
            return row[0]  # Return the profile_img
        else:
            return None  # No matching faculty ID found


def view_certificate(request, faculty_id, certificate_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT filePath FROM certificate WHERE facultyid = %s AND certid = %s", [faculty_id, certificate_id])
        row = cursor.fetchone()

    # Check if the file path exists
    if row and row[0]:
        file_path = row[0]
        try:
            # Open the file in binary mode
            with open(file_path, 'rb') as file:
                # Create an HttpResponse with the file content
                response = HttpResponse(
                    file.read(), content_type='application/pdf')

                # Set the Content-Disposition header for force download
                response[
                    'Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'

                return response
        except FileNotFoundError:
            # Raise Http404 if the file is not found
            raise Http404("File not found")
    else:
        # Raise Http404 if the file path is not available
        raise Http404("File path not available")

def get_certificate_url(teacher_id):
    certificate_query = f"""
    SELECT CertID, CertificateName, Filepath
    FROM CERTIFICATE
    WHERE FacultyID = '{teacher_id} '
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(certificate_query)
            if cursor.description:
                data = cursor.fetchall()
                context = []
                for datum in data:
                    dict_temp = {
                        'certID': datum[0],
                        'name': datum[1],
                        'path' : datum[2]
                    }
                    context.append(dict_temp)
                certificate = context
                print_colored(certificate)
                return certificate
    except Exception as e:
        print(f"Error executing |get_certificate_url| SQL query: {e}")
