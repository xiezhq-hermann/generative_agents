from sglang import function, system, user, assistant, gen, set_default_backend, RuntimeEndpoint
import sglang as sgl
from gpt_structure import llm_safe_generation


def LLM_request(prompt,model_parameter):
  set_default_backend(RuntimeEndpoint("http://localhost:30000"))
  @sgl.function
  def func_wrapper(s,prompt = prompt,model_parameter = model_parameter):
    s += prompt
    s += sgl.gen(
      "response",
      **model_parameter
    )
  @sgl.function
  def base_func_wrapper(s,prompt = prompt):
    s += prompt
    s += sgl.gen(
      "response"
    )
  try:
    if isinstance(model_parameter,dict):
      return func_wrapper.run(prompt,model_parameter)["response"]
    else:
      return base_func_wrapper(prompt)["response"]
  except Exception as e: # work on python 3.x
    print('Failed: '+ str(e))
    print ("TOKEN LIMIT EXCEEDED")
    return "TOKEN LIMIT EXCEEDED"
def create_prompt_input(persona, event_description, test_input=None): 
    prompt_input = [persona.scratch.name,
                    persona.scratch.get_str_iss(),
                    persona.scratch.name,
                    event_description]
    return prompt_input
  
def __func_clean_up(gpt_response, prompt=""):
    return gpt_response.split('"')[0].strip()

def __func_validate(gpt_response, prompt=""): 
  try: 
    __func_clean_up(gpt_response, prompt)
    return True
  except:
    return False 

def get_fail_safe(): 
  return "..."


# ChatGPT Plugin ===========================================================
def __chat_func_clean_up(gpt_response, prompt=""): ############
  return gpt_response.split('"')[0].strip()

def __chat_func_validate(gpt_response, prompt=""): ############
  try: 
    __func_clean_up(gpt_response, prompt)
    return True
  except:
    return False 
prompt = "[Statements]\nJennifer Moore is sleeping\nThis is Sam Moore's plan for Monday February 13: wake up and complete the morning routine at 5:00 am, .\nSam Moore is sleeping\nwaking up\nwaking up\n\n\nBased on the statements above, summarize Sam Moore and Jennifer Moore's relationship. What do they feel or know about each other?\n\n\n\""
# example_output = "{\"output\"\:5}"
# special_instruction = "only return the emoji without anyother things"
# special_instruction = special_instruction = "The output should ONLY contain the phrase that should go in <fill in>."
special_instruction = " Generate one set of results in json format like {\"output\": <output>} in about 20 words. Do not generate code."
fail_safe = 5
act_game_object = "sth"
example_output = f"{{\"output\": ...}}"
result = llm_safe_generation(prompt,example_output,special_instruction,3,fail_safe,
                             __chat_func_validate,__chat_func_clean_up,
                             {"max_tokens":100,"temperature":0.3,"frequency_penalty": 0.1})
print("result",result)
