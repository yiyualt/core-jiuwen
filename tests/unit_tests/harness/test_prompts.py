# coding: utf-8
"""Tests for PromptBuilder and sections."""

from jiuwen.harness.prompts.base import BaseSection
from jiuwen.harness.prompts.builder import PromptBuilder, default_builder
from jiuwen.harness.prompts.sections import (
    IdentitySection,
    ToolsSection,
    SafetySection,
    WorkspaceSection,
)


class TestSections:
    def test_identity(self):
        text = IdentitySection().build({})
        assert "expert software engineer" in text

    def test_identity_custom_role(self):
        text = IdentitySection(role="a Python specialist").build({})
        assert "Python specialist" in text

    def test_tools(self):
        text = ToolsSection().build({})
        assert "bash" in text
        assert "read" in text
        assert "write" in text

    def test_safety(self):
        text = SafetySection().build({})
        assert "destructive" in text

    def test_workspace(self):
        text = WorkspaceSection().build({"workspace": "/my/project"})
        assert "/my/project" in text


class TestPromptBuilder:
    def test_empty_builder(self):
        builder = PromptBuilder()
        assert builder.build({}) == ""

    def test_add_section(self):
        builder = PromptBuilder()
        builder.add_section(IdentitySection())
        assert "engineer" in builder.build({})

    def test_multiple_sections(self):
        builder = PromptBuilder([IdentitySection(), SafetySection()])
        result = builder.build({})
        assert "engineer" in result
        assert "destructive" in result

    def test_custom_section(self):
        class GreetingSection(BaseSection):
            def build(self, context):
                return f"Hello, {context.get('name', 'world')}!"

        builder = PromptBuilder([GreetingSection()])
        assert builder.build({"name": "Alice"}) == "Hello, Alice!"

    def test_default_builder(self):
        result = default_builder.build({"workspace": "/tmp"})
        assert "engineer" in result
        assert "bash" in result
        assert "Safety" in result
        assert "/tmp" in result
