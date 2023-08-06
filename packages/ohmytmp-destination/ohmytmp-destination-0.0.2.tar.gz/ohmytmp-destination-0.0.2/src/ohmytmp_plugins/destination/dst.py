from ohmytmp import TYPE, Info, PluginDestination


class DstType(PluginDestination):
    def __init__(self, dst: str, level: int = -1) -> None:
        super().__init__(dst, level)
        self.data = dict()

    def mkdirs(self) -> None:
        super().mkdirs()
        for i in TYPE.to_dict().values():
            self.mkdir(self.join(i))

    def get_dst(self, _info: Info) -> str:
        ans = self.join(_info.TYPE)
        self.data[_info.SRC] = ans
        return ans
