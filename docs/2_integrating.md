## Integrating Vue into Your Own Project

The following steps will add a very simple Vue project to your Django project, allowing you to use Vue 
components by custom-tag name in your Django templates. 

For advanced techniques, see [Annotated Code](#annotated-code).

### Create a Vue Project
From your Django root directory

```
mkdir -p vue
cd vue
npm create vue@latest
```

Answer the questions.  
 * Name your project, e.g. `frontend`
 * I recommend enabling at the following features 
   * TypeScript
   * Pinia
   * ESLint
* Include example code or not as you prefer.


### Run the Vue Dev Server

```
   cd frontend
   npm install
   npm run dev
```

### Vue SFCs to Native Web Components

In the entrypoint `main.ts/js`, define Vue Single File Components (SFCs) as native web components.

For example, to define the 'App' element, use the following:

```js
import {defineCustomElement} from 'vue'

customElements.define('my-app',
    defineCustomElement(App, {
        shadowRoot: false,
        configureApp: (app) => {
            app.use(pinia) // if using pinia
        }
    }),
);

```

This will create a custom element `my-app` that can be used in your HTML.

See [Annotated Code](#annotated-code) for additional strategies.

### Import entrypoint in Django

Somewhere in the Django template tree where the custom element is used, import the entrypoint.

```html
<script type="module" src="http://localhost:5173/src/main.js"></script>
```

Note this links to the Vue dev server.  For production configuration, see [Annotated Code](#annotated-code).

### Use your Custom Element in Django Templates

In your django templates, use the custom element by tag name, providing any property values as simple HTML attributes.


```html
<my-app welcome-message="Hello World!"></my-app>
```

