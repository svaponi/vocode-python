import asyncio
import logging
import os
import signal

from dotenv import load_dotenv

from vocode.helpers import create_streaming_microphone_input_and_speaker_output
from vocode.streaming.action.take_a_note_action import TakeANoteActionConfig
from vocode.streaming.agent import *
from vocode.streaming.models.agent import *
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.synthesizer import *
from vocode.streaming.models.transcriber import *
from vocode.streaming.streaming_conversation import StreamingConversation
from vocode.streaming.synthesizer import *
from vocode.streaming.transcriber import *

load_dotenv()
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def main():
    (
        microphone_input,
        speaker_output,
    ) = create_streaming_microphone_input_and_speaker_output(
        use_default_devices=False,
        # NOTE: input must not be able to hear output device, or you'll get interference (bot replying to itself)
        input_device_name=os.getenv("INPUT_DEVICE_NAME", None),
        output_device_name=os.getenv("OUTPUT_DEVICE_NAME", None),
        logger=logger,
        use_blocking_speaker_output=True,  # this moves the playback to a separate thread, set to False to use the main thread
    )

    conversation = StreamingConversation(
        output_device=speaker_output,
        transcriber=GoogleTranscriber(
            GoogleTranscriberConfig.from_input_device(
                microphone_input,
            )
        ),
        agent=ChatGPTAgent(
            ChatGPTAgentConfig(
                initial_message=BaseMessage(text="What's up"),
                prompt_preamble="""The AI is having a pleasant conversation about life""",
                actions=[TakeANoteActionConfig()],
            )
        ),
        synthesizer=GoogleSynthesizer(
            GoogleSynthesizerConfig.from_output_device(speaker_output)
        ),
        logger=logger,
    )
    await conversation.start()
    print("Conversation started, press Ctrl+C to end")
    signal.signal(
        signal.SIGINT, lambda _0, _1: asyncio.create_task(conversation.terminate())
    )
    while conversation.is_active():
        chunk = await microphone_input.get_audio()
        conversation.receive_audio(chunk)


if __name__ == "__main__":
    asyncio.run(main())
