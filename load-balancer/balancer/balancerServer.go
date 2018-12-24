package balancer

import (
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/napster11/load-balancer/instanceServer"
	"github.com/unrolled/render"
)

//Generally reverse-proxy like Nginx set timeout of 10 second for any request. In our case one request is at max taking 200 ms,
//so in our case we set it up to 2 sec (means 20 Retries)
const maxRetry = 20

//Handler function for the exposed base endpoint of load-balancer service
func myHandler(w http.ResponseWriter, r *http.Request) {

	fmt.Println("Request")
	//Create Round Robin object with size upto registered service count
	robin := RoundRobin{instanceServer.GetInstanceServerListSize()}

	//Find the Live server using Round Robin strategy
	ser, err := getLiveServer(robin)
	fmt.Println("size ", instanceServer.GetSize())
	if err != nil {
		w.WriteHeader(http.StatusServiceUnavailable)
		w.Write([]byte("503 - Something bad happened!")) //No Live server found
		return
	}
	kv, _ := instanceServer.InstanceList.Get(ser)
	server := kv.HOST
	fmt.Println("server ", server)
	fmt.Println("ser ", ser)
	//Get the server response for above selected server
	_, err = getServerResponse(ser, maxRetry)
	if err != nil {
		w.WriteHeader(http.StatusServiceUnavailable)
		w.Write([]byte("no server found after multiple retries"))
		return
	}
	type Response struct {
		HOST string `json:"HOST"`
		PORT string `json:"PORT"`
	}
	// str := strings.Split(server, "://")
	render := render.New()
	res := Response{HOST: strings.Split(server, ":")[0], PORT: strings.Split(server, ":")[1]}
	render.JSON(w, http.StatusOK, res)
	return
}

// InitServer initializes server to server any incoming request
func InitServer(port string) {
	fmt.Println("started running on port", port)
	http.HandleFunc("/", myHandler)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
