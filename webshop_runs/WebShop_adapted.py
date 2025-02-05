#!/usr/bin/env python
# coding: utf-8

# # Setup

# In[1]:


import os
import anthropic
import sys


USE_GPT = True

GPT_MODEL = "gpt-3.5-turbo-instruct"
LLM_TYPE="NORMAL"

# GPT_MODEL = "gpt-3.5-turbo-0125"
# GPT_MODEL = "gpt-3.5-turbo-1106"
# GPT_MODEL = "gpt-4-0613"
# GPT_MODEL = "gpt-3.5-turbo"
# LLM_TYPE="CHAT"

MAX_PROMPT_LENGTH=6400


CLAUDE_MODEL="claude-3-5-sonnet-latest"

# LLM_TYPE="CHAT"
# GPT_MODEL = "gpt-3.5-turbo-1106"
# GPT_MODEL = "gpt-4o"
# GPT_MODEL = "gpt-4o-mini"
# MAX_PROMPT_LENGTH=128000

if USE_GPT:
  print(f"USING OPENAI:{GPT_MODEL} of type: {LLM_TYPE}")
  import openai
  openai.api_key = os.environ["OPENAI_API_KEY"]
  client = openai.OpenAI()
  MODEL = GPT_MODEL

else:
  print(f"USING ANTHROPIC: {CLAUDE_MODEL}")
  import anthropic
  client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
  LLM_TYPE="TROPIC"
  MODEL = CLAUDE_MODEL

def llm(prompt, stop=["\n"]):
    # MODEL = MODEL
    # response = openai.Completion.create(
    response = client.completions.create(
      # model="text-davinci-002",
      model=MODEL,
      prompt=prompt,
      temperature=0,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=stop
    )
    # return response["choices"][0]["text"]
    return response.choices[0].text


def llm_chat(prompt, stop=["\n"]):
    # MODEL = MODEL
    # MODEL = "gpt-4-turbo-preview"
    chat_prompt = [
            {
                "role": "system", 
                "content": prompt
            }
        ]
    response = client.chat.completions.create(
      model=MODEL,
      messages=chat_prompt,
      temperature=0,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=stop
    )
    # return response["choices"][0]["text"]
    return response.choices[0].message.content

def llm_tropic(prompt, stop=["\n"]):
  chat_prompt = [
          {
              "role": "user", 
              "content": prompt
          }
      ]
  response = client.messages.create(
    model=MODEL,
    max_tokens = 500,
    temperature = 0,
    top_p=1,
    # frequency_penalty=0.0,
    # presence_penalty=0.0,
    stop_sequences=stop,
    messages = chat_prompt
  )
  return response.content[0].text

# In[2]:

if LLM_TYPE=="NORMAL":
  call_llm = llm
elif LLM_TYPE=="CHAT":
  call_llm = llm_chat
elif LLM_TYPE=="TROPIC":
  call_llm = llm_tropic



import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

# WEBSHOP_URL = "http://3.83.245.205:3000"
# WEBSHOP_URL = "http://127.0.0.1:3000"
WEBSHOP_URL = "tmp/webshop.sock"
ACTION_TO_TEMPLATE = {
    'Description': 'description_page.html',
    'Features': 'features_page.html',
    'Reviews': 'review_page.html',
    'Attributes': 'attributes_page.html',
}

def clean_str(p):
  return p.encode().decode("unicode-escape").encode("latin1").decode("utf-8")


def tag_visible(element):
    ignore = {'style', 'script', 'head', 'title', 'meta', '[document]'}
    return (
        element.parent.name not in ignore and not isinstance(element, Comment)
    )


# ################################
# # PATCHING THE CONNECTION TO WORK WITH UNIX SOCKETS AS WELL
# # Monkeypatch to switch between unix socket and tcp+port
# import urllib3.connection
# import urllib3.util.connection
# _orig_create_connection = urllib3.util.connection.create_connection

# def patched_create_connection(address, *args, **kwargs):
#     host, port = address
#     if host.startswith("/"):
#         import socket
#         sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#         sock.connect(host)
#         return sock
#     return _orig_create_connection(address, *args, **kwargs)

# urllib3.util.connection.create_connection = patched_create_connection

# # END OF PATCH
# ################################

