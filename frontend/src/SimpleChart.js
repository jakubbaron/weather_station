import React from "react";
import Websocket from 'react-websocket';
import { TimeRange, TimeSeries, Index } from "pondjs";
import {
  Resizable,
  Charts,
  ChartContainer,
  ChartRow,
  YAxis,
  styler,
  LineChart,
  MultiBrush,
} from "react-timeseries-charts";


// Sosnowiec 50.2863° N, 19.1041° E

class SimpleChart extends React.Component {
  constructor(props) {
    super(props);
    this.SunCalc = require('suncalc');
    let today = new Date();
    this.times = this.SunCalc.getTimes(today, 50.2863, 19.1041);
    let yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    this.yesterday_times = this.SunCalc.getTimes(yesterday, 50.2863, 19.1041);
    let tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    this.tomorrow_times= this.SunCalc.getTimes(tomorrow, 50.2863, 19.1041);

    this.state = {
	nightTimes: [
		new TimeRange(this.yesterday_times.sunset, this.times.sunrise),
		new TimeRange(this.times.sunset, this.tomorrow_times.sunrise)],
	humiditySeries: this.getTimeSeries([[yesterday, 25], [today, 25]], 'humidities', 'humidity'),
	tempSeries: this.getTimeSeries([[yesterday, 35], [today, 35]], 'temperatures', 'temp'),
    };
  }

  getTimeSeries(arr, series_name, column_name) {
    const series = new TimeSeries({
      name: series_name,
      columns: ['index', column_name],
      points: arr.map(([d, value]) => [
    	Index.getIndexString("1m", new Date(d)),
    	value	
      ])
    });
    return series;
  }

  handleData(data) {
//{"data": {"sensor": "DHT11-main", "date": "2018-12-26 15:13:36", "temperature": "21.18", "humidity": "34.04"}, "time_point": "1545837216789-0"}	O	
    	let result = JSON.parse(data);
	let humidities = [];
	let temperatures = [];
	result.map((entry) => humidities.push([entry.date, entry.humidity]));
	result.map((entry) => temperatures.push([entry.date, entry.temperature]));

	this.setState({ tempSeries: this.getTimeSeries(temperatures, 'temperatures', 'temp'),
			humiditySeries: this.getTimeSeries(humidities, 'humidities', 'humidity') });
  }
  render() {

    const style = styler([
        { key: "temp", color: "#CA4040" },
        { key: "humidity", color: "#9467bd" },
    ]);

    return (
      <div>
      <Websocket url='ws://192.168.0.123:5679/' onMessage={this.handleData.bind(this)}/>
      <Resizable>
        <ChartContainer timeRange={this.state.tempSeries.range()}>
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
		  	series={this.state.tempSeries}
		  	columns={["temp"]}
		  	style={style} />
		  <LineChart
		  	axis="humidity"
		  	series={this.state.humiditySeries}
		  	columns={["humidity"]}
		  	style={style} />
		  <MultiBrush
          timeRanges={this.state.nightTimes}
		      style={i => {
            return { fill: "#cccccc" };
		      }}
      />
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
