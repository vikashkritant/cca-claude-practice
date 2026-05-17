from tools import add_numbers, multiply_numbers

def execute_step(step, prev_result):
    tool = step.get("tool")
    args = step.get("args", {})

    # 🔁 replace $prev
    for k, v in args.items():
        if v == "$prev":
            args[k] = prev_result

    print(f"\n🔧 Executing: {tool} with {args}")

    if tool == "add_numbers":
        return add_numbers(**args)

    elif tool == "multiply_numbers":
        return multiply_numbers(**args)

    else:
        raise Exception(f"Unknown tool: {tool}")