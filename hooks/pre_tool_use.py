import sys
import json

FORBIDDEN_KEYWORDS = ["apply", "delete", "edit", "scale", "patch", "replace"]

def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool", "")
        tool_args = json.dumps(input_data.get("args", {})).lower()

        for keyword in FORBIDDEN_KEYWORDS:
            if keyword in tool_args:
                print(json.dumps({
                    "decision": "BLOCK",
                    "reason": f"Execution blocked: Mutating command '{keyword}' is prohibited."
                }))
                sys.exit(0)

        print(json.dumps({"decision": "ALLOW"}))
    except Exception as e:
        print(json.dumps({"decision": "ALLOW"}))

if __name__ == "__main__":
    main()
