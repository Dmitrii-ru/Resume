from drf_yasg import openapi
from rest_framework import status
from core.settings import ALLOWED_HOSTS
host = "http://" + ALLOWED_HOSTS[1]



def send_code_verification_schema():
    return {
        'method': 'post',

        'responses': {
            status.HTTP_201_CREATED: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_STRING,
                                               example='6666'),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Validation Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'object': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='+7(929)927-19-00'
                        ),

                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Not unique number'
                        )
                    }
                )
            )
        }
    }


def invite_code_verification_schema():
    return {
        "method": 'post',
        "responses": {
            status.HTTP_201_CREATED: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,

                    properties={
                        'invite': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='sYKnvY'
                        ),
                        'user_profile_url': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example=f'{host}/api/verification_phone/profile/+7(929)927-19-00',
                        )
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Validation Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'object': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='+7(929)927-19-00'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Not unique number'
                        )
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
                            properties={
                                'phone_number': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='+7(929)924-19-01'
                                ),
                                'invite': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='5Tq67R'
                                ),
                                'self_invite': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='5Tq67R'
                                ),
                                'is_active': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    example=False
                                )
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
        'responses': {
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
