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


class
ClosTopo(Topo):

  
 
 def __init__(self, fanout, cores, **opts):
    
 

        Topo.__init__(self, **opts)
  
        corelst=[]
 
        aggrlist=[]
    
        core=self.cores
      
        aggr=core*self.fanout
 
    
        for i in range(core):
            
         corelist.append("c"+str(i+1))
 
       
        for j in range(aggr):
            
         aggrlist.append("a"+str(j+1))
     
        for i in range(core):
          
         for j in range(aggr):
         
           self.addlink(corelist[i],aggrlist[j])

       

        edgelist=[]    
        
        edge=aggr*self.fanout 
      
        for k in range(edge):
             
           edgelist.append("e"+str(k+1))
      
        for i in range(aggr):
          
            for j in range(edge):
        
              self.addlink(aggrlist[i],edgelist[j])

       
        
     
  
    # "Set up Host level, Connection Edge - Host level "
  
    
     #WRITE YOUR CODE HERE!
  
       
         hostlist=[]  
      
         host=edge*self.fanout
    
         for q in range( host):
          
           host.append("h"+str(q+1))
           
           print ("h"+str(q+1))

      
        for i in range(edge):
          
           for j in range(host):
          
             self.addlink(edgelist[i],hostlist[j])
        
       if j==fanout:  
                 
           break

 
  def setup_clos_topo(fanout=2,cores=1):
   
  assert(fanout>0)
  
  assert(cores>0)
  
   
  topo = ClosTopo(fanout, cores)
  
  
  net = Mininet(topo=topo, controller=lambda name: RemoteController('c0', "127.0.0.1"), autoSetMacs=True, link=TCLink)
   
 
  net.start()
  
  
  time.sleep(20) #wait 20 sec for routing to converge
  
 
 net.pingAll()  #test all to all ping and learn the ARP info over this process
   
  
  CLI(net)       #invoke the mininet CLI to test your own commands
   
   
  net.stop()     #stop the emulation (in practice Ctrl-C from the CLI  #and then sudo mn -c will be performed by programmer)

   
 
  
def main(argv):
   
   
  parser = argparse.ArgumentParser(description="Parse input information for mininet Clos network")
  
   
  parser.add_argument('--num_of_core_switches', '-c', dest='cores', type=int, help='number of core switches')
 
   
  parser.add_argument('--fanout', '-f', dest='fanout', type=int, help='network fanout')
    
 
  args = parser.parse_args(argv)
   
  
  setLogLevel('info')
    
  
  setup_clos_topo(args.fanout, args.cores)



  
  if __name__ == '__main__':
    main(sys.argv[1:])


