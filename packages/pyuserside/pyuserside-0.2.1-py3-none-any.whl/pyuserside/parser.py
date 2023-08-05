def parse_response(response: dict):
    if (id_ := response.get('Id') or response.get('id')) is not None:
        return id_
    if (data := response.get('Data') or response.get('data')) is not None:
        return data
    if (list_ := response.get('list')) is not None:
        return list_.split(',')
    return response