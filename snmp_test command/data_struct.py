class Field:
    """
    Field(fname='iswStpPortPriority', val=240, dtype='int')
    Field(fname='iswStpPortEnable', val=0)                   # default is 'int'
    Field(fname='iswStpPortEnable', val="abc", dtype='str')  # is str
    """

    def __init__(self, fname, val, dtype='int'):
        self.fname = fname
        self.val = val
        self.dtype = dtype

    def idx(self, idx: int):
        res = ""
        if self.dtype == 'int':
            res = f"{self.fname}.{idx} = {self.val} "
        elif self.dtype == 'str':
            res = f"{self.fname}.{idx} = \"{self.val}\" "
        elif self.dtype == 'ip':
            res = f"{self.fname}.{idx} = {self.val} "
        # elif self.dtype == 'OTHER_DTYPE':
        #    res = f"{self.fname}.{idx} x \"{self.val}\""
        else:
            raise NotImplementedError("not support dtype:", self.dtype)

        return res


class Recoder_history:

    SET_CMD_DEFINE = 'snmpset'
    GET_CMD_DEFINE = 'snmpget'
    WALK_CMD_DEFINE = 'snmpwalk'
    def __init__(self, ll: list):
        self.history = ll
        self.set_history = []
        self.__put_history_by_define(ll, self.set_history, Recoder_history.SET_CMD_DEFINE)

    def __put_history_by_define(self, history, history_save_space, cmd_define):
        if isinstance(history, list) is False:
            history = [history]
        for cmd in history:
            if str(cmd).lower().startswith(cmd_define):
                history_save_space.append(cmd)

    def _show(self, history):
        for i in history:
            print(i)

    def show(self):
        self._show(self.history)

    def show_set_cmd(self):
        self._show(self.set_history)

    def append(self, item):
        self.history.append(item)
        self.__put_history_by_define(item, self.set_history, Recoder_history.SET_CMD_DEFINE)

    def get_history(self):
        "\r\n".join(self.history)
        return self.history
    def get_set_history(self, no_list_format=True):
        res = self.set_history
        if no_list_format:
            res = "\n".join(self.set_history)
        return res

