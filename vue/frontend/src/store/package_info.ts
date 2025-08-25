import {ref} from "vue";
import {defineStore} from "pinia";

export const usePackageInfoStore = defineStore('package', () => {

  const packageInfo = ref<any[]>([])

  function setPackageInfo(info: any) {
    packageInfo.value = info;
  }

  return {
    packageInfo,
    setPackageInfo,
  }
});

