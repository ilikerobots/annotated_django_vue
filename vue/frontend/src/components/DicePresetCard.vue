<script setup lang="ts">

import {computed, ref} from "vue";
import {Motion} from "motion-v";
import {useDiceStore} from "@/store/dice.ts";
import {type Dice} from "@/types/dice.ts"
import Dice3dAnimation from "@/components/Dice3dAnimation.vue";
import {storeToRefs} from "pinia";

const props = defineProps<{
  rollUrl: string,
  presetName?: string,
}>();

const diceStore = useDiceStore();
const {presetNameFilter, enable3d} = storeToRefs(diceStore)

const matchesFilter = computed(() => {
  const term = (presetNameFilter.value || "").trim().toLowerCase();
  if (!term) return true;
  const name = (props.presetName || "").toLowerCase();
  return name.includes(term);
});

const rollTotal = ref<number | null>(null);
const rollHtml = ref<string>('');
const isMax = ref<boolean>(false);
const rollResults = ref<Dice[]>([]);
const modalTimer = ref<number>(0);

async function roll() {
  // django-vue: ajax-json-view@2
  const r = await fetch(props.rollUrl, {
    headers: {'X-Requested-With': 'XMLHttpRequest'}
  })
  const {total, is_max, dice_results, result_html} = await r.json()
  rollTotal.value = total
  rollHtml.value = result_html
  isMax.value = is_max
  rollResults.value = dice_results

  // Disable teleport after 2 seconds
  modalTimer.value = setTimeout(() => modalTimer.value = 0, 2500)

}


</script>

<template>

  <article v-show="matchesFilter" class="preset-card">

    <!-- django-vue: slot@1 -->
    <slot name="content"></slot>

    <!-- django-vue: teleport@1 -->
    <teleport
        to="#modal"
        v-if="modalTimer && enable3d"
    >
      <Motion
          v-if="isMax"
          class="celebration"
          :animate="{opacity: 0, scale: 8}"
          :transition="{duration: 2.0}"
      >!!!
      </Motion>
      <Dice3dAnimation v-if="rollResults" :rolls="rollResults"></Dice3dAnimation>
    </teleport>

    <!-- Note our response contains web components. No problem! -->
    <div v-else-if="rollHtml">


      <section>
        <div class="dice-result">{{ rollTotal }}</div>
      </section>
      <section>

        <div class="dice-container" v-html="rollHtml"></div>
      </section>

    </div>

    <footer>
      <button @click="roll">Quick Roll</button>
    </footer>

  </article>

</template>

<style scoped>

.dice-result {
  font-size: 2.0rem;
  font-weight: bold;
  color: #222;
  text-align: center;
  border: 4px solid #c2c7d0;
  background-color: #c2c7d0;
}

.dice-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;

  span {
    align-items: center;
  }

  i {
    position: relative;
    font-size: 64pt;
    line-height: 64pt;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}

.celebration {
  position: absolute;
  top: calc(50% - 36px);
  left: calc(50% - 26px);
  font-size: 64px;
  color: gold;
  pointer-events: none;
}

button {
  width: 100%;
}

</style>

<!-- To style the dynamic response (not explicitly part of the template), use unscoped style -->
<style>
.dice-container span {
  font-size: 4rem;
  display: flex;
  align-items: center;
  align-content: center;
  color: v-bind('diceStore.diceColor');
}
</style>
