import React from "react";
import Websocket from 'react-websocket';
import { TimeSeries, Index } from "pondjs";
import {
  Resizable,
  Charts,
  ChartContainer,
  ChartRow,
  YAxis,
  BarChart,
  styler,
} from "react-timeseries-charts";

class Thermometer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      temperature: 25,
      date: new Date(),
      humidity: 35,
    };
  }
  handleData(data) {
    let result = JSON.parse(data);
    this.setState({temperature: result.data.temperature,
    		   humidity: result.data.humidity,
    	           date: result.data.date});
  }
  render() {
    const data = [
      [this.state.date, this.state.temperature]
    ]
    const series = new TimeSeries({
      name: "Current Temperature",
      columns: ["index", "temp"],
      points: data.map(([d, value]) => [
        Index.getIndexString("1d", new Date(d)),
        value
      ])
    });

    const style = styler([
      {
        key: "temp",
        color: "#A5C8E1",
        selected: "#2CB1CF"
      }
    ]);

    return (
      <div>
      <p>Current Temp: <strong>{this.state.temperature}</strong></p>
      <p>Current Humidity: <strong>{this.state.humidity}</strong></p>
      <Websocket url='ws://192.168.0.123:5678/' onMessage={this.handleData.bind(this)}/>
      <Resizable>
        <ChartContainer timeRange={series.range()}>
          <ChartRow height="300">
            <YAxis
              id="temp"
              label="Current Temperature"
              min={0}
              max={35}
              format=".2f"
              width="50"
              type="linear"
            />
            <Charts>
              <BarChart
                axis="temp"
                style={style}
                size={150}
                columns={["temp"]}
                series={series}
                minBarHeight={1}
              />
            </Charts>
          </ChartRow>
        </ChartContainer>
      </Resizable>
      </div>
    );
  }
}

export default Thermometer;
