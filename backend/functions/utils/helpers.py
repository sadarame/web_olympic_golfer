from functools import wraps
from firebase_functions import https_fn
import json

def cors_enabled(f):
    """A decorator to add CORS headers to a Firebase Function response."""
    @wraps(f)
    def decorated_function(request: https_fn.Request, *args, **kwargs):
        # Handle preflight OPTIONS request
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Max-Age': '3600'
            }
            return https_fn.Response('', status=204, headers=headers)

        # Call the actual function
        response = f(request, *args, **kwargs)

        # Add CORS headers to the response
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        return response

    return decorated_function