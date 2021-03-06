#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController
import argparse
import sys
import time

class ClosTopo(Topo):

    def __init__(self, fanout, cores, **opts):
        # Initialize topology and default options

        Topo.__init__(self, **opts)


        "Set up Core and Aggregate level, Connection Core - Aggregation level"

        corelist=[]
        aggrlist=[]
        
        corelistswitch=[]
        aggrlistswitch=[]

        core=cores

        aggr=core*fanout

        for i in range(core):
          corelist.append("c"+str(i+1))       

        for k in range(len(corelist)):       
          corelistswitch.append(self.addSwitch(corelist[k]))

        for j in range(aggr):
          aggrlist.append("a"+str(j+1))

        for y in range(len(aggrlist)):
          aggrlistswitch.append(self.addSwitch(aggrlist[y]))


        for i in range(len(corelistswitch)):
         for j in range(len(aggrlistswitch)):
           self.addLink(corelistswitch[i],aggrlistswitch[j])

        pass

        "Set up Edge level, Connection Aggregation - Edge level "

        edgelist=[]
        edgelistswitch=[]

        edge=aggr*fanout

        for k in range(edge):
           edgelist.append("e"+str(k+1))

        for f in range(len(edgelist)):
           edgelistswitch.append(self.addSwitch(edgelist[f]))


        for i in range(len(aggrlistswitch)):
            for j in range(len(edgelistswitch)):
              self.addLink(aggrlistswitch[i],edgelistswitch[j])
              
        pass


        "Set up Host level, Connection Edge - Host level "
        hostlist=[]
        hostlistHost=[]

        host=edge*fanout

        for q in range(host):
           hostlist.append("h"+str(q+1))


        for g in range(len(hostlist)):
           hostlistHost.append(self.addHost(hostlist[g])) 

        count=0
        m=0

        for i in range(len(hostlistHost)):
           self.addLink(hostlistHost[i],edgelistswitch[m])
           count=count+1

           if count==fanout:
               m=m+1
               count=0 
        pass

def setup_clos_topo(fanout=2, cores=1):

    "Create and test a simple clos network"
    assert(fanout>0)
    assert(cores>0)
    topo = ClosTopo(fanout, cores)
    net = Mininet(topo=topo, controller=lambda name: RemoteController('c0', "127.0.0.1"), autoSetMacs=True, link=TCLink)
    net.start()
    time.sleep(20) #wait 20 sec for routing to converge

     
    net.pingAll()  #test all to all ping and learn the ARP info over this process


    CLI(net)       #invoke the mininet CLI to test your own commands

    net.stop()     #stop the emulation (in practice Ctrl-C from the CLI

                   #and then sudo mn -c will be performed by programmer)
def main(argv):


    parser = argparse.ArgumentParser(description="Parse input information for mininet Clos network")

    parser.add_argument('--num_of_core_switches', '-c', dest='cores', type=int, help='number of core switches')

    parser.add_argument('--fanout', '-f', dest='fanout', type=int, help='network fanout')

    args = parser.parse_args(argv)

    setLogLevel('info')

    setup_clos_topo(args.fanout, args.cores)

if __name__ == '__main__':
    main(sys.argv[1:])
