"""Small integration exercise; this is not a deployed backend server."""
import argparse
import importlib
import importlib.util

FEATURES = {"hello": "Hello World", "xinchao": "Xin chào World"}


def collect_messages(require_all=False):
    messages = []
    missing = []
    for name, expected in FEATURES.items():
        module_name = f"features.{name}"
        if importlib.util.find_spec(module_name) is None:
            missing.append(name)
            continue
        # Import/runtime errors inside an existing feature must fail CI.
        module = importlib.import_module(module_name)
        function = getattr(module, name)
        actual = function()
        if actual != expected:
            raise ValueError(f"{name} returned {actual!r}; expected {expected!r}")
        messages.append(actual)
    if require_all and missing:
        raise RuntimeError("Missing required features: " + ", ".join(missing))
    return messages, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-all", action="store_true",
                        help="Fail unless both features are installed")
    args = parser.parse_args()
    messages, missing = collect_messages(require_all=args.require_all)
    for message in messages:
        print(message)
    for name in missing:
        print(f"Waiting for feature: {name}")


if __name__ == "__main__":
    main()
