import React from "react";
import SimpleChart from "./SimpleChart"
import HumidityAndThermometer from "./HumidityAndThermometer"

class App extends React.Component {
  state = {};

  render() {
    return (
      <div className="p-3 m-4 border border-muted">
        <SimpleChart />
        <HumidityAndThermometer />
      </div>
    );
  }
}

export default App;
