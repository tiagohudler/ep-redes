# CONSTANTS

DEFEND = "DEFEND"
SHOOT = "SHOOT"
RELOAD = "RELOAD"

class game:
    p1Games = 0
    p2Games = 0
    p1Points = 0
    p2Points = 0
    rounds = 3
    p1Lives = 2
    p2Lives = 2
    p1Bullets = 1
    p2Bullets = 1
    roundWinner = ''

    def resetBullets(self):
        self.p1Bullets = 1
        self.p2Bullets = 1
    def restart(self):
        self.p1Points = 0
        self.p2Points = 0
        self.rounds = 3
        self.p1Lives = 2
        self.p2Lives = 2
        self.p1Bullets = 1
        self.p2Bullets = 1

    # Deals with player's actions and game logic
    def action(self, p1Action, p2Action):
        
        p1Shot = False
        p2Shot = False
        if p1Action == SHOOT:
            p1Shot = True
        if p2Action == SHOOT:
            p2Shot = True
        
        if p1Action == RELOAD:
            self.p1Bullets += 1
        if p2Action == RELOAD:
            self.p2Bullets += 1

        if p1Shot:
            self.p1Bullets -= 1
            if p2Action != DEFEND:
                self.p2Lives -= 1
                self.resetBullets()


        if p2Shot:
            self.p2Bullets -= 1
            if p1Action != DEFEND:  
                self.p1Lives -= 1
                self.resetBullets()

        
        if self.p1Lives == 0 or self.p2Lives == 0:

            # Both died
            if self.p1Lives == 0 and self.p2Lives == 0:
                self.resetBullets()
                self.p1Lives += 1
                self.p2Lives += 1
                return "Both players lost all their lives, so both are alive with 1 life"

            # Whoever didn't die gets a point
            if self.p1Lives == 0:
                self.p2Points += 1
            else:
                self.p1Points += 1

            self.rounds -= 1

            # End game
            if self.rounds < self.p1Points or self.rounds < self.p2Points:
                if self.p1Points > self.p2Points:
                    self.p1Games += 1
                    self.roundWinner = 'Player 1'
                else:
                    self.p2Games += 1
                    self.roundWinner = 'Player 2'
                self.restart()
                return 3
            
            self.p1Lives = 2
            self.p2Lives = 2
            return 1
        
        return 2
            
    