import requests_unixsocket
def query_url(base_url,url_path):
  """Handle both unix socket and regular HTTP requests."""
  print(f"Attempting to query URL: {url_path}")
  if base_url.endswith(".sock"): 
      url = f"unix://{base_url.replace('/', '%2F')}"
      full_url = url+url_path
      print(f"Cleaned_URL_FOR SOCKET: {full_url}")
      # Create adapter using the unix socket
      with requests_unixsocket.monkeypatch():
        response = requests.get(full_url)
  else:
      full_url = base_url + url_path
      # For regular HTTP requests
      response = requests.get(full_url)
  return response.text


def webshop_text(session, page_type, query_string='', page_num=1, asin='', options={}, subpage='', **kwargs):
    if page_type == 'init':
      url_path = (
          f'/{session}'
      )
    if page_type == 'search':
      url_path = (
          f'/search_results/{session}/'
          f'{query_string}/{page_num}'
      )
    elif page_type == 'item':
      url_path = (
          f'/item_page/{session}/'
          f'{asin}/{query_string}/{page_num}/{options}'
      )
    elif page_type == 'item_sub':
      url_path = (
          f'/item_sub_page/{session}/'
          f'{asin}/{query_string}/{page_num}/{subpage}/{options}'
      )
    elif page_type == 'end':
      url_pathrl = (
          f'/done/{session}/'
          f'{asin}/{options}'
      )
    # print(url)
    html = query_url(WEBSHOP_URL, url_path)
    html_obj = BeautifulSoup(html, 'html.parser')
    texts = html_obj.findAll(text=True)
    visible_texts = list(filter(tag_visible, texts))
    # visible_texts = [str(text).strip().strip('\\n') for text in visible_texts]
    # if page_type == 'end': import pdb; pdb.set_trace()
    if False:
        # For `simple` mode, return just [SEP] separators
        return ' [SEP] '.join(t.strip() for t in visible_texts if t != '\n')
    else:
        # Otherwise, return an observation with tags mapped to specific, unique separators
        observation = ''
        option_type = ''
        options = {}
        asins = []
        cnt = 0
        prod_cnt = 0
        just_prod = 0
        for t in visible_texts:
            if t == '\n': continue
            if t.replace('\n', '').replace('\\n', '').replace(' ', '') == '': continue
            # if t.startswith('Instruction:') and page_type != 'init': continue
            # print(t.parent.name, t)
            if t.parent.name == 'button':  # button
                processed_t = f'\n[{t}] '
            elif t.parent.name == 'label':  # options
                if f"'{t}'" in url_path:
                    processed_t = f'[[{t}]]'
                    # observation = f'You have clicked {t}.\n' + observation
                else:
                    processed_t = f'[{t}]'
                options[str(t)] = option_type
                # options[option_type] = options.get(option_type, []) + [str(t)]
            elif t.parent.get('class') == ["product-link"]: # product asins
                processed_t = f'\n[{t}] '
                if prod_cnt >= 3:
                  processed_t = ''
                prod_cnt += 1
                asins.append(str(t))
                just_prod = 0
            else: # regular, unclickable text
                processed_t =  '\n' + str(t) + ' '
                if cnt < 2 and page_type != 'init': processed_t = ''
                if just_prod <= 2 and prod_cnt >= 4: processed_t = ''
                option_type = str(t)
                cnt += 1
            just_prod += 1
            observation += processed_t
        info = {}
        if options:
          info['option_types'] = options
        if asins:
          info['asins'] = asins
        if 'Your score (min 0.0, max 1.0)' in visible_texts:
          idx = visible_texts.index('Your score (min 0.0, max 1.0)')
          info['reward'] = float(visible_texts[idx + 1])
          observation = 'Your score (min 0.0, max 1.0): ' + (visible_texts[idx + 1])
        return clean_str(observation), info

