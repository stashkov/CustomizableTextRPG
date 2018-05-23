class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return f'{self.name}\n---\n{self.description}\n'


class Gold(Item):
    def __init__(self, amount):
        self.amount = amount
        super().__init__(name="Gold",
                         description=f"{str(self.amount)} Gold",
                         value=self.amount)


class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)

    def __str__(self):
        return f"{self.name}\n---\n{self.description}\nDamage: {self.damage}"


class Rock(Weapon):
    def __init__(self):
        super().__init__(name="Rock",
                         description="A fist-sized rock, suitable for bludgeoning.",
                         value=0,
                         damage=5)
