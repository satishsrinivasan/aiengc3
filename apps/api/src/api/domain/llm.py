from openai import OpenAI
from groq import Groq
from google import genai


class LLMProvider:

    OPENAI: str = "OpenAI"
    GEMINI: str = "Gemini"
    GROQ: str = "Groq"

    client_factory = {
        OPENAI: lambda model, config: OpenAIClient(model, config),
        GEMINI: lambda model, config: GeminiClient(model, config),
        GROQ:   lambda model, config: GroqClient(model, config)
    }

    models: dict[str: list[str]] = {
        OPENAI: ["gpt-5-nano", "gpt-5-mini"],
        GEMINI: ["gemini-2.5-flash"],
        GROQ: ["llama-3.3-70b-versatile"]
    }

    @staticmethod
    def create_client(config, provider, model):
        return LLMProvider.client_factory[provider](model, config)

class LLMClient:

    def __init__(self, model, config):
        self.model = model
        self.config = config
        self.client = None

    def send(self, messages, max_tokens = 500) -> str:
        pass

class OpenAIClient(LLMClient):
    def __init__(self, model, config, reasoning_effort='minimal'):
        super().__init__(model, config)
        self.client = OpenAI(api_key = self.config.OPENAI_API_KEY)
        self.reasoning_effort = reasoning_effort

    def send(self, messages, max_tokens = 500) -> str:
        return self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            max_completion_tokens = max_tokens,
            reasoning_effort = 'minimal'
        ).choices[0].message.content

class GroqClient(LLMClient):
    def __init__(self, model, config):
        super().__init__(model, config)
        self.client = Groq(api_key=self.config.GROQ_API_KEY)

    def send(self, messages, max_tokens = 500, reasoning_effort = 'minimal') -> str:
        return self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            max_completion_tokens = max_tokens
        ).choices[0].message.content

class GeminiClient(LLMClient):
    def __init__(self, model, config):
        super().__init__(model, config)
        self.client = genai.Client(api_key=self.config.GOOGLE_API_KEY)

    def send(self, messages, max_tokens = 500, reasoning_effort = 'minimal') -> str:
        return self.client.models.generate_content(
            model = self.model,
            contents = [message['content'] for message in messages]
        ).text
