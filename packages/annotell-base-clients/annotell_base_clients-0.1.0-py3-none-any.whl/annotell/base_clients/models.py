from typing import Union, Optional

from annotell.input_api.model.base_serializer import BaseSerializer


class PageMetadata(BaseSerializer):
    next_cursor_id: Optional[int]


class PaginatedResponse(BaseSerializer):
    data: Union[dict, list]
    metadata: PageMetadata
