from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .models import create_tables
from django.contrib import messages
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
                print(data)
                return data
    except Exception as e:
        print(f"Error executing SQL query: {e}")


def return_faculty():
    raw_sql_query = """
    SELECT * FROM credential;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                print(data)
                return data
    except Exception as e:
        print(f"Error executing SQL query: {e}")


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
                print(data)
                return data
    except Exception as e:
        print(f"Error executing SQL query: {e}")


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
                print(data)
                return data
    except Exception as e:
        print(f"Error executing SQL query: {e}")

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        admin_credentials = return_admin()
        faculty_credentials = return_faculty()

        if any((username == admin_user[1] and password == admin_user[2]) for admin_user in admin_credentials):
            admin_id = get_admin_id(username)[0]
            print(admin_id)
            request.session['admin_id'] = admin_id
            return redirect(f'adminfis/{admin_id}')


        elif any((username == faculty_user[1] and password == faculty_user[2]) for faculty_user in faculty_credentials):
            faculty_id = get_faculty_id(username)[0]
            print (faculty_id)
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
                print(data)
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
        print(f"Error executing SQL query: {e}")


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
                print(data)
                context = {
                    'admin_id': data[0],
                    'username': data[1]
                }
                print (context)
                return context
    except Exception as e:
        print(f"Error executing SQL query: {e}")


def view_teacher(request, teacher_id):
    teacher = get_teacher_details(teacher_id)
    # return render(request, 'view_teacher.html', {'teacher' : teacher})
    return HttpResponse("Success!!")

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

def manage_faculty(request):
    # Retrieve all faculties from the database
    faculties = get_all_faculties()
    print (faculties)
    return render(request, 'manage_faculty.html', {'faculties': faculties})


def get_all_faculties():
    # Fetch all faculties from the database
    raw_sql_query = """
    SELECT FacultyID, FirstName, LastName, DateOfBirth, Gender, ContactNumber, Email, Address 
    FROM faculty;
    """
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
        print(f"Error executing SQL query: {e}")
        return []

def update_faculty(request, faculty_id):
    context = get_teacher_details(faculty_id)
    # views.py


def update_faculty(request, faculty_id):
    # Fetch the current details of the faculty with the given ID
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

def search_faculty(request):
    return HttpResponse("opened")

def report_view(request):
    return HttpResponse("opened")
