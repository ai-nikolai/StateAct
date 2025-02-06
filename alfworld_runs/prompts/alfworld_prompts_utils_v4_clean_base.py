clean_v4_base_0 = ["""You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a clean lettuce in diningtable.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a clean lettuce in diningtable",
  "plan": "I need to first find a lettuce, then take it, then clean it with the sinkbasin, and then put it on the diningtable.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find lettuce",
  "thought": "To solve the task, I need to find and take a lettuce, then clean it with sinkbasin, then put it in diningtable. First I need to find a lettuce. A lettuce is more likely to appear in fridge (1), diningtable (1), sinkbasin (1), stoveburner (1-3), cabinet (1-13). I can check one by one, starting with fridge 1.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a clean lettuce in diningtable",
  "plan": "I need to first find a lettuce, then take it, then clean it with the sinkbasin, and then put it on the diningtable.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find lettuce",
  "thought": "",
  "action": "open fridge 1"
}""",
"""You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a clean lettuce in diningtable",
  "plan": "I need to first find a lettuce, then take it, then clean it with the sinkbasin, and then put it on the diningtable.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find lettuce",
  "thought": "",
  "action": "go to diningtable 1"
}""",
"""On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a clean lettuce in diningtable",
  "plan": "I need to first find a lettuce, then take it, then clean it with the sinkbasin, and then put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1"
  ],
  "current_inventory": "",
  "current_location": "diningtable 1",
  "current_objective": "take lettuce",
  "thought": "Now I find a lettuce (1). Next, I need to take it.",
  "action": "take lettuce 1 from diningtable 1"
}""",
"""You pick up the lettuce 1 from the diningtable 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a clean lettuce in diningtable",
  "plan": "I need to first find a lettuce, then take it, then clean it with the sinkbasin, and then put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1"
  ],
  "current_inventory": "lettuce 1",
  "current_location": "diningtable 1",
  "current_objective": "go to sinkbasin",
  "thought": "Now I take a lettuce (1). Next, I need to go to sinkbasin (1) and clean it.",
  "action": "go to sinkbasin 1"
}""",
"""On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a clean lettuce in diningtable",
  "plan": "I need to first find a lettuce, then take it, then clean it with the sinkbasin, and then put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "sinkbasin 1"
  ],
  "current_inventory": "lettuce 1",
  "current_location": "sinkbasin 1",
  "current_objective": "clean lettuce",
  "thought": "",
  "action": "clean lettuce 1 with sinkbasin 1"
}""",
"""You clean the lettuce 1 using the sinkbasin 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a clean lettuce in diningtable",
  "plan": "I need to first find a lettuce, then take it, then clean it with the sinkbasin, and then put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "sinkbasin 1"
  ],
  "current_inventory": "lettuce 1",
  "current_location": "sinkbasin 1",
  "current_objective": "go to diningtable",
  "thought": "Now I clean a lettuce (1). Next, I need to put it in/on diningtable 1.",
  "action": "go to diningtable 1"
}""",
"""On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a clean lettuce in diningtable",
  "plan": "I need to first find a lettuce, then take it, then clean it with the sinkbasin, and then put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "sinkbasin 1",
    "diningtable 1"
  ],
  "current_inventory": "lettuce 1",
  "current_location": "diningtable 1",
  "current_objective": "put lettuce in/on diningtable",
  "thought": "",
  "action": "put lettuce 1 in/on diningtable 1"
}"""
]

