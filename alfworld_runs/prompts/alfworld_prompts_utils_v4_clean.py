clean_state_goal_plan_v4a_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": [], 
    "current_inventory": [],
    "current_location": "starting location",
    "current_objective": "find lettuce",
    "action": "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1"], 
    "current_inventory": [],
    "current_location": "fridge 1",
    "current_objective": "find lettuce",
    "action": "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1"], 
    "current_inventory": [],
    "current_location": "fridge 1",
    "current_objective": "find lettuce",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1"], 
    "current_inventory": [],
    "current_location": "diningtable 1",
    "current_objective": "take lettuce",
    "action": "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "current_objective": "clean lettuce",
    "action": "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "current_objective": "clean lettuce",
    "action": "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "current_objective": "put lettuce in/on diningtable",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "current_objective": "put lettuce in/on diningtable",
    "action": "put lettuce 1 in/on diningtable 1"
}


"""

clean_state_goal_plan_v4b_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": [], 
    "current_inventory": [],
    "current_location": "starting location",
    "action": "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1"], 
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1"], 
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1"], 
    "current_inventory": [],
    "current_location": "diningtable 1",
    "action": "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "put lettuce 1 in/on diningtable 1"
}


"""


clean_state_goal_plan_v4c_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "starting location",
    "action": "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "diningtable 1",
    "action": "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "put lettuce 1 in/on diningtable 1"
}


"""


clean_state_goal_plan_v4d_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "starting location",
    "action": "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "diningtable 1",
    "action": "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "put lettuce 1 in/on diningtable 1"
}


"""

clean_state_goal_plan_v4e_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "starting location",
    "action": "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "diningtable 1",
    "action": "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "reminder": "Look at the plan and generate a valid action.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "put lettuce 1 in/on diningtable 1"
}


"""

clean_state_goal_plan_v4f_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "starting location",
    "action": "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "fridge 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": [],
    "current_location": "diningtable 1",
    "action": "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "action": "put lettuce 1 in/on diningtable 1"
}


"""

clean_state_goal_plan_v4g_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location": "starting location",
    "action": "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location": "fridge 1",
    "action": "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location": "fridge 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location": "diningtable 1",
    "action": "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location": "diningtable 1",
    "action": "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location": "sinkbasin 1",
    "action": "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location": "sinkbasin 1",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location": "diningtable 1",
    "action": "put lettuce 1 in/on diningtable 1"
}


"""


clean_state_goal_plan_v4h_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action": "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action": "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action": "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action": "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action": "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action": "put lettuce 1 in/on diningtable 1"
}


"""

clean_state_goal_plan_v4i_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
{
    "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": [], 
    "current_inventory": [],
    "current_location": "starting location",
    "current_objective": "find lettuce",
    "action": "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
{
    "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1"], 
    "current_inventory": [],
    "current_location": "fridge 1",
    "current_objective": "find lettuce",
    "action": "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
{
    "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1"], 
    "current_inventory": [],
    "current_location": "fridge 1",
    "current_objective": "find lettuce",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1"], 
    "current_inventory": [],
    "current_location": "diningtable 1",
    "current_objective": "take lettuce",
    "action": "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
{
    "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "current_objective": "clean lettuce",
    "action": "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
{
    "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "current_objective": "clean lettuce",
    "action": "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
{
    "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "sinkbasin 1",
    "current_objective": "put lettuce in/on diningtable",
    "action": "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
{
    "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
    "goal": "put a clean lettuce in diningtable",
    "plan": "I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited": ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory": ["lettuce 1"],
    "current_location": "diningtable 1",
    "current_objective": "put lettuce in/on diningtable",
    "action": "put lettuce 1 in/on diningtable 1"
}


"""
