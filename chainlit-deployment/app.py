"""
Chainlit + Forge Agent Integration
Main application entry point for deployment
"""
import os
import chainlit as cl
from typing import Optional

# Configuration
FORGE_AGENT_PATH = os.environ.get("FORGE_AGENT_PATH", "../forge-agent-main")
ENABLE_AUTH = os.environ.get("ENABLE_AUTH", "true").lower() == "true"


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """
    Authentication callback for user login
    In production, replace with real database authentication
    """
    # TODO: Replace with actual database authentication
    # For now, this is a placeholder that accepts any login
    # You'll want to integrate with WordPress users or a separate auth system
    
    if username and password:
        return cl.User(
            identifier=username,
            metadata={
                "role": "user",
                "provider": "credentials"
            }
        )
    return None


@cl.on_chat_start
async def start():
    """
    Called when a new chat session starts
    Initialize user context and session
    """
    user = cl.user_session.get("user")
    username = user.identifier if user else "Guest"
    
    # Store user-specific context
    cl.user_session.set("username", username)
    cl.user_session.set("conversation_history", [])
    
    # Welcome message
    await cl.Message(
        content=f"👋 Welcome {username}! I'm your AI assistant powered by Chainlit.\n\n"
                f"I can help you with various tasks. What would you like to do today?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """
    Handle incoming messages
    This is where you'll integrate the Forge Agent
    """
    user = cl.user_session.get("user")
    username = cl.user_session.get("username", "Guest")
    
    # Get conversation history
    history = cl.user_session.get("conversation_history", [])
    history.append({"role": "user", "content": message.content})
    
    # TODO: Integrate Forge Agent here
    # For now, simple echo response
    # When you have Claude API access, you would:
    # 1. Load the Forge Agent's CLAUDE.md system prompt
    # 2. Send user message + history to Claude API
    # 3. Process the response
    # 4. Handle any agent delegation/orchestration
    
    response_content = await process_message(message.content, history, username)
    
    # Store assistant response in history
    history.append({"role": "assistant", "content": response_content})
    cl.user_session.set("conversation_history", history)
    
    # Send response
    await cl.Message(content=response_content).send()


async def process_message(user_message: str, history: list, username: str) -> str:
    """
    Process user message and generate response
    
    TODO: This is where you'll integrate with Claude API and Forge Agent
    For now, it returns a placeholder response
    """
    # Placeholder response
    # When you have Claude API access, replace this with actual agent interaction
    
    response = f"I received your message: '{user_message}'\n\n"
    response += "**Note:** This is a test deployment without Claude API integration.\n\n"
    response += "Once you have Claude API access, this will connect to the Forge Agent and provide intelligent responses.\n\n"
    response += f"Your user context is being tracked (username: {username}, messages in history: {len(history)})"
    
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
    username = cl.user_session.get("username", "Guest")
    await cl.Message(
        content=f"Welcome back, {username}! Resuming your previous conversation..."
    ).send()


# Environment info (for debugging during deployment)
if __name__ == "__main__":
    print("Starting Chainlit application...")
    print(f"Auth enabled: {ENABLE_AUTH}")
    print(f"Forge agent path: {FORGE_AGENT_PATH}")
