# CONSTANTES

DEFEND = "DEFEND"
SHOOT = "SHOOT"
RELOAD = "RELOAD"

class game:
    p1Points = 0
    p2Points = 0
    rounds = 3
    p1Lives = 2
    p2Lives = 2
    p1Bullets = 1
    p2Bullets = 1

    def restart(self):
        self.p1Bullets = 1
        self.p2Bullets = 1

    def action(self, p1Action, p2Action):
        p1Shot = False
        p2Shot = False
        if p1Action == SHOOT and self.p1Bullets > 0:
            p1Shot = True
        if p2Action == SHOOT and self.p2Bullets > 0:
            p2Shot = True
        
        if p1Action == RELOAD:
            self.p1Bullets += 1
        if p2Action == RELOAD:
            self.p2Bullets += 1

        if p1Shot:
            self.p1Bullets -= 1
            if p2Action != DEFEND:
                self.p2Lives -= 1
                self.restart()


        if p2Shot:
            self.p2Bullets -= 1
            if p1Action != DEFEND:  
                self.p1Lives -= 1
                self.restart()
        
        if self.p1Lives == 0 or self.p2Lives == 0:
            if self.p1Lives == 0:
                self.p2Points += 1
            else:
                self.p1Points += 1
            self.rounds -= 1
            if self.rounds == 0:
                return '3'
            self.p1Lives = 2
            self.p2Lives = 2
            return '1'
        
        return f"Player 1 action: {p1Action}, Player 2 action: {p2Action}\nPlayer 1 lives: {self.p1Lives}\nPlayer 2 lives: {self.p2Lives}"
            
    