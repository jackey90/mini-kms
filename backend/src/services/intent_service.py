import json
from sqlalchemy.orm import Session
from src.db.models import IntentSpace, Document


def list_intent_spaces(db: Session) -> list[IntentSpace]:
    return db.query(IntentSpace).all()


def get_intent_space(space_id: int, db: Session) -> IntentSpace:
    space = db.query(IntentSpace).filter_by(id=space_id).first()
    if not space:
        raise ValueError(f"Intent space {space_id} not found")
    return space


def create_intent_space(name: str, description: str, keywords: list[str], db: Session) -> IntentSpace:
    existing = db.query(IntentSpace).filter_by(name=name).first()
    if existing:
        raise ValueError(f"Intent space '{name}' already exists")

    space = IntentSpace(
        name=name,
        description=description,
        keywords=json.dumps(keywords),
        is_default=False,
    )
    db.add(space)
    db.commit()
    db.refresh(space)
    return space


def update_intent_space(
    space_id: int, name: str | None, description: str | None, keywords: list[str] | None, db: Session
) -> IntentSpace:
    space = get_intent_space(space_id, db)
    if name and name != space.name:
        conflict = db.query(IntentSpace).filter_by(name=name).first()
        if conflict:
            raise ValueError(f"Intent space '{name}' already exists")
        space.name = name
    if description is not None:
        space.description = description
    if keywords is not None:
        space.keywords = json.dumps(keywords)
    db.commit()
    db.refresh(space)
    return space


def delete_intent_space(space_id: int, db: Session) -> None:
    space = get_intent_space(space_id, db)
    if space.is_default:
        raise ValueError("Cannot delete default intent spaces")
    doc_count = db.query(Document).filter_by(intent_space_id=space_id).count()
    if doc_count > 0:
        raise ValueError(f"Cannot delete: {doc_count} document(s) are associated with this intent space")
    db.delete(space)
    db.commit()


def get_document_count(space_id: int, db: Session) -> int:
    return db.query(Document).filter_by(intent_space_id=space_id).count()