class webshopEnv:
  def __init__(self):
    self.sessions = {}
  
  def step(self, session, action):
    done = False
    observation_ = None
    if action == 'reset':
      self.sessions[session] = {'session': session, 'page_type': 'init'}
    elif action.startswith('think['):
      observation = 'OK.'
    elif action.startswith('search['):
      assert self.sessions[session]['page_type'] == 'init'
      query = action[7:-1]
      self.sessions[session] = {'session': session, 'page_type': 'search',
                                'query_string': query, 'page_num': 1}
    elif action.startswith('click['):
      button = action[6:-1]
      if button == 'Buy Now':
        assert self.sessions[session]['page_type'] == 'item'
        self.sessions[session]['page_type'] = 'end'
        done = True
      elif button == 'Back to Search':
        assert self.sessions[session]['page_type'] in ['search', 'item_sub', 'item']
        self.sessions[session] = {'session': session, 'page_type': 'init'}
      elif button == 'Next >':
        # assert False # ad hoc page limitation
        assert self.sessions[session]['page_type'] == 'search'
        self.sessions[session]['page_num'] += 1
      elif button == '< Prev':
        assert self.sessions[session]['page_type'] in ['search', 'item_sub', 'item']
        if self.sessions[session]['page_type'] == 'search':
          # assert False # ad hoc page limitation
          self.sessions[session]['page_num'] -= 1
        elif self.sessions[session]['page_type'] == 'item_sub':
          self.sessions[session]['page_type'] = 'item'
        elif self.sessions[session]['page_type'] == 'item':
          self.sessions[session]['page_type'] = 'search'
          self.sessions[session]['options'] = {}
      elif button in ACTION_TO_TEMPLATE:
        assert self.sessions[session]['page_type'] == 'item'
        self.sessions[session]['page_type'] = 'item_sub'
        self.sessions[session]['subpage'] = button
      else:
        if self.sessions[session]['page_type'] == 'search':
          assert button in self.sessions[session].get('asins', [])  # must be asins
          self.sessions[session]['page_type'] = 'item'
          self.sessions[session]['asin'] = button
        elif self.sessions[session]['page_type'] == 'item':
          assert 'option_types' in self.sessions[session]
          assert button in self.sessions[session]['option_types'], (button, self.sessions[session]['option_types'])  # must be options
          option_type = self.sessions[session]['option_types'][button]
          if not 'options' in self.sessions[session]:
            self.sessions[session]['options'] = {}
          self.sessions[session]['options'][option_type] = button
          observation_ = f'You have clicked {button}.'
    else:
      assert False
    observation, info = webshop_text(**self.sessions[session])
    if observation_:
      observation = observation_
    self.sessions[session].update(info)
    reward = info.get('reward', 0.0)
    return observation, reward, done
env = webshopEnv()



# # ReAct

START="```start"
END="```end"

# START=""
# END=""
# In[3]:
system_prompt_gpt4o=f"""
You are an intelligent WebShop assistant.
Your job is to buy an item that matches the instruction as close as possible. You only have 15 steps to do so.
The environment gives you an ```Observation```, you need to produce the correct output at every turn. 
Make sure only to use the functions availble in the observations, follow the syntax of the example.

Here is an example interaction:
{START}
WebShop"""


system_prompt_gpt4o=f"""
You are an intelligent WebShop assistant.
Your job is to interact with the environment using the `[]` buttons only. 
You have 15 interactions to buy an item that is closest to the instruction.

Here is an example interaction:
{START}
WebShop"""


system_prompt_gpt4o=f"""
{START}
WebShop"""

OUTRO="""Hints:
1. When you receive the observation `Invalid action!`, this means you did not perform a valid action `[ACTION]` for that page! (Not all actions are availbale on all pages!)
2. Remember in 15 or less moves you must buy an item or you get a score of zero.

"""

OUTRO=""


# trivial search & item, choose option
prompt1 = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]
{END}
{START}
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Action: think[B078GWRC1J and B078GTKVXY are bright citrus deodorant less then 50 dollars. I can check B078GWRC1J first.]
{END}
{START}
Observation: OK.
{END}
{START}
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Action: think[For 3 ounce bottle of bright citrus deodorant for sensitive skin, the item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.]
{END}
{START}
Observation: OK.
{END}
{START}
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Action: click[Buy Now]
{END}
{OUTRO}
"""


# In[4]:


# trivial search & item, choose option
prompt1_actonly = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Action: click[bright citrus]
Observation: You have clicked bright citrus. 
{END}
{START}
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Action: click[Buy Now]
{END}
{OUTRO}
"""

# trivial search & item, choose option
stateact_prompt_ta = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Thought: None
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Thought: B078GWRC1J and B078GTKVXY are bright citrus deodorant less then 50 dollars. I can check B078GWRC1J first.
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Thought: For 3 ounce bottle of bright citrus deodorant for sensitive skin, the item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Thought: None
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Thought: None
Action: click[Buy Now]
{END}
{OUTRO}
"""


# trivial search & item, choose option
stateact_prompt_gsta = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Search Home Page
Thought: None
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Search Results Page, page 1
Thought: B078GWRC1J and B078GTKVXY are bright citrus deodorant less then 50 dollars. I can check B078GWRC1J first.
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item Page, B078GWRC1J
Thought: For 3 ounce bottle of bright citrus deodorant for sensitive skin, the item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item Page, B078GWRC1J
Thought: None
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item Page, B078GWRC1J
Thought: None
Action: click[Buy Now]
{END}
{OUTRO}
"""


