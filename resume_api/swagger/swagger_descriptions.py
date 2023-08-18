from drf_yasg import openapi
from rest_framework import status


def schema_index():
    return {

        'responses': {
            status.HTTP_200_OK: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'about_me': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'text': openapi.Schema(type=openapi.TYPE_STRING),
                                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                                'city': openapi.Schema(type=openapi.TYPE_STRING),
                                'mail': openapi.Schema(type=openapi.TYPE_STRING),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'education_my': openapi.Schema(type=openapi.TYPE_STRING),
                                'link_HH': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                            },
                        ),
                        'my_education': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'school': openapi.Schema(type=openapi.TYPE_STRING),
                                    'end': openapi.Schema(type=openapi.TYPE_STRING),
                                    'diploma': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                                    'percent': openapi.Schema(type=openapi.TYPE_INTEGER),
                                },
                            ),
                        ),
                        'stacks': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'slug': openapi.Schema(type=openapi.TYPE_STRING),
                                },
                            ),
                        ),
                        'projects': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'slug': openapi.Schema(type=openapi.TYPE_STRING),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'about': openapi.Schema(type=openapi.TYPE_STRING),
                                    'image': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                                    'link_git': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                                    'link_site': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                                    'api': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                                    'stacks': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
        },
    }


def schema_feedback():
    return {
        "responses": {
            status.HTTP_201_CREATED: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Feedback successfully created'
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
                            example='Make sure this value is at least 10 characters long.'
                        ),

                    }
                )
            )
        }
    }


def schema_todo_post():
    return {
        "manual_parameters": [
            openapi.Parameter(name='slug_day',
                              in_=openapi.IN_PATH,
                              type=openapi.TYPE_STRING,
                              description=f"Format YYYY-MM-DD",
                              example='2020-05-02'
                              ),
        ],
        "responses": {
            status.HTTP_201_CREATED: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Todo successfully created'
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
                            example='Invalid date format. Please provide a valid date in YYYY-MM-DD format.'
                        ),

                    }
                )
            )
        }
    }


def schema_todo_get():
    return {
        "manual_parameters": [
            openapi.Parameter(name='slug_day',
                              in_=openapi.IN_PATH,
                              type=openapi.TYPE_STRING,
                              description=f"Format YYYY-MM-DD",
                              example='2020-05-02'
                              ),
        ],
        "responses": {
            status.HTTP_200_OK: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'day': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'actual': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(type=openapi.TYPE_STRING)
                                ),
                                'close': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(type=openapi.TYPE_STRING)
                                ),
                                'slug': openapi.Schema(type=openapi.TYPE_STRING),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            )
        }
    }


def schema_todo_delete():
    return {
        "manual_parameters": [
            openapi.Parameter(name='slug_day',
                              in_=openapi.IN_PATH,
                              type=openapi.TYPE_STRING,
                              description=f"Format YYYY-MM-DD",
                              example='2020-05-02'
                              ),
        ],
        "responses": {
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Successfully delete buy 'ice-cream' on actual"
                        ),

                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Date not found.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Page not found.'
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
                            example='The todo does not exists'
                        ),

                    }
                )
            )
        }
    }
