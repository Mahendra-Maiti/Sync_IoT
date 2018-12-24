package balancer

import (
	"errors"
	"io/ioutil"
	"net/http"
	"time"

	"github.com/napster11/load-balancer/instanceServer"
)

//Call base endpoint of darwin server with maximum retries upto 20
func getServerResponse(url string, reTry int) ([]byte, error) {

	//If all reties doesn't give any response then just terminate the reuqest by passing error to it
	if reTry == 0 {
		return nil, errors.New("retry limit exceeded no live server found")
	}
	resp, err := http.Get(url + "/health")
	if err != nil {
		return nil, err
	}

	//If server is not working then try for some other live server
	if resp.StatusCode == 500 {
		robin := RoundRobin{instanceServer.GetInstanceServerListSize()}
		newServer, _ := getLiveServer(robin)
		if err != nil {
			return nil, err
		}

		//Don't want to bombard the load balancer with multiple requests (like a rate limiter)
		time.Sleep(100 * time.Millisecond)
		return getServerResponse(newServer, reTry-1)
	}
	return ioutil.ReadAll(resp.Body)

}
