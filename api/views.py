from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpRequest
import json

from api.models.user import User
from api.models.game_state import GameState

# Currently makes a new user and passes the ID and name back
def login(request : HttpRequest):

    last_user_id = User.objects.count() + 1
    new_username = f"User-{last_user_id}"
    user = User.objects.create(user_name = new_username)
    user.save()

    response_body = {
        "id": user.id,
        "user_name": user.user_name
    }
    
    return HttpResponse(json.dumps(response_body), content_type="application/json")

# 
def upload(request : HttpRequest):

    request_okay = _verify_upload(request)
    return_body = {
        "error": False,
        "message": "",
        "code": "",
        "enemy_user": "",
        "enemy_game_state": ""
    }
    if(request_okay):
        body_json = json.loads(request.body)
        # Check for User
        USER_LIST : User = User.objects.all().filter(id = body_json["user"])
        if(len(USER_LIST) > 0):
            USER = USER_LIST[0]
            PotentialGameStates = GameState.objects.all().exclude(user = USER).filter(turn = body_json["turn"])
            # For now we are just going to return the first one found  
            if(len(PotentialGameStates) == 0):
                return_body["error"] = True
                return_body["code"] = "GD001"
                return_body["message"] = "ERROR - No Available Enemy Data"
                return HttpResponse(json.dumps(return_body), content_type="application/json", status=400) 
            else:
                SelectedGameState : GameState = PotentialGameStates[0]
                return_body["message"] = "SUCCESS - Enemy Data Found"
                return_body["enemy_user"] = SelectedGameState.user.user_name
                return_body["enemy_game_state"] = SelectedGameState.map

                GameState(user=USER, turn=body_json["turn"], map=body_json["game_state"]).save()

                return HttpResponse(json.dumps(return_body), content_type="application/json")   
        else:
            return_body["error"] = True
            return_body["message"] = "ERROR - User Does Not Exist"
            return_body["code"] = "US001"
            return HttpResponse(json.dumps(return_body), content_type="application/json", status=400)
    else:
        return_body = {
            "error": True,
            "message": "ERROR - Request Invalid",
            "code": "RE001"
        }
        return HttpResponse(json.dumps(return_body), content_type="application/json", status=400)
    
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
