from enum import UNIQUE, Enum, auto, verify


@verify(UNIQUE)
class CustomerStatuses(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    PENDING = auto()
    SUSPENDED = auto()


CUSTOMER_STATUSES = [
    CustomerStatuses.ACTIVE.name,
    CustomerStatuses.INACTIVE.name,
    CustomerStatuses.PENDING.name,
    CustomerStatuses.SUSPENDED.name,
]
