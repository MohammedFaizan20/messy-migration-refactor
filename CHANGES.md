
# CHANGES.md

## Refactoring Summary

This document outlines the major issues identified and the comprehensive refactoring actions applied to transform a legacy user management API into a modular, secure, maintainable, and testable codebase, in full alignment with the challenge specifications.

---

## Issues Identified in Legacy Codebase

Issue                       | Description
----------------------------|---------------------------------------------------------------
Tight Coupling              | Routes handled both Flask logic and business logic directly.
Lack of Structure           | Code lacked modularization. No clear separation of concerns.
Plaintext Passwords         | User passwords were stored in raw form, making it critically insecure.
Missing Validation          | Endpoints accepted incomplete or malformed data.
Inconsistent Status Codes   | Responses did not conform to RESTful standards.
No Error Handling           | No graceful failure paths for invalid input or DB errors.
Vulnerable to SQL Injection | SQL queries used string interpolation without parameterization.
No Automated Tests          | Application lacked even basic coverage for critical routes.
No Input Sanitization       | Could expose app to injection or invalid data errors.

---

## Key Changes Made

### 1. Code Organization and Separation of Concerns

Layer                  | File              | Description
-----------------------|-------------------|--------------------------------------------------------------------
App Factory            | app/__init__.py   | create_app() creates the Flask instance with blueprint registration.
Routes                 | app/routes.py     | Only handles HTTP logic and delegates all core logic to services.
Services (Logic Layer) | app/services.py   | Contains all user logic and DB operations (CRUD, login, etc.).
Tests                  | tests/test_app.py | Validates functionality using Flask’s test client.
Startup                | app.py            | Uses create_app() to launch the app, keeping the entrypoint clean.

---

### 2. Security Improvements

Area                       | Implementation
---------------------------|-----------------------------------------------------
Password Hashing           | Passwords now hashed with bcrypt before DB insertion.
Login Verification         | Password check via bcrypt.checkpw() (secure, one-way).
SQL Injection Protection   | All SQL queries now use parameterized statements (e.g., cursor.execute(sql, params)) to prevent injection.
Sensitive Field Protection | Passwords are never returned in any API response.
Error Isolation            | All logic errors now return meaningful HTTP errors (400, 401, 404, 409).

---

### 3. Input Validation and Response Consistency

Endpoint          | Checks
------------------|--------------------------------------------------------------
POST /users       | Validates presence of username, email, full_name, password.
PUT /user/<id>    | Ensures presence of email and full_name.
POST /login       | Requires both email and password.
All Routes        | Missing or invalid fields return 400 Bad Request with clear messages.
Conflict Handling | Duplicate email or username triggers 409 Conflict.

---

### 4. Best Practices Adopted

Practice          | Example
------------------|-------------------------------------------------------------------------------
Function Naming   | create_user, get_user_by_id, delete_user — descriptive and scoped.
DRY Principle     | Common operations like password hashing and DB connection reused across functions.
Parameterization  | Avoided string formatting in DB queries to prevent SQL injection.
Testing Isolation | Used uuid.uuid4() to create unique emails and usernames during testing.
Status Codes      | Used proper HTTP codes like 201 Created, 404 Not Found, 401 Unauthorized, 409 Conflict.

---

## Automated Testing

Tool Used: unittest (Python's built-in unit testing framework)

Test File: tests/test_app.py

Test Name                | Coverage
-------------------------|-----------------------------------------------------
test_health_check        | Verifies root / endpoint returns a healthy response.
test_create_user         | Confirms successful user creation and status 201.
test_get_all_users       | Retrieves all users and checks if the response is a list.
test_search_user_by_name | Confirms name-based search returns expected structure.
test_login_user          | Validates password-authenticated login using hashed password.

Each test generates unique user data using uuid to avoid conflicts across runs.

---

## Manual Testing with Postman

All endpoints were manually verified using Postman. The following actions were confirmed:

- Created users with required fields via POST /users
- Logged in with matching password via POST /login
- Retrieved users using GET /users and GET /user/<id>
- Performed name-based searches with GET /search?name=
- Updated users using PUT /user/<id>
- Deleted users using DELETE /user/<id>
- Verified that incorrect or missing inputs returned expected error codes
- Confirmed password checking logic with bcrypt integration

---

## Tools and Libraries Used

Tool/Library | Purpose
-------------|----------------------------------------
Flask        | Core web framework
bcrypt       | Secure password hashing and verification
sqlite3      | Lightweight, file-based database
unittest     | Automated testing framework
uuid         | Dynamic data generation during tests
Postman      | Manual endpoint testing
Python 3.10+ | Runtime environment

---

## Assumptions and Trade-offs

Decision                              | Reason
--------------------------------------|------------------------------------------------------------------
Avoided JWT/session-based auth        | Not required by the challenge; would exceed scope.
Used raw sqlite3 instead of ORM       | Kept implementation simple and aligned with challenge expectations.
No input sanitization beyond presence | Parameterized queries already prevent SQL injection; additional sanitization skipped for time constraints.
Used email as login credential        | Simplifies authentication and avoids username ambiguity.
No password strength enforcement      | Considered out of scope for refactor-only task.

---

## If Given More Time

- Add JWT-based session management and refresh tokens
- Introduce user roles like is_admin or is_active
- Create Swagger/OpenAPI documentation for all routes
- Add additional tests for PUT, DELETE, edge cases, and error flows
- Implement database cleanup after each test run
- Use SQLAlchemy for maintainability and scalability in large apps

---

## AI Usage Disclosure

Tool             | Usage
-----------------|------------------------------------------------------------------------------------------------
ChatGPT          | Used to brainstorm code structure, implement bcrypt securely, design test logic, and validate patterns.
Human Oversight  | All AI-generated content was reviewed and customized before inclusion.
No Blind Copying | Suggestions were filtered and integrated thoughtfully; unnecessary complexity was avoided.

---

## Final Status

Evaluation Criteria   | Status
----------------------|-------------------------------------------------------------------
Code organization     | Achieved — modular, clean, and scalable
Security improvements | Achieved — hashed passwords, safe SQL queries
Best practices        | Achieved — correct HTTP codes, input validation, reusability
Testing coverage      | Achieved — core functionality tested with unittest and Postman
Documentation         | Achieved — all improvements explained with reasoning and trade-offs

---

## Submission Checklist

- [x] All original endpoints are functional and unchanged
- [x] Refactored to a production-viable code structure
- [x] Password hashing implemented using bcrypt
- [x] Tests written and passing with unittest
- [x] Manual tests conducted using Postman
- [x] CHANGES.md created with detailed notes and decisions
- [x] Application works with `python app.py` as instructed
