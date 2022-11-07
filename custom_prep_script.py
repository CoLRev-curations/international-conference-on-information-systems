#!/usr/bin/env python3
"""Template for a custom Prep PackageEndpoint"""
from __future__ import annotations

from typing import TYPE_CHECKING

import timeout_decorator
import zope.interface
from dacite import from_dict

import colrev.operation

if TYPE_CHECKING:
    import colrev.ops.prep

# pylint: disable=too-few-public-methods


@zope.interface.implementer(colrev.env.package_manager.PrepPackageEndpointInterface)
class CustomPrep:
    """Class for custom prep scripts"""

    source_correction_hint = "check with the developer"
    always_apply_changes = True
    settings_class = colrev.env.package_manager.DefaultSettings

    def __init__(
        self,
        *,
        prep_operation: colrev.ops.prep.Prep,  # pylint: disable=unused-argument
        settings: dict,
    ) -> None:
        self.settings = from_dict(data_class=self.settings_class, data=settings)

    # @timeout_decorator.timeout(60, use_signals=False)
    def prepare(
        self,
        prep_operation: colrev.ops.prep.Prep,  # pylint: disable=unused-argument
        record: colrev.record.Record,
    ) -> colrev.record.Record:
        """Update record (metadata)"""

        if "author" in record.data:
            if "Paper, Research and " in record.data["author"]:
                record.data["author"] = record.data["author"].replace("Paper, Research and ", "")

            if "Research, Completed and " in record.data["author"]:
                record.data["author"] = record.data["author"].replace("Research, Completed and ", "")

            if "Research, Paper and " in record.data["author"]:
                record.data["author"] = record.data["author"].replace("Research, Paper and ", "")

            if "Paper, Research" == record.data["author"]:
                record.update_field(key="author", value="UNKNOWN", source="pdf_source_prep_script", note="missing")

        if "title" in record.data:
            if record.data["title"].endswith(" Research in Progress"):
                record.data["title"] = record.data["title"].replace(" Research in Progress", "")
            if record.data["title"].endswith(" Research Paper"):
                record.data["title"] = record.data["title"].replace(" Research Paper", "")
            if record.data["title"].endswith(" Research paper"):
                record.data["title"] = record.data["title"].replace(" Research paper", "")
            if record.data["title"].endswith(" Full Paper"):
                record.data["title"] = record.data["title"].replace(" Full Paper", "")
            if record.data["title"].endswith(" Full Papers"):
                record.data["title"] = record.data["title"].replace(" Full Papers", "")
            if record.data["title"].endswith(" Short Paper"):
                record.data["title"] = record.data["title"].replace(" Short Paper", "")

                


        return record


if __name__ == "__main__":
    pass
