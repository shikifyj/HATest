import utils
import timeout_decorator
import re
import time

"""
1.不同crm st的判断依据
2.port需要ssh操作
3.刷新资源的命令"crm res ref"
"""

class Corosync(object):
    def __init__(self):
        self.corosync_data = './corosync.conf'
        self.corosync_path = '/etc/corosync/corosync.conf'
        self.original_attr = {'cluster_name': 'debian',
                              'bindnetaddr': '127.0.0.1'}

        self.interface_pos = '''                ttl: 1
            }'''

        self.nodelist_pos = "logging {"

    # 重启Corosync
    def restart_corosync(self, ssh_conn=None):
        cmd = f'systemctl restart corosync'
        utils.exec_cmd(cmd, ssh_conn)
    # 同步时间
    def sync_time(self, ssh_conn=None):
        cmd = 'ntpdate -u ntp.api.bz'
        utils.exec_cmd(cmd, ssh_conn)
    # 配置Corosync
    def change_corosync_conf(self, cluster_name, bindnetaddr_list, interface, nodelist):
        editor = utils.FileEdit(self.corosync_data)

        editor.replace_data(f"cluster_name: {self.original_attr['cluster_name']}", f"cluster_name: {cluster_name}")
        editor.replace_data(f"bindnetaddr: {self.original_attr['bindnetaddr']}", f"bindnetaddr: {bindnetaddr_list[0]}")
        editor.insert_data(interface, anchor=self.interface_pos, type='under')
        editor.insert_data(nodelist, anchor=self.nodelist_pos, type='above')
        if len(bindnetaddr_list) > 1:
            editor.insert_data(f'\trrp_mode: passive', anchor='        # also set rrp_mode.', type='under')

        utils.exec_cmd(f'echo "{editor.data}" > {self.corosync_path}', self.conn)

    @timeout_decorator.timeout(30)
    def restart_corosync(self, ssh_conn=None):
        cmd = 'systemctl restart corosync'
        utils.exec_cmd(cmd, ssh_conn)
    # 检查心跳线
    def check_ring_status(self, node, ssh_conn=None):
        cmd = 'corosync-cfgtool -s'
        data = utils.exec_cmd(cmd, ssh_conn)
        ring_data = re.findall('RING ID\s\d*[\s\S]*?id\s*=\s*(.*)', data)
        for ip in node["heartbeat_line"]:
            if ip not in ring_data:
                return False
        return True
    # 检查在线的节点
    def check_corosync_status(self, nodes, timeout=60):
        cmd = 'crm st | cat'
        t_beginning = time.time()
        node_online = []
        while not node_online:
            data = utils.exec_cmd(cmd, self.conn)
            node_online = re.findall('Online:\s\[(.*?)\]', data)
            if node_online:
                node_online = node_online[0].strip().split(' ')
                if set(node_online) == set(nodes):
                    return True
                else:
                    time.sleep(1)
            seconds_passed = time.time() - t_beginning
            if timeout and seconds_passed > timeout:
                return


class Pacemaker(object):
    # 配置Pacemaker集群
    def modify_cluster_name(self, cluster_name, ssh_conn=None):
        cmd = f"crm config property cluster-name={cluster_name}"
        utils.exec_cmd(cmd, ssh_conn)

    def modify_policy(self, status='stop', ssh_conn=None):
        cmd = f"crm config property no-quorum-policy={status}"
        utils.exec_cmd(cmd, ssh_conn)

    def modify_stonith_enabled(self, ssh_conn=None):
        cmd = "crm config property stonith-enabled=false"
        utils.exec_cmd(cmd, ssh_conn)

    def modify_stickiness(self, ssh_conn=None):
        cmd = "crm config rsc_defaults resource-stickiness=1000"
        utils.exec_cmd(cmd, ssh_conn)
    # 重启Pacemaker
    def restart(self, ssh_conn=None):
        cmd = "systemctl restart pacemaker"
        utils.exec_cmd(cmd, ssh_conn)
    # 检查Pacemaker集群
    def check_pacemaker(self, ssh_conn=None):
        cmd = f'crm st'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result
    # 移动资源
    def move_resources(self, node, ssh_conn=None):
        cmd = f'crm res move r0{node}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result
    # 恢复移动的资源
    def unmove_resources(self, ssh_conn=None):
        cmd = f'crm res unmove r0'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result
    # 关闭资源
    def stop_resources(self, ssh_conn=None):
        cmd = f'crm res stop r0'
        utils.exec_cmd(cmd, ssh_conn)
    # 启动资源
    def start_resources(self, ssh_conn=None):
        cmd = f'crm res start r0'
        utils.exec_cmd(cmd, ssh_conn)
    # 重启资源
    def restart_resources(self, ssh_conn=None):
        cmd = f'crm res restart r0'
        utils.exec_cmd(cmd, ssh_conn)
    # 设置节点为standby
    def set_standby(self, ssh_conn=None):
        cmd = f'crm node standby'
        utils.exec_cmd(cmd, ssh_conn)
    # 设置节点online
    def set_online(self, ssh_conn=None):
        cmd = f'crm node online'
        utils.exec_cmd(cmd, ssh_conn)
    # 关闭iSCSILogicalUnit资源
    def shutdown_node(self, ssh_conn=None):
        cmd = f'shutdown now'
        utils.exec_cmd(cmd, ssh_conn)


