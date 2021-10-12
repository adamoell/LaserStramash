class Game:
    def __init__(self):
        print("Initiating Game")
    # TODO properties
    # id - short GUID - 
    #   generate using something like urlsafe_b64encode(os.urandom(6)) (import base64, os)
    #   or better still
    #       alphabet = string.ascii_letters + string.digits
    #       >>> ''.join(random.choices(alphabet, k=8))
    # name
    # start_time
    # players
    # teams
    # status: 0=Unstarted, 1=Active, 2=Finished
    # state (MQTT state message)

    # TODO methods
    # serialise (JSON)
    # deserialise (JSON)
    # save
    # load
    # addplayer
    # deleteplayer
    # addteam
    # deleteteam

    