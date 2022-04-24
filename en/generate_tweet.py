from en.generate_definition import generate_definition_en


async def generate_tweet_en() -> str:
    generated: dict = await generate_definition_en(percentage=0.4)
    string: str = generated["string"].capitalize()
    type: str = generated["type"]
    definition: str = generated["definition"]
    return f"{string} ({type}): {definition}"
