import os
import subprocess
from pathlib import Path
from subprocess import CalledProcessError
from data_struct import Field, Recoder_history
import sys

MY_IP = "172.16.10.8"
WALK_COMMAND = f"snmpwalk -v1 -c public -m +IMP-HF528-MIB {MY_IP} "
GET_COMMAND = f"snmpget -v1 -c public -m +IMP-HF528-MIB {MY_IP} "
SET_COMMAND = f"snmpset -v1 -c public -m +IMP-HF528-MIB {MY_IP} "


class SNMP_runner:
    def __init__(self, runtime=r"C:\usr\bin"):
        os.chdir(runtime)
        self.runtime = runtime + ">"
        self._last_cmd = "[NOT RUN ANY COMMAND]"
        self._recoder_history = []
        self.__recoder_enable = False
        self.__clipboard = ""
        #

        print("snmp runtime path:", os.getcwd())
        print("============= init =============\n")
        self.command_saver = []

    def print2copyboard(self, *args, **kwargs):
        _tmp = self.__clipboard
        args_res = " ".join(args)
        args_res += '\n'
        self.__clipboard = f"{_tmp}{args_res}"
        print(*args, **kwargs)

    def get_clipboard(self):
        return self.__clipboard

    def clear_clipboard(self):
        self.__clipboard = ""
    def export_copyboard_and_clear(self):
        _tmp = self.__clipboard
        self.__clipboard = ""
        return _tmp
    def recoder_enable_state(self):
        return self.__recoder_enable

    def get_history(self):
        return self._recoder_history

    def __enter__(self):
        self.__recoder_enable = True
        self._recoder_history = Recoder_history([])
        return self._recoder_history

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__recoder_enable = False

        print("exc_type, exc_val, exc_tb:", exc_type, exc_val, exc_tb)

    def check_obj_name(self, name):
        if len(str(name).split(' ')) >= 2:
            raise ValueError(f"Please check walk function input, your input obj_name = \"{name}\", ensure this input is single word?")

    def walk(self, obj_name, fptr=r"C:\Users\User\Desktop\123.txt", recorard_mode='w'):
        cmd = WALK_COMMAND + obj_name
        self.check_obj_name(obj_name)
        raw_return = self._exec_cmd(cmd)
        if fptr is not None:
            with open(Path(fptr), mode=recorard_mode, encoding='utf-8') as f:
                f.write(f"{self.runtime}{cmd}".replace("\n", ""))  # first command
                f.write(f"{raw_return}".replace("\n", ""))  # command output
        self.print2copyboard(f"{self.runtime}{cmd}")  # first command
        self.print2copyboard(f"{raw_return}")  # command output
        if raw_return == "":
            print(" === WARNNING: THIS COMMAND NO RESPONSE ===")
            print(cmd)

    def __recode_cmd(self, cmd):
        if self.__recoder_enable:
            self._recoder_history.append(cmd)

    def _exec_cmd(self, cmd):
        res = ""
        self._last_cmd = cmd
        try:
            res = subprocess.check_output(cmd).decode('utf-8')
            self.__recode_cmd(cmd)
        except CalledProcessError as e:
            print(" ================= CalledProcessError occur ================")
            print(e)
            print(f"COMMAND = {cmd}\n")
            sys.exit(-1)
        except Exception as e:
            print(" ================= general exception ================")
            print(e)
            print(f"COMMAND = {cmd}\n")
            sys.exit(-1)

        return res

    def get(self, obj_name, idx, fptr=r"C:\Users\User\Desktop\123.txt", recorard_mode='w'):
        cmd = GET_COMMAND + obj_name + f".{idx}"
        raw_return = self._exec_cmd(cmd)
        if fptr is not None:
            with open(Path(fptr), recorard_mode, encoding='utf-8') as f:
                f.write("\n# get\n")
                f.write(f"{self.runtime}{cmd}\n")  # first command
                f.writelines(raw_return)  # command output
        self.print2copyboard("# get")
        self.print2copyboard(f"{self.runtime}{cmd}")  # first command
        self.print2copyboard(f"{raw_return}")  # command output

    def set(self, obj_name, idx, val, dtype='int', fptr=r"C:\Users\User\Desktop\123.txt", recorard_mode='w'):
        """
        只允許設訂單一 field.
        """
        if dtype == 'int':
            cmd = SET_COMMAND + obj_name + f".{idx}" + " = " + str(val)
        elif dtype == 'str':
            cmd = SET_COMMAND + obj_name + f".{idx}" + " = " + f"\"{str(val)}\""
        else:
            assert 0  # please assign dtype
        raw_return = None
        raw_return = self._exec_cmd(cmd)
        self.command_saver.append(cmd)
        if fptr is not None:
            with open(Path(fptr), recorard_mode, encoding='utf-8') as f:
                f.write("\n# set\n")
                f.write(f"{self.runtime}{cmd}\n")  # first command
                f.writelines(raw_return)  # command output
        self.print2copyboard("# set")
        self.print2copyboard(f"{self.runtime}{cmd}")  # first command
        self.print2copyboard(f"{raw_return}")  # command output

    def test_ShowSetShow(self, obj_name, idx, val):
        self.get(obj_name, idx, recorard_mode='w')
        self.set(obj_name, idx, val=val, recorard_mode='a')
        self.get(obj_name, idx, recorard_mode='a')

    def test_get_continue_set(self, obj_name, idx, val_list):
        """
        測試連續數值, 多筆但不同value 測試。
        """
        self.command_saver = []
        self.get(obj_name, idx, recorard_mode='w')
        for val in val_list:
            self.set(obj_name, idx, val=val, recorard_mode='a')
        self.get(obj_name, idx, recorard_mode='a')

        for _ in self.command_saver:
            print(_)

    def set_table(self, idx, set_fields: list, row_status=None):
        quota_mark = ""
        cmd = SET_COMMAND
        for field in set_fields:
            assert isinstance(field, Field)
            cmd += field.idx(idx)
        raw_return = ""
        raw_return = self._exec_cmd(cmd)
        self.print2copyboard(f"{self.runtime}{cmd}")  # first command
        self.print2copyboard(f"{raw_return}")  # command output
        if raw_return == "":
            print(" === WARNNING: THIS COMMAND NO RESPONSE ===")
            print(cmd)

    def multiple_get(self, idx, fields_list: list, show=True):
        cmd = GET_COMMAND
        cmd_history = []
        _cmd = []
        for i, field_name in enumerate(fields_list):
            _tmp_cmd = cmd+field_name+f".{idx}"
            raw_return = self._exec_cmd(_tmp_cmd)
            _cmd.append(_tmp_cmd)
            cmd_history.append(self.get_last_cmd_and_prompt())
            cmd_history.append(raw_return)
            if show:
                print(f"# {i+1}")
                print(self.get_last_cmd_and_prompt())
                print(raw_return)
        print(" =========== commands ============= ")
        for _ in _cmd:
            print(_)

        return cmd_history

    def get_last_cmd_and_prompt(self):
        return self.runtime+self._last_cmd


    def multi_string_2_list(self, instr):
        fine_ = []
        for __ in [_.strip() for _ in instr.splitlines()]:
            if len(__) > 0:
                fine_.append(__)
        return fine_


if __name__ == "__main__":
    snmp = SNMP_runner()
    fields_list = ['iswEtherStatsDropEvents',
     'iswEtherStatsOctets',
     'iswEtherStatsPkts',
     'iswEtherStatsBroadcastPkts',
     'iswEtherStatsMulticastPkts',
     'iswEtherStatsCRCAlignErrors',
     'iswEtherStatsUndersizePkts',
     'iswEtherStatsOversizePkts',
     'iswEtherStatsFragments',
     'iswEtherStatsJabbers',
     'iswEtherStatsCollisions',
     'iswEtherStatsPkts64Octets',
     'iswEtherStatsPks65to127Octets',
     'iswEtherStatsPkts128to255Octets',
     'iswEtherStatsPkts256to511Octets',
     'iswEtherStatsPkts512to1023Octets',
     'iswEtherStatsPkts1024to1518Octets',
     'iswEtherStatsClear']
    res = snmp.multiple_get(1, fields_list)

    for _ in res:
        print(_)



