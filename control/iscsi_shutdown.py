from .. import utils
from .. import pacemaker_test

class Test:
    def __init__(self,config,obj_list):
        self.config = config
        self.obj_list = obj_list
        self.linstor_obj = pacemaker_test.Linstor()
        self.pacemaker_obj = pacemaker_test.Pacemaker()
        self.target_obj = pacemaker_test.Target()
        self.go_meter_obj = pacemaker_test.GoMeter()
        self.node1 = self.config["test_node"][0]
        self.node2 = self.config["test_node"][1]
        self.node3 = self.config["test_node"][2]
        self.node_other = self.config["test_node"][3]

    def test(self):
        self.target_obj.connect_target(ip=None,ssh_conn=self.obj_list[3])

        result1 = self.target_obj.check_conn(ssh_conn=self.obj_list[3])
        # 进行正则表达式判断

        self.go_meter_obj.start_gometer(ssh_conn=self.obj_list[3])
        self.pacemaker_obj.shutdown_node(ssh_conn=self.obj_list[0])

        result1 = self.pacemaker_obj.check_pacemaker(ssh_conn=self.obj_list[1])
        #进行正则表达式判断

        """节点开机"""

        result1 = self.pacemaker_obj.check_pacemaker(ssh_conn=self.obj_list[1])
        #进行正则表达式判断

        self.pacemaker_obj.move_resources(node=self.node1["name"],ssh_conn=self.obj_list[1])

        result1 = self.pacemaker_obj.check_pacemaker(ssh_conn=self.obj_list[1])
        #进行正则表达式判断

        self.go_meter_obj.compare(ssh_conn=self.obj_list[3])


