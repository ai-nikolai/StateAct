cool_simple_goal_plan_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a cool mug in shelf.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("go to countertop 1")

Input:
On the countertop 1, you see a knife 1, a pan 2, a pan 1, and a plate 1.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("go to countertop 2")

Input:
On the countertop 2, you see a apple 2, a butterknife 2, a fork 3, a houseplant 1, a knife 2, a lettuce 3, a spatula 1, and a winebottle 1.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("go to cabinet 1")

Input:
The cabinet 1 is closed.

Ouput:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("open cabinet 1")


Input:
You open the cabinet 1. The cabinet 1 is open. In it, you see a mug 3.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("take mug 3 from cabinet 1")

Input:
You pick up the mug 3 from the cabinet 1.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
ction("go to fridge 1")

Input:
The fridge 1 is closed.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("cool mug 3 with fridge 1")

Input:
You cool the mug 3 using the fridge 1.

Ouput:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("go to shelf 1")

Input:
On the shelf 1, you see a cup 2, a cup 1, a peppershaker 1, and a saltshaker 1.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("put mug 3 in/on shelf 1")
"""


clean_simple_goal_plan_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
action("go to fridge 1")

Input:
The fridge 1 is closed.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
action("open fridge 1")

Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
action("go to diningtable 1")

Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
action("take lettuce 1 from diningtable 1")

Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
action("go to sinkbasin 1")

Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
action("clean lettuce 1 with sinkbasin 1")

Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
action("go to diningtable 1")

Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
action("put lettuce 1 in/on diningtable 1")
"""


examine_simple_goal_plan_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a bed 1, a desk 1, a drawer 3, a drawer 2, a drawer 1, a garbagecan 1, a safe 1, a shelf 5, a shelf 4, a shelf 3, a shelf 2, a shelf 1, a sidetable 2, and a sidetable 1.
Your task is to: look at bowl under the desklamp.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to drawer 1")

Input:
On the drawer 1, you see nothing.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to drawer 2")

Input:
The drawer 2 is closed.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("open drawer 2")

Input:
You open the drawer 2. The drawer 2 is open. In it, you see
nothing.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to drawer 3")


Input:
The drawer 3 is closed.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("open drawer 3")


Input:
You open the drawer 3. The drawer 3 is open. In it, you see
nothing.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to desk 1")


Input:
On the desk 1, you see a alarmclock 2, a book 1, a
cellphone 1, a keychain 1, a laptop 2, a laptop 1, and a
pen 3.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to sidetable 1")

Input:
On the sidetable 1, you see a cd 1, a pen 1, and a pencil
1.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to shelf 1")


Input:
On the shelf 1, you see nothing.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to shelf 2")

Input:
On the shelf 2, you see a bowl 1.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("take bowl 1 from shelf 2")

Input:
You pick up the bowl 1 from the shelf 2.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to desk 1")

Input:
On the desk 1, you see a alarmclock 2, a book 1, a
cellphone 1, a keychain 1, a laptop 2, a laptop 1, and a
pen 3.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to sidetable 1")

Input:
On the sidetable 1, you see a cd 1, a pen 1, and a pencil
1.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("go to sidetable 2")

Input:
On the sidetable 2, you see a alarmclock 1, a desklamp 1,
and a pen 2.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("use desklamp 1")

Input:
You turn on the desklamp 1.

Output:
goal("look at bowl under the desklamp")
plan("Looking at the goal and the room, I need to first find a bowl, then take it. Then I need to find a desklamp, then I need to turn it on and put the bowl in/on the same place as the desklamp.")
action("put bowl 1 in/on sidetable 2")
"""



heat_simple_goal_plan_1="""
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a diningtable 1, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: heat some egg and put it in diningtable.

Ouput:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("go to fridge 1")

Input:
The fridge 1 is closed.

Output:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("open fridge 1")

Input:
You open the fridge 1. The fridge 1 is open. In it, you see a lettuce 2, a mug 2, and a potato 3.

Output:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("go to countertop 1")

Input:
On the countertop 1, you see a bread 1, a fork 1, and a saltshaker 1.

Output:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("go to countertop 2")

Input:
On the countertop 2, you see nothing.

Output:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("go to countertop 3")

Input:
On the countertop 3, you see a bowl 1, a butterknife 1, a egg 2, a kettle 2, a plate 1, a sink 1, and a spatula 2.

