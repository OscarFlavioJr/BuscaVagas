import { useEffect, useState } from "react";
import "./vaga.css";

function tiraAcento(str: string): string {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, ""); 
}

interface Vaga {
  titulo: string;
  link: string;
  empresa: string;
}

const empresas = [
  { nome: "Fleury", cor: "#670000", logo: "./fleury.png"}
];

const Vagas = () => {
  const [vagas, setVagas] = useState<Vaga[]>([]);
  const [filtro, setFiltro] = useState("");
  const [empresaSelecionada, setEmpresaSelecionada] = useState<string | null>(
    null
  );
  const [historicoVagas, setHistoricoVagas] = useState<string[]>([]); 

  useEffect(() => {
    const buscarVagas = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/vagas");
        const data: Vaga[] = await response.json();

        if (data.length > 0) {
          const novosTitulos = data.map((vaga) => vaga.titulo);
          const novasVagas = novosTitulos.filter(
            (titulo) => !historicoVagas.includes(titulo)
          );

          if (novasVagas.length > 0) {
            if (novasVagas.length === 1) {
              new Notification("Nova vaga disponível!", {
                body: `${novasVagas[0]} está disponível no nosso site.`,
              });
            } else {
              new Notification("Novas vagas disponíveis!", {
                body: `Novas vagas de ${novasVagas[0]} e outras estão disponíveis.`,
              });
            }

            setHistoricoVagas(novosTitulos); 
          }

          setVagas(data);
        }
      } catch (error) {
        console.error("Erro ao buscar vagas:", error);
      }
    };

    if (Notification.permission === "default") {
      Notification.requestPermission();
    }

    buscarVagas();

    let interval = setInterval(buscarVagas, 86400);
    return () => clearInterval(interval);
  }, []);


  const vagasFiltradas = vagas.filter(
    (vaga) =>
      tiraAcento(vaga.titulo.toLowerCase()).includes(
        tiraAcento(filtro.toLowerCase())
      ) &&
      (!empresaSelecionada || vaga.empresa === empresaSelecionada)
  );

  const empresaAtual = empresas.find((e) => e.nome === empresaSelecionada);

  return (
    <div
      className="container"
      style={{
        backgroundColor: empresaAtual?.cor || "#222",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-start",
        alignItems: "center",
        padding: "20px",
        boxSizing: "border-box",
        overflowY: "auto",
        transition: "all .5s ease",
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
              <img src={empresa.logo} alt={empresa.nome} className="logo" />
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

      <div className="vagas-container">
        {vagasFiltradas.map((vaga) => (
          <a
            key={vaga.link}
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
    </div>
  );
};

export default Vagas;
