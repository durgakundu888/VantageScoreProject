from fastapi import FastAPI, HTTPException, status, Depends, Body
from pydantic import BaseModel, Field, EmailStr
from random import randrange
from jwt_handler import signJWT
from jwt_bearer import jwtBearer

import math

app = FastAPI()

class LinkedInPost(BaseModel):
    """
    LinkedInPost: Represents a post on LinkedIn.
    
    Attributes:
    - title (str): The title of the post.
    - content (str): The content of the post.
    - category (str): The category of the post.
    - published (bool): Indicates if the post is published (default True).
    """
    title: str
    content: str
    category: str
    published: bool = True

class User(BaseModel):
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

class UserLogin(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

# Sample initial data
linkedin_posts = [
    {"title": "New Job Post", "content": "I got a new job", "id": 1},
    {"title": "Open To Work Post", "content": "I am available on the job market", "id": 2}
]

users = []

# Utility functions
def find_linkedin_post(post_id):
    for post in linkedin_posts:
        if post["id"] == post_id:
            return post

def find_index_of_linkedin_post(post_id):
    for index, post in enumerate(linkedin_posts):
        if post['id'] == post_id:
            return index

def paginate_posts(page: int = 1, page_size: int = 10):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return linkedin_posts[start_index:end_index]

@app.post("/user/signup", tags=["user"])
def user_signup(user : User = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLogin):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False

@app.post("/user/login", tags=["user"])
def user_login(user: UserLogin = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details!"
        }

# Get all posts with pagination
@app.get("/linkedinposts", dependencies=[Depends(jwtBearer())], tags=["posts"], status_code=status.HTTP_200_OK)
def get_all_posts(page: int = 1, page_size: int = 10):
    """
    Retrieve all LinkedIn posts with pagination.

    Parameters:
    - page (int): The page number to retrieve (default 1).
    - page_size (int): The number of posts per page (default 10).

    Returns:
    - data (list): List of LinkedIn post details.
    """
    if (page < 1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid page number. Must be integer greater than 0.')
    if (page_size < 1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid page size. Must be integer greater than 0.')
    # Check if there are any posts available
    if len(linkedin_posts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: No posts found")
    
    # Paginate the posts
    paginated_posts = paginate_posts(page, page_size)
    
    # If no posts found for the given page, raise 404
    if not paginated_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: No posts found")
    
    return {"data": paginated_posts}

# Get the latest post
@app.get("/linkedinposts/latest", dependencies=[Depends(jwtBearer())], tags=["posts"], status_code=status.HTTP_200_OK)
def get_latest_post():
    """
    Retrieve the latest LinkedIn post.

    Returns:
    - post_detail (dict): Details of the latest post.
    """
    if len(linkedin_posts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: No posts found")
    post = linkedin_posts[-1]
    return {"post_detail": post}

# Get post by ID
@app.get("/linkedinposts/{id}", dependencies=[Depends(jwtBearer())], tags=["posts"], status_code=status.HTTP_200_OK)
def get_post_by_id(id: int):
    """
    Retrieve a LinkedIn post by its ID.

    Parameters:
    - id (int): The ID of the post to retrieve.

    Returns:
    - post_detail (dict): Details of the requested post.
    """
    if len(linkedin_posts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: No posts found")
    if id < 0 or math.isnan(id):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"ID {id} is invalid. ID must be a number greater than -1.")
    post = find_linkedin_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")
    return {"post_detail": post}

# Create a new post
@app.post("/linkedinposts", dependencies=[Depends(jwtBearer())], tags=["posts"], status_code=status.HTTP_201_CREATED)
def create_post(post: LinkedInPost):
    """
    Create a new LinkedIn post.

    Parameters:
    - post (LinkedInPost): The details of the post to create.

    Returns:
    - data (dict): Details of the created post.
    """
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    linkedin_posts.append(post_dict)
    return {"data": post_dict}

# Update a post by ID
@app.put("/linkedinposts/{id}", dependencies=[Depends(jwtBearer())], tags=["posts"], status_code=status.HTTP_200_OK)
def update_post_by_id(id: int, post: LinkedInPost):
    """
    Update a LinkedIn post by its ID.

    Parameters:
    - id (int): The ID of the post to update.
    - post (LinkedInPost): The updated details of the post.

    Returns:
    - message (str): A message indicating the success of the update.
    - post_details (dict): Details of the updated post.
    """
    if len(linkedin_posts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: No posts found")
    indx = find_index_of_linkedin_post(id)
    if indx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    linkedin_posts[indx] = post_dict
    return {"message": f"Post with ID {id} successfully updated", "post_details": post_dict}

# Update all posts
@app.put("/linkedinposts", dependencies=[Depends(jwtBearer())], tags=["posts"], status_code=status.HTTP_200_OK)
def update_all_posts(post: LinkedInPost):
    """
    Update all LinkedIn posts with the same details.

    Parameters:
    - post (LinkedInPost): The updated details for all posts.

    Returns:
    - message (str): A message indicating the success of the update.
    - Updated Posts (list): Details of all updated posts.
    """
    if len(linkedin_posts) == 0:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: No posts found")
    post_dict = post.dict()
    for post in linkedin_posts:
        post['title'] = post_dict['title']
        post['content'] = post_dict['content']
        post['category'] = post_dict['category']
        post['published'] = post_dict['published']
    return {"message": "All posts successfully updated", "Updated Posts": linkedin_posts}

# Delete a post by ID
@app.delete("/linkedinposts/{id}", dependencies=[Depends(jwtBearer())], tags=["posts"], status_code=status.HTTP_200_OK)
def delete_post(id: int):
    """
    Delete a LinkedIn post by its ID.

    Parameters:
    - id (int): The ID of the post to delete.

    Returns:
    - message (str): A message indicating the success of the deletion.
    """
    if len(linkedin_posts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: No posts found")
    indx = find_index_of_linkedin_post(id)
    if indx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist")
    linkedin_posts.pop(indx)
    return {"message": f"Post with ID {id} successfully deleted"}

# Delete all posts
@app.delete("/linkedinposts", dependencies=[Depends(jwtBearer())], tags=["posts"], status_code=status.HTTP_200_OK)
def delete_all_posts():
    """
    Delete all LinkedIn posts.

    Returns:
    - message (str): A message indicating the success of the deletion.
    """
    if len(linkedin_posts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: No posts found")
    linkedin_posts.clear()
    return {"message": "All posts deleted"}