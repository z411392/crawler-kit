from asyncio import get_running_loop, new_event_loop, set_event_loop


def ensure_event_loop():
    try:
        return get_running_loop()
    except RuntimeError:
        loop = new_event_loop()
        set_event_loop(loop)
        return loop
