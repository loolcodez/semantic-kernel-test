import os
import logging
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from app.lights_plugin import LightsPlugin

log = logging.getLogger("uvicorn.error")

class Assistant:
    def __init__(self):
        log.info("Starting assistant")
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("MODEL")
        self.kernel = Kernel()
        if not self.api_key:
            raise ValueError("API_KEY must be set in the .env file to call OpenAI.")
        if not self.model:
            raise ValueError("MODEL must be set to a valid OpenAI chat model.")
        log.info(f"Using OpenAI model: {self.model}")

        # Add OpenAI specific chat completion
        self.chat_completion = OpenAIChatCompletion(
            ai_model_id=self.model,
            api_key=self.api_key,
        )
        self.kernel.add_service(self.chat_completion)

        # Add a plugin (the LightsPlugin class is defined below)
        self.kernel.add_plugin(
            LightsPlugin(),
            plugin_name="Lights",
        )

        # Enable planning
        self.execution_settings = OpenAIChatPromptExecutionSettings() # OpenAI specific function
        self.execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

        # Create a history of the conversation
        self.history = ChatHistory()

    # Send user input to AI
    async def chat(self, user_input: str) -> str:

        log.info("User: %s", str(user_input))

        # Add user input to the history
        self.history.add_user_message(user_input)

        # Get the response from the AI
        result = await self.chat_completion.get_chat_message_content(
            chat_history=self.history,
            settings=self.execution_settings,
            kernel=self.kernel,
            arguments=KernelArguments()
        )
        log.info("AI: %s", str(result))

        # Add the message from the agent to the chat history
        self.history.add_message(result)
        return str(result)
