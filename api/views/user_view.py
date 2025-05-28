from django.shortcuts import render
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from api.models.user import User

# @csrf_exempt BAD TO DO but for now we ball
# Currently makes a new user and passes the ID and name back
# REQUEST -
# {
#     "user_name": String,
# }
@csrf_exempt
def create_guest(request : HttpRequest):
    print("ENTER")
    if(request.method == 'POST'):   
        return_body = {
            "error": False,
            "message": "",
            "code": "",
            "user_name": "",
            "user_id": ""
        }
        request_okay = _verify_create_guest(request)
        status = 200
        if(request_okay):
            body_json = json.loads(request.body)
            user_name = body_json["user_name"]
            user = User.objects.create(user_name = user_name)
            user.save()

            return_body["user_id"] = user.id
            return_body["user_name"] = user.user_name            
        else:
            return_body["error"] = True
            return_body["message"] = "ERROR - Request Invalid"
            return_body["code"] = "RE001"
            status = 400

        # Return return_body
        return JsonResponse(return_body, status=status)
    else:
        return JsonResponse({
            "error": True,
            "message": "Stop It"
        }, status=403)


# @csrf_exempt BAD TO DO but for now we ball
# Currently makes a new user and passes the ID and name back
# Username is is automatic
# REQUEST -
# {
# }
@csrf_exempt
def login(request : HttpRequest):
    if(request.method == 'POST'):   

        last_user_id = User.objects.count() + 1
        new_username = f"User-{last_user_id}"
        user = User.objects.create(user_name = new_username)
        user.save()

        response_body = {
            "id": user.id,
            "user_name": user.user_name
        }
        
        return JsonResponse(response_body)
    else:
        return JsonResponse({
            "error": True,
            "message": "Stop It"
        }, status=403)

def _verify_create_guest(request : HttpRequest):
    # TODO
    return True