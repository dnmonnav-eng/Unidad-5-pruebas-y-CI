from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)


def test_admin_cancels_other_user_new_order():
    # Un administrador intenta cancelar un pedido NEW que pertenece a otro usuario
    created = datetime(2026, 1, 1, 10, 0, 0)
    now = datetime(2026, 1, 1, 12, 0, 0) # 2 horas de antigüedad
    # Pasamos los argumentos por posición para evitar errores de nombres de parámetros
    assert can_cancel("NEW", "user_a", "admin_user", True, created, now) == True

def test_owner_cannot_cancel_after_24_hours():
    # El propietario intenta cancelar exactamente a las 24 horas (debe denegarse)
    created = datetime(2026, 1, 1, 10, 0, 0)
    now = created + timedelta(hours=24) # Exactamente 24 horas después
    assert can_cancel("NEW", "user_a", "user_a", False, created, now) == False