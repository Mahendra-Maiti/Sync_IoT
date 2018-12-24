package balancer

import (
	"github.com/napster11/load-balancer/instanceServer"
	"github.com/pkg/errors"
)

var CurrentRoundIndex = 0

type RoundRobin struct {
	RoundSize int
}

func (r RoundRobin) liveNode() (string, error) {
	var server string
	var err error

	if instanceServer.GetSize() == 0 {
		// fmt.Println("no server is live")
		return "", errors.New("no server is live")
	}
	if CurrentRoundIndex >= r.RoundSize {
		CurrentRoundIndex = 0
	}

	server, err = instanceServer.GetInstanceStatusByIndex(CurrentRoundIndex)
	CurrentRoundIndex++
	if err != nil {
		return r.liveNode()
	}
	return server, err
}
