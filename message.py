# Codes
# 0 - Waiting for opponent
# 1 - Game start
# 2 - Action
# 3 - Game over

class message:
    code = ""
    action = ""
    message = ""
    bullets = ""
    score = ""
    rounds = ""

    def __init__(self, code, action, message):
        self.code = code
        self.action = action
        self.message = message

