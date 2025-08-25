<script setup lang="ts">
import {usePackageInfoStore} from "@/store/package_info.ts";
import {storeToRefs} from "pinia";

// django-vue: passing-complex-data@4
const packageStore = usePackageInfoStore();
const {packageInfo} = storeToRefs(packageStore);

</script>

<template>

  <table>
    <tbody>
    <tr v-for="pkg in packageInfo" :key="pkg.name">
      <td>
        <a :data-tooltip="pkg.description" data-placement="right" :href="pkg.url">{{ pkg.name }}</a>
      </td>
    </tr>
    </tbody>
  </table>

</template>

<style scoped>
</style>
