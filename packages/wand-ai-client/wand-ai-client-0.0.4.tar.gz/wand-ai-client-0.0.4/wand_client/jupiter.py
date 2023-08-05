from wand_client.sdk.core import WandClient


def chat(model_id: str, client: WandClient) -> None:
    chat_session = client.models.start_chat(model_id)

    print(f"You are talking to model with id {model_id}. Type 'exit' to close.")

    while True:
        prompt_text = input("> ")
        if prompt_text == "exit":
            return
        print(chat_session.ask(prompt_text))