Output:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("take egg 2 from countertop 3")

Input:
You pick up the egg 2 from the countertop 3.

Output:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("go to microwave 1")

Input:
The microwave 1 is closed.

Output:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("heat egg 2 with microwave 1")

Input:
You heat the egg 2 using the microwave 1.

Output:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("go to diningtable 1")

Input:
On the diningtable 1, you see a apple 2, a bread 3, a egg 1, a kettle 1, a knife 1, a mug 1, a papertowelroll 1, a peppershaker 2, a potato 1, a soapbottle 1, and a spatula 1.

Output:
goal("heat some egg and put it in diningtable")
plan("Looking at the goal and the room, I need to first find an egg, then take it, then go to the microwave, then heat the egg using the microwave, and then go to the diningtable and put the egg in/on the diningtable.")
action("put egg 2 in/on diningtable 1")
"""



clean_state_goal_plan_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
state({"Places Visited":[], "Objects Taken":[]})
action("go to fridge 1")

Input:
The fridge 1 is closed.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
state({"Places Visited":["fridge 1"], "Objects Taken":[]})
action("open fridge 1")

Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
state({"Places Visited":["fridge 1"], "Objects Taken":[]})
action("go to diningtable 1")

Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
state({"Places Visited":["fridge 1", "diningtable 1"], "Objects Taken":[]})
action("take lettuce 1 from diningtable 1")

Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
state({"Places Visited":["fridge 1", "diningtable 1"], "Objects Taken":["lettuce 1"]})
action("go to sinkbasin 1")

Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
state({"Places Visited":["fridge 1", "diningtable 1", "sinkbasin 1"], "Objects Taken":["lettuce 1"]})
action("clean lettuce 1 with sinkbasin 1")

Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
state({"Places Visited":["fridge 1", "diningtable 1", "sinkbasin 1"], "Objects Taken":["lettuce 1"]})
action("go to diningtable 1")

Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
goal("put a clean lettuce in diningtable")
plan("Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.")
state({"Places Visited":["fridge 1", "diningtable 1", "sinkbasin 1","diningtable 1"], "Objects Taken":["lettuce 1"]})
action("put lettuce 1 in/on diningtable 1")
"""


clean_state_goal_plan_v2_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "goal":"put a clean lettuce in diningtable",
    "plan":"Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" :[], 
    "objects_taken":[],
    "current_objective" : "find lettuce",
}
action("go to fridge 1")

Input:
The fridge 1 is closed.

Output:
state = {
    "goal":"put a clean lettuce in diningtable",
    "plan":"Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" :["fridge 1"], 
    "objects_taken":[],
    "current_objective" : "find lettuce",
}
action("open fridge 1")

Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "goal":"put a clean lettuce in diningtable",
    "plan":"Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" :["fridge 1"], 
    "objects_taken":[],
    "current_objective" : "find lettuce",
}
action("go to diningtable 1")

Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal":"put a clean lettuce in diningtable",
    "plan":"Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" :["fridge 1", "diningtable 1"], 
    "objects_taken":[],
    "current_objective" : "take lettuce",
}
action("take lettuce 1 from diningtable 1")

Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "goal":"put a clean lettuce in diningtable",
    "plan":"Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" :["fridge 1", "diningtable 1"], 
    "objects_taken":["lettuce 1"],
    "current_objective" : "clean lettuce",
}
action("go to sinkbasin 1")

Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "goal":"put a clean lettuce in diningtable",
    "plan":"Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" :["fridge 1", "diningtable 1","sinkbasin 1"], 
    "objects_taken":["lettuce 1"],
    "current_objective" : "clean lettuce",
}
action("clean lettuce 1 with sinkbasin 1")

Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "goal":"put a clean lettuce in diningtable",
    "plan":"Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" :["fridge 1", "diningtable 1","sinkbasin 1"], 
    "objects_taken":["lettuce 1"],
    "current_objective" : "put lettuce in/on diningtable",
}
action("go to diningtable 1")

Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal":"put a clean lettuce in diningtable",
    "plan":"Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" :["fridge 1", "diningtable 1","sinkbasin 1"], 
    "objects_taken":["lettuce 1"],
    "current_objective" : "put lettuce in/on diningtable",
}
action("put lettuce 1 in/on diningtable 1")
"""

clean_state_goal_plan_v3_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : [], 
    "current_inventory" : [],
    "current_location" : "starting location",
    "current_objective" : "find lettuce",
}
action("go to fridge 1")

Input:
The fridge 1 is closed.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1"], 
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "current_objective" : "find lettuce",
}
action("open fridge 1")

Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1"], 
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "current_objective" : "find lettuce",
}
action("go to diningtable 1")

Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1"], 
    "current_inventory" : [],
    "current_location" : "diningtable 1",
    "current_objective" : "take lettuce",
}
action("take lettuce 1 from diningtable 1")

Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "current_objective" : "clean lettuce",
}
action("go to sinkbasin 1")

Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "current_objective" : "clean lettuce",
}
action("clean lettuce 1 with sinkbasin 1")

Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "current_objective" : "put lettuce in/on diningtable",
}
action("go to diningtable 1")

Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "current_objective" : "put lettuce in/on diningtable",
}
action("put lettuce 1 in/on diningtable 1")
"""


