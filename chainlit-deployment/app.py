"""
Chainlit + Forge Agent Integration
Main application entry point for deployment
"""
import os
import chainlit as cl

# Configuration
FORGE_AGENT_PATH = os.environ.get("FORGE_AGENT_PATH", "../forge-agent-main")


@cl.on_chat_start
async def start():
    """
    Called when a new chat session starts
    """
    welcome_msg = "👋 Welcome to the AI Assistant!\n\n"
    welcome_msg += "I can help you with various tasks. What would you like to do today?"
    
    await cl.Message(content=welcome_msg).send()


@cl.on_message
async def main(message: cl.Message):
    """
    Handle incoming messages
    This is where you'll integrate the Forge Agent
    """
    # TODO: Integrate Forge Agent here
    # When you have Claude API access, you would:
    # 1. Load the Forge Agent's CLAUDE.md system prompt
    # 2. Get conversation history from the current session
    # 3. Send to Claude API with Forge Agent context
    # 4. Handle any agent delegation/orchestration
    
    response_content = await process_message(message.content)
    
    # Send response
    await cl.Message(content=response_content).send()


async def process_message(user_message: str) -> str:
    """
    Process user message and generate response
    
    TODO: This is where you'll integrate with Claude API and Forge Agent
    For now, it returns a placeholder response
    """
    response = f"I received your message: '{user_message}'\n\n"
    response += "**Status:** Test deployment without Claude API integration.\n\n"
    response += "**When Claude API is added:**\n"
    response += "- I'll use the Forge Agent system prompt\n"
    response += "- Provide intelligent, context-aware responses\n"
    response += "- Coordinate with specialized sub-agents\n\n"
    response += "For now, this is a simple echo response to verify the deployment is working."
    
    return response


@cl.on_chat_end
def end():
    """
    Called when chat session ends
    Clean up resources
    """
    print(f"Chat session ended for user: {cl.user_session.get('username')}")


@cl.on_chat_resume
async def resume(thread: dict):
    """
    Called when a user resumes a previous conversation
    Load previous context
    """
    await cl.Message(
        content="Welcome back! Resuming your previous conversation..."
    ).send()


# Environment info (for debugging during deployment)
if __name__ == "__main__":
    print("Starting Chainlit application...")
    print(f"Forge agent path: {FORGE_AGENT_PATH}")
