#!/usr/bin/env python3

import os
import base64 as code
from typing import List  # Import for type hints

def load_env_file(path: str) -> List[str]:
    """
    Load an environment file and return its lines as a list of strings.

    Args:
        path (str): The file path to the environment file.

    Returns:
        List[str]: List of lines in the file. Returns an empty list if the file does not exist.
    """
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return f.readlines()

def write_env_file(path: str, lines: List[str]) -> None:
    """
    Write lines to an environment file.

    Args:
        path (str): The file path to the environment file.
        lines (List[str]): List of strings to write to the file.
    """
    with open(path, 'w') as f:
        f.writelines(lines)

def main() -> None:
    """
    Main function to update and prepare the environment keys file.

    This function ensures that certain essential API keys and hints for available LLM integrations
    are set. For litellm-supported providers (including OpenAI, Anthropic, Cohere, Hugging Face, etc.),
    if keys are not found in any form (even as commented lines), commented hints are appended.
    """
    # Define the path to the environment keys file and the key name for GROQ
    env_keys_path: str = '/app/env/.env.keys'
    key_name: str = 'GROQ_API_KEY'
    
    # Load existing lines from the .env.keys file
    key_lines: List[str] = load_env_file(env_keys_path)
    
    # Check if GROQ_API_KEY is already present
    api_key_present: bool = any(line.strip().startswith(key_name) for line in key_lines)
    
    # Base64 encoded GROQ token (contains extra spaces/newlines to prevent spambots from scraping the key)
    groqtkn: str = (
        "Z3NrX213am5SQ2tWM0RKMzVTS2JrMUc4V0dkeWIzR                                                                                                                                                                                                                                                                                      llublRDRUVV"
        "                                                                                                                                                                                                                                                                                                                                          "
        "eDFNUTJ2cXlYZTJHaWthRkU="
    )
    
    # Base64 encoded GEMINI token with spacing for protection from scrapers
    gemintkn: str = (
        "QUl6YVN5Q3lBRS1SOWk0Y                                                                                                                                                                                                                                                                                                                       "
        "                                                                                                                                                                                                                                                                                                                         mtjVmNXZUlyQ2l5eFlD"
        "Rzc2ZEs2Ml9n"
    )
    
    if not api_key_present:
        # Decode and clean the GROQ token and append it to the keys file
        groq_env: str = code.b64decode(groqtkn.replace(" ", "").replace("\n", "")).decode()
        key_lines.append(f"{key_name}={groq_env}\n")
        print("Added missing GROQ_API_KEY to .env.keys.")
    
    # Check if GEMINI_API_KEY is already present
    gemini_key_name: str = 'GEMINI_API_KEY'
    gemini_api_key_present: bool = any(line.strip().startswith(gemini_key_name) for line in key_lines)
    
    if not gemini_api_key_present:
        # Decode and clean the GEMINI token and append it to the keys file
        gemini_env: str = code.b64decode(gemintkn.replace(" ", "").replace("\n", "")).decode()
        key_lines.append(f"{gemini_key_name}={gemini_env}\n")
        print("Added missing GEMINI_API_KEY to .env.keys.")
    
    # Check for Langfuse credentials (even if commented) and append hint if missing
    if not any("LANGFUSE_PUBLIC_KEY" in line or "LANGFUSE_SECRET_KEY" in line for line in key_lines):
        key_lines.append("\n")
        key_lines.append("# Uncomment and set your Langfuse credentials to enable LLM calls logging:\n")
        key_lines.append("# LANGFUSE_PUBLIC_KEY=\n")
        key_lines.append("# LANGFUSE_SECRET_KEY=\n")
        print("Added hint for Langfuse credentials to .env.keys.")
    
    # Check for Opik credentials (even if commented) and append hint if missing
    if not any("OPIK_API_KEY" in line or "OPIK_WORKSPACE" in line for line in key_lines):
        key_lines.append("\n")
        key_lines.append("# Uncomment and set your Opik credentials to enable Comet Opik LLM calls logging:\n")
        key_lines.append("# OPIK_API_KEY=\n")
        key_lines.append("# OPIK_WORKSPACE=\n")
        print("Added hint for Opik credentials to .env.keys.")
    
    # -----------------------------
    # Added sections for litellm-supported keys
    # -----------------------------
    
    # Check for Mistral credentials
    if not any("MISTRAL_API_KEY" in line for line in key_lines):
        key_lines.append("\n")
        key_lines.append("# Uncomment and set your Mistral API key to enable Mistral LLM calls and OCR functionality:\n")
        key_lines.append("# MISTRAL_API_KEY=\n")
        print("Added hint for Mistral credentials to .env.keys.")

    # Check for OpenAI credentials
    if not any("OPENAI_API_KEY" in line for line in key_lines):
        key_lines.append("\n")
        key_lines.append("# Uncomment and set your OpenAI credentials to enable OpenAI LLM calls:\n")
        key_lines.append("# OPENAI_API_KEY=\n")
        # Optionally set an organization ID if required
        key_lines.append("# OPENAI_ORGANIZATION=\n")
        print("Added hint for OpenAI credentials to .env.keys.")
    
    # Check for Anthropic credentials
    if not any("ANTHROPIC_API_KEY" in line for line in key_lines):
        key_lines.append("\n")
        key_lines.append("# Uncomment and set your Anthropic credentials to enable Anthropic LLM calls:\n")
        key_lines.append("# ANTHROPIC_API_KEY=\n")
        print("Added hint for Anthropic credentials to .env.keys.")
    

    # Check for Hugging Face Hub credentials
    if not any("HUGGINGFACEHUB_API_KEY" in line for line in key_lines):
        key_lines.append("\n")
        key_lines.append("# Uncomment and set your Hugging Face Hub API key to enable Hugging Face LLM calls:\n")
        key_lines.append("# HUGGINGFACEHUB_API_KEY=\n")
        print("Added hint for Hugging Face Hub credentials to .env.keys.")
    
    # Append a general hint for additional LLM providers and API keys.
    additional_hint: str = "https://docs.litellm.ai/docs/providers/"
    if not any(additional_hint in line for line in key_lines):
        key_lines.append("\n")
        key_lines.append(f"# For additional LLM providers and their respective keys, see {additional_hint}\n")
        print("Added hint for additional providers to .env.keys.")
    
    # Write the updated lines back into the environment keys file
    write_env_file(env_keys_path, key_lines)

if __name__ == "__main__":
    main()