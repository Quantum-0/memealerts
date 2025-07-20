from typing import Any

from memealerts.types.user_id import StickerID, UserID


def replace_rootmodel_with_str(obj: Any) -> Any:
    if isinstance(obj, UserID | StickerID):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: replace_rootmodel_with_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_rootmodel_with_str(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(replace_rootmodel_with_str(item) for item in obj)
    return obj
