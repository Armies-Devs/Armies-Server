from django.shortcuts import render
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random

from api.models.user import User
from api.models.game_state import GameState

# @csrf_exempt BAD TO DO but for now we ball
# REQUEST -
# {
#     "user": int,
#     "turn": int,
#     "game_state": String
# }
@csrf_exempt
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