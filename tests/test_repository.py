from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain import Order
from src.repository import OrderRow, SqlOrderRepository, make_engine


def test_repository_commit():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(1, Order(120))
        session.commit()
        assert session.scalar(select(OrderRow).where(OrderRow.id == 1)).total == 120

def test_repository_rollback():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(1, Order(120))
        session.rollback()
        assert session.scalar(select(OrderRow).where(OrderRow.id == 1)) is None

def test_repository_commit_custom_order():
    engine = make_engine()
    with Session(engine) as session:
        repo = SqlOrderRepository(session)
        order = Order(250)
        repo.save(2, order)
        session.commit()
    
    with Session(engine) as session:
        # Consultamos directamente usando session.get(OrderRow, 2) como lo hace el resto de pruebas
        row = session.get(OrderRow, 2)
        assert row is not None
        assert row.id == 2
        assert row.total == 250.0
        assert row.status == "NEW"
