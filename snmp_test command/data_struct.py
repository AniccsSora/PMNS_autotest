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
        # elif self.dtype == 'OTHER_DTYPE':
        #    res = f"{self.fname}.{idx} x \"{self.val}\""
        else:
            raise NotImplementedError("not support dtype:", self.dtype)

        return res