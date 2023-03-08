from .. import utils
from .. import pacemaker_test

class Test:
    def __init__(self,config,obj_list):
        self.config = config
        self.obj_list = obj_list
        self.linstor_obj = pacemaker_test.Linstor()
        self.pacemaker_obj = pacemaker_test.Pacemaker()
        self.node1 = self.config["test_node"][0]
        self.node2 = self.config["test_node"][1]
        self.node3 = self.config["test_node"][2]

    def move_test(self):
        result1 = self.pacemaker_obj.check_pacemaker(ssh_conn=self.obj_list[0])
        #进行正则表达式判断

        self.pacemaker_obj.move_resources(node=self.node2["name"],ssh_conn=self.obj_list[0])

        result1 = self.pacemaker_obj.check_pacemaker(ssh_conn=self.obj_list[0])
        #进行正则表达式判断

        self.pacemaker_obj.unmove_resources(ssh_conn=self.obj_list[0])

    def node_standby_online_test(self):
        result1 = self.pacemaker_obj.check_pacemaker(ssh_conn=self.obj_list[0])
        #进行正则表达式判断

        self.pacemaker_obj.set_standby(ssh_conn=self.obj_list[0])

        result1 = self.pacemaker_obj.check_pacemaker(ssh_conn=self.obj_list[0])
        #进行正则表达式判断

        self.pacemaker_obj.set_online(ssh_conn=self.obj_list[0])

        result1 = self.pacemaker_obj.check_pacemaker(ssh_conn=self.obj_list[0])
        #进行正则表达式判断

    def main(self):
        self.move_test()
        self.node_standby_online_test()




