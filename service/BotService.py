from telegram import Bot
from utils.env import get_env_variable


class BotService:
    
    def __init__(self) -> None:
        self.bot_token = get_env_variable('bot.token')
        # Create a bot instance
        self.bot = Bot(token=self.bot_token)
    


    