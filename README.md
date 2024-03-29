Setting Up the API:

Clone the Repository: Clone the repository containing your API code.

Install Dependencies: 

Navigate to the project directory and install the required dependencies using the following command:

pip install fastapi uvicorn pydantic
pip install 'pydantic[email]'
pip install python-decouple  
pip install PyJWT 

Running the API:

ENV file: Create a .env file where you should initialize your secret key and algorithm variable. 
Generate your secret key in your terminal with the following commands:

import secrets
secrets.token_hex(16)

Then, set the result value to the secret key in your .env file. Set the algorithm key to value HS256. For example:

secret = f12c12c676726cbb8ad1d784a2bd3bd1
algorithm = HS256

Development Server: You can run the API using the development server provided by FastAPI with the following command:

uvicorn main:app --reload

This will start the server on http://127.0.0.1:8000 by default.

Production Server: For production use, it's recommended to deploy your API using ASGI servers like Uvicorn behind a reverse proxy like Nginx or Gunicorn.

Testing the API:

Swagger Documentation: Once the server is running, you can access the Swagger documentation at http://localhost:8000/docs. This interactive documentation provides details about the API endpoints, request formats, and responses.

API Requests: You can make requests to the API endpoints with curl commands in your terminal or by using Postman.

Resource Attributes:

LinkedInPost:
title (str): The title of the LinkedIn post.
content (str): The content of the LinkedIn post.
category (str): The category of the LinkedIn post.
published (bool, default True): Indicates if the post is published.

User:
fullname (str): The full name of the user
email (EmailStr): The email of the user
password (str): The password of the user

UserLogin:
email (EmailStr): The email of the user
password (str): The password of the user

API Endpoints:

POST /user/signup: Signup new user
Parameters:
user (User): The details of the new user to signup.
Returns:
access_token (json): The bearer token for authorization

POST /user/login: Login and authenticate user
Parameters:
user (UserLogin): The details of the user to login.
Returns:
access_token (json): The bearer token for authorization

GET /linkedinposts: Retrieve all LinkedIn posts with pagination.
Parameters:
page (int): The page number to retrieve (default 1).
page_size (int): The number of posts per page (default 10).
Returns:
data (list): List of LinkedIn post details.

GET /linkedinposts/latest: Retrieve the latest LinkedIn post.
Returns:
post_detail (dict): Details of the latest post.

GET /linkedinposts/{id}: Retrieve a LinkedIn post by its ID.
Parameters:
id (int): The ID of the post to retrieve.
Returns:
post_detail (dict): Details of the requested post.

POST /linkedinposts: Create a new LinkedIn post.
Parameters:
post (LinkedInPost): The details of the post to create.
Returns:
data (dict): Details of the created post.

PUT /linkedinposts/{id}: Update a LinkedIn post by its ID.
Parameters:
id (int): The ID of the post to update.
post (LinkedInPost): The updated details of the post.
Returns:
message (str): A message indicating the success of the update.
post_details (dict): Details of the updated post.

PUT /linkedinposts: Update all LinkedIn posts with the same details.
Parameters:
post (LinkedInPost): The updated details for all posts.
Returns:
message (str): A message indicating the success of the update.
Updated Posts (list): Details of all updated posts.

DELETE /linkedinposts/{id}: Delete a LinkedIn post by its ID.
Parameters:
id (int): The ID of the post to delete.
Returns:
message (str): A message indicating the success of the deletion.

DELETE /linkedinposts: Delete all LinkedIn posts.
Returns:
message (str): A message indicating the success of the deletion.

Configuration Options:

Pagination: You can adjust the pagination settings by providing page and page_size parameters in the GET requests to /linkedinposts.

