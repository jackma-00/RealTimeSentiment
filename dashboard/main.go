package main

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"time"

	"github.com/labstack/echo/v4"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var trumpDb *mongo.Collection
var harrisDb *mongo.Collection

type candidateData struct {
	Timestamp time.Time `bson:"timestamp"`
	Support   int       `bson:"support"`
	Oppose    int       `bson:"oppose"`
}

func getData() string {

	filter := bson.D{}
	opts := options.FindOne().SetSort(bson.D{{"timestamp", -1}})
	var currentTrump candidateData
	var currentHarris candidateData
	err := trumpDb.FindOne(context.TODO(), filter, opts).Decode(&currentTrump)
	if err != nil {
		log.Println(err)
	}

	err = harrisDb.FindOne(context.TODO(), filter, opts).Decode(&currentHarris)
	if err != nil {
		log.Println(err)
	}

	totalCount := currentTrump.Support + currentTrump.Oppose + currentHarris.Oppose + currentHarris.Support
	if totalCount == 0 {
		log.Println("No data for Trump and Harris")
		return "{}"
	}
	trumpSupport := int((float32(currentTrump.Support + currentHarris.Oppose)/float32(totalCount))*100)
	log.Println("Current trump: ", currentTrump)
	log.Println("Current trump support: ", currentTrump.Support)
	log.Println("Current harris oppose: ", currentHarris.Oppose)
	log.Println("Harris support: ", currentHarris.Oppose)
	harrisSupport := 100 - trumpSupport
	log.Println("Trump support: ", trumpSupport)
	log.Println("Harris support: ", harrisSupport)
	log.Println("Total count: ", totalCount)

	type result struct {
		Timestamps       string `json:"timestamps"`
		TrumpPopularity  int    `json:"trumpPopularity"`
		HarrisPopularity int    `json:"harrisPopularity"`
	}
	currentTime := time.Now().Format("15:04:05")
	res, err := json.Marshal(result{Timestamps: currentTime, TrumpPopularity: trumpSupport, HarrisPopularity: harrisSupport})
	if err != nil {
		return "{}"
	}
	return string(res)

}

func chartHandler(c echo.Context) error {
	jsonData := getData()
	return c.JSON(200, jsonData)
}

func main() {
	//connect to mongoDB

	//get mongo uri from env
	uri := os.Getenv("MONGO_URI")
	if uri == "" {
		uri = "mongodb://localhost:27017"
	}

	client, err := mongo.Connect(context.TODO(), options.Client().
		ApplyURI(uri))
	if err != nil {
		panic(err)
	}
	defer func() {
		if err := client.Disconnect(context.TODO()); err != nil {
			panic(err)
		}
	}()
	trumpDb = client.Database("usa2024").Collection("trump")
	harrisDb = client.Database("usa2024").Collection("harris")

	e := echo.New()
	e.Static("/", "view")
	e.GET("/chart-data", chartHandler)
	e.Logger.Fatal(e.Start(":1323"))

}
