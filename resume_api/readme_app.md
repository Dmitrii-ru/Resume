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
___


## Get List of To-Do Items for a Specific Day

### `GET /v1/todo_session/{slug_day}/`

Retrieve to-do list items for a specific day.

#### Parameters

- `slug_day` (string): The day in `YYYY-MM-DD` format.

#### Response

- Status Code: 200 OK
- Body:
  ```json
  {
    "day": {
      "actual": [22, 234234234],
      "close": [],
      "slug": "2020-02-04",
      "name": "Tuesday, February 4, 2020"
    }
  }
    ```
  
### Example Error Response
- Status Code: 400 Bad Request
- Body:
```json
{
  "success": false,
  "error": "Invalid date format. Please provide a valid date in `YYYY-MM-DD` format."
}
```
___
# Create a New To-Do Item

## POST /v1/todo_session/{slug_day}/

Create a new to-do list item for a specific day.

### Parameters

- `slug_day` (string): The day in `YYYY-MM-DD` format.

### Request Body

- `todo` (string): The text of the to-do list item.

### Response

- Status Code: 201 Created
- Body:
  ```json
  {
    "success": true,
    "message": "To-do item successfully created."
  }
    ```
  

### Example Error Response
- Status Code: 400 Bad Request
- Body:
```json
{
  "success": false,
  "error": "Invalid date format. Please provide a valid date in `YYYY-MM-DD` format."
}
```
___


## Delete or Change Status of a To-Do
### Delete a to-do or change its status to closed or actual for a specific day.

### Endpoint
- DELETE /api/todo/{slug_day}/delete - Delete a to-do item for a specific day.

- PUT /api/todo/{slug_day}/status - Change the status of a to-do item for a specific day.

#### Request Parameters
- slug_day: The slug of the day in the format YYYY-MM-DD.
#### Request Body
#### For DELETE:

```json

{
  "todo": "to-do to be deleted"
}
```
#### For PUT:

```json
{
  "todo": "Task to be updated"
}
```
#### Responses
- 204 No Content - Successfully deleted the to-do item.
- 201 Created - Successfully changed the status of the to-do item.
- 404 Not Found - Day not found.
- 400 Bad Request - Invalid request or parameters.
#### Usage
- To use this API, make requests to the provided endpoints with the appropriate parameters and request body.


### Request
#### DELETE /api/todo/2023-06-15/delete

Request Body:
```json
{
  "todo": "Buy groceries"
}
```

### Response
- Status: 204 No Content
- Message:
```json

{
  "success": true,
  "message": "Successfully deleted 'Buy groceries'."
}
```
