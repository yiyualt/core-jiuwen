# coding: utf-8
"""Tests for BaseCard — the foundational metadata card class."""

import pytest
from pydantic import BaseModel

from jiuwen.core.common import BaseCard


class TestBaseCard:
    """Tests for BaseCard creation and behavior."""

    def test_default_construction(self):
        """BaseCard can be constructed with no arguments — all fields get defaults."""
        card = BaseCard()
        assert card.id  # auto-generated UUID hex
        assert isinstance(card.id, str)
        assert len(card.id) == 32  # UUID hex is 32 chars
        assert card.name == ""
        assert card.description == ""

    def test_construction_with_fields(self):
        """BaseCard accepts name and description."""
        card = BaseCard(name="test_card", description="A test card for unit tests.")
        assert card.name == "test_card"
        assert card.description == "A test card for unit tests."
        assert card.id  # still auto-generated

    def test_id_is_unique_per_instance(self):
        """Each BaseCard gets a unique ID."""
        card1 = BaseCard()
        card2 = BaseCard()
        assert card1.id != card2.id

    def test_custom_id(self):
        """BaseCard accepts a custom ID."""
        card = BaseCard(id="my-custom-id", name="custom")
        assert card.id == "my-custom-id"

    def test_is_pydantic_model(self):
        """BaseCard is a Pydantic BaseModel."""
        card = BaseCard()
        assert isinstance(card, BaseModel)

    def test_model_dump(self):
        """BaseCard can be serialized with model_dump()."""
        card = BaseCard(id="abc123", name="serialize_test", description="Testing serialization")
        dumped = card.model_dump()
        assert dumped == {
            "id": "abc123",
            "name": "serialize_test",
            "description": "Testing serialization",
        }

    def test_model_dump_json(self):
        """BaseCard can be serialized to JSON."""
        card = BaseCard(id="abc123", name="json_test")
        json_str = card.model_dump_json()
        assert '"id":"abc123"' in json_str
        assert '"name":"json_test"' in json_str

    def test_to_str(self):
        """to_str() returns a compact representation."""
        card = BaseCard(id="abc", name="mycard")
        assert card.to_str() == "id=abc,name=mycard"

    def test_tool_info_returns_none_by_default(self):
        """tool_info() returns None by default (bare Ellipsis body)."""
        card = BaseCard()
        assert card.tool_info() is None


class TestBaseCardSubclass:
    """Tests for subclassing BaseCard."""

    def test_subclass_inherits_fields(self):
        """Subclasses inherit id, name, description."""

        class AgentCard(BaseCard):
            version: str = "0.1.0"
            model: str = "default"

        card = AgentCard(name="my_agent", description="An agent card")
        assert card.name == "my_agent"
        assert card.description == "An agent card"
        assert card.version == "0.1.0"
        assert card.model == "default"
        assert card.id  # inherited auto-generated

    def test_subclass_can_override_tool_info(self):
        """Subclasses can provide their own tool_info()."""

        class ToolCard(BaseCard):
            parameters: dict | None = None

            def tool_info(self):
                return {
                    "name": self.name,
                    "description": self.description,
                    "parameters": self.parameters or {},
                }

        card = ToolCard(
            name="search",
            description="Search the web",
            parameters={"query": {"type": "string"}},
        )
        info = card.tool_info()
        assert info["name"] == "search"
        assert info["parameters"]["query"]["type"] == "string"


class TestBaseCardValidation:
    """Tests for Pydantic validation on BaseCard."""

    def test_id_must_be_string(self):
        """ID field validates as string."""
        with pytest.raises(Exception):  # Pydantic validation error
            BaseCard(id=123)  # type: ignore

    def test_name_must_be_string(self):
        """Name field validates as string."""
        with pytest.raises(Exception):
            BaseCard(name=123)  # type: ignore

    def test_extra_fields_are_ignored(self):
        """Extra fields not in the model are ignored by default."""
        # Pydantic v2 ignores extra fields by default
        card = BaseCard(name="test", extra_field="should_be_ignored")  # type: ignore
        assert card.name == "test"
