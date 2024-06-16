from sglang import function, system, user, assistant, gen, set_default_backend, RuntimeEndpoint
import sglang as sgl
from gpt_structure import llm_safe_generation
# @staticmethod
# def llm_call(prompt, max_tokens):
#     set_default_backend(RuntimeEndpoint("http://localhost:30000"))
#     @sgl.function
#     def func_wrapper(s, prompt,max_tokens = max_tokens):
#         # todo, support for priority scheduling for sgl
#         s += prompt
#         s += sgl.gen("response",
#                         max_tokens=max_tokens)

#     response = func_wrapper.run(prompt)
#     return response["response"]

# @staticmethod
# def llm_call1(prompt):
#     set_default_backend(RuntimeEndpoint("http://localhost:30000"))
#     @sgl.function
#     def func_wrapper(s, prompt):
#         # todo, support for priority scheduling for sgl
#         s += prompt
#         s += sgl.gen("response",
#                         )

#     response = func_wrapper.run(prompt)
#     return response["response"]
# result = llm_call1("I want you to write a schedule for me, starting from 8:00 am to 5 p.m.")
# print(result)

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
def __chat_func_clean_up(gpt_response, prompt=""): ############
  cr = gpt_response.strip()
  if len(cr) > 3:
    cr = cr[:3]
  return cr

def __chat_func_validate(gpt_response, prompt=""): ############
  try: 
    __func_clean_up(gpt_response, prompt="")
    if len(gpt_response) == 0: 
      return False
  except: return False
  return True 
def __func_clean_up(gpt_response, prompt=""):
  cr = gpt_response.strip()
  if len(cr) > 3:
    cr = cr[:3]
  return cr
prompt = "Task: We want to understand the state of an object that is being used by someone. \n\nLet's think step by step. \nWe want to know about closet's state. \nStep 1. Yuriko Yamamoto is at/using the sleeping.\nStep 2. Describe the closet's state."
example_output = "{output\:closet is idle}"
# special_instruction = "only return the emoji without anyother things"
# special_instruction = special_instruction = "The output should ONLY contain the phrase that should go in <fill in>."
special_instruction = "output the answer in json format like {output: <result>}, give the answer to the problem, do not generate code or any unrelated results."
fail_safe = "closet is idle"

result = llm_safe_generation(prompt,example_output,special_instruction,3,fail_safe,
                             __chat_func_validate,__chat_func_clean_up,
                             {"max_tokens":50,"temperature":0.3})
print("result",result)