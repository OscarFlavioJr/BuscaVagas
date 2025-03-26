import React from "react";
import Vaga from "./vaga";

const App: React.FC = () => {
  return (
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#f5f5f5",
      }}
    >
      <Vaga />
    </div>
  );
};

export default App;
