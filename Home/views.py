from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .models import create_tables
from django.contrib import messages
from colorcode import Color, print_colored
import random


def return_admin():
    raw_sql_query = """
    SELECT * FROM adminuser;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                print_colored(data)
                return data
    except Exception as e:
        print_colored(f"Error executing SQL query: {e}")


def return_faculty():
    raw_sql_query = """
    SELECT * FROM credential;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                print_colored(data)
                return data
    except Exception as e:
        print_colored(f"Error executing SQL query: {e}")


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
                print_colored(data)
                return data
    except Exception as e:
        print_colored(f"Error executing SQL query: {e}")


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
                print_colored(data)
                return data
    except Exception as e:
        print_colored(f"Error executing SQL query: {e}")

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print_colored(username, password)

        admin_credentials = return_admin()
        faculty_credentials = return_faculty()

        if any((username == admin_user[1] and password == admin_user[2]) for admin_user in admin_credentials):
            admin_id = get_admin_id(username)[0]
            print_colored(admin_id)
            request.session['admin_id'] = admin_id
            return redirect(f'adminfis/{admin_id}')


        elif any((username == faculty_user[1] and password == faculty_user[2]) for faculty_user in faculty_credentials):
            faculty_id = get_faculty_id(username)[0]
            print_colored (faculty_id)
            return redirect(f'teacher/{faculty_id}')


        else:
            return render(request, 'login.html')

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
                print_colored(data)
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
        print_colored(f"Error executing SQL query: {e}")


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
                print_colored(data)
                context = {
                    'admin_id': data[0],
                    'username': data[1]
                }
                print_colored (context)
                return context
    except Exception as e:
        print_colored(f"Error executing SQL query: {e}")

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
                print_colored(data, color=Color.BLUE)
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
        print_colored(f"Error executing SQL query: {e}")


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
                print_colored(data, color=Color.BLUE)
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
                return conference
    except Exception as e:
        print_colored(f"Error executing SQL query: {e}", color=Color.GREEN)


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
                print_colored(data, color=Color.BLUE)
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
        print_colored(f"Error executing SQL query: {e}")
    
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
                print_colored(data, color=Color.BLUE)
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
        print_colored(f"Error executing SQL query: {e}")


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
                print_colored(data, color=Color.BLUE)
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
        print_colored(f"Error executing SQL query: {e}")

def get_workexp(teacher_id):
    WorkExperience = f"""
    SELECT ExpID,FacultyID,Organization,Position,StartDate,EndDate
    FROM WorkExperience
    WHERE FacultyId = '{teacher_id}';
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(WorkExperience)
            if cursor.description:
                data = cursor.fetchall()
                print_colored(data, color=Color.BLUE)
                context = []
                for datum in data:
                    dict_temp = {
                        'expID': datum[0],
                        'facultyID': datum[1],
                        'ord': datum[2],
                        'position': datum[3],
                        'startdate': datum[4],
                        'enddate': datum[5]
                    }
                    context.append(dict_temp)

                return context
    except Exception as e:
        print_colored(f"Error executing SQL query: {e}")

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
                print_colored(data, color=Color.BLUE)
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
        print_colored(f"Error executing SQL query: {e}")

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
                print_colored(data, color=Color.BLUE)
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

                return context
    except Exception as e:
        print_colored(f"Error executing SQL query: {e}")
    
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

def teacher_dashboard(request, teacher_id):
    context = get_teacher_details(teacher_id)
    
    return render(request, 'teacher_dashboard.html', context)


def admin_home(request, admin_id):
    context = get_admin_details(admin_id)

    return render(request, 'admin_home.html', context)

def manage_faculty(request):
    return HttpResponse("Failure")

def id_generator():
    faculty_id = random.randint(1000, 9999)
    return faculty_id

def add_faculty(request, admin_id):
    if request.method == "GET":
        return render(request, 'add_faculty.html', {'admin_id': admin_id})
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
        print_colored("ERROR HERE by id", color=Color.BLUE)
        print_colored(f"Error executing SQL query: {e}")

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
                print_colored(context)
                return context
    except Exception as e:
        print_colored("ERROR HERE by name", color=Color.BLUE)
        print_colored(f"Error executing SQL query: {e}")

def manage_faculty(request):
    sort = None
    if request.method == "GET":
        faculties = get_all_faculties(sort)
        return render(request, 'manage_faculty.html', {'faculties': faculties})
    if request.method == "POST":
        if request.POST.get('search_category') == 'id':
            id1 = request.POST.get('search')
            id2 = request.POST.get('search_id')
            if request.POST.get('sort') != "":
                sort = request.POST.get('sort')
            result_id = id1 if id1 is not None else id2
            print_colored (id, id2, result_id)
            faculties = (selected_faculties(result_id, sort),)
            if any(faculties) is False:
                print_colored(request.POST.get('filter'), color=Color.CYAN)
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
            print_colored (faculties)
            print_colored(sort, color=Color.RED)

            if faculties is None:
                print_colored(request.POST.get('filter'), color=Color.CYAN)
                if request.POST.get('filter') is None:
                    faculties = get_all_faculties(sort)
                else:
                    gender = request.POST.get('filter')
                    faculties = get_faculty_by_gender(gender, sort)
        return render(request, 'manage_faculty.html', {'faculties': faculties})


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
        print_colored(f"Error executing SQL query: {e}")
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
        print_colored(f"Error executing SQL query: {e}")
        return []


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


def delete_faculty(request, faculty_id):
    raw_sql_query = f"""
    DELETE FROM Faculty 
    WHERE facultyId = '{faculty_id}'
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_sql_query)
    return redirect('manage_faculty')


def report_view(request):
    return HttpResponse("opened")


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
    print_colored("OPENED")
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
    return HttpResponse("POST request has been dealt with!!")


