from enum import Enum

from .email import create_dataflow_job_for_sending_emails, trigger_welcome_email


class CHANNEL(str, Enum):
    EMAIL = 'email'
    WHATSAPP = 'whatsapp'
