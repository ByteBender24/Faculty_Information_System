
# Faculty Information System (FIS)

The Faculty Information System (FIS) is a comprehensive solution designed to efficiently organize and manage crucial information related to faculty members in educational institutions. This system aims to streamline the management of faculty details, educational qualifications, work experience, research papers, and more.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Faculty Management:** Add, update, or delete faculty information, including designation, qualification, date of joining, and more.

- **Biodata:** Capture specific details such as name, gender, nationality, marital status, contact information, skills, and language spoken.

- **Login Credentials:** Provide secure and authorized access to the faculty user through a dedicated login system.

- **Admin Dashboard:** Admin users can access a dashboard for comprehensive control over the system, including adding new faculty members, deleting records, and searching for specific faculty based on various parameters.

## Technologies Used

- **Database:** Utilize a relational database system (e.g., MySQL) for efficient data organization. Usage of all basic queries such as CRUD, Joins and usage of PLSQL is seen here.

- **Backend Framework:** Develop the backend using Django, a high-level Python framework known for its security and scalability.

- **Frontend Technologies:** Craft a user-friendly interface using HTML, CSS, and JavaScript to enhance user interactions.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ByteBender24/Faculty_Information_System.git

## Project Setup Instructions

### 1. Install Dependencies:

```bash
pip install -r requirements.txt 
```

### 2. Database Setup
* Create a MySQL database
* Update the database configurations in _settings.py_

### 3. Run Migrations:

`python manage.py migrate` 


### 4. Start the Development Server:

`python manage.py runserver` 

## Usage

Visit the application at [http://localhost:8000](http://localhost:8000/) in your web browser.

Login Credentials:
* Admin Login - admin - 0000
* Teacher Login - varsha - 0000
```sql
Use database_name;
Select * from Credential;

--Refer Credentials table for username and password
--Check _models.py_ for table information
```

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

