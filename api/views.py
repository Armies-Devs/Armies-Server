from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random

from api.models.user import User
from api.models.game_state import GameState

# @csrf_exempt BAD TO DO but for now we ball
@csrf_exempt
# Currently makes a new user and passes the ID and name back
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

# @csrf_exempt BAD TO DO but for now we ball
@csrf_exempt
# REQUEST -
# {
#     "user": int,
#     "turn": int,
#     "game_state": String
# }
def upload(request : HttpRequest):

    if(request.method == 'POST'):
        # See below as the interface of return body
        return_body = {
            "error": False,
            "message": "",
            "code": "",
            "enemy_user": "",
            "enemy_game_state": ""
        }
        request_okay = _verify_upload(request)
        status = 200
        if(request_okay):
            body_json = json.loads(request.body)
            # Check for User
            USER_LIST = User.objects.all().filter(id = body_json["user"])
            if(len(USER_LIST) > 0):
                USER = USER_LIST[0]
                PotentialGameStates = GameState.objects.all().exclude(user = USER).filter(turn = body_json["turn"])
                if(len(PotentialGameStates) == 0):
                    return_body["error"] = True
                    return_body["code"] = "GD001"
                    return_body["message"] = "ERROR - No Available Enemy Data"
                    status = 400

                else:
                    n = random.randint(0,len(PotentialGameStates)-1)
                    print(n)
                    SelectedGameState : GameState = PotentialGameStates[n]
                    return_body["message"] = "SUCCESS - Enemy Data Found"
                    return_body["enemy_user"] = SelectedGameState.user.user_name
                    return_body["enemy_game_state"] = SelectedGameState.map

                    GameState(user=USER, turn=body_json["turn"], map=body_json["game_state"]).save()
            else:
                return_body["error"] = True
                return_body["message"] = "ERROR - User Does Not Exist"
                return_body["code"] = "US001"
                status = 400
                
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
    
def _verify_upload(request : HttpRequest):
    return True

def _debug_upload(request : HttpRequest):
    print("BODY")
    print(request.body)
    print("HEADERS")
    print(request.headers)
    
    last_user_id = User.objects.count() + 1
    new_username = f"User-{last_user_id}"
    user = User.objects.create(user_name = new_username)
    user.save()
      
    map_string = f'{{"user":{user.id}}}'
    map = GameState.objects.create(user=user, turn=3, map=json.loads(map_string))
    map.save()
    
    user_string = str(user)
    map_string = str(map)
    print(user_string)
    print(map_string)
    
    return_object = {
        "user": user_string,
        "map": map_string
    }
    
    data = json.dumps(return_object)
    
    return HttpResponse(data, content_type="application/json")
    
    
"""
Verifies the request object has all fields and is correct
"""
def _verify_request_object(request):
    return True
