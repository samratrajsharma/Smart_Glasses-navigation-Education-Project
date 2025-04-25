import asyncio
import logging
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm, Agent
from livekit.plugins import openai, silero

# Enable logging to track what’s happening
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

async def entrypoint(ctx: JobContext):
    logging.info("🟡 Entry point started.")

    # Initial prompt for the LLM
    initial_ctx = llm.ChatContent().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, avoiding unpronounceable punctuation."
        ),
    )

    # Connect to the LiveKit room
    logging.info("🔌 Connecting to the room...")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logging.info("✅ Connected to room.")

    # Initialize assistant components
    assistant = Agent(
        stt=openai.STT(),
        llm=openai.LLM(chat_ctx=initial_ctx),
        tts=openai.TTS(),
        vad=silero.VAD.load(),
    )

    # Start the assistant
    logging.info("🚀 Starting assistant...")
    await assistant.start(ctx.room)
    logging.info("🎤 Assistant is active.")

    await asyncio.sleep(1)
    await assistant.say("Hey, how can I help you today?", allow_interruptions=True)
    logging.info("📣 Greeting sent.")

if __name__ == "__main__":
    logging.info("🏁 Launching voice assistant app...")
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
