from logging import Logger

from buz.event import EventBus
from buz.event.kombu import EventNotPublishedException
from buz.event.transactional_outbox import OutboxRepository, EventToOutboxRecordTranslator, OutboxCriteria
from buz.event.transactional_outbox.outbox_criteria import OutboxSortingCriteria
from buz.locator import MessageFqnNotFoundException


class TransactionalOutboxWorker:
    def __init__(
        self,
        outbox_repository: OutboxRepository,
        event_to_outbox_record_translator: EventToOutboxRecordTranslator,
        event_bus: EventBus,
        logger: Logger,
    ):
        self.__outbox_repository = outbox_repository
        self.__event_to_outbox_record_translator = event_to_outbox_record_translator
        self.__event_bus = event_bus
        self.__logger = logger

    def start(self) -> None:
        criteria = OutboxCriteria(delivered_at=None, order_by=OutboxSortingCriteria.CREATED_AT)
        for outbox_record in self.__outbox_repository.find(criteria):
            try:
                event = self.__event_to_outbox_record_translator.to_event(outbox_record)

                self.__event_bus.publish(event)
                outbox_record.mark_as_delivered()

            except (EventNotPublishedException, MessageFqnNotFoundException, Exception) as e:
                self.__logger.exception(e)
                outbox_record.mark_delivery_error()

            self.__outbox_repository.save(outbox_record)
