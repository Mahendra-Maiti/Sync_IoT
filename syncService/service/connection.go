package service

import (
	"encoding/json"
	"fmt"
	"net"
	"os"
	"time"

	redis "github.com/go-redis/redis"
)

type ClientManager struct {
	clients    map[*Client]bool
	register   chan *Client
	unregister chan *Client
}

type Client struct {
	socket net.Conn
	data   chan []byte
}

var ConnectionCount = 0
var RedisClient = &redis.Client{}
var SocketConnectionHOST = ""

func (manager *ClientManager) start() {
	redisURL := os.Args[2]
	fmt.Println("Redis ", redisURL)
	RedisClient = redis.NewClient(&redis.Options{
		Addr:     redisURL,
		Password: "", // no password set
		DB:       0,  // use default DB
	})
	pong, err := RedisClient.Ping().Result()
	fmt.Println(pong, err)
	for {
		select {
		case connection := <-manager.register:
			manager.clients[connection] = true
			ConnectionCount++
			fmt.Println("Added new connection!")
		case connection := <-manager.unregister:
			if _, ok := manager.clients[connection]; ok {
				close(connection.data)
				delete(manager.clients, connection)
				ConnectionCount--
				fmt.Println("A connection has terminated!")
			}
		}
	}
}

func (manager *ClientManager) receive(client *Client) {
	for {
		message := make([]byte, 1024)
		length, err := client.socket.Read(message)
		if err != nil {
			manager.unregister <- client
			client.socket.Close()
			break
		}
		if length > 0 {
			type request struct {
				Data struct {
					Destination string `json:"destination"`
					Value       string `json:"value"`
					Timestamp   string `json:"timestamp"`
					XLoc        int    `json:"x_loc"`
					YLoc        int    `json:"y_loc"`
				} `json:"Data"`
				DeviceName string `json:"deviceName"`
			}
			trimmedMessage := message[:length]
			var req request
			if err := json.Unmarshal(trimmedMessage, &req); err != nil {
				fmt.Println("error ", err.Error())
			}
			// fmt.Println("RECEIVED: " + string(message))
			// fmt.Println("JSON: ", req)
			d, err := json.Marshal(&req.Data)
			if err != nil {
				fmt.Println("error ", err.Error())
			}
			RedisClient.Set(req.DeviceName+"_"+req.Data.Timestamp, d, 0)

		}
	}
}

func (client *Client) receive() {
	for {
		message := make([]byte, 4096)
		length, err := client.socket.Read(message)
		if err != nil {
			client.socket.Close()
			break
		}
		if length > 0 {
			fmt.Println("RECEIVED: " + string(message))
		}
	}
}

func (manager *ClientManager) send(client *Client) {
	defer client.socket.Close()
	for {
		select {
		case message, ok := <-client.data:
			if !ok {
				return
			}
			client.socket.Write(message)
		}
	}
}

func StartServerMode() {
	fmt.Println("Starting server...")
	SocketConnectionHOST = os.Args[3]
	listener, error := net.Listen("tcp", SocketConnectionHOST)
	if error != nil {
		fmt.Println(error)
	}
	manager := ClientManager{
		clients:    make(map[*Client]bool),
		register:   make(chan *Client),
		unregister: make(chan *Client),
	}
	go BootRouter(":" + os.Args[4]) //API Server for health check
	go manager.start()
	go syncing()
	for {
		connection, _ := listener.Accept()
		if error != nil {
			fmt.Println(error)
		}
		client := &Client{socket: connection, data: make(chan []byte)}
		manager.register <- client
		go manager.receive(client)
		go manager.send(client)
	}
}

func syncing() {
	go func() {
		for range time.NewTicker(10 * time.Second).C {
			ReadKeys()
		}
	}()
}

// func StartClientMode() {
// 	fmt.Println("Starting client...")
// 	connection, error := net.Dial("tcp", "10.0.0.18:8081")
// 	if error != nil {
// 		fmt.Println(error)
// 	}
// 	client := &Client{socket: connection}
// 	go client.receive()
// 	for {
// 		reader := bufio.NewReader(os.Stdin)
// 		message, _ := reader.ReadString('\n')
// 		connection.Write([]byte(strings.TrimRight(message, "\n")))
// 	}
// }