# trivial search & item, choose option
stateact_prompt_sta = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Current Location: Search Home Page
Thought: None
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Current Location: Search Results Page, page 1
Thought: B078GWRC1J and B078GTKVXY are bright citrus deodorant less then 50 dollars. I can check B078GWRC1J first.
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Current Location: Item B078GWRC1J Page
Thought: For 3 ounce bottle of bright citrus deodorant for sensitive skin, the item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Current Location: Item B078GWRC1J Page
Thought: None
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Current Location: Item B078GWRC1J Page
Thought: None
Action: click[Buy Now]
{END}
{OUTRO}
"""


# trivial search & item, choose option
stateact_prompt_ssta = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Current Location: Search Home Page
Current Selection: None
Thought: None
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Current Location: Search Results Page, page 1
Current Selection: None
Thought: B078GWRC1J and B078GTKVXY are bright citrus deodorant less then 50 dollars. I can check B078GWRC1J first.
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Current Location: Item B078GWRC1J Page
Current Selection: None
Thought: For 3 ounce bottle of bright citrus deodorant for sensitive skin, the item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus
Thought: None
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus, 3 ounce (pack of 1)
Thought: None
Action: click[Buy Now]
{END}
{OUTRO}
"""

# trivial search & item, choose option
stateact_prompt_gssta = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Search Home Page
Current Selection: None
Thought: None
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Search Results Page, page 1
Current Selection: None
Thought: B078GWRC1J and B078GTKVXY are bright citrus deodorant less then 50 dollars. I can check B078GWRC1J first.
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item B078GWRC1J Page
Current Selection: None
Thought: For 3 ounce bottle of bright citrus deodorant for sensitive skin, the item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus
Thought: None
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus, 3 ounce (pack of 1)
Thought: None
Action: click[Buy Now]
{END}
{OUTRO}
"""


# trivial search & item, choose option
stateact_prompt_ssa = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Current Location: Search Home Page
Current Selection: None
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Current Location: Search Results Page, page 1
Current Selection: None
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Current Location: Item B078GWRC1J Page
Current Selection: None
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus, 3 ounce (pack of 1)
Action: click[Buy Now]
{END}
{OUTRO}
"""


# trivial search & item, choose option
stateact_prompt_a = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Action: click[Buy Now]
{END}
{OUTRO}
"""


# trivial search & item, choose option
stateact_prompt_gssa = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Search Home Page
Current Selection: None
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Search Results Page, page 1
Current Selection: None
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item B078GWRC1J Page
Current Selection: None
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus, 3 ounce (pack of 1)
Action: click[Buy Now]
{END}
{OUTRO}
"""

# trivial search & item, choose option
stateact_prompt_ga = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Search Results Page, page 1
Current Selection: None
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Action: click[Buy Now]
{END}
{OUTRO}
"""


# trivial search & item, choose option
stateact_prompt_gta = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Thought: None
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Thought: B078GWRC1J and B078GTKVXY are bright citrus deodorant less then 50 dollars. I can check B078GWRC1J first.
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Thought: For 3 ounce bottle of bright citrus deodorant for sensitive skin, the item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Thought: None
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Thought: None
Action: click[Buy Now]
{END}
{OUTRO}
"""

# trivial search & item, choose option
stateact_prompt_ta2 = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Thought: To solve the task I should search for a suitable product, browse the products for a good match, then select the most suitable and then make the correct selections and then buy it. I should start by searching for the 3 ounce bright citrus deodarant for sensitive skin.
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Thought: The search produced good results. B078GWRC1J is a bright citrus deodorant for sensitive skin for less then 50 dollars. I should check B078GWRC1J out.
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Thought: The item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Thought: None
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Thought: I have now selected all the required options. I should now buy the product.
Action: click[Buy Now]
{END}
{OUTRO}
"""

# trivial search & item, choose option
stateact_prompt_gssta2 = \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Search Home Page
Current Selection: None
Thought: To solve the task I should search for a suitable product, browse the products for a good match, then select the most suitable and then make the correct selections and then buy it. I should start by searching for the 3 ounce bright citrus deodarant for sensitive skin.
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Search Results Page, page 1
Current Selection: None
Thought: The search produced good results. B078GWRC1J is a bright citrus deodorant for sensitive skin for less then 50 dollars. I should check B078GWRC1J out.
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item B078GWRC1J Page
Current Selection: None
Thought: The item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus
Thought: None
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Goal: Buy a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus, 3 ounce (pack of 1)
Thought: I have now selected all the required options. I should now buy the product.
Action: click[Buy Now]
{END}
{OUTRO}
"""

