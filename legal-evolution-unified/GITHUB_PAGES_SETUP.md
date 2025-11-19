# 🚀 GitHub Pages Deployment Guide

## ✅ **Setup Completo - Listo para Deploy**

Tu repositorio ya está configurado para deployment automático en GitHub Pages.

---

## 📋 **Paso a Paso para Activar**

### **1. Habilitar GitHub Pages en tu Repositorio**

1. Ve a tu repositorio: https://github.com/adrianlerer/legal-evolution-unified
2. Click **Settings** (⚙️)
3. En el menú izquierdo, click **Pages**
4. En **Source**, selecciona:
   - **Source**: `GitHub Actions`
5. Click **Save**

¡Eso es todo! El workflow ya está configurado.

---

### **2. Trigger el Deploy**

El deploy se ejecuta automáticamente cuando:
- ✅ Haces `git push` a la rama `main`
- ✅ Mergeas un Pull Request a `main`
- ✅ Manualmente desde Actions tab

**Para forzar deploy ahora:**

```bash
# Hacer un pequeño cambio y push
cd /home/user/webapp
git pull origin main
echo "# Deployed to GitHub Pages" >> GITHUB_PAGES_SETUP.md
git add .
git commit -m "docs: Enable GitHub Pages deployment"
git push origin main
```

---

### **3. Verificar el Deploy**

1. Ve a: https://github.com/adrianlerer/legal-evolution-unified/actions
2. Verás workflow **"Deploy to GitHub Pages"** ejecutándose
3. Toma ~2-3 minutos
4. Cuando esté ✅ verde, tu app estará en:

```
https://adrianlerer.github.io/legal-evolution-unified/
```

---

## 🌐 **Tu URL Pública Será**

```
https://adrianlerer.github.io/legal-evolution-unified/
```

Esta URL:
- ✅ Es **permanente** (no expira como sandbox)
- ✅ Tiene **SSL gratis** (HTTPS automático)
- ✅ **CDN global** de GitHub (rápido en todo el mundo)
- ✅ Se **actualiza automáticamente** con cada push a main
- ✅ Soporta **PWA completa** (instalable, offline)

---

## 🔧 **Cómo Funciona**

### **Workflow Automático**

El archivo `.github/workflows/deploy-pages.yml` hace esto:

1. **Trigger**: Cada push a `main`
2. **Build**: 
   - Instala Node.js 18
   - Ejecuta `npm ci` (instala dependencias)
   - Ejecuta `npm run build` (genera bundle optimizado)
   - Output en `dist/` folder
3. **Deploy**:
   - Sube `dist/` a GitHub Pages
   - Publica en `https://adrianlerer.github.io/legal-evolution-unified/`

### **Base Path Configurado**

El `vite.config.ts` usa:
```typescript
base: process.env.BASE_PATH || '/'
```

Esto permite que la app funcione en:
- **Local**: `http://localhost:3000` (base = `/`)
- **GitHub Pages**: `https://username.github.io/legal-evolution-unified/` (base = `/legal-evolution-unified`)

---

## 📱 **Después del Deploy**

### **Instalar como PWA desde GitHub Pages**

**Desktop:**
1. Abre `https://adrianlerer.github.io/legal-evolution-unified/`
2. Click icono de instalación en barra de direcciones
3. "Instalar Legal Evolution Unified"
4. App independiente en tu sistema

**Móvil:**
1. Abre la URL en Safari/Chrome
2. "Agregar a Pantalla de Inicio"
3. Ícono en home screen
4. Funciona offline

---

## 🔄 **Actualizar la App**

Simplemente haz push a main:

```bash
# Hacer cambios en el código
git add .
git commit -m "feat: Add new feature"
git push origin main

# GitHub Actions automáticamente:
# 1. Detecta el push
# 2. Ejecuta build
# 3. Deploya nueva versión
# 4. ~3 minutos después, cambios en vivo
```

---

## 🐛 **Troubleshooting**

### **El workflow falla**

1. Ve a Actions tab: https://github.com/adrianlerer/legal-evolution-unified/actions
2. Click en el workflow fallido
3. Revisa logs para ver error
4. Errores comunes:
   - **Permisos**: Verifica que Pages esté habilitado en Settings
   - **Build error**: Ejecuta `npm run build` localmente para debuggear
   - **Node version**: Workflow usa Node 18

