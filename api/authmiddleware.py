from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import  status
from rest_framework.renderers import JSONRenderer
import jwt

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        print(request.path)
        auth_header = request.headers.get("Authorization")

        
       
       
        
        
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # Code to be executed for each request/response after
        # the view is called.
        # print("toekn",tokens)
        open_paths = [
           '/api/auth02/',
           '/api/auth/login/',  # Assuming '/login/' is the path for your login view, 
           '/api/auth/register/',
           '/api/schema/',
           '/api/schema/redoc/',
           '/api/schema/swagger-ui/',
           '/swagger-ui',
           '/api/course/',
           '/api/course/<int:pk>/'
          
           
           # Add any other paths that should be publicly accessible
       ]
       
        if request.path not in open_paths:
            if not auth_header:
                response = Response()
                response.data =  {"detail": "Authorization header missing."},
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response

            # Check if the header follows the "Bearer <token>" format
            if not auth_header.startswith("Bearer "):
                response = Response()
                response.data =  {"detail": "Invalid Authorization header format. Expected 'Bearer <token>'."},
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response
            print(auth_header)
            try:
                tokens = auth_header.split(" ")[1]
                
                payload = jwt.decode(tokens,'secret',algorithms='HS256')
              
            except:
                response = Response()
                response.data = {"error":"Token Expired Unauthenticated!"}
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response


        # # Continue processing the request
        response = self.get_response(request)
      

        return response