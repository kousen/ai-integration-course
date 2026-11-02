"""The tools the portfolio chatbot may ask for, and the code that decides whether to run them.

A tool has two halves. The *schema* is what the model sees: a name, a description, and the
JSON Schema of the arguments. The *function* is what your program runs, after it has checked the
arguments itself. The model never runs anything. It writes a request; `run_tool` decides.

Three tools, on purpose:
  lookup_project(name)       read-only, answers from profile.json
  check_skill(skill)         read-only, says shipped / not yet / not in the profile
  request_intro(email, msg)  a side effect (it would write to an outbox); never run without a person
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
PROFILE = json.loads((HERE / "profile.json").read_text())

# ---- the schemas: this list goes in the request as `tools` --------------------------------------
TOOLS = [
    {"type": "function", "function": {
        "name": "lookup_project",
        "description": "Look up one of the person's projects by name and return its four-question "
                       "annotation (what, why, what breaks, what was learned). Use this before saying "
                       "anything about a project.",
        "parameters": {"type": "object",
                       "properties": {"name": {"type": "string", "description": "The project's name, or part of it"}},
                       "required": ["name"]}}},
    {"type": "function", "function": {
        "name": "check_skill",
        "description": "Say whether the person has shipped work with a skill or tool, has deliberately "
                       "not learned it yet, or has no record of it. Use this before any claim about a skill.",
        "parameters": {"type": "object",
                       "properties": {"skill": {"type": "string", "description": "A language, tool, or technology"}},
                       "required": ["skill"]}}},
    {"type": "function", "function": {
        "name": "request_intro",
        "description": "Send the person an introduction request from a visitor. Only when the visitor "
                       "explicitly asks to be introduced and gives an email address.",
        "parameters": {"type": "object",
                       "properties": {"email": {"type": "string", "description": "The visitor's email address"},
                                      "message": {"type": "string", "description": "What the visitor wants"}},
                       "required": ["email", "message"]}}},
]
SIDE_EFFECTS = {"request_intro"}          # tools the program never runs on the model's say-so alone


# ---- the functions ------------------------------------------------------------------------------
def lookup_project(name: str) -> dict:
    needle = name.strip().lower()
    for p in PROFILE["projects"]:
        if needle and (needle in p["name"].lower() or p["name"].lower() in needle):
            return {"found": True, "project": p}
    return {"found": False, "name": name, "projects_on_record": [p["name"] for p in PROFILE["projects"]]}


def check_skill(skill: str) -> dict:
    needle = skill.strip().lower()
    for s in PROFILE["skills_shipped"]:
        if needle and needle in s.lower():
            return {"skill": skill, "status": "shipped", "as_listed": s}
    for n in PROFILE["not_yet"]:
        if needle and needle in n["skill"].lower():
            return {"skill": skill, "status": "not_yet", "why": n["why"]}
    return {"skill": skill, "status": "no_record"}


def request_intro(email: str, message: str) -> dict:
    """The side effect. In a real site this writes to an outbox or sends mail. Here it appends a line
    to outbox.jsonl so a test can prove it did or did not happen."""
    with open(HERE / "outbox.jsonl", "a") as f:
        f.write(json.dumps({"email": email, "message": message}) + "\n")
    return {"sent": True}


FUNCTIONS = {"lookup_project": lookup_project, "check_skill": check_skill, "request_intro": request_intro}


# ---- the decision -------------------------------------------------------------------------------
def validate(name: str, args) -> str | None:
    """Return an error message, or None if the call is well formed. Plain code, no model."""
    schema = next((t["function"]["parameters"] for t in TOOLS if t["function"]["name"] == name), None)
    if schema is None:
        return f"unknown tool {name!r}; the tools are {sorted(FUNCTIONS)}"
    if not isinstance(args, dict):
        return "arguments must be a JSON object"
    for req in schema.get("required", []):
        if req not in args:
            return f"missing required argument {req!r}"
    for key, val in args.items():
        spec = schema["properties"].get(key)
        if spec is None:
            return f"unexpected argument {key!r}"
        if spec["type"] == "string" and not isinstance(val, str):
            return f"argument {key!r} must be a string, got {type(val).__name__}"
    return None


def run_tool(name: str, arguments: str | dict, allow_side_effects: bool = False) -> dict:
    """What the loop calls for every tool request. Never raises on a bad request: the error goes
    back to the model as the tool's result, so the model can correct itself or give up."""
    if isinstance(arguments, str):
        try:
            args = json.loads(arguments or "{}")
        except json.JSONDecodeError as e:
            return {"error": f"arguments were not valid JSON: {e.msg}"}
    else:
        args = arguments
    problem = validate(name, args)
    if problem:
        return {"error": problem}
    if name in SIDE_EFFECTS and not allow_side_effects:
        return {"error": f"{name} has a side effect and needs the visitor's confirmation first",
                "pending": {"tool": name, "arguments": args}}
    return FUNCTIONS[name](**args)
