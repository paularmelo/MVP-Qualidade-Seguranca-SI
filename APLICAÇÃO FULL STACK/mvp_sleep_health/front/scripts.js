/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/pessoas';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.pessoas.forEach(item => insertList(item.person_id,
        item.gender,
        item.age,
        item.sleep_duration,
        item.quality_sleep,
        item.activity_level,
        item.stress_level,
        item.bmi_category,
        item.blood_pressure,
        item.heart_rate,
        item.daily_steps,
        item.outcome
      ))
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
const postItem = async (inputPersonID, inputGender, inputAge,
  inputDuration, inputQuality, inputLevelActivity,
  inputLevelStress, inputBMI, inputPressure, inputHeartRate, inputDailySteps) => {

  const formData = new FormData();
  formData.append('person_id', inputPersonID);
  formData.append('gender', inputGender);
  formData.append('age', inputAge);
  formData.append('sleep_duration', inputDuration);
  formData.append('quality_sleep', inputQuality);
  formData.append('activity_level', inputLevelActivity);
  formData.append('stress_level', inputLevelStress);
  formData.append('bmi_category', inputBMI);
  formData.append('blood_pressure', inputPressure);
  formData.append('heart_rate', inputHeartRate);
  formData.append('daily_steps', inputDailySteps);

  let url = 'http://127.0.0.1:5000/pessoa';
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
  let url = 'http://127.0.0.1:5000/pessoa?person_id=' + item;
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

const newItem = async () => {
  let inputPersonID = document.getElementById("newPersonID").value;
  let inputGender = document.getElementById("newGender").value;
  let inputAge = document.getElementById("newAge").value;
  let inputDuration = document.getElementById("newDuration").value;
  let inputQuality = document.getElementById("newQuality").value;
  let inputLevelActivity = document.getElementById("newLevelActivity").value;
  let inputLevelStress = document.getElementById("newLevelStress").value;
  let inputBMI = document.getElementById("newBMI").value;
  let inputPressure = document.getElementById("newPressure").value;
  let inputHeartRate = document.getElementById("newHeartRate").value;
  let inputDailySteps = document.getElementById("newDailySteps").value;

  // Verifique se o nome da pessoa já existe antes de adicionar
  const checkUrl = `http://127.0.0.1:5000/pessoas?person_id=${inputPersonID}`;
  fetch(checkUrl, {
    method: 'get'
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.pacientes && data.pacientes.some(item => item.person_id === inputPersonID)) {
        alert("A pessoa já está cadastrada.\nCadastre uma pessoa com identificação diferente ou atualize o existente.");
      } else if (inputPersonID === '') {
        alert("A identificaçao da pessoa não pode ser vazio!");
      } else if (isNaN(inputPersonID) || isNaN(inputAge) || isNaN(inputDuration) || isNaN(inputQuality) || isNaN(inputLevelActivity) || isNaN(inputLevelStress) || isNaN(inputBMI) || isNaN(inputPressure) || isNaN(inputHeartRate) || isNaN(inputDailySteps)) {
        alert("Esse(s) campo(s) precisam ser números!");
      } else {
        insertList(inputPersonID, inputGender, inputAge, inputDuration, inputQuality, inputLevelActivity, inputLevelStress, inputBMI, inputPressure, inputHeartRate, inputDailySteps);
        postItem(inputPersonID, inputGender, inputAge, inputDuration, inputQuality, inputLevelActivity, inputLevelStress, inputBMI, inputPressure, inputHeartRate, inputDailySteps);
        alert("Item adicionado!");
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (person_id, gender, age, sleep_duration, quality_sleep, activity_level, stress_level, bmi_category, blood_pressure, heart_rate, daily_steps, outcome) => {
  var item = [person_id, gender, age, sleep_duration, quality_sleep, activity_level, stress_level, bmi_category, blood_pressure, heart_rate, daily_steps, outcome];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);

  document.getElementById("newPersonID").value = "";
  document.getElementById("newGender").value = "";
  document.getElementById("newAge").value = "";
  document.getElementById("newDuration").value = "";
  document.getElementById("newQuality").value = "";
  document.getElementById("newLevelActivity").value = "";
  document.getElementById("newLevelStress").value = "";
  document.getElementById("newBMI").value = "";
  document.getElementById("newPressure").value = "";
  document.getElementById("newHeartRate").value = "";
  document.getElementById("newDailySteps").value = "";

  removeElement();
}