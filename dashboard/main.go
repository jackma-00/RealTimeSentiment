package main

import (
	"context"
	"fmt"
	"time"

	"github.com/arejula27/data-intensive-demo/dashboard/view"
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

func getData() ([]string, []int) {
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
	for i, result := range trumpResults {
		timestamps = append(timestamps, fmt.Sprintf("%d", i))
		if result.Support+result.Oppose != 0 {
			trump = append(trump, result.Support/(result.Support+result.Oppose)*100)
		}
	}
	return timestamps, trump
}

func IndexPageHandler(c echo.Context) error {
	timestamps, trump := getData()
	component := view.IndexPage(timestamps, trump)
	return component.Render(c.Request().Context(), c.Response())
}

func main() {
	//connect to mongoDB

	uri := "mongodb://localhost:27017"
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
	e.GET("/", IndexPageHandler)
	e.Logger.Fatal(e.Start(":1323"))

}
