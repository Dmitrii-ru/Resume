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
                description="Bad Request",
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

