from dataclasses import dataclass
from datetime import datetime
from typing import Optional, ClassVar

from buz.event.transactional_outbox import OutboxSortingCriteria


@dataclass(frozen=True)
class OutboxCriteria:
    UNSET_VALUE: ClassVar[object] = object()

    delivered_at: Optional[datetime] = UNSET_VALUE  # type: ignore
    order_by: Optional[OutboxSortingCriteria] = UNSET_VALUE
