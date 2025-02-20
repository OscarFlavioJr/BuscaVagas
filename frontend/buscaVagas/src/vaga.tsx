import { useEffect, useState } from "react";
import "./vaga.css";

interface Vaga {
  titulo: string;
  link: string;
  empresa: string;
}

const empresas = [
  { nome: "Fleury", cor: "#670000", logo: "./fleury.png" },
  { nome: "Natura", cor: "#FF6E0D", logo: "./natura.png" },
  { nome: "Raízen", cor: "#83008E", logo: "./raizen.png" },
  { nome: "Cosan", cor: "#0095A9", logo: "./cosan.png" },
];

const Vagas = () => {
  const [vagas, setVagas] = useState<Vaga[]>([]);
  const [filtro, setFiltro] = useState("");
  const [empresaSelecionada, setEmpresaSelecionada] = useState<string | null>(
    null
  );

  useEffect(() => {
    fetch("http://127.0.0.1:8000/vagas")
      .then((response) => response.json())
      .then((data) => setVagas(data))
      .catch((error) => console.error("Erro ao buscar vagas:", error));
  }, []);

  const vagasFiltradas = vagas.filter(
    (vaga) =>
      vaga.titulo.toLowerCase().includes(filtro.toLowerCase()) &&
      (!empresaSelecionada || vaga.empresa === empresaSelecionada)
  );

  const empresaAtual = empresas.find((e) => e.nome === empresaSelecionada);

  return (
    <div
      className="container"
      style={{
        backgroundColor: empresaAtual?.cor || "#222",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {!empresaSelecionada ? (
        <div className="logos-container">
          {empresas.map((empresa) => (
            <div
              key={empresa.nome}
              className="logo-wrapper"
              onClick={() => setEmpresaSelecionada(empresa.nome)}
            >
              <img
                src={`/logos/${empresa.logo}`}
                alt={empresa.nome}
                className="logo"
              />
              <span className="logo-nome">{empresa.nome}</span>
            </div>
          ))}
        </div>
      ) : (
        <button className="voltar" onClick={() => setEmpresaSelecionada(null)}>
          Voltar
        </button>
      )}

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
              <div className="vaga-info">
                <strong className="vaga-titulo">{vaga.titulo}</strong>
                <span className="vaga-empresa">{vaga.empresa}</span>
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
};

export default Vagas;
