from snmp_util import SNMP_runner, Field
import subprocess
def connect_test():
    command = "snmpwalk -v1 -c public -m +IMP-HF528-MIB 172.16.10.8 sysUpTime"
    token = subprocess.Popen(command)
    print('Command success: {}'.format(token.returncode is None))
    print(subprocess.check_output(command).decode('utf-8'))

if __name__ == "__main__":
    # test connected
    connect_test()

    command = "snmpwalk -v1 -c public -m +IMP-HF528-MIB 172.16.10.8 sysUpTime"
    snmp = SNMP_runner()
    snmp.walk("sysUpTime")
