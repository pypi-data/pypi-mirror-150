from typing import Any, Callable, List


def generate_strip_sensitive_data(strip_key_list: List[str]) -> Callable[[Any, Any], Any]:
    """
    Generate a function to filter sensitive data.
    Set the return value of this function to before_send of sentry.

    Args:
        strip_key_list (List[str]): list of keys to strip

    Returns:
        Callable[[Any, Any], Any]: The first argument of the return function is sentry's event,
        and the second is sentry's hint.
        Also, the return value is the event of sentry after processing.
    """

    def strip_sensitive_data(event, hint):
        for v in event["exception"]["values"]:
            for s in v["stacktrace"]["frames"]:
                s["vars"] = __recurse_filter_vars(s["vars"], strip_key_list)
        return event

    return strip_sensitive_data


def __recurse_filter_vars(obj, del_target_keys):
    for del_target_key in del_target_keys:
        if del_target_key in obj:
            del obj[del_target_key]
    for v in obj.values():
        if isinstance(v, dict):
            __recurse_filter_vars(v, del_target_keys)
        if isinstance(v, list):
            for e in v:
                if isinstance(e, dict):
                    __recurse_filter_vars(e, del_target_keys)
    return obj
