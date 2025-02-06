heat_v4_base_0 = ["""You are in the middle of a room. Looking quickly around you, you see a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a diningtable 1, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: heat some egg and put it in diningtable.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find egg",
  "thought": "To solve the task, I need to find and take an egg, then heat it with microwave, then put it in diningtable. First I need to find an egg. An egg is more likely to appear in fridge (1), countertop (1-3), diningtable (1), stoveburner (1-4), toaster (1), garbagecan (1), cabinet (1-10). I can check one by one, starting with fridge 1.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find egg",
  "thought": "",
  "action": "open fridge 1"
}""",
"""You open the fridge 1. The fridge 1 is open. In it, you see a lettuce 2, a mug 2, and a potato 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find egg",
  "thought": "",
  "action": "go to countertop 1"
}""",
"""On the countertop 1, you see a bread 1, a fork 1, and a saltshaker 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [
    "fridge 1",
    "countertop 1"
  ],
  "current_inventory": "",
  "current_location": "countertop 1",
  "current_objective": "find egg",
  "thought": "",
  "action": "go to countertop 2"
}""",
"""On the countertop 2, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [
    "fridge 1",
    "countertop 1",
    "countertop 2"
  ],
  "current_inventory": "",
  "current_location": "countertop 2",
  "current_objective": "find egg",
  "thought": "",
  "action": "go to countertop 3"
}""",
"""On the countertop 3, you see a bowl 1, a butterknife 1, a egg 2, a kettle 2, a plate 1, a sink 1, and a spatula 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [
    "fridge 1",
    "countertop 1",
    "countertop 2",
    "countertop 3"
  ],
  "current_inventory": "",
  "current_location": "countertop 3",
  "current_objective": "take egg",
  "thought": "Now I find an egg (2). Next, I need to take it.",
  "action": "take egg 2 from countertop 3"
}""",
"""You pick up the egg 2 from the countertop 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [
    "fridge 1",
    "countertop 1",
    "countertop 2",
    "countertop 3"
  ],
  "current_inventory": "egg 2",
  "current_location": "countertop 3",
  "current_objective": "go to microwave",
  "thought": "Now I take an egg (2). Next, I need go to a microwave (1) and heat it.",
  "action": "go to microwave 1"
}""",
"""The microwave 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [
    "fridge 1",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "microwave 1"
  ],
  "current_inventory": "egg 2",
  "current_location": "microwave 1",
  "current_objective": "heat egg",
  "thought": "",
  "action": "heat egg 2 with microwave 1"
}""",
"""You heat the egg 2 using the microwave 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [
    "fridge 1",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "microwave 1"
  ],
  "current_inventory": "egg 2",
  "current_location": "microwave 1",
  "current_objective": "go to diningtable",
  "thought": "Now I heat an egg (2). Next, I need to put it in/on diningtable 1.",
  "action": "go to diningtable 1"
}""",
"""On the diningtable 1, you see a apple 2, a bread 3, a egg 1, a kettle 1, a knife 1, a mug 1, a papertowelroll 1, a peppershaker 2, a potato 1, a soapbottle 1, and a spatula 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some egg and put it in diningtable",
  "plan": "I need to first find an egg, then take it, then heat it in the microwave, then go to the diningtable and put the heated egg on it.",
  "locations_visited": [
    "fridge 1",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "microwave 1",
    "diningtable 1"
  ],
  "current_inventory": "egg 2",
  "current_location": "diningtable 1",
  "current_objective": "put egg in/on diningtable",
  "thought": "",
  "action": "put egg 2 in/on diningtable 1"
}"""
]

