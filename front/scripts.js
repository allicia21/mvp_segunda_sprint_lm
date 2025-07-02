/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/clientes';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.cliente.forEach(item => insertList(
        item.person_age,
        item.person_gender,
        item.person_education,
        item.person_income,
        item.person_emp_exp,
        item.person_home_ownership,
        item.loan_amnt,
        item.loan_intent,
        item.loan_int_rate,
        item.loan_percent_income,
        item.cb_person_cred_hist_length,
        item.credit_score,
        item.previous_loan_defaults_on_file,
        item.loan_status
      ));
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para limpar a tabela antes de recarregar os dados
  --------------------------------------------------------------------------------------
*/
const clearTable = () => {
  var table = document.getElementById('myTable');
  // Remove todas as linhas exceto o cabeçalho (primeira linha)
  while (table.rows.length > 1) {
    table.deleteRow(1);
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para recarregar a lista completa do servidor
  --------------------------------------------------------------------------------------
*/
const refreshList = async () => {
  clearTable();
  await getList();
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
// Carrega a lista apenas uma vez quando a página é carregada
document.addEventListener('DOMContentLoaded', function () {
  getList();
});

/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
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
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
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
  let url = 'http://127.0.0.1:5000/cliente?name=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = async (event) => {
  event.preventDefault();

  let person_age = document.getElementById("person_age").value;
  let person_gender = document.getElementById("person_gender").value;
  let person_education = document.getElementById("person_education").value;
  let person_income = document.getElementById("person_income").value;
  let person_emp_exp = document.getElementById("person_emp_exp").value;
  let person_home_ownership = document.getElementById("person_home_ownership").value;
  let loan_amnt = document.getElementById("loan_amnt").value;
  let loan_intent = document.getElementById("loan_intent").value;
  let loan_int_rate = document.getElementById("loan_int_rate").value;
  let loan_percent_income = document.getElementById("loan_percent_income").value;
  let cb_person_cred_hist_length = document.getElementById("cb_person_cred_hist_length").value;
  let credit_score = document.getElementById("credit_score").value;
  let previous_loan_defaults_on_file = document.getElementById("previous_loan_defaults_on_file").value;

  // Validar se todos os campos obrigatórios foram preenchidos e são números quando necessário
  if (
    [person_age, person_gender, person_education, person_income, person_emp_exp, person_home_ownership,
      loan_amnt, loan_intent, loan_int_rate, loan_percent_income, cb_person_cred_hist_length,
      credit_score, previous_loan_defaults_on_file].some(field => field === "")
  ) {
    alert("Por favor, preencha todos os campos.");
    return;
  }

  // Campos que devem ser numéricos
const numericFields = [
  person_age,
  person_income,
  person_emp_exp,
  loan_amnt,
  loan_int_rate,
  loan_percent_income,
  cb_person_cred_hist_length,
  credit_score,
  previous_loan_defaults_on_file
];

// Verifica se algum campo numérico está vazio
if (
  numericFields.some(field => field === "")
) {
  alert("Preencha todos os campos numéricos.");
  return;
}

// Verifica se algum campo numérico não é número
if (
  numericFields.some(field => isNaN(field))
) {
  alert("Alguns campos numéricos contêm valores inválidos.");
  return;
}

// Verifica se campos string obrigatórios foram preenchidos
if (
  !person_gender || !person_education || !person_home_ownership || !loan_intent
) {
  alert("Preencha todos os campos de seleção (gênero, escolaridade, moradia e intenção).");
  return;
}

  // Montar objeto JSON para enviar via POST
  const data = {
    person_age: Number(person_age),
    person_gender: person_gender,               // string
    person_education: person_education,         // string
    person_income: Number(person_income),
    person_emp_exp: Number(person_emp_exp),
    person_home_ownership: person_home_ownership, // string
    loan_amnt: Number(loan_amnt),
    loan_intent: loan_intent,                   // string
    loan_int_rate: Number(loan_int_rate),
    loan_percent_income: Number(loan_percent_income),
    cb_person_cred_hist_length: Number(cb_person_cred_hist_length),
    credit_score: Number(credit_score),
    previous_loan_defaults_on_file: Number(previous_loan_defaults_on_file),
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/cliente", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Erro na API:", errJson);
      alert("Erro: " + (errJson.message || "Dados inválidos"));
      return;
    }

    const result = await response.json();

    // Limpar campos após adicionar
    document.getElementById("person_age").value = "";
    document.getElementById("person_gender").value = "";
    document.getElementById("person_education").value = "";
    document.getElementById("person_income").value = "";
    document.getElementById("person_emp_exp").value = "";
    document.getElementById("person_home_ownership").value = "";
    document.getElementById("loan_amnt").value = "";
    document.getElementById("loan_intent").value = "";
    document.getElementById("loan_int_rate").value = "";
    document.getElementById("loan_percent_income").value = "";
    document.getElementById("cb_person_cred_hist_length").value = "";
    document.getElementById("credit_score").value = "";
    document.getElementById("previous_loan_defaults_on_file").value = "";

    await refreshList();

    const situacao = result.loan_status === 1 ? "Aprovado" : "NÃO Aprovado";
    alert(`Cliente adicionado com sucesso!\nDiagnóstico: ${situacao}`);

    document.querySelector(".items").scrollIntoView({
      behavior: "smooth",
      block: "center",
    });

  } catch (error) {
    console.error("Erro ao adicionar cliente:", error);
    alert("Erro ao adicionar cliente. Tente novamente.");
  }
};


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (age, gender, education, person_income, person_emp_exp,
  person_home_ownership, loan_amnt, loan_intent, loan_int_rate, loan_percent_income,
  cb_person_cred_hist_length, credit_score, previous_loan_defaults_on_file, loan_status) => {
  var item = [age, gender, education, person_income, person_emp_exp, person_home_ownership, loan_amnt,
    loan_intent, loan_int_rate,loan_percent_income,cb_person_cred_hist_length,credit_score,previous_loan_defaults_on_file,loan_status];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  // Insere as células com os dados do paciente
  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  // Insere a célula do diagnóstico com styling
 // var diagnosticCell = row.insertCell(item.length);
  //const diagnosticText = outcome === 1 ? "Aprovado" : "Não Aprovado";
  //diagnosticCell.textContent = diagnosticText;

  const diagnosticText = loan_status === 1 ? "Aprovado" : "Não Aprovado";
  diagnosticCell.textContent = diagnosticText;
  diagnosticCell.className = loan_status === 1 ? "diagnostic-positive" : "diagnostic-negative";


  // Aplica styling baseado no diagnóstico
  if (loan_status === 1) {
    diagnosticCell.className = "diagnostic-positive";
  } else {
    diagnosticCell.className = "diagnostic-negative";
  }

  // Insere o botão de deletar
  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);

  removeElement();
}