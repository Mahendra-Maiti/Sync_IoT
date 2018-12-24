package instanceServer

import (
	"errors"
	"sync"
)

const (
	healthyMessage = "healthy"
)

var (
	InstanceList *nodeStatus
	cOnce        sync.Once
)

type repoInfo struct {
	Lat        float64 `json:"lat"`
	Long       float64 `json:"long"`
	Connection int     `json:"connection"`
	Keys       int     `json:"keys"`
	HOST       string  `json:"host"`
}

type nodeStatus struct {
	m map[string]repoInfo // map of url vs success
	l *sync.RWMutex
}

func initList() *nodeStatus {

	cOnce.Do(func() {
		InstanceList = &nodeStatus{
			l: new(sync.RWMutex),
			m: make(map[string]repoInfo),
		}
	})
	return InstanceList
}

func init() {
	InstanceList = initList()
}

func (c *nodeStatus) Set(key string, value repoInfo) {
	c.l.Lock()
	defer c.l.Unlock()
	c.m[key] = value
}

func (c *nodeStatus) Get(key string) (repoInfo, error) {
	c.l.RLock()
	defer c.l.RUnlock()
	cURL, ok := c.m[key]
	if !ok {
		return repoInfo{}, errors.New(key + " unhealthy instance ip")
	}
	return cURL, nil
}
func (c *nodeStatus) Delete(key string) {
	c.l.Lock()
	defer c.l.Unlock()
	delete(c.m, key)
}

func GetSize() int {
	InstanceList.l.RLock()
	defer InstanceList.l.RUnlock()
	return len(InstanceList.m)
}
