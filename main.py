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
import numpy as np


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "YongBattleSnake",  # TODO: Your Battlesnake Username
        "color": "#736CCB",  # TODO: Choose color
        "head": "beluga",  # TODO: Choose head
        "tail": "curled",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# Calculating Manhattan Distance between 2 points
def manhattan_distance(point1, point2):
    return sum(abs(value1 - value2) for value1, value2 in zip(point1, point2))


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {
        "up": True,
        "down": True,
        "left": True,
        "right": True
    }

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

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if my_head["x"] == board_width-1:
        is_move_safe["right"] = False
    elif my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["y"] == board_height-1:
        is_move_safe["up"] = False
    elif my_head["y"] == 0:
        is_move_safe["down"] = False
    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    youSnake = game_state['you']
    my_body = youSnake['body']
    # print(my_body)
    # print(is_move_safe)
    # print(game_state)

    # print(my_body)

    if (is_move_safe["left"] and {"x": my_head["x"]-1, "y": my_head["y"]} in my_body[1:]):
        is_move_safe["left"] = False
    if (is_move_safe["right"] and {"x": my_head["x"]+1, "y": my_head["y"]} in my_body[1:]):
        is_move_safe["right"] = False
    if (is_move_safe["up"] and {"x": my_head["x"], "y": my_head["y"]+1} in my_body[1:]):
        is_move_safe["up"] = False
    if (is_move_safe["down"] and {"x": my_head["x"], "y": my_head["y"]-1} in my_body[1:]):
        is_move_safe["down"] = False
    # print(is_move_safe)

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    opponentsNotYouBody = [opponent['body'] for opponent in opponents if opponent['id']
                           != youSnake['id']]
    opponentsNotYouBody = [
        item for sublist in opponentsNotYouBody for item in sublist]

    if (is_move_safe["left"] and {"x": my_head["x"]-1, "y": my_head["y"]} in opponentsNotYouBody):
        is_move_safe["left"] = False
    if (is_move_safe["right"] and {"x": my_head["x"]+1, "y": my_head["y"]} in opponentsNotYouBody):
        is_move_safe["right"] = False
    if (is_move_safe["up"] and {"x": my_head["x"], "y": my_head["y"]+1} in opponentsNotYouBody):
        is_move_safe["up"] = False
    if (is_move_safe["down"] and {"x": my_head["x"], "y": my_head["y"]-1} in opponentsNotYouBody):
        is_move_safe["down"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(
            f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    min_distance = board_width + board_height
    min_food = {'x': 0, 'y': 0}
    for food_coordinate in food:
        to_distance = manhattan_distance(
            my_head.values(), food_coordinate.values())
        if to_distance < min_distance:
            min_distance = to_distance
            min_food = food_coordinate

    better_moves = []
    if ("left" in safe_moves and my_head['x'] > min_food['x']):
        better_moves.append("left")
    if ("right" in safe_moves and my_head['x'] < min_food['x']):
        better_moves.append("right")
    if ("up" in safe_moves and my_head['y'] < min_food['y']):
        better_moves.append("up")
    if ("down" in safe_moves and my_head['y'] > min_food['y']):
        better_moves.append("down")

    if len(better_moves) != 0:
        # dont do this when there is a head to head collision and you know you will lose
        next_move = random.choice(better_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info,
        "start": start,
        "move": move,
        "end": end
    })
