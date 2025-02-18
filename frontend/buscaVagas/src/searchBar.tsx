import React, { useState, useEffect } from "react";
import axios from "axios";

// Definição do tipo das vagas
interface Vaga {
  titulo: string;
  link: string;
}

const SearchBar: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [vagas, setVagas] = useState<Vaga[]>([]);
  const [filteredVagas, setFilteredVagas] = useState<Vaga[]>([]);
  const [suggestions, setSuggestions] = useState<Vaga[]>([]);
  const [showResults, setShowResults] = useState<boolean>(false);

  // Buscar vagas na API quando o componente for montado
  useEffect(() => {
    axios
      .get<Vaga[]>("http://localhost/vagas")
      .then((response) => {
        setVagas(response.data);
      })
      .catch((error) => console.error("Erro ao buscar vagas:", error));
  }, []);

  // Atualizar sugestões conforme o usuário digita
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const searchTerm = e.target.value.toLowerCase();
    setQuery(searchTerm);

    if (searchTerm === "") {
      setSuggestions([]);
      return;
    }

    const matches = vagas.filter((vaga) =>
      vaga.titulo.toLowerCase().includes(searchTerm)
    );
    setSuggestions(matches.slice(0, 5)); // Mostra até 5 sugestões
  };

  // Exibir os resultados filtrados ao clicar no botão
  const handleSearchClick = () => {
    setFilteredVagas(suggestions);
    setShowResults(true);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <div className="relative">
        <input
          type="text"
          placeholder="Buscar vagas..."
          value={query}
          onChange={handleSearch}
          className="w-full p-2 border border-gray-300 rounded-md"
        />
        {suggestions.length > 0 && (
          <ul className="absolute w-full bg-white border border-gray-300 rounded-md mt-1 shadow-md">
            {suggestions.map((vaga, index) => (
              <li
                key={index}
                className="p-2 hover:bg-gray-100 cursor-pointer"
                onClick={() => {
                  setQuery(vaga.titulo);
                  setSuggestions([]);
                }}
              >
                {vaga.titulo}
              </li>
            ))}
          </ul>
        )}
      </div>
      <button
        onClick={handleSearchClick}
        className="mt-2 w-full bg-blue-600 text-white p-2 rounded-md"
      >
        Buscar
      </button>
      {showResults && (
        <ul className="mt-4">
          {filteredVagas.map((vaga, index) => (
            <li key={index} className="border-b py-2">
              <a
                href={vaga.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600"
              >
                {vaga.titulo}
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBar;
