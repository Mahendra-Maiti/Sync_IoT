package instanceServer

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"time"
)

var instanceServerList = make([]string, 0)
var REDIS_CONST = 100
var CONNECTION_CONST = 100

func healthCheck(key string) {
	go func() {
		for range time.NewTicker(5 * time.Second).C {
			CheckInstanceHealth(key)
		}
	}()
}

func GetInstanceServerListSize() int {
	return len(instanceServerList)
}

func RegisterServerList(ips []string) {
	instanceServerList = append(instanceServerList, ips...)
	for _, key := range instanceServerList {
		healthCheck(key)
	}
}

func GetInstanceStatusByIndex(index int) (string, error) {

	if _, err := InstanceList.Get(instanceServerList[index]); err != nil {
		return "", errors.New("server is unhealthy")
	}
	return instanceServerList[index], nil
}

func CheckInstanceHealth(s string) {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", s+"/health", nil)
	client.Timeout = time.Duration(5 * time.Second)
	// Make request
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("error")
		InstanceList.Delete(s)
		return
	}
	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		var data repoInfo
		bodyBytes, _ := ioutil.ReadAll(resp.Body)
		err = json.Unmarshal(bodyBytes, &data)
		InstanceList.Set(s, data)
		fmt.Println("data ", data)
	} else {
		fmt.Println("delete")
		InstanceList.Delete(s)
	}
	fmt.Println("length ", len(InstanceList.m))
}

func getFitnessValue(url string) (repoInfo, error) {
	numKeys, _ := InstanceList.Get(url)
	countKeys := numKeys.Connection/REDIS_CONST + CONNECTION_CONST
	return InstanceList.Get(strconv.Itoa(countKeys))
}
