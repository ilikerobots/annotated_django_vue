import {defineCustomElement} from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedState from 'pinia-plugin-persistedstate'
import DiceIcon from './components/DiceIcon.vue'
import DiceKey from "@/components/DiceKey.vue";

// django-vue: pinia@1
const pinia = createPinia()

// django-vue: pinia-persist@1
pinia.use(piniaPluginPersistedState)


// django-vue: basic-component@2
// Cross compile this component and register it immediately with the browser
customElements.define('dice-icon',
  defineCustomElement(DiceIcon, {
    shadowRoot: false,
    // django-vue: pinia@2
    configureApp: (app) => { app.use(pinia)}
  }),
);

customElements.define('dice-key',
  defineCustomElement(DiceKey, {
    shadowRoot: false,
  }),
);

// django-vue: dynamic-registration@1
// Export the register function to allow the calling page to selectively register
export async function registerDicePresetCard(tag: string = 'dice-preset-card') {
    // Dynamic import ensures the component and it's dependencies are loaded only when needed
    const {default: DicePresetCard} = await import("@/components/DicePresetCard.vue");

    customElements.define(tag, defineCustomElement(DicePresetCard, {
        shadowRoot: false,
        configureApp: (app) => {
            app.use(pinia)}  // this component uses pinia
    }))
}

export async function registerDicePresetNameFilter(tag: string = 'dice-settings-preset-name-filter') {
    const {default: DicePresetNameFilter} = await import("@/components/settings/DicePresetNameFilter.vue");
    customElements.define(tag, defineCustomElement(DicePresetNameFilter, {
        shadowRoot: false,
        configureApp: (app) => { app.use(pinia)}  // this component uses pinia
    }))
}
export async function registerDiceColorChoice(tag: string = 'dice-settings-color-choice') {
    const {default: DiceColorChoice} = await import("@/components/settings/DiceColorChoice.vue");
    customElements.define(tag, defineCustomElement(DiceColorChoice, {
        shadowRoot: false,
        configureApp: (app) => { app.use(pinia)}  // this component uses pinia
    }))
}
export async function registerDiceEnable3d(tag: string = 'dice-settings-enable-3d') {
    const {default: DiceEnable3d} = await import("@/components/settings/DiceEnable3d.vue");
    customElements.define(tag, defineCustomElement(DiceEnable3d, {
        shadowRoot: false,
        configureApp: (app) => { app.use(pinia)}  // this component uses pinia
    }))
}
