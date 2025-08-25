<script setup lang="ts">
import {useDiceStore} from "@/store/dice.ts";
import {storeToRefs} from "pinia";

const diceStore = useDiceStore();
const {presetNameFilter} = storeToRefs(diceStore)

function clearSearch() {
  presetNameFilter.value = ''
}

</script>

<template>
  <label>
    Preset Name
    <input
        type="search"
        name="presetName"
        placeholder="Search presets by name..."
        v-model.trim="presetNameFilter"
    />
  </label>


  <Teleport to="#filter_indicator" v-if="presetNameFilter">
    <small>Search: {{ presetNameFilter }}</small>
    &nbsp;
    <!-- django-vue: teleport@3 -->
    <i @click="clearSearch" class="ra ra-interdiction"></i>
  </Teleport>
</template>

<!-- django-vue: scss@1 -->
<style lang="scss" scoped>

// django-vue: scss@2
@use "../../../../../scss/variables";

i {
  font-size: .8rem;
  cursor: pointer;
  color: variables.$danger; // django-vue: scss@3
}
</style>
