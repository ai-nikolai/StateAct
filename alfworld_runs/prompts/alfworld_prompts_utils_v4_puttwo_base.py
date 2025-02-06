puttwo_v4_base_0 = ["""You are in the middle of a room. Looking quickly around you, you see a armchair 2, a armchair 1, a bed 1, a countertop 1, a diningtable 1, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a laundryhamper 1, and a sidetable 1.
Your task is to: put two creditcard in dresser.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find creditcard",
  "thought": "To solve the task, I need to find and take the first creditcard, then put it in dresser, then find and take the second creditcard, then put it in dresser. First I need to find the first creditcard. A creditcard is more likely to appear in drawer (1-2), coutertop (1), sidetable (1), diningtable (1), armchair (1-2), bed (1). I can check one by one, starting with drawer 1.",
  "action": "go to drawer 1"
}""",
"""The drawer 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1"
  ],
  "current_inventory": "",
  "current_location": "drawer 1",
  "current_objective": "open drawer",
  "thought": "",
  "action": "open drawer 1"
}""",
"""You open the drawer 1. The drawer 1 is open. In it, you see a book 1, a cd 1, and a pen 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1"
  ],
  "current_inventory": "",
  "current_location": "drawer 1",
  "current_objective": "find creditcard",
  "thought": "",
  "action": "go to drawer 2"
}""",
"""The drawer 2 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1",
    "drawer 2"
  ],
  "current_inventory": "",
  "current_location": "drawer 2",
  "current_objective": "open drawer",
  "thought": "",
  "action": "open drawer 2"
}""",
"""You open the drawer 2. The drawer 2 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1",
    "drawer 2"
  ],
  "current_inventory": "",
  "current_location": "drawer 2",
  "current_objective": "find creditcard",
  "thought": "",
  "action": "go to countertop 1"
}""",
"""On the countertop 1, you see a cellphone 2, a creditcard 4, a creditcard 3, a creditcard 2, a mirror 1, a pencil 2, and a pencil 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "countertop 1"
  ],
  "current_inventory": "",
  "current_location": "countertop 1",
  "current_objective": "take creditcard",
  "thought": "Now I find the first creditcard (2). Next, I need to take it. I can find the second creditcard (3) later in countertop 1.",
  "action": "take creditcard 2 from countertop 1"
}""",
"""You pick up the creditcard 2 from the countertop 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "countertop 1"
  ],
  "current_inventory": "creditcard 2",
  "current_location": "countertop 1",
  "current_objective": "go to dresser",
  "thought": "Now I take the first creditcard (2). Next, I need to put it in/on dresser 1.",
  "action": "go to dresser 1"
}""",
"""On the dresser 1, you see a mug 1, and a television 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "countertop 1",
    "dresser 1"
  ],
  "current_inventory": "creditcard 2",
  "current_location": "dresser 1",
  "current_objective": "put creditcard in/on dresser",
  "thought": "",
  "action": "put creditcard 2 in/on dresser 1"
}""",
"""You put the creditcard 2 in/on the dresser 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "countertop 1",
    "dresser 1"
  ],
  "current_inventory": "",
  "current_location": "dresser 1",
  "current_objective": "find another creditcard",
  "thought": "Now I put the first creditcard in dresser. Next, I need to find the second creditcard. I can directly go to countertop 1.",
  "action": "go to countertop 1"
}""",
"""On the countertop 1, you see a cellphone 2, a creditcard 4, a creditcard 3, a mirror 1, a pencil 2, and a pencil 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "countertop 1",
    "dresser 1",
    "countertop 1"
  ],
  "current_inventory": "",
  "current_location": "countertop 1",
  "current_objective": "take creditcard",
  "thought": "Now I find the second creditcard (3). Next, I need to take it.",
  "action": "take creditcard 3 from countertop 1"
}""",
"""You pick up the creditcard 3 from the countertop 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "countertop 1",
    "dresser 1",
    "countertop 1"
  ],
  "current_inventory": "creditcard 3",
  "current_location": "countertop 1",
  "current_objective": "go to dresser",
  "thought": "Now I take the second creditcard (3). Next, I need to put it in/on dresser 1.",
  "action": "go to dresser 1"
}""",
"""On the dresser 1, you see a creditcard 2, a mug 1, and a television 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two creditcards in dresser",
  "plan": "I need to find the first creditcard, then take it, and then go to the dresser and put it there. Then I need to find the second creditcard, take it and go to the dresser and put in/on the dresser.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "countertop 1",
    "dresser 1",
    "countertop 1",
    "dresser 1"
  ],
  "current_inventory": "creditcard 3",
  "current_location": "dresser 1",
  "current_objective": "put creditcard in/on dresser",
  "thought": "",
  "action": "put creditcard 3 in/on dresser 1"
}"""
]