heat_v4_base_1 = ["""You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a hot apple in fridge.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a hot apple in fridge",
  "plan": "I need to first find an apple, then take it, then heat it in the microwave, then go to the fridge and put the hot apple in/on the fridge.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find apple",
  "thought": "To solve the task, I need to find and take an apple, then heat it with microwave, then put it in fridge. First I need to find an apple. An apple is more likely to appear in fridge (1), diningtable (1), coffeetable (1), drawer (1), cabinet (1-13), garbagecan (1). I can check one by one, starting with fridge 1.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a hot apple in fridge",
  "plan": "I need to first find an apple, then take it, then heat it in the microwave, then go to the fridge and put the hot apple in/on the fridge.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find apple",
  "thought": "",
  "action": "open fridge 1"
}""",
"""You open the fridge 1. The fridge 1 is open. In it, you see a cup 1, and a egg 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a hot apple in fridge",
  "plan": "I need to first find an apple, then take it, then heat it in the microwave, then go to the fridge and put the hot apple in/on the fridge.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find apple",
  "thought": "",
  "action": "go to diningtable 1"
}""",
"""On the diningtable 1, you see a apple 1, a bread 1, a fork 3, a fork 2, a fork 1, a mug 2, a peppershaker 3, a plate 2, a pot 1, a soapbottle 3, a spatula 1, a spoon 3, a spoon 2, a spoon 1, a winebottle 3, and a winebottle 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a hot apple in fridge",
  "plan": "I need to first find an apple, then take it, then heat it in the microwave, then go to the fridge and put the hot apple in/on the fridge.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1"
  ],
  "current_inventory": "",
  "current_location": "diningtable 1",
  "current_objective": "take apple",
  "thought": "Now I find an apple (1). Next, I need to take it.",
  "action": "take apple 1 from diningtable 1"
}""",
"""You pick up the apple 1 from the diningtable 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a hot apple in fridge",
  "plan": "I need to first find an apple, then take it, then heat it in the microwave, then go to the fridge and put the hot apple in/on the fridge.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1"
  ],
  "current_inventory": "apple 1",
  "current_location": "diningtable 1",
  "current_objective": "go to microwave",
  "thought": "Now I take an apple (1). Next, I need to go to a microwave (1) and heat it.",
  "action": "go to microwave 1"
}""",
"""The microwave 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a hot apple in fridge",
  "plan": "I need to first find an apple, then take it, then heat it in the microwave, then go to the fridge and put the hot apple in/on the fridge.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "microwave 1"
  ],
  "current_inventory": "apple 1",
  "current_location": "microwave 1",
  "current_objective": "heat apple",
  "thought": "",
  "action": "heat apple 1 with microwave 1"
}""",
"""You heat the apple 1 using the microwave 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a hot apple in fridge",
  "plan": "I need to first find an apple, then take it, then heat it in the microwave, then go to the fridge and put the hot apple in/on the fridge.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "microwave 1"
  ],
  "current_inventory": "apple 1",
  "current_location": "microwave 1",
  "current_objective": "go to fridge",
  "thought": "Now I heat an apple (1). Next, I need to put it in/on fridge 1.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is open. In it, you see a cup 1, and a egg 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a hot apple in fridge",
  "plan": "I need to first find an apple, then take it, then heat it in the microwave, then go to the fridge and put the hot apple in/on the fridge.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "microwave 1",
    "fridge 1"
  ],
 "current_inventory": "apple 1",
  "current_location": "fridge 1",
  "current_objective": "put apple in/on fridge",
  "thought": "",
  "action": "put apple 1 in/on fridge 1"
}"""
]

