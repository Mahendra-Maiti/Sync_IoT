package test

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

// only needed below for sample processing

func main() {

	fmt.Println("Launching server...")

	// listen on all interfaces
	hostname, _ := os.Hostname()
	println("hostname ", hostname)
	ln, _ := net.Listen("tcp", hostname+":8081")

	// accept connection on port
	conn, _ := ln.Accept()

	// run loop forever (or until ctrl-c)
	for {
		// will listen for message to process ending in newline (\n)
		message, _ := bufio.NewReader(conn).ReadString('\n')
		// output message received
		fmt.Print("Message Received:", string(message))
		// sample process for string received
		newmessage := strings.ToUpper(message)
		// send new string back to client
		conn.Write([]byte(newmessage + "\n"))
	}
}
