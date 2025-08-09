from firebase_functions import https_fn
from firebase_admin import initialize_app
from controllers import game_controller

initialize_app()

@https_fn.on_request()
def startGame(request: https_fn.Request):
    return game_controller.start_game_controller(request)

@https_fn.on_request()
def updateScoreAndGameStatus(request: https_fn.Request):
    return game_controller.update_score_and_game_status_controller(request)

@https_fn.on_request()
def getGameList(request: https_fn.Request):
    return game_controller.get_game_list_controller(request)

@https_fn.on_request()
def deleteGame(request: https_fn.Request):
    return game_controller.delete_game_controller(request)

@https_fn.on_request()
def getGameInfo(request: https_fn.Request):
    return game_controller.get_game_info_controller(request)
