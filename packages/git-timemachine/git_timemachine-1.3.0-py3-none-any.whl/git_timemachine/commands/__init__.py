from .log import log_command
from .commit import commit_command
from .switch_date import switch_date_command
from .migrate import migrate_command

command_group = [log_command, commit_command, switch_date_command, migrate_command]
