import glob
import os
import typing as tp

import simbricks.orchestration.experiments as exp
import simbricks.orchestration.nodeconfig as node
import simbricks.orchestration.simulators as sim
from simbricks.orchestration.nodeconfig import NodeConfig


class RecoNICWorkload(node.AppConfig):
    def __init__(
        self,
        pci_dev: str,
    ) -> None:
        super().__init__()
        self.pci_dev = pci_dev

    def prepare_pre_cp(self) -> tp.List[str]:
        return [
            'mount -t proc proc /proc',
            'mount -t sysfs sysfs /sys',
            'echo 1 >/sys/module/vfio/parameters/enable_unsafe_noiommu_mode',
            'echo "dead beef" >/sys/bus/pci/drivers/vfio-pci/new_id'
        ]

    def run_cmds(self, node: NodeConfig) -> tp.List[str]:
        cmds = [
            # 'gcc reconic_dma.c -o reconic_dma',
            # './reconic_dma',
            'sleep infinity'
        ]
        return cmds


experiments: tp.List[exp.Experiment] = []

e = exp.Experiment(f'reconic-qemu')

SERVER_SIDE = 0
CLIENT_SIDE = 1
testcase = 'read_2rdma'        # Supported options: {write_2rdma, read_2rdma}

node_cfg1 = node.NodeConfig()
node_cfg1.kcmd_append = 'memmap=512M!1G'
node_cfg1.memory = 2 * 1024
node_cfg1.app = RecoNICWorkload(
    '0000:00:02.0'
)
node_cfg1.app.pci_dev = '0000:00:02.0'

node_cfg2 = node.NodeConfig()
node_cfg2.kcmd_append = 'memmap=512M!1G'
node_cfg2.memory = 2 * 1024
node_cfg2.app = RecoNICWorkload(
    '0000:00:04.0'
)
node_cfg1.app.pci_dev = '0000:00:04.0'

reconic1 = sim.XsimDev('rec_server', testcase, SERVER_SIDE)
reconic1.name = 'rec_server'
host1 = sim.QemuHost(node_cfg1)
host1.name = 'server'
host1.wait = True
host1.sync = False
e.add_host(host1)
host1.add_pcidev(reconic1)
e.add_pcidev(reconic1)

reconic2 = sim.XsimDev('rec_client', testcase, CLIENT_SIDE)
reconic2.name = 'rec_client'
host2 = sim.QemuHost(node_cfg2)
host2.name = 'client'
host2.wait = True
host2.sync = False
e.add_host(host2)
host2.add_pcidev(reconic2)
e.add_pcidev(reconic2)

# Not supported currently, XsimDev only inheriting PciDev instead of NICSim for now
# network = sim.WireNet()
# e.add_network(network)
# reconic1.set_network(network)
# reconic2.set_network(network)

experiments.append(e)
