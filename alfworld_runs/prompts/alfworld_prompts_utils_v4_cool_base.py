cool_v4_base_0 = ["""You are in the middle of a room. Looking quickly around you, you see a cabinet 16, a cabinet 15, a cabinet 14, a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 2, a countertop 1, a diningtable 1, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a safe 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: cool some pan and put it in stoveburner.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some pan and put it in stoveburner",
  "plan": "I need to first find a pan, then take it, then go to the fridge and cool the pan and then go to the stoveburner and put the pan in/on the stoveburner.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find pan",
  "thought": "To solve the task, I need to find and take a pan, then cool it with fridge, then put it in stoveburner. First I need to find a pan. An pan is more likely to appear in stoveburner (1-4), sinkbasin (1), diningtable (1), countertop (1-2), cabinet (1-16), drawer (1-5). I can check one by one, starting with stoveburner 1.",
  "action": "go to stoveburner 1"
}""",
"""On the stoveburner 1, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some pan and put it in stoveburner",
  "plan": "I need to first find a pan, then take it, then go to the fridge and cool the pan and then go to the stoveburner and put the pan in/on the stoveburner.",
  "locations_visited": [
    "stoveburner 1"
  ],
  "current_inventory": "",
  "current_location": "stoveburner 1",
  "current_objective": "find pan",
  "thought": "",
  "action": "go to stoveburner 2"
}""",
"""On the stoveburner 2, you see a pot 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some pan and put it in stoveburner",
  "plan": "I need to first find a pan, then take it, then go to the fridge and cool the pan and then go to the stoveburner and put the pan in/on the stoveburner.",
  "locations_visited": [
    "stoveburner 1",
    "stoveburner 2"
  ],
  "current_inventory": "",
  "current_location": "stoveburner 2",
  "current_objective": "find pan",
  "thought": "",
  "action": "go to stoveburner 3"
}""",
"""On the stoveburner 3, you see a pan 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some pan and put it in stoveburner",
  "plan": "I need to first find a pan, then take it, then go to the fridge and cool the pan and then go to the stoveburner and put the pan in/on the stoveburner.",
  "locations_visited": [
    "stoveburner 1",
    "stoveburner 2",
    "stoveburner 3"
  ],
  "current_inventory": "",
  "current_location": "stoveburner 3",
  "current_objective": "take pan",
  "thought": "Now I find a pan (1). Next, I need to take it.",
  "action": "take pan 1 from stoveburner 3"
}""",
"""You pick up the pan 1 from the stoveburner 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some pan and put it in stoveburner",
  "plan": "I need to first find a pan, then take it, then go to the fridge and cool the pan and then go to the stoveburner and put the pan in/on the stoveburner.",
  "locations_visited": [
    "stoveburner 1",
    "stoveburner 2",
    "stoveburner 3"
  ],
  "current_inventory": "pan 1",
  "current_location": "stoveburner 3",
  "current_objective": "go to fridge",
  "thought": "Now I take a pan (1). Next, I need to go to a fridge (1) and cool it.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some pan and put it in stoveburner",
  "plan": "I need to first find a pan, then take it, then go to the fridge and cool the pan and then go to the stoveburner and put the pan in/on the stoveburner.",
  "locations_visited": [
    "stoveburner 1",
    "stoveburner 2",
    "stoveburner 3",
    "fridge 1"
  ],
  "current_inventory": "pan 1",
  "current_location": "fridge 1",
  "current_objective": "cool pan",
  "thought": "",
  "action": "cool pan 1 with fridge 1"
}""",
"""You cool the pan 1 using the fridge 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some pan and put it in stoveburner",
  "plan": "I need to first find a pan, then take it, then go to the fridge and cool the pan and then go to the stoveburner and put the pan in/on the stoveburner.",
  "locations_visited": [
    "stoveburner 1",
    "stoveburner 2",
    "stoveburner 3",
    "fridge 1"
  ],
  "current_inventory": "pan 1",
  "current_location": "fridge 1",
  "current_objective": "go to stoveburner",
  "thought": "Now I cool a pan (1). Next, I need to put it in/on stoveburner 1.",
  "action": "go to stoveburner 1"
}""",
"""On the stoveburner 1, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some pan and put it in stoveburner",
  "plan": "I need to first find a pan, then take it, then go to the fridge and cool the pan and then go to the stoveburner and put the pan in/on the stoveburner.",
  "locations_visited": [
    "stoveburner 1",
    "stoveburner 2",
    "stoveburner 3",
    "fridge 1",
    "stoveburner 1"
  ],
  "current_inventory": "pan 1",
  "current_location": "stoveburner 1",
  "current_objective": "put pan in/on stoveburner",
  "thought": "",
  "action": "put pan 1 in/on stoveburner 1"
}"""
]

