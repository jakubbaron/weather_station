import React from "react";
import Websocket from 'react-websocket';
import Thermometer from 'react-thermometer-component'

class HumidityAndThermometer extends React.Component {
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
    return (
      <div className="m-4 border border-muted">
      <Websocket url='ws://192.168.0.123:5678/' onMessage={this.handleData.bind(this)}/>

      <div className="thermometer-container">
        <Thermometer
          theme="light"
          value={this.state.temperature}
          max={35}
          steps="3"
          format="°C"
          size="large"
          height="300"
          reverseGradient={false}
        />
        <Thermometer
          theme="light"
          value={this.state.humidity}
          max={100}
          steps="4"
          format="%"
          size="large"
          height="300"
          reverseGradient={false}
        />
      </div>

      </div>
    );
  }
}

export default HumidityAndThermometer;
