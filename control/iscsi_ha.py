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

    def main(self):
        """
        默认node已经创建
        默认已有sp名为"sp1"
        """
        self.linstor_obj.create_rd(rd_name="r1",ssh_conn=self.obj_list[0])
        self.linstor_obj.create_vd(vd_name="r1",vd_size="10G",ssh_conn=self.obj_list[0])
        self.linstor_obj.create_diskful_resource(node_name=self.node1["name"],resource_name="r1",sp_name="sp1"
                                                 ,ssh_conn=self.obj_list[0])
        self.linstor_obj.create_diskful_resource(node_name=self.node2["name"],resource_name="r1",sp_name="sp1"
                                                 ,ssh_conn=self.obj_list[1])
        self.linstor_obj.create_diskless_resource(node_name=self.node3["name"],resource_name="r1"
                                                  ,ssh_conn=self.obj_list[2])
        pass    #配置pacemaker资源

        result1 = self.pacemaker_obj.check_pacemaker(ssh_conn=self.obj_list[0])
        #进行正则表达式判断





