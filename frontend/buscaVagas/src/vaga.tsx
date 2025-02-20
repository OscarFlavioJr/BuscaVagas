import { useEffect, useState } from "react";
import "./vaga.css";

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
    <div className="container">
      <input
        type="text"
        className="input-busca"
        placeholder="Digite para buscar vagas..."
        value={filtro}
        onChange={(e) => setFiltro(e.target.value)}
      />

      {filtro && (
        <div className="vagas-container">
          {vagasFiltradas.map((vaga, index) => (
            <a
              key={index}
              href={vaga.link}
              target="_blank"
              rel="noopener noreferrer"
              className="vaga"
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
