"""CLI entry"""

import argparse

from datetime import datetime
from functools import wraps
from vaultops.logging_config import setup_logging
from vaultops.models.credential import Credential
from vaultops.exceptions import EntryNotFoundError, StorageError, ValidationError, DuplicateEntryError
from vaultops.storage.json_storage import StorageSession
from vaultops.config import FILE_PATH, KEY_PATH


logger = setup_logging()


def log_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Running command: {func.__name__}")
        res = func(*args, **kwargs)
        logger.info(f"Finished command: {func.__name__}")
        return res
    return wrapper


@log_command
def handle_list(args, file_path = FILE_PATH, key_path = KEY_PATH) -> None:
    with StorageSession(file_path, key_path) as store:
        creds = store.list_all()

    if args.service is not None:
        creds = list(
            filter(
                lambda entry: entry.service_name.lower() == args.service.lower(),
                creds
            )
        )

    if creds == []:
        logger.info("No credentials stored.")
        return

    for entry in creds:
        logger.info(f"{entry.display_id} {entry.service_name} ({entry.username})")


def main() -> None:
    parser = argparse.ArgumentParser(prog="vaultops", description="Vaultops Started")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--entry-id", required=True)
    add_parser.add_argument("--service-name", required=True)
    add_parser.add_argument("--username", required=True)
    add_parser.add_argument("--password", required=True)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--service", required=False, default=None)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--entry-id", required=True)

    args = parser.parse_args()

    try:
        match args.command:
            case "add":
                created_at = datetime.now()

                kwargs = vars(args)
                del kwargs["command"]

                entry = Credential(
                    **kwargs,
                    created_at=created_at
                )

                with StorageSession(FILE_PATH, KEY_PATH) as store:
                    store.save(entry)

                logger.info(f"Added credential: {entry.display_id}")
            case "list":
                handle_list(args)
            case "delete":
                with StorageSession(FILE_PATH, KEY_PATH) as store:
                    store.delete(entry_id=args.entry_id)

                logger.info(f"Deleted credential: {args.entry_id}")
    except ValidationError as e:
        logger.error(e)
    except DuplicateEntryError as e:
        logger.error(e)
    except EntryNotFoundError as e:
        logger.error(e)
    except StorageError as e:
        logger.error(e)


if __name__ == "__main__": main()

