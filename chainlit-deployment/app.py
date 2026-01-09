"""
Chainlit + Forge Agent Integration
Main application entry point for deployment
"""
import os
import json
import sqlite3
from pathlib import Path
from typing import Optional
import chainlit as cl
from chainlit import user_session

# Configuration
FORGE_AGENT_PATH = os.environ.get("FORGE_AGENT_PATH", "../forge-agent-main")
ENABLE_AUTH = os.environ.get("ENABLE_AUTH", "true").lower() == "true"

# Database setup
DB_PATH = Path("users.db")

def init_database():
    """Initialize SQLite database for users"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username: str, password: str) -> bool:
    """Create a new user (simple version - in production, hash passwords!)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # User already exists

def verify_user(username: str, password: str) -> bool:
    """Verify user credentials"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] == password:
        return True
    return False

# Initialize database on startup
init_database()


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """
    Authentication callback for user login
    Checks against SQLite database
    """
    # Try to verify existing user
    if verify_user(username, password):
        return cl.User(
            identifier=username,
            metadata={
                "role": "user",
                "provider": "credentials"
            }
        )
    
    # If user doesn't exist, create them (auto-registration)
    # In production, you might want a separate registration flow
    if create_user(username, password):
        return cl.User(
            identifier=username,
            metadata={
                "role": "user",
                "provider": "credentials",
                "new_user": True
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
    is_new_user = user.metadata.get("new_user", False) if user else False
    
    # Store user-specific context
    cl.user_session.set("username", username)
    
    # Welcome message
    if is_new_user:
        welcome_msg = f"👋 Welcome {username}! Your account has been created.\n\n"
        welcome_msg += "I'm your AI assistant powered by Chainlit. Your conversations will be saved and you can return anytime.\n\n"
    else:
        welcome_msg = f"👋 Welcome back, {username}!\n\n"
    
    welcome_msg += "I can help you with various tasks. What would you like to do today?"
    
    await cl.Message(content=welcome_msg).send()


@cl.on_message
async def main(message: cl.Message):
    """
    Handle incoming messages
    This is where you'll integrate the Forge Agent
    """
    user = cl.user_session.get("user")
    username = cl.user_session.get("username", "Guest")
    
    # Chainlit automatically stores message history when data_persistence is enabled
    # You can access it via cl.user_session or the thread
    
    # TODO: Integrate Forge Agent here
    # When you have Claude API access, you would:
    # 1. Load the Forge Agent's CLAUDE.md system prompt
    # 2. Get conversation history from Chainlit's thread
    # 3. Send to Claude API with Forge Agent context
    # 4. Handle any agent delegation/orchestration
    
    response_content = await process_message(message.content, username)
    
    # Send response - Chainlit automatically saves it to history
    await cl.Message(content=response_content).send()


async def process_message(user_message: str, username: str) -> str:
    """
    Process user message and generate response
    
    TODO: This is where you'll integrate with Claude API and Forge Agent
    For now, it returns a placeholder response
    """
    # Placeholder response
    # When you have Claude API access, replace this with actual agent interaction
    
    response = f"I received your message: '{user_message}'\n\n"
    response += "**Status:** Test deployment without Claude API integration.\n\n"
    response += "**When Claude API is added:**\n"
    response += "- I'll use the Forge Agent system prompt\n"
    response += "- Provide intelligent, context-aware responses\n"
    response += "- Remember our conversation history\n"
    response += "- Coordinate with specialized sub-agents\n\n"
    response += f"Your username: `{username}` - Your chats are being saved!"
    
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
