from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.action.nylas_send_email import (
    NylasSendEmail,
    NylasSendEmailActionConfig,
)
from vocode.streaming.action.take_a_note_action import TakeANoteActionConfig, TakeANote
from vocode.streaming.action.transfer_call import TransferCall, TransferCallActionConfig
from vocode.streaming.models.actions import ActionConfig


class ActionFactory:
    def create_action(self, action_config: ActionConfig) -> BaseAction:
        if isinstance(action_config, NylasSendEmailActionConfig):
            return NylasSendEmail(action_config, should_respond=True)
        elif isinstance(action_config, TransferCallActionConfig):
            return TransferCall(action_config)
        elif isinstance(action_config, TakeANoteActionConfig):
            return TakeANote(action_config)
        else:
            raise Exception("Invalid action type")
