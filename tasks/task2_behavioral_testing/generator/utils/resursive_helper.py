def get_start_state_for_recursive(fsa_path: str) -> str:
    with open(fsa_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line.startswith("start:"):
                return line.split(":", 1)[1].strip()

    raise ValueError("Start state not found in FSA file")
