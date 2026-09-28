#Mother class of all weapons
class Weapon:
    def __init__(self, damage: int, range: float, ammo: int, equipped: bool):
        self.damage = damage
        self.range = range
        self.ammo = ammo
        self.equipped = equipped

    def canFire(self):
        return self.ammo >= 0

    def fire(self):
        if self.canFire():
            self.ammo -= 1

    def isEquipped(self):
        return self.equipped