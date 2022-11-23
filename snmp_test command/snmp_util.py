import os
import subprocess
from pathlib import Path
from subprocess import CalledProcessError
from data_struct import Field
import sys

MY_IP = "172.16.10.8"
WALK_COMMAND = f"snmpwalk -v1 -c public -m +IMP-HF528-MIB {MY_IP} "
GET_COMMAND = f"snmpget -v1 -c public -m +IMP-HF528-MIB {MY_IP} "
SET_COMMAND = f"snmpset -v1 -c public -m +IMP-HF528-MIB {MY_IP} "


class SNMP_runner:
    def __init__(self, runtime=r"C:\usr\bin"):
        os.chdir(runtime)
        self.runtime = runtime + ">"
        #

        print("snmp runtime path:", os.getcwd())
        print("============= init =============\n")
        self.command_saver = []

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
        print(f"{self.runtime}{cmd}")  # first command
        print(f"{raw_return}")  # command output
        if raw_return == "":
            print(" === WARNNING: THIS COMMAND NO RESPONSE ===")
            print(cmd)

    def _exec_cmd(self, cmd):
        res = ""
        try:
            res = subprocess.check_output(cmd).decode('utf-8')
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
        print("# get")
        print(f"{self.runtime}{cmd}")  # first command
        print(f"{raw_return}")  # command output

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
        print("# set")
        print(f"{self.runtime}{cmd}")  # first command
        print(f"{raw_return}")  # command output

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
        print(f"{self.runtime}{cmd}")  # first command
        print(f"{raw_return}")  # command output
        if raw_return == "":
            print(" === WARNNING: THIS COMMAND NO RESPONSE ===")
            print(cmd)