clean_state_goal_plan_v4_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : [], 
    "current_inventory" : [],
    "current_location" : "starting location",
    "current_objective" : "find lettuce",
    "action" : "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1"], 
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "current_objective" : "find lettuce",
    "action" : "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1"], 
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "current_objective" : "find lettuce",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1"], 
    "current_inventory" : [],
    "current_location" : "diningtable 1",
    "current_objective" : "take lettuce",
    "action" : "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "current_objective" : "clean lettuce",
    "action" : "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "current_objective" : "clean lettuce",
    "action" : "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "current_objective" : "put lettuce in/on diningtable",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "current_objective" : "put lettuce in/on diningtable",
    "action" : "put lettuce 1 in/on diningtable 1"
}


"""

clean_state_goal_plan_v4b_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : [], 
    "current_inventory" : [],
    "current_location" : "starting location",
    "action" : "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1"], 
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1"], 
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1"], 
    "current_inventory" : [],
    "current_location" : "diningtable 1",
    "action" : "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "places_visited" : ["fridge 1", "diningtable 1", "sinkbasin 1"], 
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "put lettuce 1 in/on diningtable 1"
}


"""


clean_state_goal_plan_v4c_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "starting location",
    "action" : "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "diningtable 1",
    "action" : "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "put lettuce 1 in/on diningtable 1"
}


"""


clean_state_goal_plan_v4d_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "starting location",
    "action" : "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "diningtable 1",
    "action" : "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "Looking at the goal and the room, I need to first find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "put lettuce 1 in/on diningtable 1"
}


"""

clean_state_goal_plan_v4e_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "starting location",
    "action" : "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "diningtable 1",
    "action" : "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "reminder" : "Look at the plan and generate a valid action.",
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "put lettuce 1 in/on diningtable 1"
}


"""

clean_state_goal_plan_v4f_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "starting location",
    "action" : "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "fridge 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : [],
    "current_location" : "diningtable 1",
    "action" : "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "sinkbasin 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_inventory" : ["lettuce 1"],
    "current_location" : "diningtable 1",
    "action" : "put lettuce 1 in/on diningtable 1"
}


"""

clean_state_goal_plan_v4g_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location" : "starting location",
    "action" : "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location" : "fridge 1",
    "action" : "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location" : "fridge 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location" : "diningtable 1",
    "action" : "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location" : "diningtable 1",
    "action" : "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location" : "sinkbasin 1",
    "action" : "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location" : "sinkbasin 1",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "current_location" : "diningtable 1",
    "action" : "put lettuce 1 in/on diningtable 1"
}


"""


clean_state_goal_plan_v4h_1 = """
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action" : "go to fridge 1"
}


Input:
The fridge 1 is closed.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action" : "open fridge 1"
}


Input:
You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.

Output: 
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action" : "take lettuce 1 from diningtable 1"
}


Input:
You pick up the lettuce 1 from the diningtable 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action" : "go to sinkbasin 1"
}


Input:
On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action" : "clean lettuce 1 with sinkbasin 1"
}


Input:
You clean the lettuce 1 using the sinkbasin 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action" : "go to diningtable 1"
}


Input:
On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.

Output:
state = {
    "goal" : "put a clean lettuce in diningtable",
    "plan" : "I need to find a lettuce, then take it, then go to the sink, then clean the lettuce in the sink and then go to the diningtable and put the lettuce in/on the diningtable.",
    "action" : "put lettuce 1 in/on diningtable 1"
}


"""



