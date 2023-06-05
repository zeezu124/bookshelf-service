# Bookshelf Service README

This allows you to view, add and delete books from a user's library. Steps for installation and application use will be given below.


## Setup

- Download the project
- Navigate to the terminal
- Create a .env with the following variables:

```bash
DATABASE_URL=YOUR_MONGODB_URL
SECRET_KEY=YOUR_SECRET_KEY
```
Edit the .env to your own specifications.
## Installation

You can run the application locally or using a docker container. Steps for both ways are shown below.
### Run Locally

Make sure you have python installed: https://www.python.org/downloads/



Check your python version, this makes sure you have it installed

```bash
  python --version
```

Clone the project

```bash
  git clone https://gitlab.surrey.ac.uk/com301457/bookshelf-backend.git
```

Go to the project directory

```bash
  cd bookshelf-backend
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver 0.0.0.0:8000
```
You can choose whichever port you wish to run the service on.



### Run using docker container


Make sure you have python and docker installed: https://docs.docker.com/get-docker/

Open Docker Desktop so it is running in the background, then clone the project and go into the directory as you would if you were running it locally.

Build the docker container

```bash
  docker-compose build
```

Run the container

```bash
  docker-compose up
```
Note: this will automatically run the server on port `8000`



## API Reference

#### Get all books for a user

```http
  GET /api/books/${username}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. The username of the currently logged in user |

Returns a JSON object with the username and an array of book ids.

#### Get specific book in user library

```http
  GET /api/books/${username}/${book_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Username of logged in user |
| `book_id`      | `string` | **Required**. Book id of requested book |

Returns a JSON object with the username and an array of book ids. Will return 'book does not exist' if the book does not exist in the user's library.

#### Add book to a user's library

```http
  POST /api/books/${username}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. The username of the currently logged in user |

Expects a JSON body as input with the book id like this:

```JSON
  {
    "book_id": "insert_book_id_here"
  }
```

Returns the book_id with a success status. Will return "book already exists" if the book exists.


#### Delete a book from user's library

```http
  DELETE /api/books/${username}/${book_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Username of logged in user |
| `book_id`      | `string` | **Required**. Book id of requested book |

Returns "Deleted {book_id}" indicating the book with that id has been deleted from the user's library. Will return "book does not exist" if book does not exist.
