import enum

class StatusTypes(enum.Enum):
    saved = 'Saved'
    applied = 'Applied'
    interviewing = 'interviewing'
    hired = 'Hired'
    rejected = 'Rejected'
    archived = 'Archived'