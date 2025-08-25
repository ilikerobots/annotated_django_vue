import {createPinia} from "pinia";
import {usePackageInfoStore} from "@/store/package_info.ts";
import {defineCustomElement} from "vue";
import PackageInfo from "@/components/PackageInfo.vue";

const pinia = createPinia();

customElements.define('package-info',
  defineCustomElement(PackageInfo, {
    shadowRoot: false,
    configureApp(app) {
      app.use(pinia)
    }
  }),
);


// django-vue: passing-complex-data@1
// We can expose the store so that our Django template can potentially inject data
export const packageStore = usePackageInfoStore(pinia)