class Network(object):
    # 关闭网卡
    def close_heartbeat(self, network_card, ssh_conn=None):
        cmd = f'ifconfig {network_card} down'
        utils.exec_cmd(cmd, ssh_conn)
    # 启动网卡
    def recovery_heartbeat(self, network_card, ssh_conn=None):
        cmd = f'ifconfig {network_card} up'
        utils.exec_cmd(cmd, ssh_conn)
    # 检查网卡
    def check_networkcard(self, network_card, ssh_conn=None):
        cmd = f'ifconfig {network_card}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result
    # 关闭port
    def close_port(self, ip, ssh_conn=None):
        cmd = f'telnet {ip}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result


class Linstor(object):
    # node创建
    def create_node(self, node_name, ip, node_type, ssh_conn=None):
        cmd = f'linstor n create {node_name} {ip} --node-type {node_type}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # sotrage pool创建
    def create_sp(self, node_name, sp_type, sp_name, vg_name, ssh_conn=None):
        cmd = f'linstor sp create {sp_type} {node_name} {sp_name} {vg_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # resource definition创建
    def create_rd(self, rd_name, ssh_conn=None):
        cmd = f'linsotr rd create {rd_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # volume definition创建
    def create_vd(self, vd_name, vd_size, ssh_conn=None):
        cmd = f'linstor vd create {vd_name} {vd_size}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # diskless资源创建
    def create_diskless_resource(self, node_name, resource_name, ssh_conn=None):
        cmd = f'linstor r create {node_name} {resource_name} --diskless'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # diskful资源创建
    def create_diskful_resource(self, node_name, resource_name, sp_name, ssh_conn=None):
        cmd = f'linstor r create {node_name} {resource_name} --storage-pool {sp_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看resource信息
    def check_resource(self, ssh_conn=None):
        cmd = f'linstor r l'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看节点信息
    def check_node(self, ssh_conn=None):
        cmd = f'linstor n l'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看存储池信息
    def check_sp(self, ssh_conn=None):
        cmd = f'linstor sp l'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result
    # 备份linstordb
    def backup_linstordb(self, ssh_conn=None):
        utils.exec_cmd('mkdir /root/linstor_backup', ssh_conn)
        utils.exec_cmd('cd /var/lib/linstor', ssh_conn)
        utils.exec_cmd('cp * /root/linstor_backup/', ssh_conn)
    # 停止linstor-controller并将linstordb移至DRBD设备
    def stop_linstordb(self, ssh_conn=None):
        utils.exec_cmd('systemctl stop linstor-controller.service', ssh_conn)
        utils.exec_cmd('rsync -avp /var/lib/linstor /tmp/', ssh_conn)
        utils.exec_cmd('mkfs.ext4 /dev/drbd/by-res/linstordb/0', ssh_conn)
        utils.exec_cmd('rm -rf /var/lib/linstor/*', ssh_conn)
        utils.exec_cmd('mount /dev/drbd/by-res/linstordb/0 /var/lib/linstor', ssh_conn)
        utils.exec_cmd('rsync -avp /tmp/linstor/ /var/lib/linstor/', ssh_conn)


class Target(object):
    def connect_target(self, ip, ssh_conn=None):
        cmd = f'iscsiadm -m discovery -t st -p {ip} -l'
        utils.exec_cmd(cmd, ssh_conn)

    def check_conn(self, ssh_conn=None):
        cmd = 'lsblk'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

class GoMeter(object):
    def start_gometer(self, ssh_conn=None):
        cmd = './main write'
        utils.exec_cmd(cmd, ssh_conn)

    def compare(self, ssh_conn=None):
        cmd = './main compare'
        utils.exec_cmd(cmd, ssh_conn)

