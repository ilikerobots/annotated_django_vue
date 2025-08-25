import {ref} from "vue";
import {defineStore} from "pinia";

// django-vue: pinia@3
export const useDiceStore = defineStore('dice', () => {

    const diceColor = ref("")
    const presetNameFilter = ref("")
    const enable3d = ref(true)

    return {
        diceColor,
        presetNameFilter,
        enable3d,
    }
}, {
    // django-vue: pinia-persist@2
    persist: true
});

