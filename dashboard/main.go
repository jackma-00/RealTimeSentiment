package main

import (
	"context"
	"encoding/json"
	"os"
	"time"

	"github.com/labstack/echo/v4"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var trump_db *mongo.Collection
var harris_db *mongo.Collection

type candidateData struct {
	Timestamp time.Time `bson:"timestamp"`
	Support   int       `bson:"support"`
	Oppose    int       `bson:"oppose"`
}

func getData() string {
	cursor, err := trump_db.Find(context.TODO(), bson.D{})
	if err != nil {
		panic(err)
	}

	var trumpResults []candidateData
	if err = cursor.All(context.TODO(), &trumpResults); err != nil {
		panic(err)
	}
	var harrisResults []candidateData
	cursor, err = harris_db.Find(context.TODO(), bson.D{})
	if err != nil {
		panic(err)
	}
	if err = cursor.All(context.TODO(), &harrisResults); err != nil {
		panic(err)
	}

	//iterate over the results create a slice with the timestamps and a slice with probablity of trump winning
	var timestamps []string
	var trump []int
	var harris []int
	for _, result := range trumpResults {
		timestamps = append(timestamps, result.Timestamp.Format("2006-01-02 15:04:05"))
		if result.Support+result.Oppose != 0 {
			currentTrumpSupport := result.Support / (result.Support + result.Oppose) * 100
			trump = append(trump, currentTrumpSupport)
			harris = append(harris, 100-currentTrumpSupport)
		}
	}
	type result struct {
		Timestamps       []string `json:"timestamps"`
		TrumpPopularity  []int    `json:"trumpPopularity"`
		HarrisPopularity []int    `json:"harrisPopularity"`
	}
	res, err := json.Marshal(result{Timestamps: timestamps, TrumpPopularity: trump, HarrisPopularity: harris})
	if err != nil {
		return ""
	}
	return string(res)

}

func ChartHandler(c echo.Context) error {
	jsonData := getData()
	return c.JSON(200, jsonData)
}

func main() {
	//connect to mongoDB

	//get mongo uri from env
	uri := os.Getenv("MONGO_URI")
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
	trump_db = client.Database("usa2024").Collection("trump")
	harris_db = client.Database("usa2024").Collection("harris")

	e := echo.New()
	e.Static("/", "view")
	e.GET("/chart-data", ChartHandler)
	e.Logger.Fatal(e.Start(":1323"))

}
