# 🚀 Manual GitHub Pages Setup (Sin GitHub Actions)

Debido a restricciones de permisos, necesitas agregar los archivos de deployment manualmente.

## 📋 **Opción 1: Via GitHub Web Interface (Más Fácil)**

### **1. Habilitar GitHub Pages**

1. Ve a: https://github.com/adrianlerer/legal-evolution-unified/settings/pages
2. En **Source**, selecciona: `Deploy from a branch`
3. En **Branch**, selecciona: `gh-pages` / `root`
4. Click **Save**

### **2. Crear el Workflow Manualmente**

1. Ve a tu repositorio: https://github.com/adrianlerer/legal-evolution-unified
2. Click en **Add file** → **Create new file**
3. Nombre del archivo: `.github/workflows/deploy-pages.yml`
4. Copia y pega este contenido:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          BASE_PATH: /legal-evolution-unified

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

5. Click **Commit changes** → **Commit directly to the main branch**

### **3. Cambiar Source a GitHub Actions**

1. Vuelve a: https://github.com/adrianlerer/legal-evolution-unified/settings/pages
2. En **Source**, ahora selecciona: `GitHub Actions`
3. Ya no necesitas seleccionar branch

### **4. Trigger el Deploy**

El workflow se ejecutará automáticamente. Para forzarlo:

1. Ve a: https://github.com/adrianlerer/legal-evolution-unified/actions
2. Click en workflow **"Deploy to GitHub Pages"** (si lo ves)
3. Click **Run workflow**

O simplemente haz cualquier commit a main.

---

## 📋 **Opción 2: Deploy Manual desde tu Computadora**

### **Prerrequisitos**

```bash
# Clona el repo (si no lo tienes)
git clone https://github.com/adrianlerer/legal-evolution-unified.git
cd legal-evolution-unified

# Instala dependencias
npm install
```

### **Script de Deploy Manual**

Crea el archivo `deploy-manual.sh`:

```bash
#!/bin/bash

echo "🚀 Building for GitHub Pages..."

# Build con base path correcto
BASE_PATH=/legal-evolution-unified npm run build

# Agregar .nojekyll
touch dist/.nojekyll

# Copiar index.html a 404.html (para SPA routing)
cp dist/index.html dist/404.html

echo "✅ Build complete!"
echo ""
echo "📦 Now deploying to gh-pages branch..."

# Ir a dist
cd dist

# Init git si no existe
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://github.com/adrianlerer/legal-evolution-unified.git
fi

# Commit y push
git add -A
git commit -m "Deploy to GitHub Pages - $(date)"
git push -f origin HEAD:gh-pages

cd ..

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your app will be live at:"
echo "   https://adrianlerer.github.io/legal-evolution-unified/"
echo ""
echo "⏱️  First deployment takes 5-10 minutes to propagate."
```

### **Ejecutar Deploy**

```bash
chmod +x deploy-manual.sh
./deploy-manual.sh
```

---

## 📋 **Opción 3: Deploy con gh-pages npm package**

### **Instalar gh-pages**

```bash
npm install --save-dev gh-pages
```

### **Agregar script a package.json**

```json
{
  "scripts": {
    "predeploy": "BASE_PATH=/legal-evolution-unified npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

### **Deploy**

```bash
npm run deploy
```

Esto automáticamente:
1. Hace build con base path correcto
2. Crea/actualiza rama gh-pages
3. Hace push

---

## 🎯 **Método Recomendado**

**Para ti**: **Opción 1** (Via Web Interface)

Por qué:
- ✅ No requiere clonar repo
- ✅ No requiere comandos
- ✅ Auto-deploy en cada push
- ✅ 2 minutos de setup

**Pasos resumidos:**
1. Settings → Pages → Source = "GitHub Actions"
2. Create file `.github/workflows/deploy-pages.yml` con el contenido de arriba
3. Commit
4. ¡Listo! Deploy automático

---

## 🌐 **Tu URL será:**

```
https://adrianlerer.github.io/legal-evolution-unified/
```

---

## ✅ **Verificar que funcionó**

1. Ve a: https://github.com/adrianlerer/legal-evolution-unified/actions
2. Deberías ver workflow ejecutándose (círculo amarillo) o completado (check verde)
3. Espera 3-5 minutos
4. Abre: https://adrianlerer.github.io/legal-evolution-unified/
5. ¡Tu PWA está en vivo!

---

## 🐛 **Si algo falla**

### **Error: "refusing to allow a GitHub App to create workflow"**

Esto significa que el token de GitHub no tiene permiso para crear workflows.

**Solución**: Usa **Opción 1** (crear el archivo manualmente via web interface).

### **404 Not Found**

- Espera 10 minutos (primera vez toma tiempo)
- Verifica que Pages esté habilitado en Settings
- Verifica que el workflow haya terminado exitosamente

### **Página en blanco**

- Verifica que `base` en vite.config.ts sea `/legal-evolution-unified`
- Rebuild: `BASE_PATH=/legal-evolution-unified npm run build`
- Redeploy

---

## 📱 **Después del Deploy**

### **Instalar como PWA**

1. Abre https://adrianlerer.github.io/legal-evolution-unified/
2. Desktop: Click icono de instalación en barra de direcciones
3. Mobile: "Agregar a Pantalla de Inicio"
4. ¡App independiente lista!

---

## 🔄 **Actualizar la App**

Con GitHub Actions (después de setup):
- Simplemente push a main
- Deploy automático en 3 minutos

Sin GitHub Actions:
- Ejecuta `./deploy-manual.sh`
- O `npm run deploy` (si instalaste gh-pages)

---

## 💡 **Tip Pro**

Después de configurar, puedes editar archivos directamente en GitHub:

1. Ve al archivo que quieres editar
2. Click en ícono de lápiz (Edit)
3. Haz cambios
4. Commit → Esto triggerea deploy automático
5. 3 minutos después: cambios en vivo

Perfecto para fixes rápidos sin clonar el repo.

---

**¿Prefieres que te guíe paso a paso en la Opción 1?** Es la más rápida (2 minutos).
