# Resume API

- Provides information about a person's skills, contacts, education, stacks, and projects.
- Todo
- Feedback


## Get Person's Skills

Get information about a person's skills, contacts, education, stacks, and projects.

### Endpoint

`GET v1/resume/`

### Example Request

- **Status:** 200 OK
- **Response Content Type:** application/json

```json
{
    "about_me": {},
    "my_education": [],
    "stacks": [],
    "projects": []
}
```
___
## Create New Feedback

Create a new feedback object by providing the text in the request body.

### Endpoint

`POST v1/resume/feedback/`

### Request Body

- `text` (string): The feedback text. Minimum length: 10 characters.

#### Example Request

```json
{
   "message": "Feedback successfully created"
}
```


