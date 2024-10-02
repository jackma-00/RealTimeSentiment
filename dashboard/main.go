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
	err := trumpDb.FindOne(context.TODO(), filter, opts).Decode(&currentTrump)
	if err != nil {
		log.Println(err)
		return "{}"
	}

	if currentTrump.Support+currentTrump.Oppose == 0 {
		log.Println("No data for Trump")
		return "{}"
	}
	trumpSupport := currentTrump.Support / (currentTrump.Support + currentTrump.Oppose) * 100
	harrisSupport := 100 - trumpSupport
	type result struct {
		Timestamps       string `json:"timestamps"`
		TrumpPopularity  int    `json:"trumpPopularity"`
		HarrisPopularity int    `json:"harrisPopularity"`
	}
	currentTime := time.Now().Format("2006-01-02 15:04:05")
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
