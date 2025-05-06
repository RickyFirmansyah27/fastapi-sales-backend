from fastapi.responses import JSONResponse

def BaseResponse(response_type: str, message: str, data=None) -> JSONResponse:
    if response_type == 'success':
        response_data = successResponse(data, message)
        status_code = 200
    elif response_type == 'error':
        response_data = badRequestResponse(message)
        status_code = 400
    elif response_type == 'notfound':
        response_data = notFoundResponse(message)
        status_code = 404
    else:
        response_data = internalServerErrorResponse(message)
        status_code = 500

    return JSONResponse(content=response_data, status_code=status_code)

def successResponse(data, message):
    return {
        "statusCode": 200,
        "status": True,
        "data": data,
        "message": message
    }

def invalidResponse(message):
    return {
        "statusCode": 400,
        "status": False,
        "data": None,
        "message": message
    }

def badRequestResponse(message):
    return {
        "statusCode": 400,
        "status": False,
        "data": None,
        "message": message
    }

def internalServerErrorResponse(message):
    return {
        "statusCode": 500,
        "status": False,
        "message": message
    }

def notFoundResponse(message):
    return {
        "statusCode": 404,
        "status": False,
        "message": message
    }
