# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "herobrine",  # battlesnake username
        "color": "#888888",  # snake color
        "head": "default",  # head
        "tail": "default",  # tail
    }

# measures the absolute distance from head to food
def measure_food_distance(headcoords: typing.Dict, game_state: typing.Dict):
    food_coords = game_state["board"]["food"]
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    result = board_height + board_width
    for c in food_coords:
        distance = abs(c["x"] - headcoords["x"]) + abs(c["y"] - headcoords["y"])
        if distance < result:
            result = distance
    return result

# returns all potential next moves
def next_move_coord(head_coords: typing.Dict, move: str):
    match move:
        case "right":
            return {"x": head_coords["x"] + 1, "y": head_coords["y"]}
        case "left":
            return {"x": head_coords["x"] - 1, "y": head_coords["y"]}
        case "up":
            return {"x": head_coords["x"], "y": head_coords["y"] + 1}
        case "down":
            return {"x": head_coords["x"], "y": head_coords["y"] - 1}
        case _:
            return head_coords


# calculates the next best move to get to the closest food
def best_move_for_food(head_coords: typing.Dict, game_state: typing.Dict, safe_moves):
    result = "down"
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    distance = board_height + board_width
    for move in safe_moves:
        food_distance = measure_food_distance(next_move_coord(head_coords, move), game_state)
        if food_distance < distance:
            distance = food_distance
            result = move
    return result





# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

# checks if specific set of coordinates are in a list
def contains(coordlist: typing.Dict, coord: typing.Dict):
    for c in coordlist:
        if c["x"] == coord["x"] and c["y"] == coord["y"]:
            return True
    return False



# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"



    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if my_head["x"] == 0:
        is_move_safe["left"] = False

    if my_head["y"] == 0:
        is_move_safe["down"] = False

    if board_width - 1 == my_head["x"]:
        is_move_safe["right"] = False

    if board_height - 1 == my_head["y"]:
        is_move_safe["up"] = False


    # prevent Battlesnake from colliding with itself

    my_body = game_state['you']['body']
    if contains(my_body, {"x": my_head["x"] + 1, "y": my_head["y"]}):
        is_move_safe["right"] = False

    if contains(my_body, {"x": my_head["x"] - 1, "y": my_head["y"]}):
        is_move_safe["left"] = False

    if contains(my_body, {"x": my_head["x"], "y": my_head["y"] + 1}):
        is_move_safe["up"] = False

    if contains(my_body, {"x": my_head["x"], "y": my_head["y"] - 1}):
        is_move_safe["down"] = False

    # Prevent Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    for snake in opponents:
        snake_coords = snake["body"]
        snake_coords.append(snake["head"])
        if contains(snake_coords, {"x": my_head["x"] + 1, "y": my_head["y"]}):
            is_move_safe["right"] = False

        if contains(snake_coords, {"x": my_head["x"] - 1, "y": my_head["y"]}):
            is_move_safe["left"] = False

        if contains(snake_coords, {"x": my_head["x"], "y": my_head["y"] + 1}):
            is_move_safe["up"] = False

        if contains(snake_coords, {"x": my_head["x"], "y": my_head["y"] - 1}):
            is_move_safe["down"] = False




    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    food = game_state['board']['food']

    # Choose a random move from the safe ones
    next_move = best_move_for_food(my_head, game_state, safe_moves)


    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
