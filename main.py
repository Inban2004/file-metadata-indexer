# src/main.py

from database import create_tables, get_session
from scanner import scan_folder
from repository import upsert_file, delete_missing_files


def main(folder_path: str) -> None:
    # 1. Ensure tables exist
    print("Ensuring tables exist...")
    create_tables()

    session = get_session()
    scanned_paths: set[str] = set()

    try:
        # 2. Scan filesystem and upsert records
        for metadata in scan_folder(folder_path):
            upsert_file(session, metadata)
            scanned_paths.add(metadata["full_path"])

        # 3. Delete files no longer present
        delete_missing_files(session, scanned_paths)

        # 4. Commit once — atomic truth update
        session.commit()

    except Exception:
        # Any failure = rollback everything
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    # Temporary hardcoded path for v1
    main(r"C:\Users")
