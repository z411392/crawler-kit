from os import getenv, environ


def is_emulating():
    return getenv("FUNCTIONS_EMULATOR") == "true"


def get_environment():
    if is_emulating():
        return "emulating"

    env = getenv("ENVIRONMENT", "").lower()
    if env in ["dev", "development", "local"]:
        return "development"
    elif env in ["prod", "production"]:
        return "production"

    run_mode = getenv("RUN_MODE", "").lower()
    if run_mode == "cli":
        return "development"

    if getenv("GOOGLE_CLOUD_PROJECT") or getenv("GCP_PROJECT"):
        return "production"

    return "development"


def is_development() -> bool:
    return get_environment() == "development"


def is_testing():
    return "PYTEST_CURRENT_TEST" in environ


def is_production() -> bool:
    return get_environment() == "production"


def headless_flag() -> bool:
    headless_env = getenv("HEADLESS", "").lower()
    if headless_env in ["true", "1", "yes"]:
        return True
    elif headless_env in ["false", "0", "no"]:
        return False

    return is_production() or is_emulating()
