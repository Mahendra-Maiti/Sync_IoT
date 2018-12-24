package service

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

//BootRouter to startup the router
func BootRouter(port string) {
	router := mux.NewRouter()
	router.HandleFunc("/health", healthCheck).Methods("GET")
	log.Fatal(http.ListenAndServe(port, router))
}
