import enum


class UserType(enum.Enum):
    STUDENT = 0
    SUPERVISOR = 1
    HOD = 2
    AD = 3
    PSD = 4


class TransferType(enum.Enum):
    PS2TS = 0
    TS2PS = 1


class CampusType(enum.Enum):
	GOA = 0
	HYD = 1
	PILANI = 2


class ApplicationsStatus(enum.Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
