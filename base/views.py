<<<<<<< HEAD
=======
# from django.shortcuts import render
# from django.http import JsonResponse
# import random
# import time
# from agora_token_builder import RtcTokenBuilder
# from .models import RoomMember
# import json
# from django.views.decorators.csrf import csrf_exempt



# # Create your views here.

# def lobby(request):
#     return render(request, 'base/lobby.html')

# def room(request):
#     return render(request, 'base/room.html')


# def getToken(request):
#     appId = "7345b59e1c5b4521a6fea44d45ca613e"
#     appCertificate = "90f532de7464418ea3aeea98e550603b"
#     channelName = request.GET.get('channel')
#     uid = random.randint(1, 230)
#     expirationTimeInSeconds = 3600
#     currentTimeStamp = int(time.time())
#     privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
#     role = 1

#     token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

#     return JsonResponse({'token': token, 'uid': uid}, safe=False)


# @csrf_exempt
# def createMember(request):
#     data = json.loads(request.body)
#     member, created = RoomMember.objects.get_or_create(
#         name=data['name'],
#         uid=data['UID'],
#         room_name=data['room_name']
#     )

#     return JsonResponse({'name':data['name']}, safe=False)


# def getMember(request):
#     uid = request.GET.get('UID')
#     room_name = request.GET.get('room_name')

#     member = RoomMember.objects.get(
#         uid=uid,
#         room_name=room_name,
#     )
#     name = member.name
#     return JsonResponse({'name':member.name}, safe=False)

# @csrf_exempt
# def deleteMember(request):
#     data = json.loads(request.body)
#     member = RoomMember.objects.get(
#         name=data['name'],
#         uid=data['UID'],
#         room_name=data['room_name']
#     )
#     member.delete()
#     return JsonResponse('Member deleted', safe=False)
>>>>>>> main
from django.shortcuts import render
from django.http import JsonResponse
import random
import time
<<<<<<< HEAD
from agora_token_builder import RtcTokenBuilder
=======
# Removed real import of agora_token_builder to avoid ModuleNotFoundError
# from agora_token_builder import RtcTokenBuilder
>>>>>>> main
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt

<<<<<<< HEAD

=======
# --- Placeholder dummy class to replace RtcTokenBuilder ---
class DummyRtcTokenBuilder:
    @staticmethod
    def buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs):
        # Instead of generating a real Agora token, return a fake placeholder string
        return "FAKE_AGORA_TOKEN_PLACEHOLDER"

# Override RtcTokenBuilder with dummy so the rest of the code works without the real module
RtcTokenBuilder = DummyRtcTokenBuilder
>>>>>>> main

# Create your views here.

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')


def getToken(request):
<<<<<<< HEAD
    appId = "7345b59e1c5b4521a6fea44d45ca613e"
    appCertificate = "90f532de7464418ea3aeea98e550603b"
=======
    # Placeholder Agora credentials - replace with real ones if/when you install the real SDK
    appId = "YOUR_AGORA_APP_ID_PLACEHOLDER"
    appCertificate = "YOUR_AGORA_APP_CERTIFICATE_PLACEHOLDER"
>>>>>>> main
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

<<<<<<< HEAD
=======
    # This will call the dummy buildTokenWithUid method and return the fake token string
>>>>>>> main
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

<<<<<<< HEAD
=======

>>>>>>> main
@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)