puttwo_v4_base_1 = ["""You are in the middle of a room. Looking quickly around you, you see a coffeetable 1, a diningtable 1, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a sidetable 2, a sidetable 1, and a sofa 1.
Your task is to: put two cellphone in sofa.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two cellphones in sofa",
  "plan": "I need to find the first cellphone, then take it, and then go to the sofa and put it there. Then I need to find the second cellphone, take it and go to the sofa and put in/on the sofa.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find cellphone",
  "thought": "To solve the task, I need to find and take the first cellphone, then put it in sofa, then find and take the second cellphone, then put it in sofa. First I need to find the first cellphone. A cellphone is more likely to appear in coffeetable (1), diningtable (1), sidetable (1-2), drawer (1-4), sofa (1), dresser (1), garbagecan (1). I can check one by one, starting with coffeetable 1.",
  "action": "go to coffeetable 1"
}""",
"""On the coffeetable 1, you see a box 1, a cellphone 3, and a plate 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two cellphones in sofa",
  "plan": "I need to find the first cellphone, then take it, and then go to the sofa and put it there. Then I need to find the second cellphone, take it and go to the sofa and put in/on the sofa.",
  "locations_visited": [
    "coffeetable 1"
  ],
  "current_inventory": "",
  "current_location": "coffeetable 1",
  "current_objective": "take cellphone",
  "thought": "",
  "action": "take cellphone 3 from coffeetable 1"
}""",
"""You pick up the cellphone 3 from the coffeetable 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two cellphones in sofa",
  "plan": "I need to find the first cellphone, then take it, and then go to the sofa and put it there. Then I need to find the second cellphone, take it and go to the sofa and put in/on the sofa.",
  "locations_visited": [
    "coffeetable 1"
  ],
  "current_inventory": "cellphone 3",
  "current_location": "coffeetable 1",
  "current_objective": "go to sofa",
  "thought": "Now I find the first cellphone (3). Next, I need to put it in/on sofa 1.",
  "action": "go to sofa 1"
}""",
"""On the sofa 1, you see a newspaper 2, a pillow 1, a remotecontrol 2, and a remotecontrol 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two cellphones in sofa",
  "plan": "I need to find the first cellphone, then take it, and then go to the sofa and put it there. Then I need to find the second cellphone, take it and go to the sofa and put in/on the sofa.",
  "locations_visited": [
    "coffeetable 1",
    "sofa 1"
  ],
  "current_inventory": "cellphone 3",
  "current_location": "sofa 1",
  "current_objective": "put cellphone in/on sofa",
  "thought": "",
  "action": "put cellphone 3 in/on sofa 1"
}""",
"""You put the cellphone 3 in/on the sofa 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two cellphones in sofa",
  "plan": "I need to find the first cellphone, then take it, and then go to the sofa and put it there. Then I need to find the second cellphone, take it and go to the sofa and put in/on the sofa.",
  "locations_visited": [
    "coffeetable 1",
    "sofa 1"
  ],
  "current_inventory": "",
  "current_location": "sofa 1",
  "current_objective": "find another cellphone",
  "thought": "Now I put the first cellphone in sofa. Next, I need to find the second cellphone. I have visited coffeetable (1), so the second cellphone is more likely to appear in diningtable (1), sidetable (1-2), drawer (1-4), sofa (1), dresser (1), garbagecan (1). I can check one by one, starting with coffeetable 1.",
  "action": "go to diningtable 1"
}""",
"""On the diningtable 1, you see a cellphone 2, a keychain 2, a laptop 1, a statue 2, and a statue 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two cellphones in sofa",
  "plan": "I need to find the first cellphone, then take it, and then go to the sofa and put it there. Then I need to find the second cellphone, take it and go to the sofa and put in/on the sofa.",
  "locations_visited": [
    "coffeetable 1",
    "sofa 1",
    "diningtable 1"
  ],
  "current_inventory": "",
  "current_location": "diningtable 1",
  "current_objective": "take cellphone",
  "thought": "Now I find the second cellphone (2). Next, I need to take it.",
  "action": "take cellphone 2 from diningtable 1"
}""",
"""You pick up the cellphone 2 from the diningtable 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two cellphones in sofa",
  "plan": "I need to find the first cellphone, then take it, and then go to the sofa and put it there. Then I need to find the second cellphone, take it and go to the sofa and put in/on the sofa.",
  "locations_visited": [
    "coffeetable 1",
    "sofa 1",
    "diningtable 1"
  ],
  "current_inventory": "cellphone 2",
  "current_location": "diningtable 1",
  "current_objective": "go to sofa",
  "thought": "Now I take the second cellphone (2). Next, I need to put it in/on sofa 1.",
  "action": "go to sofa 1"
}""",
"""On the sofa 1, you see a cellphone 3, a newspaper 2, a pillow 1, a remotecontrol 2, and a remotecontrol 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two cellphones in sofa",
  "plan": "I need to find the first cellphone, then take it, and then go to the sofa and put it there. Then I need to find the second cellphone, take it and go to the sofa and put in/on the sofa.",
  "locations_visited": [
    "coffeetable 1",
    "sofa 1",
    "diningtable 1",
    "sofa 1"
  ],
  "current_inventory": "cellphone 2",
  "current_location": "sofa 1",
  "current_objective": "put cellphone in/on sofa",
  "thought": "",
  "action": "put cellphone 2 in/on sofa 1"
}"""
]

