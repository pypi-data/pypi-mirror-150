from rest_framework.response import Response


def response_handler(content=None):
    """
     Returns formatted response
     """
    if content is None:
        return {}
    else:
        return Response(content)
