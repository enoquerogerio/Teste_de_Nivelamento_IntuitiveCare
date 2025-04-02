<template>
  <div id="app" class="container">
    <h1>Consulta de Operadoras</h1>

    <div class="search-form">
      <input
        type="text"
        v-model="cnpj"
        placeholder="Digite o CNPJ da operadora (apenas números)"
        @keyup.enter="buscarOperadora"
      />
      <button @click="buscarOperadora">Buscar</button>
    </div>

    <div v-if="loading" class="loading">
      <p>Carregando dados...</p>
    </div>

    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-if="operadora && !loading" class="operadora-data">
      <h2>Dados da Operadora</h2>
      <table>
        <tbody>
          <tr>
            <td class="label">Registro ANS</td>
            <td>{{ operadora.Registro_ANS }}</td>
          </tr>
          <tr>
            <td class="label">CNPJ</td>
            <td>{{ operadora.CNPJ }}</td>
          </tr>
          <tr>
            <td class="label">Razão Social</td>
            <td>{{ operadora.Razao_Social }}</td>
          </tr>
          <tr>
            <td class="label">Modalidade</td>
            <td>{{ operadora.Modalidade }}</td>
          </tr>
          <tr>
            <td class="label">Telefone</td>
            <td>{{ operadora.Telefone }}</td>
          </tr>
          <tr>
            <td class="label">Endereço</td>
            <td>
              {{ operadora.Logradouro }}, {{ operadora.Numero }} -
              {{ operadora.Bairro }}
            </td>
          </tr>
          <tr>
            <td class="label">Cidade/UF</td>
            <td>{{ operadora.Cidade }}/{{ operadora.UF }}</td>
          </tr>
          <tr>
            <td class="label">CEP</td>
            <td>{{ operadora.CEP }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!operadora && !loading && !error" class="no-data">
      <p>Nenhum dado encontrado. Faça uma busca pelo CNPJ.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const cnpj = ref("");
const operadora = ref(null);
const loading = ref(false);
const error = ref("");

const buscarOperadora = async () => {
  error.value = "";
  loading.value = true;

  try {
    const response = await fetch(
      `http://localhost:5000/api/operadoras/${cnpj.value}`
    );
    if (!response.ok) throw new Error("Operadora não encontrada");
    operadora.value = await response.json();
  } catch (e) {
    error.value = e.message || "Erro ao buscar dados da operadora";
    operadora.value = null;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

body {
  background-color: #f5f5f5;
  padding: 20px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

.search-form {
  display: flex;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #2980b9;
}

.operadora-data {
  margin-top: 20px;
}

.loading {
  text-align: center;
  color: #7f8c8d;
  margin: 20px 0;
}

.error {
  color: #e74c3c;
  margin: 20px 0;
  padding: 10px;
  background-color: #fadbd8;
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

.label {
  font-weight: bold;
  width: 30%;
}

.no-data {
  text-align: center;
  color: #7f8c8d;
  margin: 20px 0;
}
</style>
