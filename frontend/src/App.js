import React from "react";
import SimpleChart from "./SimpleChart"
import Thermometer from "./Thermometer"

class App extends React.Component {
  state = {};

  render() {
    return (
      <div className="p-3 m-4 border border-muted">
        <SimpleChart />
        <Thermometer />
      </div>
    );
  }
}

export default App;
