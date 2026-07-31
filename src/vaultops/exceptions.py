"""vaultops exceptions module"""


class VaultOpsError(Exception):
    """The Base Exception"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ValidationError(VaultOpsError):
    """Validation Error Exception"""


class StorageError(VaultOpsError):
    """Storage Error Exception"""


class DuplicateEntryError(StorageError):
    """Duplicate Entry Error Exception"""


class EntryNotFoundError(StorageError):
    """Entry Not Found Error Exception"""


class SecurityError(VaultOpsError):
    """Security Error"""

