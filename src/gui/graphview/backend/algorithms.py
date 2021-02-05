from django.http import response


def algorithms_post_handler(request):
    post_param = request.POST
    method = post_param['method']
    params = post_param['params']
    result = 'none'

    if method == compute_network_graph.__name__:
        result = compute_network_graph(params)

    return response.HttpResponse(result)


def compute_network_graph(network_text):
    return network_text
