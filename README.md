# BookManagement-Automation-Playwright-Python
UI and API Automation Testing Framework using Playwright, Python and Pytest 
# Book Management Automation Framework

## Overview

This project is a hybrid UI and API automation testing framework developed using Python, Playwright, and Pytest.

The framework is designed to validate core functionalities of the Book Management System and File Management System, covering both frontend and backend layers.

---

## Technology Stack

* Python
* Playwright
* Pytest
* REST API Testing
* Page Object Model (POM)
* JSON Schema Validation
* GitHub
* Allure Report

---

## Project Structure

```text
api/
ui/
assertions/
configs/
core/
data/
utils/
```

---

## Test Coverage

### UI Testing

#### Authentication

* Login

#### File Management

* Upload File
* View File
* Search File
* Move File
* Copy File
* Delete File

#### Book Management

* Create Book
* Update Book
* Search Book
* Delete Book

#### User Management

* Search User
* User Validation

---

### API Testing

#### Authentication API

* Login API
* Register API

#### Book Management API

* Create Book
* Update Book
* Delete Book
* Get Book Detail

#### Category API

* Get Categories
* Create Category

#### Promotion API

* Create Promotion
* Update Promotion
* Delete Promotion

#### User API

* Get User Information

#### File Management API

* Upload File
* Delete File
* Search File

---

## Design Patterns

* Page Object Model (POM)
* Factory Pattern
* Service Layer Pattern
* Data Driven Testing

---

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

Run all tests:

```bash
pytest
```

Run UI tests:

```bash
pytest ui/testcases
```

Run API tests:

```bash
pytest api/testcases
```

---

## Author

Luyen Nguyen

Automation QA Engineer
