<script setup lang="ts">
import {ref} from "vue";

const props = defineProps<{
  keyUrl: string
}>()



const keyHtml = ref<null | string>(null);

// django-vue: render-partial-view@3
async function getKey() {
  const r = await fetch(props.keyUrl)
  keyHtml.value = await r.text()
}

function dismiss() {
  keyHtml.value = null
}


</script>

<template>
  <!-- django-vue: render-partial-view@2 -->
  <span @click="getKey">
  <slot></slot>
  </span>

  <Teleport to="#modal" v-if="keyHtml">
    <article>

      <!-- django-vue: render-partial-view@4 -->
      <div v-html="keyHtml"></div>

      <section>
        <!-- django-vue: teleport@2 -->
        <!-- the button still works despite being teleported into the modal -->
        <button @click="dismiss">Dismiss</button>
      </section>
    </article>
  </Teleport>

</template>

<style scoped>
span {
  cursor: pointer;
}

article {
  text-align: center
}
</style>
