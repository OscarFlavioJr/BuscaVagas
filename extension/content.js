let historicoVagas = [];

const buscarVagas = async () => {
  console.log("Extensão funcionando!");
  try {
    const response = await fetch("http://127.0.0.1:8000/vagas");

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log("Dados recebidos:", data);

    if (!Array.isArray(data)) {
      throw new Error("Formato inválido da resposta da API");
    }

    const listaVagas = document.getElementById("lista-vagas");
    vagas = listaVagas.innerHTML = "";

    const novosTitulos = data.map((vaga) => vaga.titulo);
    const novasVagas = novosTitulos.filter(
      (titulo) => !historicoVagas.includes(titulo)
    );

    if (novasVagas.length > 0) {
      if (Notification.permission === "granted") {
        if (novasVagas.length === 1) {
          new Notification("Nova vaga disponível!", {
            body: `${novasVagas[0]} está disponível no nosso site.`,
          });
        } else {
          new Notification("Novas vagas disponíveis!", {
            body: `Novas vagas de ${novasVagas[0]} e outras estão disponíveis.`,
          });
        }
      } else {
        console.warn("Permissão de notificação negada");
      }

      historicoVagas = novosTitulos;
    }

    data.forEach((vaga) => {
      const li = document.createElement("li");
      li.textContent = vaga.titulo;
      listaVagas.appendChild(li);
    });

    document.getElementById("erro-msg").textContent = "";
  } catch (error) {
    console.error("Erro ao buscar vagas:", error);
    document.getElementById("erro-msg").textContent = "Erro ao buscar vagas.";
  }
};

if (Notification.permission === "default") {
  Notification.requestPermission().then((permission) => {
    if (permission !== "granted") {
      console.warn("Notificações bloqueadas pelo usuário");
    }
  });
}

buscarVagas();