puttwo_v4_base_2 = ["""You are in the middle of a room. Looking quickly around you, you see a cabinet 20, a cabinet 19, a cabinet 18, a cabinet 17, a cabinet 16, a cabinet 15, a cabinet 14, a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put two saltshaker in drawer.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find saltshaker",
  "thought": "To solve the task, I need to find and take the first saltshaker, then put it in drawer, then find and take the second salkshaker, then put it in drawer. First I need to find the first saltshaker. A saltshaker is more likely to appear in drawer (1-3), countertop (1-3), shelf (1-3), cabinet (1-20). I can check one by one, starting with drawer 1.",
  "action": "go to drawer 1"
}""",
"""The drawer 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1"
  ],
  "current_inventory": "",
  "current_location": "drawer 1",
  "current_objective": "find saltshaker",
  "thought": "",
  "action": "open drawer 1"
}""",
"""You open the drawer 1. The drawer 1 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1"
  ],
  "current_inventory": "",
  "current_location": "drawer 1",
  "current_objective": "find saltshaker",
  "thought": "",
  "action": "go to drawer 2"
}""",
"""The drawer 2 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2"
  ],
  "current_inventory": "",
  "current_location": "drawer 2",
  "current_objective": "find saltshaker",
  "thought": "",
  "action": "open drawer 2"
}""",
"""You open the drawer 2. The drawer 2 is open. In it, you see a dishsponge 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2"
  ],
  "current_inventory": "",
  "current_location": "drawer 2",
  "current_objective": "find saltshaker",
  "thought": "",
  "action": "go to drawer 3"
}""",
"""The drawer 3 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3"
  ],
  "current_inventory": "",
  "current_location": "drawer 3",
  "current_objective": "find saltshaker",
  "thought": "",
  "action": "open drawer 3"
}""",
"""You open the drawer 3. The drawer 3 is open. In it, you see a fork 2, a ladle 2, and a spoon 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3"
  ],
  "current_inventory": "",
  "current_location": "drawer 3",
  "current_objective": "find saltshaker",
  "thought": "",
  "action": "go to countertop 1"
}""",
"""On the countertop 1, you see a bowl 1, a butterknife 1, a mug 2, a pan 1, a papertowelroll 1, a spatula 1, and a statue 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1"
  ],
  "current_inventory": "",
  "current_location": "countertop 1",
  "current_objective": "find saltshaker",
  "thought": "",
  "action": "go to countertop 2"
}""",
"""On the countertop 2, you see a bread 1, a butterknife 2, a dishsponge 2, a fork 1, a kettle 1, a knife 1, a ladle 1, a spatula 3, a spoon 2, a statue 2, and a vase 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2"
  ],
  "current_inventory": "",
  "current_location": "countertop 2",
  "current_objective": "find saltshaker",
  "thought": "",
  "action": "go to countertop 3"
}""",
"""On the countertop 3, you see a bowl 2, a houseplant 1, a knife 2, a peppershaker 1, a saltshaker 4, a soapbottle 1, a spatula 2, and a tomato 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3"
  ],
  "current_inventory": "",
  "current_location": "countertop 3",
  "current_objective": "take saltshaker",
  "thought": "Now I find the first saltshaker (4). Next, I need to take it.",
  "action": "take saltshaker 4 from countertop 3"
}""",
"""You pick up the saltshaker 4 from the countertop 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3"
  ],
  "current_inventory": "saltshaker 4",
  "current_location": "countertop 3",
  "current_objective": "go to drawer",
  "thought": "Now I take the first saltshaker (4). Next, I need to put it in/on drawer 1.",
  "action": "go to drawer 1"
}""",
"""The drawer 1 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1"
  ],
  "current_inventory": "saltshaker 4",
  "current_location": "drawer 1",
  "current_objective": "put saltshaker in/on drawer",
  "thought": "",
  "action": "put saltshaker 4 in/on drawer 1"
}""",
"""You put the saltshaker 4 in/on the drawer 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1"
  ],
  "current_inventory": "",
  "current_location": "drawer 1",
  "current_objective": "find another saltshaker",
  "thought": "Now I put the first saltshaker in drawer. Next, I need to find the second saltshaker. I have visited drawer (1-3), countertop (1-3), so the second saltshaker is more likely to appear in shelf (1-3), cabinet (1-20). I can check one by one, starting with shelf 1.",
  "action": "go to shelf 1"
}""",
"""On the shelf 1, you see a statue 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1"
  ],
  "current_inventory": "",
  "current_location": "shelf 1",
  "current_objective": "find another saltshaker",
  "thought": "",
  "action": "go to shelf 2"
}""",
"""On the shelf 2, you see a dishsponge 1, and a vase 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2"
  ],
  "current_inventory": "",
  "current_location": "shelf 2",
  "current_objective": "find another saltshaker",
  "thought": "",
  "action": "go to shelf 3"
}""",
"""On the shelf 3, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2",
    "shelf 3"
  ],
  "current_inventory": "",
  "current_location": "shelf 3",
  "current_objective": "find another saltshaker",
  "thought": "",
  "action": "go to cabinet 1"
}""",
"""The cabinet 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2",
    "shelf 3",
    "cabinet 1"
  ],
  "current_inventory": "",
  "current_location": "cabinet 1",
  "current_objective": "find another saltshaker",
  "thought": "",
  "action": "open cabinet 1"
}""",
"""You open the cabinet 1. The cabinet 1 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2",
    "shelf 3",
    "cabinet 1"
  ],
  "current_inventory": "",
  "current_location": "cabinet 1",
  "current_objective": "find another saltshaker",
  "thought": "",
  "action": "go to cabinet 2"
}""",
"""Nothing happens.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2",
    "shelf 3",
    "cabinet 1",
    "cabinet 2"
  ],
  "current_inventory": "",
  "current_location": "cabinet 2",
  "current_objective": "find another saltshaker",
  "thought": "",
  "action": "look"
}""",
"""You are facing the cabinet 2, and cabinet 1. Next to it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2",
    "shelf 3",
    "cabinet 1",
    "cabinet 2"
  ],
  "current_inventory": "",
  "current_location": "cabinet 2",
  "current_objective": "find another saltshaker",
  "thought": "",
  "action": "go to cabinet 3"
}""",
"""The cabinet 3 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2",
    "shelf 3",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3"
  ],
  "current_inventory": "",
  "current_location": "cabinet 3",
  "current_objective": "find another saltshaker",
  "thought": "",
  "action": "open cabinet 3"
}""",
"""You open the cabinet 3. The cabinet 3 is open. In it, you see a saltshaker 3, and a saltshaker 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2",
    "shelf 3",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3"
  ],
  "current_inventory": "",
  "current_location": "cabinet 3",
  "current_objective": "take saltshaker",
  "thought": "Now I find the second saltshaker (2). Next, I need to take it.",
  "action": "take saltshaker 2 from cabinet 3"
}""",
"""You pick up the saltshaker 2 from the cabinet 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2",
    "shelf 3",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3"
  ],
  "current_inventory": "saltshaker 2",
  "current_location": "cabinet 3",
  "current_objective": "go to drawer",
  "thought": "Now I take the second saltshaker (2). Next, I need to put it in/on drawer 1.",
  "action": "go to drawer 1"
}""",
"""The drawer 1 is open. In it, you see a saltshaker 4.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "put two saltshaker in drawer",
  "plan": "I need to find the first saltshaker, then take it, and then go to the drawer and put it there. Then I need to find the second saltshaker, take it and go to the drawer and put in/on the drawer.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "countertop 1",
    "countertop 2",
    "countertop 3",
    "drawer 1",
    "shelf 1",
    "shelf 2",
    "shelf 3",
    "cabinet 1",
    "cabinet 2",
    "cabinet 3",
    "drawer 1"
  ],
  "current_inventory": "saltshaker 2",
  "current_location": "drawer 1",
  "current_objective": "put saltshaker in/on drawer",
  "thought": "",
  "action": "put saltshaker 2 in/on drawer 1"
}"""
]
