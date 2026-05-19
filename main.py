#!/usr/bin/env python3
"""
Hermes Agent - Main entry point

A fork of NousResearch/hermes-agent with custom tool support.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("hermes-agent")


def get_required_env(key: str) -> str:
    """Fetch a required environment variable or exit with an error."""
    value = os.getenv(key)
    if not value:
        logger.error(f"Required environment variable '{key}' is not set.")
        sys.exit(1)
    return value


def build_agent():
    """
    Build and return the Hermes agent with all registered tools.
    Imports are deferred so missing deps surface as clear errors.
    """
    try:
        from agent import HermesAgent
        from tools import load_tools
    except ImportError as exc:
        logger.error(f"Failed to import agent modules: {exc}")
        sys.exit(1)

    model_name = os.getenv("MODEL_NAME", "NousResearch/Hermes-3-Llama-3.1-8B")
    api_base = os.getenv("OPENAI_API_BASE", "http://localhost:8000/v1")
    api_key = os.getenv("OPENAI_API_KEY", "EMPTY")

    tools = load_tools()
    agent = HermesAgent(
        model=model_name,
        api_base=api_base,
        api_key=api_key,
        tools=tools,
    )
    logger.info(f"Agent initialised with model='{model_name}' and {len(tools)} tool(s).")
    return agent


def interactive_loop(agent) -> None:
    """Run a simple REPL for chatting with the agent."""
    print("\nHermes Agent ready. Type 'exit' or 'quit' to stop.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            response = agent.chat(user_input)
            print(f"\nHermes: {response}\n")
        except Exception as exc:  # noqa: BLE001
            logger.error(f"Error during agent chat: {exc}")


def main() -> None:
    """Entry point."""
    logger.info("Starting Hermes Agent...")
    agent = build_agent()
    interactive_loop(agent)


if __name__ == "__main__":
    main()
