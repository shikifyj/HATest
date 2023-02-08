import re
import subprocess
import yaml
import paramiko
import telnetlib
import logging
import logging.handlers
import datetime
import sys
import socket
import time
import json

class Telnetconn:
    def __init__(self, ip):
        self.ip = ip
        self.tn = telnetlib.Telnet(f"{self.ip}")

    def exec_cmd(self, cmd):
        self.tn.write(f"{cmd}".encode('utf-8') + b'\n')
        res = self.tn.read_very_eager().decode('utf-8')


class SSHconn(object):
    def __init__(self, host, port=22, username="root", password=None, timeout=8):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self.timeout = timeout
        self.sshconnection = None
        self.ssh_conn()
        self.invoke_conn = self.sshconnection.invoke_shell()
        self.invoke_conn.keep_this = self.sshconnection

    def __str__(self):
        return f"node:{self._host}"

    def ssh_conn(self):
        """
        SSH连接
        """
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname=self._host,
                         username=self._username,
                         port=self._port,
                         password=self._password,
                         timeout=self.timeout,
                         look_for_keys=False,
                         allow_agent=False)
            self.sshconnection = conn
        except paramiko.AuthenticationException:
            print(f" Error SSH connection message of {self._host}")
        except Exception as e:
            print(f" Failed to connect {self._host}")

    def exec_cmd(self, command):
        """
        命令执行
        """
        if self.sshconnection:
            stdin, stdout, stderr = self.sshconnection.exec_command(command)
            result = stdout.read()
            result = result.decode() if isinstance(result, bytes) else result
            if result is not None:
                return {"st": True, "rt": result}

            err = stderr.read()
            if err is not None:
                return {"st": False, "rt": err}


