# Código
# 0 - waiting for opponent
# 1 - game start
# 2 - action
# 3 - game over

class message:
    code = ""
    action = ""
    message = ""
    bullets = ""
    score = ""

    def __init__(self, code, action, message, bullets, score):
        self.code = code
        self.action = action
        self.message = message
        self.bullets = bullets
        self.score = score

