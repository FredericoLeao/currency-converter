<template>
  <div class="container-fluid">
    <div class="row p-4 mt-5">
      <div class="col-12 col-md-2 offset-md-4">
        <div class="p-2">
          <input
            type="text"
            name="convert_amount"
            placeholder="Valor a ser convertido"
            class="form-control text-end"
            v-model="amount"
            v-money="moneyMask"
            maxlength="12">
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
            <div v-if="httpLoading">
              <div class="loader"></div>
            </div>
            <div v-else>
              <p><b>{{ tgtCurrency }}</b> {{ convertedAmount.toFixed(tgtCurrencyDecimals) }}</p>
            </div>
          </template>
          <div v-if="!tgtCurrency || !srcCurrency || !amount || parseFloat(amount) <= 0">
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
import { VMoney } from 'v-money';

const amount = ref('');
const convertedAmount = ref(0);

const srcCurrency = ref('');
const tgtCurrency = ref('');

const currencyOpts = ref([
  { id: 'USD', name: 'Dólar americano' },
  { id: 'BRL', name: 'Real Brasileiro' },
  { id: 'EUR', name: 'Euro' },
  { id: 'BTC', name: 'Bitcoin', maskDecimals: 6 },
  { id: 'ETH', name: 'Ethereum' },
]);
const tgtCurrencyOpts = computed(() => currencyOpts.value.filter((c) => c.id !== srcCurrency.value));

const tgtCurrencyDecimals = computed(() => {
  let precision = currencyOpts.value.find((c) => c.id === tgtCurrency.value)?.maskDecimals;
  if (!precision)
    precision = 2;
  return precision;
});
const moneyMask = computed(() => {
  let precision = currencyOpts.value.find((c) => c.id === srcCurrency.value)?.maskDecimals;
  if (!precision)
    precision = 2;
    
  return {
    decimal: '.',
    thousands: '',
    prefix: '',
    suffix: '',
    precision: precision,
  }
});

const httpLoading = ref(false);
const responseError = ref('');
const requestTimeout = ref(null);
const convertAmount = () => {
  if (amount.value <= 0 ||
      !currencyOpts.value.map((c) => c.id).includes(srcCurrency.value) ||
      !currencyOpts.value.map((c) => c.id).includes(tgtCurrency.value)
    )
    return;

  responseError.value = '';
  httpLoading.value = true;
  clearTimeout(requestTimeout.value);
  requestTimeout.value = setTimeout(() => {
    axios.get(`/api/convert/${srcCurrency.value}/${tgtCurrency.value}/${amount.value}/`)
      .then((response) => {
        if (response.data['converted_amount'])
          convertedAmount.value = response.data['converted_amount'];
        else
          responseError.value = 'Erro inesperado';
      })
      .catch((errors) => {
        responseError.value = errors.response.data;
      })
      .finally(() => httpLoading.value = false);
  }, 440);
}

watch([tgtCurrency, srcCurrency, amount], () => {
  convertAmount();
});
</script>


<style scoped>
.loader {
  width: 20px;
  aspect-ratio: 4;
  background: radial-gradient(circle closest-side,#000 90%,#0000) 0/calc(100%/3) 100% space;
  clip-path: inset(0 100% 0 0);
  animation: l1 1s steps(4) infinite;
}
@keyframes l1 {to{clip-path: inset(0 -34% 0 0)}}
</style>
