import sys
sys.path.insert(0, '..')

import api.vk.network as network 
import api.vk.netType as Type
if __name__ == "__main__":
    net = network.Network(Type.NetType.emulate)
    net.Post("https://vk.com/","{test:0}")
