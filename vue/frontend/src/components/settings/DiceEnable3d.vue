<script setup lang="ts">

import {useDiceStore} from "@/store/dice.ts";

const diceStore = useDiceStore();


</script>

<template>
  <input type="checkbox" name="diceEnable3d" v-model="diceStore.enable3d">
  <label>Enable 3D Animation
  </label>
</template>

<style scoped>

</style>
