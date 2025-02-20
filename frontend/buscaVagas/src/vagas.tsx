import { useEffect, useState } from "react";
import "./Vagas.css";

interface Vaga {
  titulo: string;
  link: string;
}

const Vagas = () => {
  const [vagas, setVagas] = useState<Vaga[]>([]);
  const [filtro, setFiltro] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/vagas")
      .then((response) => response.json())
      .then((data) => setVagas(data))
      .catch((error) => console.error("Erro ao buscar vagas:", error));
  }, []);

  const vagasFiltradas = vagas.filter((vaga) =>
    vaga.titulo.toLowerCase().includes(filtro.toLowerCase())
  );

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <input
        type="text"
        placeholder="Digite para buscar vagas..."
        value={filtro}
        onChange={(e) => setFiltro(e.target.value)}
        style={{
          padding: "10px",
          width: "300px",
          border: "2px solid #F86465",
          borderRadius: "8px",
          outline: "none",
          fontSize: "16px",
          textAlign: "center",
        }}
      />

      {filtro && (
        <div
          style={{
            marginTop: "20px",
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "10px",
          }}
        >
          {vagasFiltradas.map((vaga, index) => (
            <a
              key={index}
              href={vaga.link}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                backgroundColor: "#F86465",
                padding: "15px",
                borderRadius: "10px",
                textDecoration: "none",
                color: "white",
                fontWeight: "bold",
                width: "250px",
                textAlign: "center",
                transition: "0.3s",
              }}
              onMouseOver={(e) =>
                (e.currentTarget.style.backgroundColor = "black")
              }
              onMouseOut={(e) =>
                (e.currentTarget.style.backgroundColor = "#F86465")
              }
            >
              {vaga.titulo}
            </a>
          ))}
        </div>
      )}
    </div>
  );
};

export default Vagas;
