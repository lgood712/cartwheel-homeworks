from __future__ import annotations

from agent import db, tools
from agent.agent import TOOLS_BY_ROLE
from agent.auth import AuthContext


def test_get_product_returns_public_catalog_record() -> None:
    ctx = AuthContext(user_id=1, role="shopper")
    result = tools.get_product(ctx, 1)

    assert result == {
        "ok": True,
        "product_id": 1,
        "store_id": 1,
        "title": "Heavy-Duty Vase",
        "category": "home_and_kitchen",
        "price_usd": 298.0,
    }


def test_get_product_unknown_id_is_not_found() -> None:
    result = tools.get_product(AuthContext(user_id=9501, role="support"), 999999)
    assert result["ok"] is False
    assert result["error"] == "not_found"


def test_get_product_is_registered_for_every_role() -> None:
    assert all(
        any(tool.name == "get_product" for tool in role_tools)
        for role_tools in TOOLS_BY_ROLE.values()
    )
