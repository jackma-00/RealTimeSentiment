package main

import (
	"github.com/a-h/templ"
	"github.com/arejula27/data-intensive-demo/dashboard/view"
	"github.com/labstack/echo/v4"
)

// HistoryData is a struct that holds the data for the history of Trump's popularity
type TimeSeries struct {
	timestamp       string
	TrumpPopularity float64
}

func main() {
	e := echo.New()
	e.GET("/", echo.WrapHandler(templ.Handler(view.IndexPage())))
	e.Logger.Fatal(e.Start(":1323"))

}
