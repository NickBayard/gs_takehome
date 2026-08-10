from __future__ import annotations

from abc import ABC, abstractmethod
from greatsky.db import BaseKVDB
from greatsky.db.orm.base import DatabaseEntry
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class DeviceModel(BaseModel):
    active_session_id: str | None = None
    # Input ids and output ids must all be unique.
    # An input id cannot be the same as an output id.
    # This allows edges to connect inputs to inputs and
    # outputs to outputs.
    input_ids: list[str] = Field(default_factory=list)
    output_ids: list[str] = Field(default_factory=list)
    # each tuple in edge_ids is an edge connection
    # each end of the edge may be a input or output
    # honestly, I'm not sure if it's value to connect an
    # output to an input, so I'm bypasing validation for that here
    edge_ids: list[tuple[str, str]] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid')

    @model_validator(mode='after')
    def validate_ids(self) -> DeviceModel:
        # Validate the DeviceModel input/output/edge_ids after the
        # class has been constructed.
        
        # We don't just convert a list to set to find duplicates
        # here so that we can return the duplicates to the user.
        def duplicates(ids: list[str]) -> list[str]:
            seen = set()
            duplicates = set()
            for item in ids:
                if item in seen:
                    duplicates.add(item)
                    continue
                seen.add(item)
            return list(duplicates)
                
        # input_ids must be unique
        errors = []
        input_duplicates = duplicates(self.input_ids)
        if input_duplicates:
            errors.append(f'Duplicates found in input_ids: {input_duplicates}')
            
        # output_ids must be unique
        output_duplicates = duplicates(self.output_ids)
        if output_duplicates:
            errors.append(f'Duplicates found in output_ids: {output_duplicates}')

        # The set of input and output ids must not overlap
        # NOTE: If there were input or output id duplicates, they
        # will show up here again.
        all_ids = self.input_ids + self.output_ids
        if not errors:
            all_duplicates = duplicates(all_ids)
            if all_duplicates:
                errors.append(f'Dupicates found between input and output ids: {all_duplicates}')

        # Check that all edge_ids are found in input and output ids
        missing_edges = []
        for a, b in self.edge_ids:
            if a not in all_ids or b not in all_ids:
                missing_edges.append((a,b))

        if missing_edges:
            errors.append(f'Invalid edges. Must contain only input_ids or output_ids: {missing_edges}')

        if errors:
            raise Exception('\n'.join(errors))

        return self


class Device(DatabaseEntry):
    @classmethod
    def get_label(cls) -> str:
        return "Device"

    @classmethod
    def get_model_type(cls) -> type[BaseModel]:
        return DeviceModel