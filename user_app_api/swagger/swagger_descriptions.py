from drf_yasg import openapi
from rest_framework import status


def schema_login():
    return {
        'responses': {
            status.HTTP_200_OK: openapi.Response(
                description="Authentication successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user_name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Vasya'
                        ),
                        'access_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='LONG STRING'
                        ),
                        'refresh_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='LONG STRING'
                        ),
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="User not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='User not found'
                        ),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid password'
                        )
                    }
                )
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Forbidden",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='User is not active'
                        )
                    }
                )
            )
        }
    }


def schema_refresh_token():
    error_password_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error_token': openapi.Schema(
                type=openapi.TYPE_STRING,
                example='Bad refresh token'
            ),
        }
    )

    return {
        'responses': {
            status.HTTP_201_CREATED: openapi.Response(
                description="New refresh token",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='string'
                        ),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                content={
                    "application/json": {
                        "schema": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'error_token': error_password_schema,

                            }
                        )
                    }
                }
            )
        }
    }


def schema_user_register():
    error_email = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example='User with this email already exists'
            ),
        }
    )
    error_password = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example='Password1 will not match password2'
            ),
        }
    )

    return {
        "responses": {
            status.HTTP_201_CREATED: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'User': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'username': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='Vasya'
                                ),
                                'email': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='malibu@ya.ru'
                                ),
                                'access_token': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='long string'
                                ),
                                'refresh_token': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='long string'
                                )
                            }
                        ),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                content={
                    "application/json": {
                        "schema": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'error_email': error_email,
                                'error_password': error_password,

                            }
                        )
                    }
                }
            )
        }
    }
