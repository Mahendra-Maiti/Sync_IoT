package balancer

type LoadBalancerLiveSelector interface {
	liveNode() (string, error)
}

func getLiveServer(g LoadBalancerLiveSelector) (string, error){
	return g.liveNode()
}