clean_v4_base_1 = ["""You are in the middle of a room. Looking quickly around you, you see a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 3, a diningtable 2, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a sidetable 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: clean some apple and put it in sidetable.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find apple",
  "thought": "To solve the task, I need to find and take an apple, then clean it with sinkbasin, then put it in sidetable. First I need to find an apple. An apple is more likely to appear in fridges (1), diningtable (1-3), sidetable (1), countertop (1), sinkbasin (1), garbagecan (1). I can check one by one, starting with fridge 1.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find apple",
  "thought": "",
  "action": "open fridge 1"
}""",
"""You open the fridge 1. The fridge 1 is open. In it, you see a lettuce 2, a mug 2, a potato 2, and a tomato 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find apple",
  "thought": "",
  "action": "go to diningtable 1"
}""",
"""On the diningtable 1, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1"
  ],
  "current_inventory": "",
  "current_location": "diningtable 1",
  "current_objective": "find apple",
  "thought": "",
  "action": "go to diningtable 2"
}""",
"""On the diningtable 2, you see a pineapple 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2"
  ],
  "current_inventory": "",
  "current_location": "diningtable 2",
  "current_objective": "find apple",
  "thought": "",
  "action": "go to diningtable 3"
}""",
"""On the diningtable 3, you see a bowl 2, a bowl 1, a bread 2, and a bread 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2",
    "diningtable 3"
  ],
  "current_inventory": "",
  "current_location": "diningtable 3",
  "current_objective": "find apple",
  "thought": "",
  "action": "go to sidetable 1"
}""",
"""On the sidetable 1, you see a cup 1, a lettuce 1, a peppershaker 3, a potato 1, and a saltshaker 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2",
    "diningtable 3",
    "sidetable 1"
  ],
  "current_inventory": "",
  "current_location": "sidetable 1",
  "current_objective": "find apple",
  "thought": "",
  "action": "go to countertop 1"
}""",
"""On the countertop 1, you see a butterknife 1, a dishsponge 1, and a soapbottle 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2",
    "diningtable 3",
    "sidetable 1",
    "countertop 1"
  ],
  "current_inventory": "",
  "current_location": "countertop 1",
  "current_objective": "find apple",
  "thought": "",
  "action": "go to sinkbasin 1"
}""",
"""On the sinkbasin 1, you see a cup 2, a egg 1, a mug 1, and a potato 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2",
    "diningtable 3",
    "sidetable 1",
    "countertop 1",
    "sinkbasin 1"
  ],
  "current_inventory": "",
  "current_location": "sinkbasin 1",
  "current_objective": "find apple",
  "thought": "",
  "action": "go to garbagecan 1"
}""",
"""On the garbagecan 1, you see a apple 3, and a egg 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2",
    "diningtable 3",
    "sidetable 1",
    "countertop 1",
    "sinkbasin 1",
    "garbagecan 1"
  ],
  "current_inventory": "",
  "current_location": "garbagecan 1",
  "current_objective": "take apple",
  "thought": "Now I find an apple (3). Next, I need to take it.",
  "action": "take apple 3 from garbagecan 1"
}""",
"""You pick up the apple 3 from the garbagecan 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2",
    "diningtable 3",
    "sidetable 1",
    "countertop 1",
    "sinkbasin 1",
    "garbagecan 1"
  ],
  "current_inventory": "apple 3",
  "current_location": "garbagecan 1",
  "current_objective": "go to sinkbasin",
  "thought": "Now I take an apple (3). Next, I need to go to sinkbasin (1) and clean it.",
  "action": "go to sinkbasin 1"
}""",
"""On the sinkbasin 1, you see a cup 2, a egg 1, a mug 1, and a potato 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2",
    "diningtable 3",
    "sidetable 1",
    "countertop 1",
    "sinkbasin 1",
    "garbagecan 1",
    "sinkbasin 1"
  ],
  "current_inventory": "apple 3",
  "current_location": "sinkbasin 1",
  "current_objective": "clean apple",
  "thought": "",
  "action": "clean apple 3 with sinkbasin 1"
}""",
"""You clean the apple 3 using the sinkbasin 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2",
    "diningtable 3",
    "sidetable 1",
    "countertop 1",
    "sinkbasin 1",
    "garbagecan 1",
    "sinkbasin 1"
  ],
  "current_inventory": "apple 3",
  "current_location": "sinkbasin 1",
  "current_objective": "go to sidetable",
  "thought": "Now I clean an apple (3). Next, I need to put it in/on sidetable 1.",
  "action": "go to sidetable 1"
}""",
"""On the sidetable 1, you see a cup 1, a lettuce 1, a peppershaker 3, a potato 1, and a saltshaker 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some apple and put it in sidetable",
  "plan": "I need to first find an apple, then take it, then clean it with the sinkbasin, and then put it on the sidetable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "diningtable 2",
    "diningtable 3",
    "sidetable 1",
    "countertop 1",
    "sinkbasin 1",
    "garbagecan 1",
    "sinkbasin 1",
    "sidetable 1"
  ],
  "current_inventory": "apple 3",
  "current_location": "sidetable 1",
  "current_objective": "put apple in/on sidetable",
  "thought": "",
  "action": "put apple 3 in/on sidetable 1"
}"""
]



