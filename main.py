import argparse
import os
import requests

from core.param_scanner import get_parameters, inject_param
from core.engine_AI import detect_vulnerability

def boolean_sqli_test(url, param):
    true_payload = "0 AND 1=1"
    false_payload = "0 AND 1=2"

    true_resp, _ = inject_param(url, param, true_payload)
    false_resp, _ = inject_param(url, param, false_payload)

    if len(true_resp) != len(false_resp):
        return True

    return False

def load_payloads():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    payload_path = os.path.join(base_dir, "payloads", "bassic.txt")

    with open(payload_path, "r", encoding="utf-8") as f:
        return [p.strip() for p in f.readlines() if p.strip()]


def heuristic_detection(text):
    text_lower = text.lower()

    if "sql" in text_lower or "odbc" in text_lower or "syntax error" in text_lower:
        return "SQL Injection"

    if "<script>alert(1)</script>" in text_lower:
        return "XSS"

    if "root:x:" in text_lower:
        return "LFI"

    return None


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    target = args.url

    try:
        baseline = requests.get(target, timeout=8).text
    except:
        print("Target unreachable")
        return

    payloads = load_payloads()
    params = get_parameters(target)

    found = set()

    if not params:
        print(f"{target} → No parameters found")
        return

    for param in params:
        # Boolean-based SQLi detection
        if boolean_sqli_test(target, param):
            found.add("SQL Injection")
            continue

        for payload in payloads:

            injected_text, new_url = inject_param(target, param, payload)

            # Heuristic first
            heuristic_result = heuristic_detection(injected_text)
            if heuristic_result:
                found.add(heuristic_result)
                continue

            # AI confirmation
            ai_result = detect_vulnerability(
                baseline,
                injected_text,
                payload
            )

            if ai_result != "NONE":
                found.add(ai_result)

    if found:
        print(f"{target} → {', '.join(found)}")
    else:
        print(f"{target} → No obvious vulnerability detected")


if __name__ == "__main__":
    main()