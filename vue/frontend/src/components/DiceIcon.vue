<!-- django-vue: basic-component@1 -->
<script setup lang="ts">
import {useDiceStore} from "@/store/dice.ts";

defineProps<{
  size: number
  value: number
}
>();

const diceStore = useDiceStore();


</script>

<template>
  <!-- django-vue: pinia@6 -->
  <i :class="`df df-d${size}-${value}`"
     :style="{color: diceStore.diceColor}"
  ></i>
</template>

<style scoped>
i {
  font-size: 4.5rem;
}

</style>
