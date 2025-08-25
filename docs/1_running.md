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