heat_v4_base_2 = ["""You are in the middle of a room. Looking quickly around you, you see a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 2, a countertop 1, a diningtable 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: heat some bread and put it in countertop.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some bread and put it in countertop",
  "plan": "I need to first find some bread, then heat it using either a toaster or a microwave, and then put it on the countertop.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find bread",
  "thought": "To solve the task, I need to find and take a bread, then heat it with microwave, then put it in countertop. First I need to find a bread. A bread is more likely to appear in fridge (1), toaster (1), diningtable (1), countertop (1-2), drawer (1-3), cabinet (1-10). I can check one by one, starting with fridge 1.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some bread and put it in countertop",
  "plan": "I need to first find some bread, then heat it using either a toaster or a microwave, and then put it on the countertop.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find bread",
  "thought": "",
  "action": "open fridge 1"
}""",
"""You open the fridge 1. The fridge 1 is open. In it, you see a mug 3, and a mug 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some bread and put it in countertop",
  "plan": "I need to first find some bread, then heat it using either a toaster or a microwave, and then put it on the countertop.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find bread",
  "thought": "",
  "action": "go to toaster 1"
}""",
"""On the toaster 1, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some bread and put it in countertop",
  "plan": "I need to first find some bread, then heat it using either a toaster or a microwave, and then put it on the countertop.",
  "locations_visited": [
    "fridge 1",
    "toaster 1"
  ],
  "current_inventory": "",
  "current_location": "toaster 1",
  "current_objective": "find bread",
  "thought": "",
  "action": "go to diningtable 1"
}""",
"""On the diningtable 1, you see a bread 4, a bread 3, a bread 2, a bread 1, a cup 2, a knife 1, a lettuce 1, a potato 3, a tomato 3, a tomato 2, and a winebottle 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some bread and put it in countertop",
  "plan": "I need to first find some bread, then heat it using either a toaster or a microwave, and then put it on the countertop.",
  "locations_visited": [
    "fridge 1",
    "toaster 1",
    "diningtable 1"
  ],
  "current_inventory": "",
  "current_location": "diningtable 1",
  "current_objective": "take bread",
  "thought": "Now I find a bread (1). Next, I need to take it.",
  "action": "take bread 1 from diningtable 1"
}""",
"""You pick up the bread 1 from the diningtable 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some bread and put it in countertop",
  "plan": "I need to first find some bread, then heat it using either a toaster or a microwave, and then put it on the countertop.",
  "locations_visited": [
    "fridge 1",
    "toaster 1",
    "diningtable 1"
  ],
  "current_inventory": "bread 1",
  "current_location": "diningtable 1",
  "current_objective": "go to microwave",
  "thought": "Now I take a bread (1). Next, I need to go to a microwave (1) and heat it.",
  "action": "go to microwave 1"
}""",
"""The microwave 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some bread and put it in countertop",
  "plan": "I need to first find some bread, then heat it using either a toaster or a microwave, and then put it on the countertop.",
  "locations_visited": [
    "fridge 1",
    "toaster 1",
    "diningtable 1",
    "microwave 1"
  ],
  "current_inventory": "bread 1",
  "current_location": "microwave 1",
  "current_objective": "heat bread",
  "thought": "",
  "action": "heat bread 1 with microwave 1"
}""",
"""You heat the bread 1 using the microwave 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some bread and put it in countertop",
  "plan": "I need to first find some bread, then heat it using either a toaster or a microwave, and then put it on the countertop.",
  "locations_visited": [
    "fridge 1",
    "toaster 1",
    "diningtable 1",
    "microwave 1"
  ],
  "current_inventory": "bread 1",
  "current_location": "microwave 1",
  "current_objective": "go to countertop",
  "thought": "Now I heat a bread (1). Next, I need to put it in/on countertop 1.",
  "action": "go to countertop 1"
}""",
"""On the countertop 1, you see a apple 1, a egg 1, a pan 2, a peppershaker 3, a plate 2, a plate 1, a soapbottle 1, and a winebottle 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "heat some bread and put it in countertop",
  "plan": "I need to first find some bread, then heat it using either a toaster or a microwave, and then put it on the countertop.",
  "locations_visited": [
    "fridge 1",
    "toaster 1",
    "diningtable 1",
    "microwave 1",
    "countertop 1"
  ],
  "current_inventory": "bread 1",
  "current_location": "countertop 1",
  "current_objective": "put bread in/on countertop",
  "thought": "",
  "action": "put bread 1 in/on countertop 1"
}"""
]