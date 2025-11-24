# Guía de Estilo para Papers CriptoIus
## Preferencias del autor para redacción académica

**Autor**: Adrián Lerer  
**Fecha creación**: 2025-11-22  
**Aplicable a**: Todos los papers del proyecto CriptoIus y Legal Evolution

---

## 1. PRIMERA PERSONA SINGULAR (mandatory)

### ✅ CORRECTO (usar siempre)
- "Propongo que..."
- "En mi análisis de..."
- "Argumento que..."
- "Identifico cinco contribuciones..."
- "Sostengo que..."
- "Concluyo que..."

### ❌ INCORRECTO (evitar)
- "Proponemos que..." ❌ (plural académico)
- "Nuestro análisis..." ❌
- "Argumentamos..." ❌
- "We identify..." ❌ (en inglés)
- "One might argue..." ❌ (impersonal)

### Justificación
- Soy **autor único** de los papers
- La primera persona singular muestra **ownership** y **responsabilidad**
- Evita la falsa modestia del plural académico
- Es más directo y honesto intelectualmente

---

## 2. EVITAR EN DASHES (mandatory)

### ✅ CORRECTO
**Usar paréntesis o coma**:
- "Los precedentes (como Hadley v. Baxendale) establecen..."
- "El sistema, basado en blockchain, permite..."
- "Tres tipos de memes: parásitos, comensales y mutualistas"

**Usar dos puntos**:
- "Dennett identifica tres categorías: parásitos, comensales y mutualistas"

**Usar punto y seguido** (dividir en dos oraciones):
- "Los precedentes parásitos reducen eficiencia. Se replican por coerción, no por calidad."

### ❌ INCORRECTO
- "Los precedentes — como Hadley v. Baxendale — establecen..." ❌
- "El sistema —basado en blockchain— permite..." ❌
- "Tres tipos de memes —parásitos, comensales y mutualistas— coexisten." ❌

### Alternativas permitidas
- **Guion simple** (para rangos): "páginas 100-150"
- **Paréntesis**: "(como veremos más adelante)"
- **Comas**: ", según Dennett, "
- **Dos puntos**: ": tres categorías"

### Justificación
- Los en dashes (—) son difíciles de leer en español
- Interrumpen el flujo de la oración
- Paréntesis y comas son más claros

---

## 3. ESTRUCTURA DE ORACIONES

### Preferencias

**Oraciones cortas y directas**:
✅ "El determinismo no amenaza la libertad. Permite planificación y certeza."

**Evitar subordinadas excesivas**:
❌ "El determinismo, que a menudo se malinterpreta como una amenaza para la libertad, en realidad, si se examina cuidadosamente desde una perspectiva compatibilista, permite..."

**Mejor dividir**:
✅ "El determinismo se malinterpreta frecuentemente. Se ve como amenaza para la libertad. Sin embargo, desde una perspectiva compatibilista, el determinismo permite planificación y certeza."

---

## 4. CITAS Y REFERENCIAS

### Formato preferido

**Citas textuales cortas** (integradas en texto):
```
Dennett (2003, p. 113) afirma que "el ajedrez es un juego de 'información perfecta'".
```

**Citas textuales largas** (bloque indentado):
```
> "El ajedrez es un juego de 'información perfecta'; en este sentido es distinto 
> de los juegos de cartas, en los que se ocultan las cartas al oponente" 
> (Dennett, 2003, p. 113).
```

**Parafraseo** (sin comillas):
```
Dennett (2003) distingue entre juegos de información perfecta como el ajedrez 
y juegos de información imperfecta como el póker.
```

---

## 5. VOZ ACTIVA VS PASIVA

### ✅ PREFERIR VOZ ACTIVA
- "Propongo un sistema de precedentes vinculantes"
- "Dennett identifica tres tipos de memes"
- "El código ejecuta el contrato automáticamente"

### ⚠️ USAR VOZ PASIVA SOLO CUANDO NECESARIO
- "El precedente fue adoptado por 127 contratos" (cuando el agente es irrelevante)
- "Este problema ha sido estudiado extensamente" (cuando no hay agente específico)

---

## 6. TERMINOLOGÍA TÉCNICA

### Consistencia en términos clave

| Concepto | Término preferido | Evitar |
|----------|------------------|--------|
| Sistema propuesto | CriptoIus | "el sistema", "mi propuesta" |
| Precedentes vinculantes | voluntary stare decisis | "precedent binding", "binding precedents" |
| Métrica de adopción | JurisRank | "adoption score", "precedent score" |
| Validación constitucional | RootFinder | "constitutional validator" |
| Teoría base | Extended Phenotype Theory (EPT) | "phenotype theory" |
| Contratos inteligentes | smart contracts | "contratos autoejecutables" (solo como sinónimo ocasional) |

### En español vs inglés

**Regla general**: Escribir en español, usar términos técnicos en inglés solo cuando:
1. Son nombres propios (RootFinder, JurisRank)
2. No tienen traducción establecida (smart contracts, blockchain)
3. La traducción es ambigua (meme vs "unidad cultural")

**Italics para términos en latín**:
- *stare decisis*
- *stipulatio*
- *bona fides*

---

## 7. NUMERACIÓN Y LISTAS

### Preferencias

**Listas enumeradas** (para pasos secuenciales):
```
Propongo tres fases:
1. Diseño de cláusulas interpretativas
2. Adopción de precedentes
3. Evaluación mediante JurisRank
```

**Listas con bullets** (para elementos no secuenciales):
```
Dennett identifica tres tipos de memes:
- Parásitos (reducen eficiencia)
- Comensales (neutrales)
- Mutualistas (mejoran outcomes)
```

**No mezclar formatos** en la misma lista

---

## 8. TÍTULOS Y SECCIONES

### Estructura preferida

