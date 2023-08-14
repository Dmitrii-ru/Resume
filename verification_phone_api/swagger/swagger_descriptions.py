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


def profile_get():
    return {
        'responses': {
            status.HTTP_200_OK: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'profile': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={
                                "phone_number": "+7(929)924-19-00",
                                "invite": "mrITZ7",
                                "self_invite": "mrITZ7",
                                "is_active": "true"
                            }
                        ),
                        'duplicate_user_invite': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example=('+7(929)924-19-01', '+7(929)924-19-02')
                            )
                        )
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Validation Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Page not found'
                        ),
                    }
                )
            )
        }

    }


def profile_put():
    return {
        'responses':{
            status.HTTP_201_CREATED: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='+7(123)456-68-90 успешно активировал invite'
                        ),
                    }
                )
            ),
        }
    }