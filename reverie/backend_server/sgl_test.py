from sglang import function, system, user, assistant, gen, set_default_backend, RuntimeEndpoint
import sglang as sgl
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
      max_tokens=model_parameter["max_tokens"],
      temperature=model_parameter["temperature"],
      stop=model_parameter["stop"],
      top_p=model_parameter["top_p"],
      frequency_penalty=model_parameter["frequency_penalty"],
      presence_penalty=model_parameter["presence_penalty"],
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
result = LLM_request("I want you to write a schedule for me, starting from 8:00 am to 5 p.m.",{"max_tokens":10000,"temperature":0.5,"stop":"\n","top_p":0.9,"frequency_penalty":0.0,"presence_penalty":0.0})
print(result)