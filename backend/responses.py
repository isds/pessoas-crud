from flask import jsonify


def response_exception(resource: str, description: str = '',
                       msg: str = '', status_code=500):
    '''Responses 500 Internal Server Error'''

    if not isinstance(resource, str):
        raise ValueError('O recurso precisa ser uma string.')

    resp = jsonify({
        'resource': resource,
        'message': msg,
        'description': description
    })
    resp.status_code = status_code

    return resp


def response_ok(resource: str, message: str, data=None, **extras):
    '''Responses 200 OK'''

    response = {'message': message, 'resource': resource}

    if data:
        response['data'] = data
    response.update(extras)

    resp = jsonify(response)
    resp.status_code = 200

    return resp


def response_resource_created(resource: str, message: str, data=None, **extras):
    '''Responses 201 created'''

    response = {'message': message, 'resource': resource}

    if data:
        response['data'] = data
    response.update(extras)

    resp = jsonify(response)
    resp.status_code = 201

    return resp


def response_resource_updated(resource: str, message: str, data=None, **extras):
    '''Responses 210 updated'''

    response = {'message': message, 'resource': resource}

    if data:
        response['data'] = data
    response.update(extras)

    resp = jsonify(response)
    resp.status_code = 210

    return resp


def response_resource_deleted(resource: str, message: str, data=None, **extras):
    '''Responses 202 Accepted'''

    response = {'message': message, 'resource': resource}

    if data:
        response['data'] = data
    response.update(extras)

    resp = jsonify(response)
    resp.status_code = 202

    return resp


def response_data_invalid(resource: str, errors: dict, msg: str = 'Dados inválidos'):
    '''Responses 422 Unprocessable Entity'''

    if not isinstance(resource, str):
        raise ValueError('O recurso precisa ser uma string.')

    resp = jsonify({
        'resource': resource,
        'message': msg,
        'errors': errors,
    })
    resp.status_code = 422

    return resp
