from typing import Optional
from fastapi_filter.contrib.mongoengine import Filter


class TaskFilter(Filter):
    class Config:
        use_enum_values = True

    group: Optional[str] = None
    type: Optional[int] = None
    tags__in: Optional[list[str]] = None
    state: Optional[int] = None
    importance: Optional[int] = None