cool_v4_base_1 = ["""You are in the middle of a room. Looking quickly around you, you see a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a cool mug in shelf.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find mug",
  "thought": "To solve the task, I need to find and take a mug, then cool it with fridge, then put it in shelf. First I need to find a mug. A mug is more likely to appear in countertop (1-3), coffeemachine (1), cabinet (1-9), shelf (1-3), drawer (1-9). I can check one by one, starting with countertop 1.",
  "action": "go to countertop 1"
}""",
"""On the countertop 1, you see a knife 1, a pan 2, a pan 1, and a plate 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1"
  ],
  "current_inventory": "",
  "current_location": "countertop 1",
  "current_objective": "find mug",
  "thought": "",
  "action": "go to countertop 2"
}""",
"""On the countertop 2, you see a apple 2, a butterknife 2, a fork 3, a houseplant 1, a knife 2, a lettuce 3, a spatula 1, and a winebottle 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2"
  ],
  "current_inventory": "",
  "current_location": "countertop 2",
  "current_objective": "find mug",
  "thought": "",
  "action": "go to countertop 3"
}""",
"""On the countertop 3, you see a apple 1, a book 1, a bread 1, a butterknife 3, a glassbottle 2, a glassbottle 1, a knife 3, a lettuce 2, a lettuce 1, a papertowelroll 1, a plate 3, a spoon 1, a statue 1, and a vase 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3"
  ],
  "current_inventory": "",
  "current_location": "countertop 3",
  "current_objective": "find mug",
  "thought": "",
  "action": "go to coffeemachine 1"
}""",
"""On the coffeemachine 1, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1"
  ],
  "current_inventory": "",
  "current_location": "coffeemachine 1",
  "current_objective": "find mug",
  "thought": "",
  "action": "go to cabinet 1"
}""",
"""The cabinet 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1"
  ],
  "current_inventory": "",
  "current_location": "cabinet 1",
  "current_objective": "find mug",
  "thought": "",
  "action": "open cabinet 1"
}""",
"""You open the cabinet 1. The cabinet 1 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1"
  ],
  "current_inventory": "",
  "current_location": "cabinet 1",
  "current_objective": "find mug",
  "thought": "",
  "action": "go to cabinet 2"
}""",
"""The cabinet 2 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2"
  ],
  "current_inventory": "",
  "current_location": "cabinet 2",
  "current_objective": "find mug",
  "thought": "",
  "action": "open cabinet 2"
}""",
"""You open the cabinet 2. The cabinet 2 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2"
  ],
  "current_inventory": "",
  "current_location": "cabinet 2",
  "current_objective": "find mug",
  "thought": "",
  "action": "go to cabinet 3"
}""",
"""The cabinet 3 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3"
  ],
  "current_inventory": "",
  "current_location": "cabinet 3",
  "current_objective": "find mug",
  "thought": "",
  "action": "open cabinet 3"
}""",
"""You open the cabinet 3. The cabinet 3 is open. In it, you see a pot 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3"
  ],
  "current_inventory": "",
  "current_location": "cabinet 3",
  "current_objective": "find mug",
  "thought": "",
  "action": "go to cabinet 4"
}""",
"""On the cabinet 4, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "cabinet 4"
  ],
  "current_inventory": "",
  "current_location": "cabinet 4",
  "current_objective": "find mug",
  "thought": "",
  "action": "go to cabinet 5"
}""",
"""The cabinet 5 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "cabinet 4",
    "cabinet 5"
  ],
  "current_inventory": "",
  "current_location": "cabinet 5",
  "current_objective": "find mug",
  "thought": "",
  "action": "open cabinet 5"
}""",
"""You open the cabinet 5. The cabinet 5 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "cabinet 4",
    "cabinet 5"
  ],
  "current_inventory": "",
  "current_location": "cabinet 5",
  "current_objective": "find mug",
  "thought": "",
  "action": "go to cabinet 6"
}""",
"""The cabinet 6 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "cabinet 4",
    "cabinet 5",
    "cabinet 6"
  ],
  "current_inventory": "",
  "current_location": "cabinet 6",
  "current_objective": "find mug",
  "thought": "",
  "action": "open cabinet 6"
}""",
"""You open the cabinet 6. The cabinet 6 is open. In it, you see a mug 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "cabinet 4",
    "cabinet 5",
    "cabinet 6"
  ],
  "current_inventory": "",
  "current_location": "cabinet 6",
  "current_objective": "take mug",
  "thought": "Now I find a mug (3). Next, I need to take it.",
  "action": "take mug 3 from cabinet 6"
}""",
"""You pick up the mug 3 from the cabinet 6.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "cabinet 4",
    "cabinet 5",
    "cabinet 6"
  ],
  "current_inventory": "mug 3",
  "current_location": "cabinet 6",
  "current_objective": "go to fridge",
  "thought": "Now I take a mug (3). Next, I need to go to a fridge (1) and cool it.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "cabinet 4",
    "cabinet 5",
    "cabinet 6",
    "fridge 1"
  ],
  "current_inventory": "mug 3",
  "current_location": "fridge 1",
  "current_objective": "cool mug",
  "thought": "",
  "action": "cool mug 3 with fridge 1"
}""",
"""You cool the mug 3 using the fridge 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "cabinet 4",
    "cabinet 5",
    "cabinet 6",
    "fridge 1"
  ],
  "current_inventory": "mug 3",
  "current_location": "fridge 1",
  "current_objective": "go to shelf",
  "thought": "Now I cool the mug. Next, I need to put it in/on shelf 1.",
  "action": "go to shelf 1"
}""",
"""On the shelf 1, you see a cup 2, a cup 1, a peppershaker 1, and a saltshaker 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put a cool mug in shelf",
  "plan": "I need to first find a mug, then take it, then go to the fridge and cool the mug and then go to the shelf and put the mug in/on the shelf.",
  "locations_visited": [
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "coffeemachine 1",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "cabinet 4",
    "cabinet 5",
    "cabinet 6",
    "fridge 1",
    "shelf 1"
  ],
  "current_inventory": "mug 3",
  "current_location": "shelf 1",
  "current_objective": "put mug in/on shelf",
  "thought": "",
  "action": "put mug 3 in/on shelf 1"
}"""
]