# trivial search & item, choose option
stateact_prompt_ssta2 =  \
f"""{system_prompt_gpt4o}
Instruction:  
i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars 
[Search]  
{END}
{START}
Current Location: Search Home Page
Current Selection: None
Thought: To solve the task I should search for a suitable product, browse the products for a good match, then select the most suitable and then make the correct selections and then buy it. I should start by searching for the 3 ounce bright citrus deodarant for sensitive skin.
Action: search[3 ounce bright citrus deodorant sensitive skin]
{END}
{START}
Observation: 
[Back to Search] 
Page 1 (Total results: 50) 
[Next >] 
[B078GWRC1J] 
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B078GTKVXY] 
Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
$10.99 
[B08KBVJ4XN] 
Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack) 
$15.95  
{END}
{START}
Current Location: Search Results Page, page 1
Current Selection: None
Thought: The search produced good results. B078GWRC1J is a bright citrus deodorant for sensitive skin for less then 50 dollars. I should check B078GWRC1J out.
Action: click[B078GWRC1J]
{END}
{START}
Observation: 
[Back to Search] 
[< Prev] 
scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce 
Price: $10.99 
Rating: N.A. 
[Description] 
[Features] 
[Reviews] 
[Buy Now]  
{END}
{START}
Current Location: Item B078GWRC1J Page
Current Selection: None
Thought: The item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy.
Action: click[bright citrus]
{END}
{START}
Observation: You have clicked bright citrus. 
{END}
{START}
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus
Thought: None
Action: click[3 ounce (pack of 1)]
{END}
{START}
Observation: You have clicked 3 ounce (pack of 1). 
{END}
{START}
Current Location: Item B078GWRC1J Page
Current Selection: bright citrus, 3 ounce (pack of 1)
Thought: I have now selected all the required options. I should now buy the product.
Action: click[Buy Now]
{END}
{OUTRO}
"""

# In[5]:

def extract_action(action, debug=False):
  """extracts action."""
  SEP = "Action:"
  actual_action = action
  if SEP in action:
    actual_action = action.split(SEP)[-1].lstrip().rstrip()
  if debug:
    print("Debug:")
    for idx,c in enumerate(actual_action):
      print(f"""{idx}:{c}""")

    input()

  return actual_action


def webshop_run(idx, prompt, to_print=False, state=None, max_steps=15, debug=False):
  if state:
    print(f"STATE is TRUE:{state}")
  else:
    print("STATE is FALSE")
  action = 'reset'
  actual_action = action
  init_prompt = prompt
  # print("==init prompt==")
  # print(init_prompt)
  prompt = ''
  step_count = 0
  for i in range(max_steps):
    try:
      res = env.step(idx, actual_action)
      observation = res[0]
    except AssertionError:
      observation = 'Invalid action!'

    step_count += 1
    if action.startswith('think'):
      observation = 'OK.'

    if to_print:  
      print("=Produced Action=")
      print(action)
      print("=Extracted Action=")
      print(actual_action)
      print("=Observation=")
      print(observation)
      print()
      sys.stdout.flush()
      if debug:
        input()
    # if to_print:
    #   print(f'{action}\nObservation: {observation}\n')
    #   sys.stdout.flush()

    if i:
      prompt += f'\n{action}\n{END}\n{START}\nObservation:{observation}\n{END}'

    else:
      prompt += f'{START}{observation}\n{END}'

    if res[2]:  
      return res[1], step_count

    action = call_llm(init_prompt + prompt[-(MAX_PROMPT_LENGTH-len(init_prompt)):], stop=[END])
    # action = llm_chat(init_prompt + prompt, stop=[END])



    if state:
      actual_action = extract_action(action, debug=debug)
    elif "Action:" in action:
      actual_action = extract_action(action, debug=debug)
    else:
      print("Action was not extracted")
      actual_action = action

  return 0, step_count

