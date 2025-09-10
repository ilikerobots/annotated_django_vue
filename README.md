# Annotated Django + Vue Demo

This is a demo app illustrating an approach to integrating Vue into a Django app. Vue Single File Components are 
cross-compiled to native Web Components and used by custom element tag name in Django Templates.

A variety of techniques are demonstrated, which are described in the [Annotated Code](#annotated-code) section.

To incorporate Vue into your own project, see [Integrating Vue into your own Project](#integrating-vue-into-your-own-project)



## Running this project

### Prerequisites
- Python 3.12 (or compatible Python 3.x)
- Node.js 18+ and npm (required for the Vue dev server and optional CSS rebuilds)


### 0. Clone the project
If you have not already cloned this project, do so:
- git clone https://github.com/ilikerobots/annotated_django_vue.git

### 1. Clone and enter the project
- cd annotated_django_vue

### 2. (Recommended) Create and activate a virtual environment
- python3 -m venv .venv
- source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

### 3. Install Python dependencies
- pip install -r requirements.txt

### 3.5 Install PicoCSS sass
- npm install

### 4. Apply database migrations
- python manage.py migrate

### 5. Run the Django development server
- python manage.py runserver

### 6. Running the Vue frontend with Vite
The Vue app lives under `vue/frontend` and is served by Vite during development.

In a separate terminal, start the Vite dev server:
  1. cd vue/frontend
  2. npm install
  3. npm run dev  

Then open http://127.0.0.1:8000/ in your browser. The admin site is at http://127.0.0.1:8000/admin/ (log in with admin/admin).

### 7. (Optional) Customizing CSS

- The CSS is generated from PicoCSS Sass files located in `scss/`
- If you modify the sass, you'll need to recompile the sass files to generate the new main.css:
    1. Install Node.js and npm
    2. Run `npm install`
    3. Run `npm run build-css` for a one-off build
    4. Or run `npm run watch-css` to auto-rebuild on changes



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



## Annotated Code

### A first basic component

First, create a new Vue component (1).   Next, create a Web Component in an entrypoint file (2). Ensure the entrypoint is included in the Django template tree (3).   Finally, use the component by custom tag name (4), passing property values as simple HTML attributes.


1. [vue/frontend/src/components/DiceIcon.vue:1](vue/frontend/src/components/DiceIcon.vue#L1)
1. [vue/frontend/src/main.ts:14](vue/frontend/src/main.ts#L14)
1. [rpgdice/templates/base.html:76](rpgdice/templates/base.html#L76)
1. [rpgdice/templates/index.html:11](rpgdice/templates/index.html#L11)

### Rendering Partial HTML responses

Components can make AJAX requests to Django views and render the partial pre-rendered HTML responses.   First, create a view that will return partial HTML (1). Next, a component will listen for an event (2) and then  make the AJAX request (3). The response HTML is displayed directly in an element using v-html (4). 


1. [rpgdice/views.py:62](rpgdice/views.py#L62)
1. [vue/frontend/src/components/DiceKey.vue:26](vue/frontend/src/components/DiceKey.vue#L26)
1. [vue/frontend/src/components/DiceKey.vue:12](vue/frontend/src/components/DiceKey.vue#L12)
1. [vue/frontend/src/components/DiceKey.vue:34](vue/frontend/src/components/DiceKey.vue#L34)

### Consuming JSON responses from AJAX requests

Components consume AJAX responses that include JSON, and this can be done without needing a full REST API. Simply return a JSONResponse (1) in the view. A component makes the AJAX request and consumes the JSON payload (2).


1. [rpgdice/views.py:46](rpgdice/views.py#L46)
1. [vue/frontend/src/components/DicePresetCard.vue:32](vue/frontend/src/components/DicePresetCard.vue#L32)

### Shared State with Pinia

Components can share state information with other components using Pinia. First, create a Pinia instance in an  entrypoint (1). Next, designate which components need access to Pinia (2). Then, create a store with reactive state  variables (3). In components, access the store (4), then use the state variables within the  component (5, 6).


1. [vue/frontend/src/main.ts:7](vue/frontend/src/main.ts#L7)
1. [vue/frontend/src/main.ts:19](vue/frontend/src/main.ts#L19)
1. [vue/frontend/src/store/dice.ts:4](vue/frontend/src/store/dice.ts#L4)
1. [vue/frontend/src/components/settings/DiceColorChoice.vue:5](vue/frontend/src/components/settings/DiceColorChoice.vue#L5)
1. [vue/frontend/src/components/settings/DiceColorChoice.vue:13](vue/frontend/src/components/settings/DiceColorChoice.vue#L13)
1. [vue/frontend/src/components/DiceIcon.vue:17](vue/frontend/src/components/DiceIcon.vue#L17)

### Persisting Pinia state across page loads

Unless persisted, Pinia state is lost when the page is reloaded. State can be persisted across page loads by using pinia-plugin-persistedstate (1), which uses the browser's native storage to serialize and deserialize state. To  persist a store, use the persist: true option in the store config (2) to persist the entire store. It is also  possible to persist only specific state variables. 


1. [vue/frontend/src/main.ts:10](vue/frontend/src/main.ts#L10)
1. [vue/frontend/src/store/dice.ts:17](vue/frontend/src/store/dice.ts#L17)

### Slot rendered Django template content into a Vue component

A Vue component can provide one or more slots (1). This is very useful for passing in content that includes Django content (2), such as static and url template tags. Slots also allow different content to be passed to the same component (3). 


1. [vue/frontend/src/components/DicePresetCard.vue:54](vue/frontend/src/components/DicePresetCard.vue#L54)
1. [rpgdice/templates/rpgdice/dice_preset_list.html:21](rpgdice/templates/rpgdice/dice_preset_list.html#L21)
1. [rpgdice/templates/rpgdice/roll_dice_detail.html:8](rpgdice/templates/rpgdice/roll_dice_detail.html#L8)

### Teleport Vue content anywhere in your page

Vue components can teleport content anywhere in the DOM. This can even be done conditionally  (e.g., with v-if or :disabled). Teleported content can include any normal Vue logic, despite appearing anywhere on the page (2,3).


1. [vue/frontend/src/components/DicePresetCard.vue:57](vue/frontend/src/components/DicePresetCard.vue#L57)
1. [vue/frontend/src/components/DiceKey.vue:38](vue/frontend/src/components/DiceKey.vue#L38)
1. [vue/frontend/src/components/settings/DicePresetNameFilter.vue:29](vue/frontend/src/components/settings/DicePresetNameFilter.vue#L29)

### Multiple entry points and selective loading

Configure multiple entry points in Vite (1) and load components only on pages that need them (2, 3).  If dynamic imports are used within the registration function, then those components (along with their dependencies) will only be loaded on pages that need them.


1. [vue/frontend/vite.config.ts:26](vue/frontend/vite.config.ts#L26)
1. [rpgdice/templates/index.html:42](rpgdice/templates/index.html#L42)
1. [rpgdice/templates/rpgdice/dice_preset_list.html:41](rpgdice/templates/rpgdice/dice_preset_list.html#L41)

### Dynamically register only needed custom elements

Instead of directly registering custom elements in the entrypoint, use a helper function (1) to allow the calling page to selectively register components (2).  


1. [vue/frontend/src/main.ts:30](vue/frontend/src/main.ts#L30)
1. [rpgdice/templates/rpgdice/dice_preset_list.html:45](rpgdice/templates/rpgdice/dice_preset_list.html#L45)

### Passing complex data to a Vue component without Ajax

Vue will coerce values for string, boolean, and number properties from the HTML attributes. However, anything more complex will simply be treated as a string. If a component needs to receive more complex data, the simplest approach is usually with an AJAX request. However, if avoiding an AJAX request is desired, complex data can still be passed in other ways. One way is to expose the Pinia store in an entrypoint (1). Then call a method or use a variable from  the Django template (2) to set the state in conjunction with the Django json_script template tag (3). Components can then use the store normally to access the data (4).


1. [vue/frontend/src/packages.ts:18](vue/frontend/src/packages.ts#L18)
1. [rpgdice/templates/index.html:49](rpgdice/templates/index.html#L49)
1. [rpgdice/templates/index.html:46](rpgdice/templates/index.html#L46)
1. [vue/frontend/src/components/PackageInfo.vue:5](vue/frontend/src/components/PackageInfo.vue#L5)

### Using the Vue dev server

Even when using Django Template, the Vue development server features such as Hot Module Replacement (HMR) and Vue Dev Tools work as expected. The Vue dev server frontend can also be accessed from a browser, usually on http://localhost:5173. This feature can often be useful for larger teams, where the JavaScript crew can develop components without having to run a Django server.


* [vue/frontend/index.html:17](vue/frontend/index.html#L17)

### Styling Vue Components with SCSS

Vue components can be styled with SCSS (1). If the Django project is using an SCSS framework, those project files can be imported (2) as needed to refer to variables and mixins (3).  


1. [vue/frontend/src/components/settings/DicePresetNameFilter.vue:34](vue/frontend/src/components/settings/DicePresetNameFilter.vue#L34)
1. [vue/frontend/src/components/settings/DicePresetNameFilter.vue:37](vue/frontend/src/components/settings/DicePresetNameFilter.vue#L37)
1. [vue/frontend/src/components/settings/DicePresetNameFilter.vue:43](vue/frontend/src/components/settings/DicePresetNameFilter.vue#L43)

### Hiding undefined content with CSS

Normally, the content inside a custom tag is displayed even if the tag is not defined. Since components are registered  near the end of the body, this means there can be a brief flash of improperly rendered slot content  before the tag becomes defined. To prevent this, add CSS styles (1) that hide content inside of  undefined tags. Exceptions to this rule can be made if needed (2).


1. [scss/custom.scss:1](scss/custom.scss#L1)
1. [rpgdice/templates/index.html:13](rpgdice/templates/index.html#L13)

### CSS injected by JavaScript

During a production build, Vite will normally produce separate JavaScript and CSS files. This means both would  normally need to be loaded in the Django template. This is cumbersome at best, but can be avoided with a plugin that will automatically inject the CSS when the JavaScript entrypoint is loaded (1).


* [vue/frontend/vite.config.ts:12](vue/frontend/vite.config.ts#L12)

### Allow exports in entrypoints

Vite will normally strip any exports from entrypoints that are unused in the JavaScript project, as part of its  optimization. However, if calling exports from Django is needed, Vite must be configured to preserve the entrypoint  exports (1).


* [vue/frontend/vite.config.ts:22](vue/frontend/vite.config.ts#L22)

### Production build

In a production build, Vite will produce JavaScript files. Vite can output these to a Django static  directory (1) and from that point they can be treated as normal static files. To prevent having to manually swap URLs between static production and Vue devserver, set up settings based on the Django DEBUG setting (2). Use a context processor to add this to the template context (3), and then use the new context variable to refer to  the correct entrypoint URL throughout templates (4).

1. [vue/frontend/vite.config.ts:32](vue/frontend/vite.config.ts#L32)
1. [rpgdice/settings.py:120](rpgdice/settings.py#L120)
1. [rpgdice/context_processors.py:5](rpgdice/context_processors.py#L5)
1. [rpgdice/templates/base.html:76](rpgdice/templates/base.html#L76)

