# Freelancer Marketplace Backend

A secure and scalable backend for the Freelancer Marketplace platform: [freelancer-marketplace-cyan.vercel.app](https://freelancer-marketplace-cyan.vercel.app).  
This backend provides user authentication, role-based access control, and job management via RESTful APIs.

---

## Features

- **Authentication**: Secure user registration and login using JWT.
- **Role-Based Access Control**: Permissions tailored for Admins, Clients, and Freelancers.
- **Job Management**: Create, view, update, and delete job posts.
- **Scalable Design**: Built to handle future enhancements like payments and messaging.

## Technologies Used

- **Django**: The backend framework used to handle server-side logic, authentication, and API management.  
- **Django REST Framework (DRF)**: For building RESTful APIs.  
- **PostgreSQL**: The primary database for storing user and job-related data.  
- **SQLite**: Used as the default database during local development.  
- **JWT (JSON Web Tokens)**: For secure user authentication and session management.  
- **Python**: The programming language used for backend development.  
- **Postman**: For testing and debugging API endpoints.




## Setup Instructions

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/nafijur-rahaman/Freelancer_marketplace.git
```


### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage project dependencies. You can create and activate a virtual environment with the following commands:
#### On Windows:

```bash
python -m venv venv # Create a virtual environment 
venv\Scripts\activate # Activate the virtual environment
```

### 3. Install Dependencies
Install the required dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory of your project and add the necessary environment variables:

### 5. Run Migrations
Run the database migrations to set up your database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Optional)
Create a superuser to access the Django admin interface:

```bash
python manage.py createsuperuser
```
Follow the prompts to set the superuser's username, email, and password.

### 7. Start the Development Server
Run the development server:

The server will be running at `http://127.0.0.1:8000/`.

---


---

### Authentication Endpoints
| Method | Endpoint                | Description              |
|--------|--------------------------|--------------------------|
| POST   | `https://freelancer-marketplace-5lqt.vercel.app/api/register`     | Register a new user      |
| POST   | `https://freelancer-marketplace-5lqt.vercel.app/api/login`        | Login and receive a JWT  |

### User Role Endpoints
| Method | Endpoint                | Description                                      |
|--------|--------------------------|--------------------------------------------------|
| GET    | `https://freelancer-marketplace-5lqt.vercel.app/api/users/:id`         | View a user's details (Admin only)              |
| PATCH  | `https://freelancer-marketplace-5lqt.vercel.app/api/users/:id`         | Update user role or details (Admin only)        |

### Job Endpoints
| Method | Endpoint                | Description                                      |
|--------|--------------------------|--------------------------------------------------|
| POST   | `https://freelancer-marketplace-5lqt.vercel.app/api/jobs`              | Create a new job post (Client only)             |
| GET    | `https://freelancer-marketplace-5lqt.vercel.app/api/jobs`              | View all job posts                              |
| GET    | `https://freelancer-marketplace-5lqt.vercel.app/api/jobs/:id`          | View a specific job post                        |
| PATCH  | `https://freelancer-marketplace-5lqt.vercel.app/api/jobs/:id`          | Update a specific job post (Creator/Client only)|
| DELETE | `https://freelancer-marketplace-5lqt.vercel.app/api/jobs/:id`          | Delete a specific job post (Creator/Client/Admin)|

---

# API Testing with Postman

Follow the steps below to test the JWT-secured API endpoints using Postman.

---

## Prerequisites
1. **Install Postman**: Download and install [Postman](https://www.postman.com/).
2. **Base URL**: Use `https://freelancer-marketplace-5lqt.vercel.app` for all endpoints.

---

## Endpoints and Testing Instructions

### 1. Register a New User
- **Endpoint**: `POST /api/register`
- **Description**: Create a new user.
- **Request Body**:
    ```json
    {
        "username": "tanjid",
        "first_name": "Tanjid",
        "last_name": "Nafis",
        "email": "tanjidnafis@gmail.com",
        "password": "testpassword",
        "phone_number": "01626681291",
        "location": "Dhaka",
        "role": "Freelancer"
    }
    ```
- **Example Response**:
    ```json
    [
        {
            "id": 1,
            "user": {
                "id": 2,
                "username": "tanjid",
                "first_name": "Tanjid",
                "last_name": "Nafis",
                "email": "tanjidnafis@gmail.com"
            },
            "phone_number": "01626681291",
            "location": "Dhaka",
            "role": "Freelancer"
        },
        {
            "id": 2,
            "user": {
                "id": 1,
                "username": "admin",
                "first_name": "",
                "last_name": "",
                "email": "admin@gmail.com"
            },
            "phone_number": "01626681293",
            "location": "Dhaka",
            "role": "Admin"
        }
    ]
    ```
- **Steps**:
  1. Open Postman and create a new `POST` request.
  2. Set the URL: `https://freelancer-marketplace-5lqt.vercel.app/api/register`.
  3. Go to **Body** > **raw**, and choose `JSON`.
  4. Paste the JSON body shown above and click **Send**.
  5. Verify the `201 Created` response with the provided data format.

---

### 2. Login to Get JWT Token
- **Endpoint**: `POST /api/login`
- **Description**: Authenticate the user and receive a JWT token.
- **Request Body**:
    ```json
    {
        "email": "tanjidnafis@gmail.com",
        "password": "testpassword"
    }
    ```
- **Steps**:
  1. Create a new `POST` request.
  2. Set the URL: `https://freelancer-marketplace-5lqt.vercel.app/api/login`.
  3. Go to **Body** > **raw**, and choose `JSON`.
  4. Paste the JSON body shown above and click **Send**.
  5. Copy the `access_token` from the response.

---

### 3. Use JWT Token for Secured Endpoints
- **Adding Token**:
  1. Create a new request for any secured endpoint (e.g., `GET https://freelancer-marketplace-5lqt.vercel.app/api/jobs`).
  2. Go to the **Authorization** tab.
  3. Select **Bearer Token**.
  4. Paste the copied JWT token into the token field.

- **Example: View All Jobs**
  - **Endpoint**: `GET https://freelancer-marketplace-5lqt.vercel.app/api/jobs`
  - **Steps**:
    1. Set the URL: `https://freelancer-marketplace-5lqt.vercel.app/api/jobs`.
    2. Make sure JWT token must be a client user
    3. Add the JWT token in the **Authorization** tab as a Bearer Token.
    4. Click **Send**.
    5. Verify the response with the list of job posts.
       
- **Endpoint**: `POST /api/login`
- **Description**: Create a job.
- **Request Body**:
    ```json
    {
     "title": "Web Developer Needed for E-Commerce Site",
  "description": "We are looking for an experienced web developer to build a fully functional e-commerce website.",
  "author": 2
    }
    ```



```bash
Notice: The author field must be an integer representing the ID of the user (usually the client) posting the job. This ID should correspond to the authenticated client user in the system.
```


---

## Troubleshooting
- **Invalid Token**: Ensure the token is copied correctly.
- **Expired Token**: Log in again to generate a new token.
- **Permission Denied**: Check if your user role has access to the endpoint.

---



## Support

For support, email tanjidnafis@gmail.com 


