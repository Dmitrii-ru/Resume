# **Authorization app**
___


# API Endpoints

## Register User

**Endpoint:** `POST v1/user_app/register/`

Register a new user.

**Request Body:**

```json
{
    "username": "your-username",
    "email": "your-email@example.com",
    "password": "your-password",
    "password2": "your-password"
}
```

**Validation:**

- Check if the passwords match.
- Check if a user with the given email already exists.

**Response:**

- Status: 201 Created
- Response Body:


```json

{
    "username": "your-username",
    "email": "your-email@example.com",
    "access_token": "your-access-token",
    "refresh_token": "your-refresh-token"
}
```
___

## User Login
**Endpoint:** `POST v1/user_app/login/`

### Authenticate a user.

**Request Body:**

```json
{
    "username": "your-username",
    "password": "your-password"
}
```

**Validation:**

- Check if the username and password are valid.


**Response:**

- Status: 200 OK
- Response Body:

```json
{
    "user": "your-username",
    "access_token": "your-access-token",
    "refresh_token": "your-refresh-token"
}
```
___

## Refresh Token
**Endpoint:** `POST v1/user_app/refresh-token/`

### Refresh an access token using a refresh token.

**Request Body:**

```json
{
    "refresh_token": "your-refresh-token"
}
```
**Validation:**

- Check if the refresh token is valid.

**Response:**

- Status: 201 Created
- Response Body:
```json
{
    "access_token": "new-access-token"
}
```



