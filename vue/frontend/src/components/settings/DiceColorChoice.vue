<script setup lang="ts">

import {useDiceStore} from "@/store/dice.ts";

// django-vue: pinia@4
const diceStore = useDiceStore();


</script>

<template>
  <label> Dice Color
    <!-- django-vue: pinia@5 -->
    <select name="diceColor" v-model="diceStore.diceColor">
      <option value="" style="color: inherit"> default</option>
      <option value="Red" style="color: red">🔴 Red</option>
      <option value="Orange" style="color: orange">🟠 Orange</option>
      <option value="Yellow" style="color: Yellow">🟡 Yellow</option>
      <option value="Green" style="color: Green">🟢 Green</option>
      <option value="Cornflowerblue" style="color: Cornflowerblue">🔵 Blue</option>
      <option value="Violet" style="color: Violet">🟣 Violet</option>
    </select>
  </label>
</template>

<style scoped>

</style>
