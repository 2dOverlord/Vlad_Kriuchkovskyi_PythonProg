from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 400:
            data = {
                'errors': response.data,
            }
        elif response.status_code == 404:
            data = {
                'message': "Transaction is not found.",
            }
        finalize_data = {
            'status': response.status_code,
        }

        response.data = {**finalize_data, **data}
    return response
