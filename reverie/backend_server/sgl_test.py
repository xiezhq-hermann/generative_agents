from sglang import function, system, user, assistant, gen, set_default_backend, RuntimeEndpoint
import sglang as sgl
@staticmethod
def llm_call(prompt, max_tokens):
    set_default_backend(RuntimeEndpoint("http://localhost:30000"))
    @sgl.function
    def func_wrapper(s, prompt,max_tokens = max_tokens):
        # todo, support for priority scheduling for sgl
        s += prompt
        s += sgl.gen("response",
                        max_tokens=max_tokens)

    response = func_wrapper.run(prompt)
    return response["response"]

@staticmethod
def llm_call1(prompt):
    set_default_backend(RuntimeEndpoint("http://localhost:30000"))
    @sgl.function
    def func_wrapper(s, prompt):
        # todo, support for priority scheduling for sgl
        s += prompt
        s += sgl.gen("response",
                        )

    response = func_wrapper.run(prompt)
    return response["response"]
result = llm_call1("I want you to write a schedule for me, starting from 8:00 am to 5 p.m.")
print(result)