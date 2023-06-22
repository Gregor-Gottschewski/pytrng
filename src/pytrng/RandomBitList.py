class RandomBitList(list):
    def append(self, __object: bytes) -> None:
        if type(__object) == type(None):
            return

        if __object in self:
            print("Same bit array already in list. Skip.: " + str(__object))
            return

        super().append(__object)