### **La app no carga en GitHub Pages**

1. **Verifica base path**: Debe ser `/legal-evolution-unified`
2. **Revisa Console**: Abre DevTools (F12) → Console para ver errores
3. **Caché**: Prueba en ventana incógnita
4. **Espera**: Primera vez toma 5-10 min en propagar DNS

### **404 en rutas**

Si al refrescar `/rootfinder` da 404, crea `dist/404.html`:

```bash
# Agregar a workflow (ya incluido en el workflow actual)
cp dist/index.html dist/404.html
```

Esto hace que todas las rutas carguen el SPA.

---

## 🎨 **Customizar Dominio (Opcional)**

Si quieres usar tu propio dominio:

1. **Settings** → **Pages**
2. **Custom domain**: `legal-evolution.tudominio.com`
3. Agrega CNAME en tu DNS:
   ```
   CNAME: legal-evolution → adrianlerer.github.io
   ```
4. GitHub provee SSL gratis

---

## 📊 **Ventajas de GitHub Pages**

| Feature | GitHub Pages | Vercel | Netlify |
|---------|--------------|--------|---------|
| **Precio** | ✅ Gratis | ✅ Gratis | ✅ Gratis |
| **SSL** | ✅ Auto | ✅ Auto | ✅ Auto |
| **CDN** | ✅ Sí | ✅ Sí | ✅ Sí |
| **Deploy automático** | ✅ Sí | ✅ Sí | ✅ Sí |
| **Build time** | ~3 min | ~2 min | ~2 min |
| **Custom domain** | ✅ Gratis | ✅ Gratis | ✅ Gratis |
| **Integrado con repo** | ✅✅ Nativo | Externo | Externo |

**GitHub Pages es ideal para tu caso** porque ya está todo en GitHub.

---

## 🚀 **Quick Deploy Checklist**

- [ ] Ir a Settings → Pages
- [ ] Source = "GitHub Actions"
- [ ] Push a main (o forzar workflow)
- [ ] Esperar 3 minutos
- [ ] Abrir `https://adrianlerer.github.io/legal-evolution-unified/`
- [ ] Instalar como PWA
- [ ] ¡Disfrutar!

---

## 📝 **Notas Importantes**

### **Backend API**

⚠️ **GitHub Pages solo sirve archivos estáticos (frontend)**. 

Para el backend tienes 2 opciones:

**Opción A: Backend en Railway/Render (Recomendado)**

```bash
# 1. Deploy backend en Railway.app (gratis)
# 2. Obtén URL: https://legal-evolution-api.up.railway.app

# 3. Actualiza frontend/src/services/api.ts:
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://legal-evolution-api.up.railway.app/api/v1'
  : '/api/v1';
```

**Opción B: Solo Frontend (Demo Mode)**

Si solo quieres mostrar la UI sin backend real:

```typescript
// frontend/src/services/api.ts
// Agrega datos de ejemplo (mock data)
if (import.meta.env.PROD) {
  // Usar datos de ejemplo
  return mockData;
}
```

### **Límites de GitHub Pages**

- ✅ 1 GB de espacio
- ✅ 100 GB bandwidth/mes
- ✅ 10 builds/hora
- ⚠️ Solo contenido estático (no Node.js backend)

Para tu PWA (solo frontend) está perfecto.

---

## 🎯 **Next Steps**

1. **Ahora**: Habilitar Pages en Settings
2. **Push**: Hacer commit de este setup
3. **Esperar**: 3 minutos para deploy
4. **Usar**: `https://adrianlerer.github.io/legal-evolution-unified/`
5. **Compartir**: URL permanente para usar en cualquier lado

---

## 🔗 **Links Útiles**

- **Repo**: https://github.com/adrianlerer/legal-evolution-unified
- **Settings**: https://github.com/adrianlerer/legal-evolution-unified/settings/pages
- **Actions**: https://github.com/adrianlerer/legal-evolution-unified/actions
- **Tu App**: https://adrianlerer.github.io/legal-evolution-unified/ (después de deploy)

---

**¡Todo listo para deploy!** 🚀

Solo faltan 2 clicks en GitHub y tendrás tu PWA en vivo permanentemente.
