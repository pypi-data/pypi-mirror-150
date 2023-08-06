from typing import List, Match, Optional, Union

from sikriml.models.ner import ScoreLabel

from .abstracts.regex_handler import RegexHandler
from .abstracts.regex_handler_decorator import RegexHandlerDecorator


class YearHandler(RegexHandlerDecorator):
    def __init__(self, handler: Optional[RegexHandler] = None):
        super().__init__(handler)

    @property
    def regex(self) -> Union[str, List[str]]:
        return r"(?<!\S)-?(19|20)\d{2}?(([']|\w?)\w?)\b"

    def get_label(self, match: Match[str]) -> str:
        year_matches = self._match_regexes(match.group(), self.regex)
        if len(year_matches) > 0:
            return ScoreLabel.YEAR
        return (
            self._handler.get_label(match)
            if self._handler
            else ScoreLabel.YEAR
        )