def run_episodes(prompt, n=50, s=0, state=None, max_steps=15):
  rs = []
  cnt = 0
  total_steps = []
  for i in range(s,n):
    print('-----------------')
    print(i)
    try:
      r, steps = webshop_run(f'fixed_{i}', prompt, to_print=True, state=state, max_steps=max_steps)
    except AssertionError:
      r = 0
      cnt += 1
    rs.append(r)
    total_steps.append(steps)
    if (i+1) % 1 == 0:
      r, sr, fr = sum(rs) / len(rs), len([_ for _ in rs if _ == 1]) / len(rs), cnt / len(rs)
      print(i+1, r, sr, fr)
      print('-------------')
  r, sr, fr = sum(rs) / len(rs), len([_ for _ in rs if _ == 1]) / n, cnt / n
  avg_steps = sum(total_steps)/len(total_steps)
  print(r, sr, fr, avg_steps)
  return rs, (r, sr, fr), total_steps


# In[6]:
import time
s=0
N=30
MS = 15
 
experiments_to_run = ["act","react","stateact","stateact-no-thoughts","stateact-no-goal","stateact-no-state"]
# experiments_to_run = ["act"]
experiments_to_run = ["react"]
# experiments_to_run = ["stateact"]
# experiments_to_run = ["stateact-no-thoughts"]
# experiments_to_run = ["ssa"]
# experiments_to_run = ["stateact2"]
# experiments_to_run = ["gsta"]

# experiments_to_run = ["stateact2","ssa","react","stateact","stateact-no-thoughts"]

# experiments_to_run = ["stateact2"]

# starting price 33.11
# [0, 0.6666666666666666, 0.5, 0.75, 1.0, 0, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.5]
# (0.5416666666666667, 0.1, 0.0)

# [0, 0, 0.5, 0.75, 1.0, 0.6666666666666666, 1.0, 0.6666666666666666, 0.6666666666666666, 0.5]
# (0.575, 0.2, 0.0)

# [0, 0, 0.5, 0, 1.0, 0, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.5]
# (0.39999999999999997, 0.1, 0.0)

# [0, 0, 0.5, 0.75, 1.0, 0, 0, 0.6666666666666666, 0.6666666666666666, 1.0]
# (0.4583333333333333, 0.2, 0.0)

if "act" in experiments_to_run:
  t0s = time.localtime()
  res0, sc0, steps0 = run_episodes(prompt1_actonly, N, s=s, state=None, max_steps=MS)
  t0e = time.localtime()
  print('=====================act')
  print(res0)
  print(sc0)
  print(steps0)
  print(sum(steps0)/len(steps0))

if "react" in experiments_to_run:
  t1s = time.localtime()
  res1, sc1 , steps1 = run_episodes(prompt1, N, s=s, state=None, max_steps=MS)
  t1e = time.localtime()
  print('=====================react')
  print(res1)
  print(sc1)
  print(steps1)
  print(sum(steps1)/len(steps1))

if "ta" in experiments_to_run:
  t2s = time.localtime()
  res2, sc2 , steps2 = run_episodes(stateact_prompt_ta, N, s=s, state="Thought", max_steps=MS)
  t2e = time.localtime()
  print('=====================ta')
  print(res2)
  print(sc2)
  print(steps2)
  print(sum(steps2)/len(steps2))

if "gsta" in experiments_to_run:
  t3s = time.localtime()
  res3, sc3 , steps3 = run_episodes(stateact_prompt_gsta, N, s=s, state="Goal", max_steps=MS)
  t3e = time.localtime()
  print('=====================')
  print(res3)
  print(sc3)
  print(steps3)
  print(sum(steps3)/len(steps3))

if "ta" in experiments_to_run:
  t4s = time.localtime()
  res4, sc4 , steps4 = run_episodes(stateact_prompt_sta, N, s=s, state="Current Location", max_steps=MS)
  t4e = time.localtime()
  print('=====================')
  print(res4)
  print(sc4)
  print(steps4)
  print(sum(steps4)/len(steps4))

if "stateact-no-goal" in experiments_to_run:
  t5s = time.localtime()
  res5, sc5 , steps5 = run_episodes(stateact_prompt_ssta, N, s=s, state="Current Location", max_steps=MS)
  t5e = time.localtime()
  print('=====================')
  print(res5)
  print(sc5)
  print(steps5)
  print(sum(steps5)/len(steps5))

if "stateact" in experiments_to_run:
  t6s = time.localtime()
  res6, sc6 , steps6 = run_episodes(stateact_prompt_gssta, N, s=s, state="Goal", max_steps=MS)
  t6e = time.localtime()
  print('=====================')
  print(res6)
  print(sc6)
  print(steps6)
  print(sum(steps6)/len(steps6))

