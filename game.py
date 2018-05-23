import world
from player import Player


def play():
    wl = world.WorldLoader()
    wl.load_locations()
    player = Player()
    room = world.tile(player.location_x, player.location_y)
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile(player.location_x, player.location_y)
        # print(f"Right now I am at position {player.location_x, player.location_y}")
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            print("Choose an action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            action_input = input('Action: ')
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break


if __name__ == "__main__":
    play()
