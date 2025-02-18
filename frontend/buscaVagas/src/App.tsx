import { useState, useEffect } from "react";

interface Vaga {
  titulo: string;
  link: string;
}

export default function App() {
  const [vagas, setVagas] = useState<Vaga[]>([]);
  const [search, setSearch] = useState(""); // Estado para armazenar o termo de busca

  useEffect(() => {
    fetch("http://127.0.0.1:8000/vagas")
      .then((res) => res.json())
      .then((data) => setVagas(data))
      .catch((error) => console.error("Erro ao buscar vagas:", error));
  }, []);

  // Filtrar vagas conforme a busca
  const vagasFiltradas = vagas.filter((vaga) =>
    vaga.titulo.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="container">
      <h1>Vagas Disponíveis</h1>

      {/* Barra de pesquisa */}
      <input
        type="text"
        placeholder="Pesquisar vaga..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-bar"
      />

      {/* Lista de vagas */}
      <div className="vagas-list">
        {vagasFiltradas.map((vaga, index) => (
          <a key={index} href={vaga.link} className="vaga-card">
            <h2>{vaga.titulo}</h2>
          </a>
        ))}
      </div>
    </div>
  );
}