clean_v4_base_2 = ["""You are in the middle of a room. Looking quickly around you, you see a bathtubbasin 1, a garbagecan 1, a handtowelholder 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a toilet 1, a toiletpaperhanger 1, and a towelholder 1.
Your task is to: clean some soapbar and put it in toilet.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some soapbar and put it in toilet",
  "plan": "I need to first find a soapbar, then take it, then clean it with the sinkbasin, and then put it in the toilet.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find soapbar",
  "thought": "To solve the task, I need to find and take a soapbar, then clean it with sinkbasin, then put it in toilet. First I need to find a soapbar. A soapbar is more likely to appear in toilet (1), bathtubbasin (1), sinkbasin (1), shelf (1-3), garbagecan (1). I can check one by one, starting with toilet 1.",
  "action": "go to toilet 1"
}""",
"""On the toilet 1, you see a soapbar 4, and a soapbar 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some soapbar and put it in toilet",
  "plan": "I need to first find a soapbar, then take it, then clean it with the sinkbasin, and then put it in the toilet.",
  "locations_visited": [
    "toilet 1"
  ],
  "current_inventory": "",
  "current_location": "toilet 1",
  "current_objective": "take soapbar",
  "thought": "Now I find a soapbar (4). Next, I need to take it.",
  "action": "take soapbar 4 from toilet 1"
}""",
"""You pick up the soapbar 4 from the toilet 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some soapbar and put it in toilet",
  "plan": "I need to first find a soapbar, then take it, then clean it with the sinkbasin, and then put it in the toilet.",
  "locations_visited": [
    "toilet 1"
  ],
  "current_inventory": "soapbar 4",
  "current_location": "toilet 1",
  "current_objective": "go to sinkbasin",
  "thought": "Now I take a soapbar (4). Next, I need to go to sinkbasin (1) and clean it.",
  "action": "go to sinkbasin 1"
}""",
"""On the sinkbasin 1, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some soapbar and put it in toilet",
  "plan": "I need to first find a soapbar, then take it, then clean it with the sinkbasin, and then put it in the toilet.",
  "locations_visited": [
    "toilet 1",
    "sinkbasin 1"
  ],
  "current_inventory": "soapbar 4",
  "current_location": "sinkbasin 1",
  "current_objective": "clean soapbar",
  "thought": "",
  "action": "clean soapbar 4 with sinkbasin 1"
}""",
"""You clean the soapbar 4 using the sinkbasin 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some soapbar and put it in toilet",
  "plan": "I need to first find a soapbar, then take it, then clean it with the sinkbasin, and then put it in the toilet.",
  "locations_visited": [
    "toilet 1",
    "sinkbasin 1"
  ],
  "current_inventory": "soapbar 4",
  "current_location": "sinkbasin 1",
  "current_objective": "go to toilet",
  "thought": "Now I clean a soapbar (4). Next, I need to put it in/on toilet 1.",
  "action": "go to toilet 1"
}""",
"""On the toilet 1, you see a soapbar 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "clean some soapbar and put it in toilet",
  "plan": "I need to first find a soapbar, then take it, then clean it with the sinkbasin, and then put it in the toilet.",
  "locations_visited": [
    "toilet 1",
    "sinkbasin 1",
    "toilet 1"
  ],
  "current_inventory": "soapbar 4",
  "current_location": "toilet 1",
  "current_objective": "put soapbar in/on toilet",
  "thought": "",
  "action": "put soapbar 4 in/on toilet 1"
}"""
]