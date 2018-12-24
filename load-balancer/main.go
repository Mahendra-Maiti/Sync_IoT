package main

import (
	"flag"
	"log"
	"strings"

	"github.com/napster11/load-balancer/balancer"
	"github.com/napster11/load-balancer/instanceServer"
)

func main() {

	//Parse shell inputs
	port := flag.String("p", "", "load balancer port")
	nodes := flag.String("nodes", "", "list of servers in CSV")
	flag.Parse()

	//If there is no server to balance
	if len(*nodes) == 0 {
		log.Fatal("invalid list of registerd server")
	}
	instanceServer.RegisterServerList(strings.Split(*nodes, ","))
	balancer.InitServer(*port)
}