def get_host_ip():
    """
    查询本机ip地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def exec_cmd(cmd, conn=None):
    if conn:
        result = conn.exec_cmd(cmd)
    else:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")

    result = result.decode() if isinstance(result, bytes) else result
    log_data = f'{get_host_ip()} - {cmd} - {result}'
    Log().logger.info(log_data)
    if result['st']:
        pass
        # f_result = result['rt'].rstrip('\n')
    if result['st'] is False:
        sys.exit()
    return result['rt']


class ConfFile(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self.read_yaml()

    def read_yaml(self):
        """
        读yaml文件
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                yaml_file = yaml.load(f, Loader=yaml.FullLoader)
            return yaml_file
        except FileNotFoundError:
            print("File not found")
        except TypeError:
            print("Error in the type of file .")

    def update_yaml(self, yaml_dict):
        """
        更新yaml文件
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_dict, f, default_flow_style=False)
        except FileNotFoundError:
            print("File not found")
        except TypeError:
            print("Error in the type of file .")

    def parameter_judgment(self):
        judg_list = ["B","K","kB","KiB","M","MB","MiB","G","GB","GiB","T","TB","TiB","P","PB","PiB"]

        result1 = re.findall(r'\d+([a-zA-Z]+)',self.config["BlockSize"])
        if result1 == []:
            print("BlockSize参数填写错误")
            sys.exit()

        judg_bool1 = False
        for i in judg_list:
            if result1[0] == i:
                judg_bool1 = True

        if judg_bool1 == False:
            print("BlockSize参数填写单位错误")
            sys.exit()

        result2 = re.findall(r'\d+([a-zA-Z]+)',self.config["TotalSize"])
        if result2 == []:
            print("TotalSize参数填写错误")
            sys.exit()

        judg_bool2 = False
        for i in judg_list:
            if result2[0] == i:
                judg_bool2 = True

        if judg_bool2 == False:
            print("TotalSize参数填写单位错误")
            sys.exit()

    def get_cluster_name(self):
        datetime = time.strftime('%y%m%d')
        return f"{self.config['cluster']}_{datetime}"

    def get_bindnetaddr(self):
        ips = self.config['heartbeat_line']
        lst = []
        for ip in ips:
            ip_list = ip.split(".")
            lst.append(f"{'.'.join(ip_list[:3])}.0")
        return lst

    def get_interface(self):
        bindnetaddr_list = self.get_bindnetaddr()
        interface_list = []
        ringnumber = 0
        mcastport_number = 5405
        for bindnetaddr in bindnetaddr_list[0:]:
            interface = "interface {\n\tringnumber: %s\n\tbindnetaddr: %s\n\tmcastport: %s\n\tttl: 1\n}" % (
                ringnumber, bindnetaddr,mcastport_number)
            interface = FileEdit.add_data_to_head(interface, '\t')
            interface_list.append(interface)
            ringnumber += 1
            mcastport_number += 1
        return "\n".join(interface_list)

    def get_nodelist(self):
        hostname_list = []
        for i in self.config["test_node"]:
            hostname_list.append(i['name'])

        str_node_all = ""

        for node, hostname in zip(self.config['test_node'], hostname_list):
            dict_node = {}
            str_node = "node "
            index = 0
            for ip in self.config["heartbeat_line"]:
                dict_node.update({f"ring{index}_addr": ip})
                index += 1
            dict_node.update({'name': hostname})
            str_node += json.dumps(dict_node, indent=4, separators=(',', ': '))
            str_node = FileEdit.remove_comma(str_node)
            str_node_all += str_node + '\n'
        str_node_all = FileEdit.add_data_to_head(str_node_all, '\t')
        str_nodelist = "nodelist {\n%s\n}" % str_node_all
        return str_nodelist

class Log(object):
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            Log._instance = super().__new__(cls)
            Log._instance.logger = logging.getLogger()
            Log._instance.logger.setLevel(logging.INFO)
            Log.set_handler(Log._instance.logger)
        return Log._instance

    @staticmethod
    def set_handler(logger):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file_name = str(now_time) + '.log'
        fh = logging.FileHandler(file_name, mode='a')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)


class FileEdit(object):
    def __init__(self, path):
        self.path = path
        self.data = self.read_file()

    def read_file(self):
        with open(self.path) as f:
            data = f.read()
        return data

    def replace_data(self, old, new):
        if not old in self.data:
            print('The content does not exist')
            return
        self.data = self.data.replace(old, new)
        return self.data

    def insert_data(self, content, anchor=None, type=None):
        """
        在定位字符串anchor的上面或者下面插入数据，上面和下面由type决定（under/above）
        anchor可以是多行数据，但必须完整
        :param anchor: 定位字符串
        :param type: under/above
        :return:
        """
        list_data = self.data.splitlines()
        list_add = (content + '\n').splitlines()
        pos = len(list_data)
        lst = []

        if anchor:
            if not anchor in self.data:
                return

            list_anchor = anchor.splitlines()
            len_anchor = len(list_anchor)

            for n in range(len(list_data)):
                match_num = 0
                for m in range(len_anchor):
                    if not list_anchor[m] == list_data[n + m]:
                        break
                    match_num += 1

                if match_num == len_anchor:
                    if type == 'under':
                        pos = n + len_anchor
                    else:
                        pos = n
                    break

        lst.extend(list_data[:pos])
        lst.extend(list_add)
        lst.extend(list_data[pos:])
        self.data = '\n'.join(lst)

        return self.data

    @staticmethod
    def add_data_to_head(text, data_add):
        text_list = text.splitlines()
        for i in range(len(text_list)):
            if text_list[i] != '\n':
                text_list[i] = f'{data_add}{text_list[i]}'

        return '\n'.join(text_list)

    @staticmethod
    def remove_comma(text):
        text_list = text.splitlines()
        for i in range(len(text_list)):
            text_list[i] = text_list[i].rstrip(',')
        return '\n'.join(text_list)


def connect():
    list_ssh = []

    test = ConfFile("config.yaml")
    for i in test.config["test_node"]:
        ssh_obj = SSHconn(host=i["ip"],username=i["username"],password=i["password"])
        list_ssh.append(ssh_obj)

    return list_ssh


if __name__ == "__main__":
    a = connect()
    print(a)