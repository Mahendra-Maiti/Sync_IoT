package service

import (
	"bytes"
	"encoding/json"
	"fmt"
	"image"
	"image/png"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	redis "github.com/go-redis/redis"
	"github.com/unrolled/render"
)

var prev = 0
var after = 0

//getImage is the Handler function to generate the API Response
func getImage(w http.ResponseWriter, r *http.Request) {
	client := redis.NewClient(&redis.Options{
		Addr:     "10.0.0.18:6379",
		Password: "", // no password set
		DB:       0,  // use default DB
	})
	pong, err := client.Ping().Result()
	fmt.Println(pong, err)

	// for i := 0; i < 33; i++ {
	// 	err := client.Set(fmt.Sprintf("key%d", i), "value", 0).Err()
	// 	if err != nil {
	// 		panic(err)
	// 	}
	// }

	var cursor uint64
	keys, _, err := client.Scan(cursor, "R2*", 100).Result()
	if err != nil {
		fmt.Println("err ", err.Error())
	}
	// fmt.Println(len(keys))
	// _ = client.MGet(keys)
	for _, key := range keys {
		val, err := client.Get(key).Result()
		if err != nil {
			fmt.Println("Error in reading key")
		}
		img, _, err := image.Decode(bytes.NewReader([]byte(val)))
		if err != nil {
			fmt.Println("Error in decoding the image")
			return
		}
		fmt.Println(key)
		out, err := os.Create(key + ".png")
		if err != nil {
			fmt.Println("error in converting to image ", err.Error())
			return
		}
		png.Encode(out, img)
		out.Close()
	}

}

type Response struct {
	Destination string  `json:"destination"`
	Latitude    float64 `json:"lat"`
	Longitude   float64 `json:"long"`
	Connection  int     `json:"connection"`
	NumKeys     int     `json:"keys"`
	HOST        string  `json:"host"`
}

type Data struct {
	Destination string `json:"destination"`
	Value       string `json:"value"`
	Timestamp   string `json:"timestamp"`
	XLoc        int    `json:"x_loc"`
	YLoc        int    `json:"y_loc"`
}

type lambda struct {
	DeviceName string `json:"deviceName"`
	Timestamp  int    `json:"timestamp"`
	Payload    []Data `json:"payload"`
}

type lambdaRequest struct {
	Result []lambda `json:"sensorData"`
}

func healthCheck(w http.ResponseWriter, r *http.Request) {
	render := render.New()

	var cursor uint64
	keys, _, err := RedisClient.Scan(cursor, "*", 10000000).Result()
	if err != nil {
		fmt.Println("err ", err.Error())
	}
	// fmt.Println("HIT")
	// fmt.Println(len(keys))
	x_loc, _ := strconv.ParseFloat(os.Args[5], 64)
	y_loc, _ := strconv.ParseFloat(os.Args[6], 64)
	res := Response{Latitude: x_loc, Longitude: y_loc, Connection: ConnectionCount, NumKeys: len(keys), HOST: SocketConnectionHOST}
	render.JSON(w, http.StatusOK, res)
	return
}

func ReadKeys() {
	var cursor uint64
	keys, _, err := RedisClient.Scan(cursor, "*", 10000000).Result()
	if err != nil {
		fmt.Println("err ", err.Error())
	}
	if len(keys) < 1 {
		// fmt.Println("empty keys ")
		// prev = 0
		// after = 0
		// fmt.Println("-------------------------------------")
		return
	}
	// fmt.Println("HIT")
	// fmt.Println(len(keys))

	i := 0
	finalRes := map[string][]Data{}
	values, err := RedisClient.MGet(keys...).Result()
	if err != nil {
		fmt.Println("err ", err.Error())
	}
	for _, val := range values {
		x := fmt.Sprintf("%+s", val)
		// fmt.Printf("%+v", x)
		data := Data{}

		err = json.Unmarshal([]byte(x), &data)
		if err != nil {
			fmt.Println("err ", err.Error())
		}
		deviceName := strings.Split(keys[i], "_")[0]
		if i < len(keys) {
			finalRes[deviceName] = append(finalRes[deviceName], data)
		}
		i++
	}
	objectList := []lambda{}
	for k, v := range finalRes {
		obj := lambda{}
		obj.DeviceName = k
		filteredData := []Data{}
		prev += len(v)
		for i, val := range v {
			if i == 0 || (v[i-1].Value != v[i].Value) {
				filteredData = append(filteredData, val)
			}
		}
		after += len(filteredData)
		obj.Payload = filteredData
		obj.Timestamp = time.Now().Nanosecond()
		objectList = append(objectList, obj)
	}
	lRequest := lambdaRequest{}
	lRequest.Result = objectList

	fmt.Println("received data points  ", prev, " delivered data points ", after)
	text := strconv.Itoa(prev) + " ----- " + strconv.Itoa(after)
	f, err := os.OpenFile("/Users/shivamsingh/go/src/github.com/napster11/syncService/count.txt", os.O_APPEND|os.O_WRONLY, 0644)
	f.WriteString(text)
	f.Close()
	// fmt.Println("lrequest ", lRequest)
	bt, _ := json.Marshal(lRequest)
	URL := "https://tnpaxwqza0.execute-api.us-east-1.amazonaws.com/test/demo"
	req, err := http.NewRequest("POST", URL, bytes.NewReader(bt))
	req.Header.Set("Content-Type", "application/json")

	// Make request
	client := http.Client{}
	// start := time.Now()
	resp, err := client.Do(req)
	// elapsed := time.Since(start).Seconds()
	// fmt.Println("elapsed ", elapsed, " size of data ", req.ContentLength)
	if err != nil {
		fmt.Println("err ", err.Error())
		return
	}

	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		for _, v := range keys {
			RedisClient.Del(v)
		}
	}
	// fmt.Println("res ", resp)
	// fmt.Println("final ", finalRes)
}
