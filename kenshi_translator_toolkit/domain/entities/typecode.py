from enum import IntEnum


class TypeCode(IntEnum):
    TYPE_0 = 0
    TYPE_1 = 1
    TYPE_2 = 2
    TYPE_3 = 3
    TYPE_4 = 4
    TYPE_7 = 7
    TYPE_10 = 10
    TYPE_13 = 13
    SIMPLE_HEADER = 16
    EXTENDED_HEADER = 17
    DIALOG = 19
    TYPE_21 = 21
    TYPE_46 = 46
    TYPE_51 = 51
    TYPE_62 = 62
    GAME_START = 64
    TYPE_76 = 76
    TYPE_107 = 107
    TYPE_111 = 111

    @classmethod
    def is_editable(cls, code: int) -> bool:
        try:
            return cls(code) in {
                cls.TYPE_0,
                cls.TYPE_1,
                cls.TYPE_2,
                cls.TYPE_3,
                cls.TYPE_4,
                cls.TYPE_7,
                cls.TYPE_10,
                cls.TYPE_13,
                cls.TYPE_21,
                cls.TYPE_46,
                cls.TYPE_51,
                cls.TYPE_62,
                cls.GAME_START,
                cls.TYPE_76,
                cls.TYPE_107,
                cls.TYPE_111,
            }
        except ValueError:
            return False

    @classmethod
    def is_header(cls, code: int) -> bool:
        return code in {cls.SIMPLE_HEADER, cls.EXTENDED_HEADER}
