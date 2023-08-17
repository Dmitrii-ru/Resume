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
