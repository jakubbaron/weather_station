import React from "react";
import { render } from "react-dom";
import { TimeSeries, Index } from "pondjs";
import {
  Resizable,
  Charts,
  ChartContainer,
  ChartRow,
  YAxis,
  BarChart,
  styler,
  LineChart,
} from "react-timeseries-charts";

import data from "./data";

class SimpleChart extends React.Component {
  render() {
    const series = new TimeSeries({
      name: "hilo_rainfall",
      columns: ["index", "precip"],
      points: data.values.map(([d, value]) => [
        Index.getIndexString("1h", new Date(d)),
        value
      ])
    });

    console.log("series is ", series);
    const style = styler([
      {
        key: "precip",
        color: "#A5C8E1",
        selected: "#2CB1CF"
      }
    ]);

    return (
      <Resizable>
        <ChartContainer timeRange={series.range()}>
          <ChartRow height="150">
            <YAxis
              id="rain"
              label="Rainfall (inches/hr)"
              min={0}
              max={1.5}
              format=".2f"
              width="70"
              type="linear"
            />
            <Charts>
              <BarChart
                axis="rain"
                style={style}
                spacing={1}
                columns={["precip"]}
                series={series}
                minBarHeight={1}
              />
            </Charts>
          </ChartRow>
        </ChartContainer>
      </Resizable>
    );

    const axisStyle = {
        values: { valueColor: "Green", valueWeight: 200, valueSize: 12 }
    };

    return (
      <Resizable>
        <ChartContainer timeRange={series.range()} timeAxisStyle={axisStyle}>
          <ChartRow height="150">
            <YAxis
              style={axisStyle}
              id="price"
              label="Price ($)"
              min={series.min()}
              max={series.max()}
              width="60"
              format="$,.1f"
            />
            <Charts>
              <LineChart axis="price" series={series} style={style} />
            </Charts>
          </ChartRow>
        </ChartContainer>
      </Resizable>
    );
  }
}

class App extends React.Component {
  state = {};

  render() {
    return (
      <div className="p-3 m-4 border border-muted">
        <SimpleChart />
      </div>
    );
  }
}

export default App;