**Nivel 1** (capítulos principales):
```markdown
# I. INTRODUCCIÓN
```

**Nivel 2** (secciones):
```markdown
## A. From Stipulatio to Solidity
```

**Nivel 3** (subsecciones):
```markdown
### 1. El formalismo romano
```

**Nivel 4** (puntos específicos):
```markdown
#### a) Stipulatio como razón virtual
```

### Capitalización

**En español**: Solo primera palabra
- ✅ "Precedentes como memes mutualistas"
- ❌ "Precedentes Como Memes Mutualistas"

**En inglés**: Todas las palabras principales
- ✅ "Precedents as Mutualist Memes"
- ❌ "Precedents as mutualist memes"

---

## 9. FIGURAS Y TABLAS

### Formato de captions

**Figuras**:
```
Figura 1. Arquitectura de tres capas de CriptoIus
```

**Tablas**:
```
Tabla 1. Comparación de sistemas de resolución de disputas
```

### Referencia en texto

Primera mención:
- "Como muestra la Figura 1..."
- "La Tabla 2 resume..."

Menciones posteriores:
- "Como vimos en Figura 1..."
- "(ver Tabla 2)"

---

## 10. NOTAS AL PIE

### Uso apropiado

**✅ Para notas al pie**:
- Aclaraciones técnicas breves
- Referencias adicionales
- Comentarios tangenciales

**❌ No usar para**:
- Argumentos centrales (van en cuerpo principal)
- Citas bibliográficas (van como referencias in-text)
- Información esencial

### Formato
```
Texto principal.^1

---
^1 Esta es la nota al pie explicativa.
```

---

## 11. CÓDIGO Y EJEMPLOS TÉCNICOS

### Formato Solidity

```solidity
// Comentario explicativo en español
contract EjemploContrato {
    // Variable de estado
    uint256 public valor;
    
    // Función pública
    function actualizarValor(uint256 _nuevoValor) public {
        valor = _nuevoValor;
    }
}
```

### Pseudo-código conceptual

Usar comentarios para explicar lógica:
```javascript
// Algoritmo JurisRank simplificado
function calcularJurisRank(precedente) {
    adopciones = contarAdopciones(precedente);
    antiguedad = calcularAntiguedad(precedente);
    challenges = contarChallenges(precedente);
    
    score = (adopciones * 0.6) + 
            (antiguedad * 0.2) - 
            (challenges * 0.2);
    
    return score;
}
```

---

## 12. TRADUCCIÓN DE TÉRMINOS TÉCNICOS

### Glosario español-inglés

| Español | Inglés | Notas |
|---------|--------|-------|
| Precedente vinculante | Binding precedent | Usar "voluntary" cuando aplique |
| Cláusula interpretativa | Interpretative clause | |
| Contrato inteligente | Smart contract | Preferir término inglés |
| Autoejectable | Self-executing | |
| Cadena de bloques | Blockchain | Preferir término inglés |
| Árbitro | Arbitrator | |
| Laudo | Award | En contexto de arbitraje |
| Jurisrank | JurisRank | Nombre propio, mantener capitalización |

---

## 13. CHECKLIST PRE-PUBLICACIÓN

Antes de considerar un paper completo, verificar:

- [ ] Todo escrito en **primera persona singular** (yo, mi, propongo)
- [ ] **Cero en dashes** (—) en todo el documento
- [ ] Terminología técnica **consistente** (verificar tabla Sección 6)
- [ ] Citas correctamente formateadas (autor, año, página)
- [ ] Figuras y tablas numeradas secuencialmente
- [ ] Referencias bibliográficas completas
- [ ] Código con comentarios explicativos
- [ ] Abstracts en español E inglés (si SSRN)
- [ ] Formato según guidelines de journal target

---

## 14. PAPERS ESPECÍFICOS: CRIPTOIUS

### Estructura objetivo (15 páginas)

```
I. INTRODUCCIÓN (1,200 palabras)
II. MARCO TEÓRICO (4,000 palabras)
   A. From Stipulatio to Solidity (800)
   B. Contracts as Extended Phenotypes (1,000) [PENDIENTE]
   C. Precedents as Directed Mutations (2,500)
   D. Path Dependence Problem (1,000)
   E. RootFinder Integration (800)
   F. Contractual Compatibilism (2,600)
III. ARQUITECTURA (2,000 palabras) [PENDIENTE]
IV. DISEÑO EXPERIMENTAL (1,500 palabras) [PENDIENTE]
V. DISCUSIÓN (1,000 palabras) [PENDIENTE]
VI. CONCLUSIONES (300 palabras) [PENDIENTE]
```

### Target journals
1. **SSRN** (primary): Working paper, distribución amplia
2. **arXiv cs.CY** (secondary): Visibility en CS/legal tech
3. **Blog/Substack** (tertiary): Divulgación pública

---

## 15. CONTACTO Y ACTUALIZACIONES

**Autor**: Adrián Lerer  
**Email**: [Por completar]  
**GitHub**: adrianlerer/legal-evolution-unified  
**Última actualización**: 2025-11-22  

**Nota**: Este style guide es documento vivo. Actualizar conforme evolucionan preferencias y se descubren nuevas convenciones útiles.

---

## RESUMEN RÁPIDO (Quick Reference)

✅ **Hacer**:
- Primera persona singular
- Paréntesis en lugar de en dashes
- Oraciones cortas y directas
- Voz activa
- Terminología consistente

❌ **Evitar**:
- Plural académico ("nosotros")
- En dashes (—)
- Oraciones con múltiples subordinadas
- Voz pasiva innecesaria
- Términos técnicos inconsistentes

📝 **Recordar**:
- Soy autor único
- Escribir para ser entendido
- Claridad > elegancia
- Directness > falsa modestia
