package main

import (
	"github.com/arejula27/data-intensive-demo/dashboard/view"
	"github.com/labstack/echo/v4"
)

// HistoryData is a struct that holds the data for the history of Trump's popularity
type TimeSeries struct {
	timestamp       string
	TrumpPopularity float64
}

func getData() ([]string, []int) {
	return []string{"1", "2", "3", "4", "5"}, []int{20, 50, 70, 40, 55}
}

func IndexPageHandler(c echo.Context) error {
	timestamps, trump := getData()
	component := view.IndexPage(timestamps, trump)
	return component.Render(c.Request().Context(), c.Response())
}

func main() {
	e := echo.New()
	e.GET("/", IndexPageHandler)
	e.Logger.Fatal(e.Start(":1323"))

}
