<template>
  <div class="container-fluid">
    <div class="row p-4 mt-5">
      <div class="col-12 d-flex justify-content-center">
        <div class="d-flex flex-column">
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
        <div class="d-flex flex-column p-2">
          <div v-if="srcCurrency && amount > 0" class="p-2">
            <h2>{{ srcCurrency }} {{ amount }}</h2>
          </div>
          <div v-if="tgtCurrency && convertedAmount > 0" class="p-2">
            <h2>{{ tgtCurrency }} {{ amount }}</h2>
          </div>
          <div v-if="!tgtCurrency && !srcCurrency">
            <div class="alert alert-warning">
              Preencha as opções ao lado
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';

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

const convertAmount = () => {
  if (amount.value <= 0 ||
      !currencyOpts.value.map((c) => c.id).includes(srcCurrency.value) ||
      !currencyOpts.value.map((c) => c.id).includes(tgtCurrency.value)
    )
    return;
  
}

watch([tgtCurrency, srcCurrency, amount], () => {
  convertAmount()
})
</script>


<style scoped>
</style>