cool_v4_base_2 = ["""You are in the middle of a room. Looking quickly around you, you see a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 2, a countertop 1, a diningtable 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: cool some potato and put it in diningtable.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some potato and put it in diningtable",
  "plan": "First, I need to find a potato, then take it, then cool it using the fridge, and finally put it on the diningtable.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find potato",
  "thought": "To solve the task, I need to find and take a potato, then cool it with fridge, then put it in diningtable. First I need to find a potato. A potato is more likely to appear in fridge (1), diningtable (1), countertop (1-2), cabinet (1-12), drawer (1-3), garbagecan (1). I can check one by one, starting with fridge 1.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some potato and put it in diningtable",
  "plan": "First, I need to find a potato, then take it, then cool it using the fridge, and finally put it on the diningtable.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find potato",
  "thought": "",
  "action": "open fridge 1"
}""",
"""You open the fridge 1. The fridge 1 is open. In it, you see a apple 1, a bowl 1, a lettuce 2, and a lettuce 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some potato and put it in diningtable",
  "plan": "First, I need to find a potato, then take it, then cool it using the fridge, and finally put it on the diningtable.",
  "locations_visited": [
    "fridge 1"
  ],
  "current_inventory": "",
  "current_location": "fridge 1",
  "current_objective": "find potato",
  "thought": "",
  "action": "go to diningtable 1"
}""",
"""On the diningtable 1, you see a apple 3, a bread 1, a butterknife 3, a egg 2, a fork 1, a knife 2, a knife 1, a mug 1, a peppershaker 3, a plate 1, a potato 4, a potato 2, a saltshaker 2, a soapbottle 2, and a tomato 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some potato and put it in diningtable",
  "plan": "First, I need to find a potato, then take it, then cool it using the fridge, and finally put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1"
  ],
  "current_inventory": "",
  "current_location": "diningtable 1",
  "current_objective": "take potato",
  "thought": "Now I find a potato (2). Next, I need to take it.",
  "action": "take potato 2 from diningtable 1"
}""",
"""You pick up the potato 2 from the diningtable 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some potato and put it in diningtable",
  "plan": "First, I need to find a potato, then take it, then cool it using the fridge, and finally put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1"
  ],
  "current_inventory": "potato 2",
  "current_location": "diningtable 1",
  "current_objective": "go to fridge",
  "thought": "Now I take a potato (2). Next, I need to go to a fridge (1) and cool it.",
  "action": "go to fridge 1"
}""",
"""The fridge 1 is open. In it, you see a apple 1, a bowl 1, a lettuce 2, and a lettuce 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some potato and put it in diningtable",
  "plan": "First, I need to find a potato, then take it, then cool it using the fridge, and finally put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "fridge 1"
  ],
  "current_inventory": "potato 2",
  "current_location": "fridge 1",
  "current_objective": "cool potato",
  "thought": "",
  "action": "cool potato 2 with fridge 1"
}""",
"""You cool the potato 2 using the fridge 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some potato and put it in diningtable",
  "plan": "First, I need to find a potato, then take it, then cool it using the fridge, and finally put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "fridge 1"
  ],
  "current_inventory": "potato 2",
  "current_location": "fridge 1",
  "current_objective": "go to diningtable",
  "thought": "Now I cool a potato (2). Next, I need to put it in/on diningtable 1.",
  "action": "go to diningtable 1"
}""",
"""On the diningtable 1, you see a apple 3, a bread 1, a butterknife 3, a egg 2, a fork 1, a knife 2, a knife 1, a mug 1, a peppershaker 3, a plate 1, a potato 4, a saltshaker 2, a soapbottle 2, and a tomato 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "cool some potato and put it in diningtable",
  "plan": "First, I need to find a potato, then take it, then cool it using the fridge, and finally put it on the diningtable.",
  "locations_visited": [
    "fridge 1",
    "diningtable 1",
    "fridge 1",
    "diningtable 1"
  ],
  "current_inventory": "potato 2",
  "current_location": "diningtable 1",
  "current_objective": "put potato in/on diningtable",
  "thought": "",
  "action": "put potato 2 in/on diningtable 1"
}"""
]