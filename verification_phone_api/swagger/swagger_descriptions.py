from drf_yasg import openapi
from rest_framework import status


def send_code_verification_schema():
    return {
        'method': 'post',
        'request_body': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, format='+7(929)927-19-00',
                                               example='+7(929)927-19-00'),
            },
            required=['phone_number', ]
        ),
        'responses': {
            status.HTTP_201_CREATED: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_STRING, example='6666'),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Validation Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'object': openapi.Schema(type=openapi.TYPE_STRING, example='phone_number'),
                        'error': openapi.Schema(type=openapi.TYPE_STRING, example='Not unique number')
                    }
                )
            )
        }
    }


def invite_code_verification_schema():
    return {
        "method": 'post',
        "request_body": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, format='+7(929)927-19-00',
                                               example='+7(929)927-19-00'),
                'code': openapi.Schema(type=openapi.TYPE_STRING, format='1111', example='6839')
            },
            required=['phone_number', 'code']
        ),
        "responses": {
            status.HTTP_201_CREATED: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'invite': openapi.Schema(type=openapi.TYPE_STRING, example='sYKnvY'),
                        'user_profile_url': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='https://host/api/verification_phone/profile/+7(929)927-19-00'
                        )
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Validation Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'object': openapi.Schema(type=openapi.TYPE_STRING, example='phone_number'),
                        'error': openapi.Schema(type=openapi.TYPE_STRING, example='Not unique number')
                    }
                )
            )
        }
    }
