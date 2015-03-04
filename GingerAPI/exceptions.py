

class GingerAPIError(StandardError):
    """
    Default Error of the API wrapper
     status - HTTP status code
     type - error type
     value - error message (incl. possible URL)
    """
    def __init__(self, value, status=None, type=None):
        self.status = status or 0
        self.type = type or ''
        self.value = value or ''

    def __repr__(self):
        return '%s: %s %s\n%s' % (self.__class__.__name__, self.status, self.type, self.value)

    def __str__(self):
        return '%s: %s %s\n%s' % (self.__class__.__name__, self.status, self.type, self.value)


class HTTPError(GingerAPIError):
    """
    Errors related to the API Call
     status - the status in JSON decoded response or from response headers
     result - the JSON decoded response
     request - the initial request for the responds 
    """
    def __init__(self, status, result, request):
        self.status = result['error']['status'] if 'status' in result['error'] else status
        self.type = result['error']['type']
        self.value = result['error']['value'] + '\n\r' + request.url
