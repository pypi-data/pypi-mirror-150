import dataclasses

from buz.event import Event, Subscriber
from buz.event.transactional_outbox.outbox_record import OutboxRecord
from buz.locator import Locator


class EventToOutboxRecordTranslator:
    def __init__(self, locator: Locator[Event, Subscriber]):
        self.__locator = locator

    def to_outbox_record(self, event: Event) -> OutboxRecord:
        payload = dataclasses.asdict(event)
        payload.pop("id")
        payload.pop("created_at")
        return OutboxRecord(
            event_id=event.id,
            event_fqn=event.fqn(),
            created_at=event.parsed_created_at(),
            event_payload=payload,
        )

    def to_event(self, outbox_record: OutboxRecord) -> Event:
        event_klass = self.__locator.get_message_klass_by_fqn(outbox_record.event_fqn)
        return event_klass.restore(
            id=outbox_record.event_id, created_at=outbox_record.parsed_created_at(), **outbox_record.event_payload
        )
