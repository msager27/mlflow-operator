"""Skill Registry validation functions."""

from ..shared import TestContext
from .validation_utils import (
    validate_resource_retrieved_or_created,
)


def validate_skill_created(test_context: TestContext) -> None:
    validate_resource_retrieved_or_created(
        test_context=test_context,
        resource_field="active_skill_name",
        resource_type="Skill",
        operation="creation",
    )


def validate_skill_retrieved(test_context: TestContext) -> None:
    validate_resource_retrieved_or_created(
        test_context=test_context,
        resource_field="active_skill_name",
        resource_type="Skill",
        operation="retrieval",
    )


def validate_skill_search_excludes_other_workspace(
    test_context: TestContext,
) -> None:
    if test_context.last_error is not None:
        raise AssertionError(
            f"Skill search failed: {test_context.last_error.error.message}"
        )

    returned_names = {
        skill.name for skill in test_context.skill_search_results or []
    }
    if test_context.active_skill_name in returned_names:
        raise AssertionError(
            f"Skill {test_context.active_skill_name!r} from another workspace "
            "was returned by search"
        )


def validate_skill_search_includes_active_skill(
    test_context: TestContext,
) -> None:
    if test_context.last_error is not None:
        raise AssertionError(
            f"Skill search failed: {test_context.last_error.error.message}"
        )

    returned_names = {
        skill.name for skill in test_context.skill_search_results or []
    }
    if test_context.active_skill_name not in returned_names:
        raise AssertionError(
            f"Skill {test_context.active_skill_name!r} was not returned by search"
        )


def validate_skill_artifact_registered(test_context: TestContext) -> None:
    if test_context.last_error is not None:
        raise AssertionError(
            f"Skill registration failed: {test_context.last_error.error.message}"
        )

    source = test_context.active_skill_source
    artifact_uri = getattr(source, "artifact_path", None) or str(source or "")
    if not artifact_uri.startswith("mlflow-artifacts:/skills/"):
        raise AssertionError(
            f"Expected an MLflow Skill artifact source, got {source!r}"
        )


def validate_skill_artifact_read(test_context: TestContext) -> None:
    if test_context.last_error is not None:
        raise AssertionError(
            f"Skill artifact read failed: {test_context.last_error.error.message}"
        )

    if (
        test_context.active_skill_artifact_content
        != test_context.expected_skill_artifact_content
    ):
        raise AssertionError("Downloaded Skill artifact content did not match")
