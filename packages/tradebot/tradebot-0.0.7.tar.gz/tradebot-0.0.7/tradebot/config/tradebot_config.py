from __future__ import annotations
import os
from pathlib import Path
from typing import Mapping

from tradebot.utils import fileutils
from tradebot.utils.utils import singleton, check_singleton
import tradebot.backend.tradebot as tradebot


@singleton
class TradeBotConfigs:

    __valid_keys = {
        "consumer_key",
        "access_token",
        "refresh_token",
        "scope",
        "expires_in",
        "refresh_token_expires_in",
        "token_type",
    }


    @staticmethod
    def get_config(config_file:Path) -> TradeBotConfigs:
        if TradeBotConfigs.__instance:
            return TradeBotConfigs.__instance
        else:
            self = TradeBotConfigs()
            self.__settings_file = config_file.absolute()
            self.__data = fileutils.read(self.__settings_file, fileutils.yml_to_dict)
            TradeBotConfigs.__instance = self
            return self


    @check_singleton
    def get(self, key:str) -> str:
        return self.__data.get(key)


    @check_singleton
    def update(self, new_data:Mapping[str, str]) -> None:
        if not self.__validate_data(new_data):
            raise 
        self.__data.update(new_data)


    @check_singleton
    def write_new_access_token(self, bot:tradebot.TradeBot) -> None:
        new_data = bot.post_access_token()
        self.update(new_data) #update self.__data
        fileutils.update_yml(self.__settings_file, self.__data)


    @check_singleton
    def __validate_data(self, new_data:Mapping[str, str]) -> bool:
        for key in new_data:
            if key not in self.__valid_keys:
                return False

        return True