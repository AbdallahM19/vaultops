"""CLI entry"""

import argparse

from datetime import datetime
from vaultops.logging_config import setup_logging
from vaultops.models.credential import Credential
from vaultops.exceptions import EntryNotFoundError, StorageError, ValidationError, DuplicateEntryError
from vaultops.storage.json_storage import JsonCredentialStorage


logger = setup_logging()


def main() -> None:
    parser = argparse.ArgumentParser(prog="vaultops", description="Vaultops Started")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--entry-id", required=True)
    add_parser.add_argument("--service-name", required=True)
    add_parser.add_argument("--username", required=True)
    add_parser.add_argument("--password", required=True)

    list_parser = subparsers.add_parser("list")

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

                JsonCredentialStorage("data/credentials.json").save(entry)

                logger.info(f"Added credential: {entry.display_id}")
            case "list":
                creds = JsonCredentialStorage("data/credentials.json").list_all()

                if creds == []:
                    logger.info("No credentials stored.")
                    return

                for entry in creds:
                    logger.info(f"{entry.display_id} {entry.service_name} ({entry.username})")
            case "delete":
                JsonCredentialStorage("data/credentials.json").delete(entry_id=args.entry_id)

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

