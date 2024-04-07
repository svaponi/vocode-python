import tempfile
import time
import typing
from typing import Optional, Type

from pydantic.v1 import BaseModel, Field

from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import (
    ActionConfig,
    ActionInput,
    ActionOutput,
    ActionType,
)


class TakeANoteActionConfig(ActionConfig, type=ActionType.TAKE_A_NOTE):
    pass


class TakeANoteParameters(BaseModel):
    text: str = Field(..., description="The text content of the note.")
    filename: Optional[str] = Field(
        None, description="The filename where the note is stored."
    )


class TakeANoteResponse(BaseModel):
    success: bool
    filepath: typing.Optional[str]


class TakeANote(
    BaseAction[TakeANoteActionConfig, TakeANoteParameters, TakeANoteResponse]
):
    description: str = "Takes a note."
    parameters_type: Type[TakeANoteParameters] = TakeANoteParameters
    response_type: Type[TakeANoteResponse] = TakeANoteResponse

    async def run(
        self, action_input: ActionInput[TakeANoteParameters]
    ) -> ActionOutput[TakeANoteResponse]:
        print("Taking a note")
        print(f"Text: {action_input.params.text}")
        print(f"Filename: {action_input.params.filename}")

        filename = action_input.params.filename or f"note-{int(time.time())}.txt"
        filepath = f"{tempfile.gettempdir()}/{filename}"
        with open(filepath, "w+") as f:
            f.write(action_input.params.text)

        print("Note taken")
        print(f"Filepath: {filepath}")

        return ActionOutput(
            action_type=self.action_config.type,
            response=TakeANoteResponse(success=True, filepath=filepath),
        )
