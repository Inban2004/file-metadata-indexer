# src/repository.py

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from orm import FileInfo


def upsert_file(session: Session, metadata: dict) -> None:
    """
    Insert or update a single file record based on full_path.
    """
    try:
        if session is None:
            raise ValueError("session cannot be None")
        if metadata is None:
            raise ValueError("metadata cannot be None")

        now = datetime.utcnow()

        record = (
            session.query(FileInfo)
            .filter(FileInfo.full_path == metadata["full_path"])
            .one_or_none()
        )

        if record is None:
            record = FileInfo(
                full_path=metadata["full_path"],
                file_name=metadata["file_name"],
                extension=metadata["extension"],
                size_bytes=metadata["size_bytes"],
                created_at=metadata["created_at"],
                modified_at=metadata["modified_at"],
                last_scanned_at=now,
            )
            session.add(record)
            return

        changed = False

        for field in (
            "file_name",
            "extension",
            "size_bytes",
            "created_at",
            "modified_at",
        ):
            new_value = metadata[field]
            if getattr(record, field) != new_value:
                setattr(record, field, new_value)
                # changed = True

        record.last_scanned_at = now
    except KeyError as exc:
        raise ValueError(f"Missing required metadata key: {exc}") from exc
    except (TypeError, AttributeError) as exc:
        raise ValueError(f"Invalid metadata/session provided: {exc}") from exc
    except SQLAlchemyError as exc:
        raise RuntimeError(f"Database error while upserting file: {exc}") from exc


def delete_missing_files(session: Session, scanned_paths: set[str]) -> int:
    """
    Delete DB records for files that were not seen in the current scan.
    """
    try:
        if session is None:
            raise ValueError("session cannot be None")
        
        if not scanned_paths:
            raise ValueError("scanned_paths is empty — refusing to delete all records")

        deleted = (
            session.query(FileInfo)
            .filter(FileInfo.full_path.notin_(scanned_paths))
            .delete(synchronize_session=False)
        )
        
        return deleted
    except (TypeError, AttributeError) as exc:
        raise ValueError(f"Invalid scanned_paths/session provided: {exc}") from exc
    except SQLAlchemyError as exc:
        raise RuntimeError(f"Database error while deleting missing files: {exc}") from exc
