from openai import OpenAI


class OpenAIClient:
    def __init__(self, model="gpt-4o-mini", api_key=None):
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.conversation_history = []

    def add_to_history(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})

    def clear_history(self):
        self.conversation_history = []

    def chat(
        self,
        system_prompt: str = None,
        user_prompt: str = None,
        temperature: float = 0.7,
    ) -> str:
        if not system_prompt and not user_prompt:
            raise ValueError("Provide at least one prompt")
        if system_prompt:
            self.add_to_history("system", system_prompt)
        if user_prompt:
            self.add_to_history("user", user_prompt)

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=temperature,
        )
        content = completion.choices[0].message.content
        self.add_to_history("system", content)
        return content
