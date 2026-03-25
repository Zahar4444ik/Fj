def get_start_state_for_recursive(fsa_path: str) -> str:
    try:
        with open(fsa_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if line.startswith("initial_state:"):
                    return line.split(":", 1)[1].strip()
    except FileNotFoundError:
        return "q0"
