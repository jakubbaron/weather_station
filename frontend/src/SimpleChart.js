import React from "react";
import Websocket from 'react-websocket';
import { TimeSeries, Index } from "pondjs";
import {
  Resizable,
  Charts,
  ChartContainer,
  ChartRow,
  YAxis,
  styler,
  LineChart,
} from "react-timeseries-charts";

class SimpleChart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
	temperatures: [[Date.now(), 25]],
	humidities: [[Date.now(), 35]],
    };
  }

  handleData(data) {
//{"data": {"sensor": "DHT11-main", "date": "2018-12-26 15:13:36", "temperature": "21.18", "humidity": "34.04"}, "time_point": "1545837216789-0"}	O	
    	let result = JSON.parse(data);
	let humidities = [];
	let temperatures = [];
	result.map((entry) => humidities.push([entry.date, entry.humidity]));
	result.map((entry) => temperatures.push([entry.date, entry.temperature]));
	this.setState({ temperatures: temperatures,
			humidities: humidities});
  }
  render() {
    const tempSeries = new TimeSeries({
	name: 'temperatures',
	columns: ['index', 'temp'],
	points: this.state.temperatures.map(([d, temp]) => [
		Index.getIndexString("1m", new Date(d)),
		temp	
	])
    });

    const humiditySeries = new TimeSeries({
	name: 'temperatures',
	columns: ['index', 'humidity'],
	points: this.state.humidities.map(([d, humidity]) => [
		Index.getIndexString("1m", new Date(d)),
		humidity
	])
    });


    const style = styler([
        { key: "temp", color: "#CA4040" },
        { key: "humidity", color: "#9467bd" },
    ]);

    return (
      <div>
      <Websocket url='ws://192.168.0.123:5679/' onMessage={this.handleData.bind(this)}/>
      <Resizable>
        <ChartContainer timeRange={tempSeries.range()}>
	  <ChartRow height="350" >
	    <YAxis id="temp"
		   label="Temperature (°C)"
		   labelOffset={-5}
		   min={18}
		   max={28}
		   style={style.axisStyle("temp")}
/>
			
	    <Charts>
		<LineChart
			axis="temp"
			series={tempSeries}
			columns={["temp"]}
			style={style} />
		<LineChart
			axis="humidity"
			series={humiditySeries}
			columns={["humidity"]}
			style={style} />
	    </Charts>
	    <YAxis
		id="humidity"
		label="Humidity %"
		labelOffset={5}
		style={style.axisStyle("humidity")}
		min={20}
		max={40}
		type="linear"
		format=",.1f"
	    />
	  </ChartRow>
        </ChartContainer>
      </Resizable>
      </div>
    );
  }
}

export default SimpleChart;
