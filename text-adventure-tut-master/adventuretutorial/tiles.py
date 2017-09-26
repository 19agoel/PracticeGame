"""Describes the tiles in the world space."""
__author__ = 'Phillip Johnson'

import items, enemies, actions, world


class MapTile:
    """The base class for a tile within the world space"""
    def __init__(self, x, y):
        """Creates a new tile.

        :param x: the x-coordinate of the tile
        :param y: the y-coordinate of the tile
        """
        self.x = x
        self.y = y

    def intro_text(self):
        """Information to be displayed when the player moves into this tile."""
        raise NotImplementedError()

    def modify_player(self, the_player):
        """Process actions that change the state of the player."""
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())

        return moves


class StartingRoom(MapTile):
    def intro_text(self):
        return """
        You are standing in a small but brightly lit room.
        There is a computer interface port on the wall nearest you.
        You may exit through the door to the south.
        """

    def modify_player(self, the_player):
        #Room has no action on player
        pass


class Hallway(MapTile):
    def intro_text(self):
        return """
        You are now in a hallway.
        Different colored lights flash occasionally on the walls.
        """

    def modify_player(self, the_player):
        #Room has no action on player
        pass




class HallwayDoor(MapTile):
    def intro_text(self):
        return """
        You are now in a hallway.
        Different colored lights flash occasionally on the walls.
        There is a small door in the wall
        """

    def modify_player(self, the_player):
        #Room has no action on player
        pass


    def modify_player(self, the_player):
        #Room has no action on player
        pass


class LootRoom(MapTile):
    """A room that adds something to the player's inventory"""
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, the_player):
        the_player.inventory.append(self.item)

    def modify_player(self, the_player):
        self.add_loot(the_player)


class FindKeyRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Key())

    def intro_text(self):
        return """
        You are now in a small storage closet.
        You notice something shiny in the corner.
        It's a keycard. You pick it up.
        """

class NeedKeyRoom(MapTile):

    def intro_text(self):
        return """
        You enter what looks like a security room.
        There is a keycard slot on the wall.
        """
    def modify_player(self, the_player):
        for item in the_player.inventory:
            if item.name == "A keycard":
                print("\nYou insert the keycard into the slot. A door slides open, and an escape pod reveals itself.\nYou climb in the escape pod, and fly away.\nYOU WIN!")
                the_player.victory = True

class Find5GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(5))

    def intro_text(self):
        return """
        Someone dropped a 5 gold piece. You pick it up.
        """


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ogre())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An ogre is blocking your path!
            """
        else:
            return """
            A dead ogre reminds you of your triumph.
            """


class SnakePitRoom(MapTile):
    def intro_text(self):
        return """
        You have fallen into a pit of deadly snakes!

        You have died!
        """

    def modify_player(self, player):
        player.hp = 0


class EscapePodRoom(MapTile):
    def intro_text(self):
        return """
        You climb into the escape pod and it launches off.


        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True
