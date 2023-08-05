from virus_class import virus
from boundary_class import boundary

class person_obj:
    
    def __init__(self, x, y, vx, vy, status):
        
        # Attributes of each person
        self.x = x                  # Cartisan location
        self.y = y
        self.vx = vx                # Velocities
        self.vy = vy
        self.status = status        # 
        self.InfectedTime = 0       # Counter records number of epochs since infection
        self.ImmunityWear = 4       # Percentege for status to go 'Recovered' to 'Susceptible'
        
    # Each peron has a current string status of the following:
    #  "Susceptible" has the ability to become infected. 
    #  "Infected" can infect others if in close enough range to susceptible.
    #  "Recovered" is immune to becoming infected.
    #  "Dead" will no longer interact with anything.
           
    def BoundsCheck(self, attr):
    # Restricts the movements of the person.
    # In this case its a rectangle with specified width as X in the boundary class
    # 
    # Probaly should be in the boundary class where shape is specified and conditions below       
        if attr == 'x':                  
            if self.x > Boundary.X:
                self.x = Boundary.X
                self.vx = -self.vx
            if self.x < 0:
                self.x = 0
                self.vx = -self.vx
            return
        if attr == 'y':
            if self.y > Boundary.Y:
                self.y = Boundary.Y
                self.vy = -self.vy
            if self.y < 0:
                self.y = 0
                self.vy = -self.vy
            return

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
        if attr in ['x', 'y']:
            self.BoundsCheck(attr)
            
    def location(self):
        return np.array([self.x, self.y])
    def velocity(self):
        return np.array([self.vx, self.vy])
    def MovePerson(self):
        if self.status != 'Dead':
            Newlocation = self.location() + self.velocity()
            self.x = Newlocation[0]
            self.y = Newlocation[1]      

    def ModifyStatus(self):
        if self.status == 'Infected' and PercentChance(virus.DeathChance):
            self.status = 'Dead'
        if self.status == 'Recovered' and PercentChance(self.ImmunityWear):
            self.status = 'Susceptible'
            self.InfectedTime = 0