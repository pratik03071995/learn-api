Here's a README.md template for your University Courses API application:

```markdown
# University Courses API

This project provides a RESTful API for managing university courses, students, and their enrollments. It's built using Flask and SQLite, containerized with Docker for easy setup and deployment.

## Getting Started

These instructions will cover setup and running the application on your local machine for development and testing purposes.

### Prerequisites

- Docker


### Installation

1. Navigate into the project directory:
   
   cd university-api
   
2. Build and run the Docker containers:
   
   docker-compose up --build
   
   This command builds the Docker image for the application and starts the services defined in `docker-compose.yml`. By default, the application is accessible at `http://localhost:5000`.

### API Endpoints

The following API endpoints are available:

- **Create a Student**
  - **POST** `/students`
  - Body: `{"first_name": "John", "last_name": "Doe"}`

- **Create a Course**
  - **POST** `/courses`
  - Body: `{"name": "Computer Science", "code": "CS101", "description": "Introduction to Computer Science."}`

- **Enroll a Student in a Course**
  - **POST** `/enrollments`
  - Body: `{"student_id": 1, "course_id": 1}`

- **List Students and Courses Taken**
  - **GET** `/students/courses`

- **List Students and Courses Not Taken**
  - **GET** `/students/not_taken_courses`

### Testing

Below are some example test cases that you can use to verify the functionality of the API:

- **Test Creating a Student:**
  
  curl -X POST http://localhost:5000/students \
  -H 'Content-Type: application/json' \
  -d '{"first_name": "John", "last_name": "Doe"}'
  

- **Test Creating a Course:**
  
  curl -X POST http://localhost:5000/courses \
  -H 'Content-Type: application/json' \
  -d '{"name": "Computer Science", "code": "CS101", "description": "Introduction to Computer Science."}'
  

- **Test Enrolling a Student in a Course:**
  
  curl -X POST http://localhost:5000/enrollments \
  -H 'Content-Type: application/json' \
  -d '{"student_id": 1, "course_id": 1}'
  

- **Test Listing Students and Courses Taken:**
  
  curl http://localhost:5000/students/courses
  

- **Test Listing Students and Courses Not Taken:**
  
  curl http://localhost:5000/students/not_taken_courses
  

### Notes

- Data persistence is handled by SQLite, and the database file is stored within the Docker container. Consider volume mapping for production environments to ensure data persistence across container rebuilds.

```
