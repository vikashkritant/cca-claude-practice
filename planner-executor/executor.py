from tools import add_numbers

def execute_plan(plan):
    result = None

    for step in plan:
        tool = step.get("tool")
        args = step.get("args", {})

        # 🔥 replace $prev with last result
        for k, v in args.items():
            if v == "$prev":
                args[k] = result

        print(f"\n🔧 Executing: {tool} with {args}")

        if tool == "add_numbers":
            result = add_numbers(**args)
        else:
            raise Exception(f"Unknown tool: {tool}")

        print("Result:", result)

    return result