if "ssa" in experiments_to_run:
  t7s = time.localtime()
  res7, sc7 , steps7 = run_episodes(stateact_prompt_ssa, N, s=s, state="Current Location", max_steps=MS)
  t7e = time.localtime()
  print('=====================')
  print(res7)
  print(sc7)
  print(steps7)
  print(sum(steps7)/len(steps7))

if "ta" in experiments_to_run:
  t8s = time.localtime()
  res8, sc8 , steps8 = run_episodes(stateact_prompt_a, N, s=s, state="Action", max_steps=MS)
  t8e = time.localtime()
  print('=====================')
  print(res8)
  print(sc8)
  print(steps8)
  print(sum(steps8)/len(steps8))

if "stateact-no-thoughts" in experiments_to_run:
  t9s = time.localtime()
  res9, sc9 , steps9 = run_episodes(stateact_prompt_gssa, N, s=s, state="Goal", max_steps=MS)
  t9e = time.localtime()
  print('=====================gssa')
  print(res9)
  print(sc9)
  print(steps9)
  print(sum(steps9)/len(steps9))

if "ta" in experiments_to_run:
  t10s = time.localtime()
  res10, sc10 , steps10 = run_episodes(stateact_prompt_ga, N, s=s, state="Goal", max_steps=MS)
  t10e = time.localtime()
  print('=====================')
  print(res10)
  print(sc10)
  print(steps10)
  print(sum(steps10)/len(steps10))

if "stateact-no-state" in experiments_to_run:
  t11s = time.localtime()
  res11, sc11 , steps11 = run_episodes(stateact_prompt_gta, N, s=s, state="Goal", max_steps=MS)
  t11e = time.localtime()
  print('=====================gta')
  print(res11)
  print(sc11)
  print(steps11)
  print(sum(steps11)/len(steps11))

if "ta" in experiments_to_run:
  t12s = time.localtime()
  res12, sc12 , steps12 = run_episodes(stateact_prompt_ta2, N, s=s, state="Thought", max_steps=MS)
  t12e = time.localtime()
  print('=====================ta2')
  print(res12)
  print(sc12)
  print(steps12)
  print(sum(steps12)/len(steps12))

if "stateact2" in experiments_to_run:
  t13s = time.localtime()
  res13, sc13 , steps13 = run_episodes(stateact_prompt_gssta2, N, s=s, state="Goal", max_steps=MS)
  t13e = time.localtime()
  print('=====================gssta2')
  print(res13)
  print(sc13)
  print(steps13)
  print(sum(steps13)/len(steps13))

if "no-goal-stateact2" in experiments_to_run:
  t14s = time.localtime()
  res14, sc14 , steps14 = run_episodes(stateact_prompt_ssta2, N, s=s, state="Current Location", max_steps=MS)
  t14e = time.localtime()
  print('=====================ssta2')
  print(res14)
  print(sc14)
  print(steps14)
  print(sum(steps14)/len(steps14))


print('=====================')
print(f'-FINAL RESULTS-{GPT_MODEL}')
print('---------------------')

print(f"s={s}, N={N}")


if "act" in experiments_to_run:
  print('=====================0-actonly')
  print(res0)
  print(sc0)
  print(t0s)
  print(t0e)
  print(steps0)
  print(sum(steps0)/len(steps0))

if "react" in experiments_to_run:
  print('=====================1-react')
  print(res1)
  print(sc1)
  print(t1s)
  print(t1e)
  print(steps1)
  print(sum(steps1)/len(steps1))

if "ta" in experiments_to_run:
  print('=====================2-ta')
  print(res2)
  print(sc2)
  print(t2s)
  print(t2e)
  print(steps2)
  print(sum(steps2)/len(steps2))

if "gsta" in experiments_to_run:
  print('=====================3')
  print(res3)
  print(sc3)
  print(t3s)
  print(t3e)
  print(steps3)
  print(sum(steps3)/len(steps3))

if "ta" in experiments_to_run:
  print('=====================4')
  print(res4)
  print(sc4)
  print(t4s)
  print(t4e)
  print(steps4)
  print(sum(steps4)/len(steps4))

if "stateact-no-goal" in experiments_to_run:
  print('=====================5-ssta')
  print(res5)
  print(sc5)
  print(t5s)
  print(t5e)
  print(steps5)
  print(sum(steps5)/len(steps5))

