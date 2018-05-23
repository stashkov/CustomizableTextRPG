import actions
import enemies
import items
import world
from typing import List


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves: List[actions.Action] = list()
        if world.tile(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        return moves


class StartingRoom(MapTile):
    def __init__(self, x, y, intro_text):
        self._intro_text = intro_text
        super().__init__(x, y)

    def intro_text(self):
        return f"""
        {self._intro_text}
        """

    def modify_player(self, player):
        pass


class LootRoom(MapTile):
    def intro_text(self):
        pass

    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(MapTile):
    def intro_text(self):
        pass

    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print(f"Enemy does {self.enemy.damage} damage. You have {player.hp} HP remaining.")

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class ExitRoom(MapTile):
    def __init__(self, x, y, intro_text):
        self._intro_text = intro_text
        super().__init__(x, y)

    def intro_text(self):
        return f"""
        {self._intro_text}
         
        You won the game!
        """

    def modify_player(self, player):
        player.victory = True


class GenerateEnemyRoom(EnemyRoom):
    def __init__(self, x, y, enemy, intro_text):
        self.enemy = enemy
        self._intro_text = intro_text
        super().__init__(x, y, enemies.Enemy(enemy.name, enemy.hp, enemy.damage))

    def intro_text(self):
        if self.enemy.is_alive():
            return f"""
            A {self.enemy.name} appears in front of you! He says: {self._intro_text}
            """
        else:
            return f"""
            The corpse of a {self.enemy.name} rots on the ground.
            """


class GenerateLootRoom(LootRoom):
    def __init__(self, x, y, loot, intro_text):
        self.loot = loot
        self._intro_text = intro_text
        super().__init__(x, y, loot)

    def intro_text(self):
        return f"""
        Your notice something shiny in the corner. 
        {self._intro_text}
        """


class GenerateEmptyRoom(MapTile):
    def intro_text(self):
        return """
        Nothing to see here. You must forge onwards.
        """

    def modify_player(self, player):
        pass
