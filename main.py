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
        "author": "Nagini",  # TODO: Your Battlesnake Username
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

# Find the neighboring coordinate


def is_snake_neighbor(youSnake, min_food, opponentsNotYou):
    if (manhattan_distance(youSnake['head'].values(), min_food.values()) == 1):
        food_pointX, food_pointY = min_food.values()
        neighbor_coordinate = [(food_pointX-1, food_pointY), (food_pointX+1, food_pointY),
                               (food_pointX, food_pointY-1), (food_pointX, food_pointY+1)]
        for opponent in opponentsNotYou:
            if tuple(opponent["head"].values()) in neighbor_coordinate and opponent["length"] >= youSnake['length']:
                return True
    return False

# If your neignbor snake is 2 manhattan distance away from you, be cautious


def is_snake_too_close(youSnake, safe_move, opponentsNotYou):
    for opponent in opponentsNotYou:
        if manhattan_distance(youSnake['head'].values(), opponent["head"].values()) == 2:
            if (opponent["length"] >= youSnake['length']):
                if safe_move == "left":
                    return (youSnake['head']['x'] - opponent["head"]['x'] > 0)
                elif safe_move == "down":
                    return (youSnake['head']['y'] - opponent["head"]['y'] > 0)
                elif safe_move == "right":
                    return (youSnake['head']['x'] - opponent["head"]['x'] < 0)
                else:
                    return (youSnake['head']['y'] - opponent["head"]['y'] < 0)
            else:
                if safe_move == "left":
                    if (youSnake['head']['x'] - opponent["head"]['x'] > 0):
                        return "left"
                elif safe_move == "down":
                    if (youSnake['head']['y'] - opponent["head"]['y'] > 0):
                        return "down"
                elif safe_move == "right":
                    if (youSnake['head']['x'] - opponent["head"]['x'] < 0):
                        return "right"
                else:
                    if (youSnake['head']['y'] - opponent["head"]['y'] < 0):
                        return "up"
    return False

# if there is only 2 snakes on board now, you may want to attack this snake


def is_last_2_snakes(youSnake, safe_move, opponentsNotYou):
    if (len(opponentsNotYou) == 1) and (opponentsNotYou[0]["length"] < youSnake['length']):
        if safe_move == "left":
            if (youSnake['head']['x'] > opponentsNotYou[0]['head']['x']):
                return True
        elif safe_move == "down":
            if (youSnake['head']['y'] > opponentsNotYou[0]['head']['y']):
                return True
        elif safe_move == "right":
            if (youSnake['head']['x'] < opponentsNotYou[0]['head']['x']):
                return True
        else:
            if (youSnake['head']['y'] < opponentsNotYou[0]['head']['y']):
                return True
    return False


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
    opponentsNotYou = [
        opponent for opponent in opponents if opponent['id'] != youSnake['id']]
    opponentsNotYouBody = [opponent['body'] for opponent in opponentsNotYou]
    opponentsNotYouBody = [
        item for sublist in opponentsNotYouBody for item in sublist]

    if (is_move_safe["left"]):
        if ({"x": my_head["x"]-1, "y": my_head["y"]} in opponentsNotYouBody):
            is_move_safe["left"] = False
        else:
            result_is_snake_too_close = is_snake_too_close(
                youSnake, "left", opponentsNotYou)
            if isinstance(result_is_snake_too_close, int):
                if result_is_snake_too_close:
                    is_move_safe["left"] = False
            else:
                return {"move": "left"}
    if (is_move_safe["right"]):
        if ({"x": my_head["x"]+1, "y": my_head["y"]} in opponentsNotYouBody):
            is_move_safe["right"] = False
        else:
            result_is_snake_too_close = is_snake_too_close(
                youSnake, "right", opponentsNotYou)
            if isinstance(result_is_snake_too_close, int):
                if result_is_snake_too_close:
                    is_move_safe["right"] = False
            else:
                return {"move": "right"}
    if (is_move_safe["up"]):
        if ({"x": my_head["x"], "y": my_head["y"]+1} in opponentsNotYouBody):
            is_move_safe["up"] = False
        else:
            result_is_snake_too_close = is_snake_too_close(
                youSnake, "up", opponentsNotYou)
            if isinstance(result_is_snake_too_close, int):
                if result_is_snake_too_close:
                    is_move_safe["up"] = False
            else:
                return {"move": "up"}
    if (is_move_safe["down"]):
        if ({"x": my_head["x"], "y": my_head["y"]-1} in opponentsNotYouBody):
            is_move_safe["down"] = False
        else:
            result_is_snake_too_close = is_snake_too_close(
                youSnake, "down", opponentsNotYou)
            if isinstance(result_is_snake_too_close, int):
                if result_is_snake_too_close:
                    is_move_safe["down"] = False
            else:
                return {"move": "down"}

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
    if ("left" in safe_moves):
        if my_head['x'] > min_food['x']:
            better_moves.append("left")
        if is_last_2_snakes(youSnake, "left", opponentsNotYou):
            return {"move": "left"}
    if ("right" in safe_moves):
        if my_head['x'] < min_food['x']:
            better_moves.append("right")
        if is_last_2_snakes(youSnake, "right", opponentsNotYou):
            return {"move": "right"}
    if ("up" in safe_moves):
        if my_head['y'] < min_food['y']:
            better_moves.append("up")
        if is_last_2_snakes(youSnake, "up", opponentsNotYou):
            return {"move": "up"}
    if ("down" in safe_moves):
        if my_head['y'] > min_food['y']:
            better_moves.append("down")
        if is_last_2_snakes(youSnake, "down", opponentsNotYou):
            return {"move": "down"}

    if len(better_moves) != 0:
        # dont do this when there is a head to head collision and you know you will lose, more to come
        if len(set(better_moves)) == 1:
            if not is_snake_neighbor(youSnake, min_food, opponentsNotYou):
                next_move = better_moves[0]
            else:
                safe_moves.remove(better_moves[0])
                next_move = random.choice(safe_moves)
        else:
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
