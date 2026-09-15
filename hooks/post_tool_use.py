import sys
import json
import re

SENSITIVE_PATTERNS = [
    (r'(?i)(password|passwd|secret|token|api_key)\s*[:=]\s*["\']?[^"\s\']+["\']?', r'\1: [REDACTED]')
]

def main():
    try:
        input_data = json.load(sys.stdin)
        result_text = input_data.get("result", "")

        for pattern, replacement in SENSITIVE_PATTERNS:
            result_text = re.sub(pattern, replacement, result_text)

        print(json.dumps({"result": result_text}))
    except Exception as e:
        sys.exit(0)

if __name__ == "__main__":
    main()
