import argparse


class argparse_operator:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='argparse')
        self.setup_parse()

    def setup_parse(self):
        sub_parser = self.parser.add_subparsers()

        self.parser.add_argument('-v',
                                 '--version',
                                 dest='version',
                                 help='Show current version',
                                 action='store_true')

        parser_test = sub_parser.add_parser("test",aliases=['t'],help='Perform all tests')

        sub_parser_test = parser_test.add_subparsers()

        parser_test_heartbeat = sub_parser_test.add_parser("heartbeat",aliases=['h'],help='Heartbeat test')
        sub_parser_test_heartbeat = parser_test_heartbeat.add_subparsers()
        parser_test_heartbeat_one = sub_parser_test_heartbeat.add_parser("one",aliases=['o'],help='Heartbeat one test')
        parser_test_heartbeat_two = sub_parser_test_heartbeat.add_parser("two",aliases=['t'],help='Heartbeat two test')

        parser_test_linstor = sub_parser_test.add_parser("linstor",aliases=['l'],help='Linstor test')
        sub_parser_test_linstor = parser_test_linstor.add_subparsers()
        parser_test_linstor_ha = sub_parser_test_linstor.add_parser("ha",aliases=['h'],help='linstor HA test')
        parser_test_linstor_resource = sub_parser_test_linstor.add_parser("resource",aliases=['r'],help='linstor resource management test')

        parser_test_iscsi = sub_parser_test.add_parser("iscsi",aliases=['i'],help='iSCSI test')
        sub_parser_test_iscsi = parser_test_iscsi.add_subparsers()
        parser_test_iscsi_ha = sub_parser_test_iscsi.add_parser("ha",aliases=['h'],help='iSCSI ha test')
        parser_test_iscsi_manage = sub_parser_test_iscsi.add_parser("manage",aliases=['m'],help='iSCSILogicalUnit management test')

        parser_test_iscsi_architecture = sub_parser_test.add_parser("arch",aliases=['a'],help='iSCSI architecture test')
        sub_parser_test_iscsi_architecture = parser_test_iscsi_architecture.add_subparsers()
        parser_test_iscsi_architecture_shutdown = sub_parser_test_iscsi_architecture.add_parser("shutdown",aliases=['s'],help='Shutdown node test')
        parser_test_architecture_poweroff = sub_parser_test_iscsi_architecture.add_parser("poweroff",aliases=['po'],help='Power off node test')
        parser_test_architecture_network_card = sub_parser_test_iscsi_architecture.add_parser("card",aliases=['c'],help='Down network card test')
        parser_test_architecture_network_line = sub_parser_test_iscsi_architecture.add_parser("line",aliases=['l'],help='Down network line test')
        parser_test_architecture_port = sub_parser_test_iscsi_architecture.add_parser("port",aliases=['p'],help='Down port test')
        parser_test_architecture_switch = sub_parser_test_iscsi_architecture.add_parser("switch",aliases=['s'],help='Switch failure test')
        parser_test_architecture_resource_close = sub_parser_test_iscsi_architecture.add_parser("resource_close",aliases=['rc'],help='Resource close test')
        parser_test_architecture_resource_failed = sub_parser_test_iscsi_architecture.add_parser("resource_failed",aliases=['rf'],help='Resource failed test')


        self.parser.set_defaults(func=self.main_usage)

        parser_test.set_defaults(func=self.test_operation)

        parser_test_heartbeat.set_defaults(func=self.heartbeat_test)
        parser_test_heartbeat_one.set_defaults(func=self.heartbeat_one)
        parser_test_heartbeat_two.set_defaults(func=self.heartbeat_two)

        parser_test_linstor.set_defaults(func=self.linstor_test)
        parser_test_linstor_ha.set_defaults(func=self.linstor_ha)
        parser_test_linstor_resource.set_defaults(func=self.linstor_resource)

        parser_test_iscsi.set_defaults(func=self.iscsi_test)
        parser_test_iscsi_ha.set_defaults(func=self.iscsi_ha)
        parser_test_iscsi_manage.set_defaults(func=self.iscsi_manage)

        parser_test_iscsi_architecture.set_defaults(func=self.architecture_test)
        parser_test_iscsi_architecture_shutdown.set_defaults(func=self.architecture_shutdown)
        parser_test_architecture_poweroff.set_defaults(func=self.architecture_poweroff)
        parser_test_architecture_network_card.set_defaults(func=self.architecture_card)
        parser_test_architecture_network_line.set_defaults(func=self.architecture_line)
        parser_test_architecture_port.set_defaults(func=self.architecture_port)
        parser_test_architecture_switch.set_defaults(func=self.architecture_switch)
        parser_test_architecture_resource_close.set_defaults(func=self.architecture_resource_close)
        parser_test_architecture_resource_failed.set_defaults(func=self.architecture_resource_failed)


    def main_usage(self,args):
        if args.version:
            print(f'Version: ？')
        else:
            self.parser.print_help()

    def test_operation(self,args):
        print("python3 main.py test(t)")


    def heartbeat_test(self,args):
        print("python3 main.py test heartbeat(h)")

    def heartbeat_one(self,args):
        print("python3 main.py test heartbeat(h) one(o)")

    def heartbeat_two(self,args):
        print("python3 main.py test heartbeat(h) two(t)")


    def linstor_test(self,args):
        print("python3 main.py test linstor(l)")

    def linstor_ha(self,args):
        print("python3 main.py test linstor(l) ha(h)")

    def linstor_resource(self,args):
        print("python3 main.py test linstor(l) resource(r)")


    def iscsi_test(self,args):
        print("python3 main.py test iscsi(i)")

    def iscsi_ha(self,args):
        print("python3 main.py test iscsi(i) ha(h)")

    def iscsi_manage(self,args):
        print("python3 main.py test iscsi(i) manage(m)")


    def architecture_test(self,args):
        print("python3 main.py test arch(a)")

    def architecture_shutdown(self,args):
        print("python3 main.py test arch(a) shutdown(s)")

    def architecture_poweroff(self,args):
        print("python3 main.py test arch(a) poweroff(po)")

    def architecture_card(self,args):
        print("python3 main.py test arch(a) card(c)")

    def architecture_line(self,args):
        print("python3 main.py test arch(a) line(l)")

    def architecture_port(self,args):
        print("python3 main.py test arch(a) port(p)")

    def architecture_switch(self,args):
        print("python3 main.py test arch(a) switch(s)")

    def architecture_resource_close(self,args):
        print("python3 main.py test arch(a) resource_close(rc)")

    def architecture_resource_failed(self,args):
        print("python3 main.py test arch(a) resource_failed(rf)")



    def parser_init(self):
        args = self.parser.parse_args()
        args.func(args)

if __name__ == "__main__":
    cmd = argparse_operator()
    cmd.parser_init()