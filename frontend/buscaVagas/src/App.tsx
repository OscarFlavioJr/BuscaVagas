import React from "react";
import Vagas from "./Vagas";

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
      <Vagas />
    </div>
  );
};

export default App;
