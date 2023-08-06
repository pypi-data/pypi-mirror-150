import re
from enum import Enum
from typing import Optional, ClassVar, AnyStr


class ExophoraReferentType(Enum):
    WRITER = "著者"
    READER = "読者"
    UNSPECIFIED_PERSON = "不特定:人"
    UNSPECIFIED_MATTER = "不特定:物"
    UNSPECIFIED_SITUATION = "不特定:状況"
    PREVIOUS_SENTENCE = "前文"
    NEXT_SENTENCE = "後文"


class ExophoraReferent:
    _NUM2ZEN: dict[int, str] = {0: "０", 1: "１", 2: "２", 3: "３", 4: "４", 5: "５", 6: "６", 7: "７", 8: "８", 9: "９"}
    PAT: ClassVar[re.Pattern[str]] = re.compile(
        rf"^({'|'.join(t.value for t in ExophoraReferentType)})(?P<index>[0-9０-９]*)$"
    )

    def __init__(self, text: str) -> None:
        match: Optional[re.Match[AnyStr]] = self.PAT.match(text)
        if match is None:
            raise ValueError(f"invalid exophora referent: {text}")
        self.index: Optional[str] = match.group("index")
        self.type = ExophoraReferentType(text)

    @property
    def text(self) -> str:
        return self.type.value + "".join(self._NUM2ZEN[int(n)] for n in self.index)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(text={repr(self.text)})"
