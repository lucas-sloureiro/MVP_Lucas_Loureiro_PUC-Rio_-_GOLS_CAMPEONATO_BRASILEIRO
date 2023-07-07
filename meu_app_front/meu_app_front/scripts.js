/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/gols';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.gols.forEach(gol => insertList(gol.jogador, gol.time_jogador, gol.time_adversario, gol.rodada, gol.min_gol,gol.id ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()


/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputJogador, inputTime_jogador, inputTime_adversario, inputRodada, inputMin_gol) => {
  const formData = new FormData();
  formData.append('jogador', inputJogador);
  formData.append('time_jogador', inputTime_jogador);
  formData.append('time_adversario', inputTime_adversario);
  formData.append('rodada', inputRodada);
  formData.append('min_gol', inputMin_gol);

  let url = 'http://127.0.0.1:5000/gol';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}



/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}


/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const idItem = div.getElementsByTagName('td')[5].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(idItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/gol?id=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  -------------------------------------------------------------------------------------------------------
  Função para adicionar um novo item com jogador, time do jogador, time adversario, rodada e min 
  -------------------------------------------------------------------------------------------------------
*/
const newItem = () => {
  let inputJogador = document.getElementById("newJogador").value;
  let inputTime_jogador = document.getElementById("newTime_jogador").value;
  let inputTime_adversario = document.getElementById("newTime_adversario").value;
  let inputRodada = document.getElementById("newRodada").value;
  let inputMin_gol = document.getElementById("newMin_gol").value;

  if (inputJogador === '') {
    alert("Escreva o nome de um Jogador!");
  } else if (isNaN(inputRodada) || isNaN(inputMin_gol)) {
    alert("Rodada e Minuto precisam ser números!");
  } else if (inputRodada > 38 || inputRodada < 0) {
    alert("Preencher a rodada de 1 até 38!");
  } else if (inputMin_gol > 110) {
    alert("Preencher minutos mais acréscimo (1 até 100)");
  } else {
  
    insertList(inputJogador, inputTime_jogador, inputTime_adversario, inputRodada, inputMin_gol)
    postItem(inputJogador, inputTime_jogador, inputTime_adversario, inputRodada, inputMin_gol)
    
    alert("Item adicionado!")
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (id,jogador, time_jogador, time_adversario, rodada, min_gol) => {
  var item = [id,jogador, time_jogador, time_adversario, rodada,min_gol]
  var table = document.getElementById('myTable');
  var row = table.insertRow();
  row.className = "tabody"

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1));
  
  document.getElementById("newJogador").value = "";
  document.getElementById("newTime_jogador").value = "";
  document.getElementById("newTime_adversario").value = "";
  document.getElementById("newRodada").value = "";
  document.getElementById("newMin_gol").value = "";

  removeElement()
}