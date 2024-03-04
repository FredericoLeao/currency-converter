<template>
  <div class="container-fluid">
    <div class="row p-4 mt-5">
      <div class="col-12 col-md-2 offset-md-4">
        <div class="p-2">
          <input type="text" name="convert_amount" placeholder="Valor a ser convertido" class="form-control" v-model="amount">
        </div>
        <div class="p-2">
          <select class="form-control" id="src_currency" v-model="srcCurrency">
            <option value="" disabled>Selecione a moeda de origem</option>
            <option v-for="(currency, idx) in currencyOpts" :key="idx" :value="currency.id">
              {{ currency.name }}
            </option>
          </select>
        </div>
        <div class="p-2">
          <select placeholder="Origem" class="form-control" id="src_currency" v-model="tgtCurrency">
            <option value="" disabled>Selecione a moeda de destino</option>
            <option v-for="(currency, idx) in tgtCurrencyOpts" :key="idx" :value="currency.id">
              {{ currency.name }}
            </option>
          </select>
        </div>
      </div>
      <div class="col-md-2">
        <div class="py-5">
          <template v-if="srcCurrency && tgtCurrency && amount > 0">
            <div class="">
              <p><b>{{ srcCurrency }}</b> {{ amount }}</p>
            </div>
            <div class="">
              <p><b>{{ tgtCurrency }}</b> {{ convertedAmount }}</p>
            </div>
          </template>
          <div v-if="!tgtCurrency || !srcCurrency || !amount || parseInt(amount) <= 0">
            <div class="alert alert-warning d-none d-sm-block">
              Preencha as opções ao lado
            </div>
            <div class="alert alert-warning d-sm-none">
              Preencha as opções acima
            </div>
          </div>
          <div v-if="responseError != ''">
            <div class="alert alert-danger">{{ responseError }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import axios from 'axios';

const amount = ref('');
const convertedAmount = ref(0);

const srcCurrency = ref('');
const tgtCurrency = ref('');

const currencyOpts = ref([
  { id: 'USD', name: 'Dólar americano' },
  { id: 'BRL', name: 'Real Brasileiro' },
  { id: 'EUR', name: 'Euro' },
  { id: 'BTC', name: 'Bitcoin' },
  { id: 'ETH', name: 'Ethereum' },
]);
const tgtCurrencyOpts = computed(() => currencyOpts.value.filter((c) => c.id !== srcCurrency.value));

const responseError = ref('');
const requestTimeout = ref(null);
const convertAmount = () => {
  if (amount.value <= 0 ||
      !currencyOpts.value.map((c) => c.id).includes(srcCurrency.value) ||
      !currencyOpts.value.map((c) => c.id).includes(tgtCurrency.value)
    )
    return;

  responseError.value = ''
  clearTimeout(requestTimeout.value);
  requestTimeout.value = setTimeout(() => {
    axios.get(`/api/convert/${srcCurrency.value}/${tgtCurrency.value}/${amount.value}/`)
      .then((response) => {
        convertedAmount.value = response.data;
      })
      .catch((errors) => {
        responseError.value = errors.response.data
      });
  }, 440);
}

watch([tgtCurrency, srcCurrency, amount], () => {
  convertAmount();
});
</script>


<style scoped>
</style>
