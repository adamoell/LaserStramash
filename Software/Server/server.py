from typing_extensions import ParamSpecKwargs


class Server():
    def __init__(self):
        games = {}

    # TODO
    # attribs Games
    # methods for each message
    def newgame(self, topic, message):
        obj = json.loads(message)
        name = obj["name"]
        type = obj["type"]
        maxtime = obj["maxtime"]
        if "teams" in obj:
            # TODO parse
            print("Got some teams")
        if "players" in obj:
            # TODO parse
            print("Got some players")
        
        #  instantiate appropriate class
        # TODO make sure this is a legit class!
        gameclass = "Game_"+type 
        module = __import__("game_"+type)
        class_ = getattr(module, gameclass)
        game = class_()
        games["makeid"] = game


    pass 