if "stateact" in experiments_to_run:
  print('=====================6-gssta')
  print(res6)
  print(sc6)
  print(t6s)
  print(t6e)
  print(steps6)
  print(sum(steps6)/len(steps6))

if "ssa" in experiments_to_run:
  print('=====================7-ssa')
  print(res7)
  print(sc7)
  print(t7s)
  print(t7e)
  print(steps7)
  print(sum(steps7)/len(steps7))

if "ta" in experiments_to_run:
  print('=====================8')
  print(res8)
  print(sc8)
  print(t8s)
  print(t8e)
  print(steps8)
  print(sum(steps8)/len(steps8))

if "stateact-no-thoughts" in experiments_to_run:
  print('=====================9-gssa')
  print(res9)
  print(sc9)
  print(t9s)
  print(t9e)
  print(steps9)
  print(sum(steps9)/len(steps9))

if "ta" in experiments_to_run:
  print('=====================10')
  print(res10)
  print(sc10)
  print(t10s)
  print(t10e)
  print(steps10)
  print(sum(steps10)/len(steps10))

if "stateact-no-state" in experiments_to_run:
  print('=====================11-gta')
  print(res11)
  print(sc11)
  print(t11s)
  print(t11e)
  print(steps11)
  print(sum(steps11)/len(steps11))

if "ta" in experiments_to_run:
  print('=====================12-ta2')
  print(res12)
  print(sc12)
  print(t12s)
  print(t12e)
  print(steps12)
  print(sum(steps12)/len(steps12))

if "stateact2" in experiments_to_run:
  print('=====================13-gssta2')
  print(res13)
  print(sc13)
  print(t13s)
  print(t13e)
  print(steps13)
  print(sum(steps13)/len(steps13))

if "ta" in experiments_to_run:
  print('=====================14-ssta2')
  print(res14)
  print(sc14)
  print(t14s)
  print(t14e)
  print(steps14)
  print(sum(steps14)/len(steps14))

# =====================
# -FINAL RESULTS-
# ---------------------
# =====================1
# [0, 0, 0.5, 0.75, 1.0, 0, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# (0.0475, 0.01, 0.0)
# time.struct_time(tm_year=2024, tm_mon=5, tm_mday=25, tm_hour=18, tm_min=57, tm_sec=17, tm_wday=5, tm_yday=146, tm_isdst=1)
# time.struct_time(tm_year=2024, tm_mon=5, tm_mday=25, tm_hour=19, tm_min=14, tm_sec=25, tm_wday=5, tm_yday=146, tm_isdst=1)
# =====================2
# [0, 0, 0.5, 0.75, 1.0, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# (0.05416666666666667, 0.01, 0.0)
# time.struct_time(tm_year=2024, tm_mon=5, tm_mday=25, tm_hour=19, tm_min=14, tm_sec=25, tm_wday=5, tm_yday=146, tm_isdst=1)
# time.struct_time(tm_year=2024, tm_mon=5, tm_mday=25, tm_hour=19, tm_min=31, tm_sec=4, tm_wday=5, tm_yday=146, tm_isdst=1)
# =====================3
# [0, 1.0, 0.5, 0.75, 1.0, 0, 0.6666666666666666, 1.0, 0.6666666666666666, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# (0.05583333333333333, 0.03, 0.0)
# time.struct_time(tm_year=2024, tm_mon=5, tm_mday=25, tm_hour=19, tm_min=31, tm_sec=4, tm_wday=5, tm_yday=146, tm_isdst=1)
# time.struct_time(tm_year=2024, tm_mon=5, tm_mday=25, tm_hour=19, tm_min=49, tm_sec=48, tm_wday=5, tm_yday=146, tm_isdst=1)
# =====================4
# [0, 0, 0.5, 0.75, 1.0, 0, 0.6666666666666666, 1.0, 0.6666666666666666, 1.0, 0.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# (0.06333333333333332, 0.03, 0.0)
# time.struct_time(tm_year=2024, tm_mon=5, tm_mday=25, tm_hour=19, tm_min=49, tm_sec=48, tm_wday=5, tm_yday=146, tm_isdst=1)
# time.struct_time(tm_year=2024, tm_mon=5, tm_mday=25, tm_hour=20, tm_min=8, tm_sec=43, tm_wday=5, tm_yday=146, tm_isdst=1)



# (0.655673333333334, 0.346, 0.0)
# (0.6262000000000003, 0.346, 0.0)
# 0.6276766666666669 0.344 0.0 7.196
