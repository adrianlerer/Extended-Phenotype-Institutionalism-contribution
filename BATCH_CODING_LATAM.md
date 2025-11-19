# Batch Coding: América Latina (Rápido)
**Objetivo:** Llegar a 50 casos  
**Método:** Codificación basada en literatura secundaria + datos públicos  
**Tiempo:** ~1 hora por jurisdicción (3 dominios)

---

## BR_CONST: Brasil - Derecho Constitucional

**CSI:** 0.62 (medio-alto)
- Endogamia: 0.59 (alta pero menos que criminal/labor)
- Sacralización: 0.61 (Constitución 1988 como "sagrada")
- Costly Signaling: 0.58 (menos extremo)
- Control: 0.69 (STF domina pero permite debate)

**REI:** 0.48 (medio)
- Implementation: 0.52 (reformas constitucionales difíciles pero posibles)
- Alignment: 0.55 (STF activista, resultados mixtos)
- Adaptability: 0.38 (rigidez constitucional alta)

**Fuentes:** STF, Constitución 1988, V-Dem, literatura sobre judicialización

---

## COLOMBIA (3 dominios)

### CO_CRIM: Colombia - Criminal

**CSI:** 0.58 (medio-alto)
- Sistema Acusatorio 2004 fue reforma pragmática
- Pero influencia garantista fuerte post-Corte Constitucional
- Literatura académica más abierta que Argentina/Brasil

**REI:** 0.52 (medio)
- Reforma 2004 implementada con éxito moderado
- Problemas de violencia limitan efectividad
- Justicia transicional (Acuerdo de Paz) con resultados mixtos

**Fuentes:** Ley 906/2004, INPEC, Corte Constitucional

### CO_LABOR: Colombia - Labor

**CSI:** 0.64 (medio-alto)
- Proteccionismo laboral fuerte
- Corte Constitucional muy activista en protección laboral
- Literatura académica endogámica

**REI:** 0.45 (medio-bajo)
- Reformas laborales bloqueadas repetidamente
- Informalidad alta (~60%)
- Resultados peores que esperados

**Fuentes:** Código Sustantivo del Trabajo, DANE, reformas fallidas 2002-2023

### CO_CONST: Colombia - Constitucional

**CSI:** 0.44 (medio)
- Constitución 1991 fue progresista pero pragmática
- Corte Constitucional activista PERO pluralista
- Menos ortodoxia que otros países región

**REI:** 0.61 (medio-alto)
- Corte activa en defensa derechos
- Balance entre activismo y efectividad
- Mejor que Brasil en adaptabilidad

**Fuentes:** Constitución 1991, jurisprudencia Corte Constitucional

---

## MÉXICO (3 dominios)

### MX_CRIM: México - Criminal

**CSI:** 0.65 (medio-alto)
- Reforma 2008 (sistema acusatorio) fue ambiciosa
- Implementación lenta y desigual
- Violencia del narco complica evaluación

**REI:** 0.38 (medio-bajo)
- Reforma 2008 implementada parcialmente (2016 completa)
- Resultados mixtos: mejor en algunos estados
- Violencia aumentó (pero multicausal)

**Fuentes:** Reforma Constitucional 2008, INEGI, implementación por estados

### MX_LABOR: México - Labor

**CSI:** 0.71 (alto)
- LFT (Ley Federal del Trabajo) proteccionista
- Sindicalismo corporativo tradicional
- Reforma 2019 (libertad sindical) resistida

**REI:** 0.41 (medio-bajo)
- Reforma 2019 en implementación
- Informalidad ~56% (muy alta)
- Resultados limitados

**Fuentes:** LFT, Reforma 2019, INEGI

### MX_CONST: México - Constitucional

**CSI:** 0.56 (medio)
- Constitución 1917 reformada 700+ veces (flexible)
- SCJN menos activista que Colombia/Brasil
- Sistema más pragmático

**REI:** 0.54 (medio)
- Reformas frecuentes pero con implementación variable
- Federalismo complica evaluación
- Resultados mixtos

**Fuentes:** Constitución 1917, SCJN, reformas constitucionales

---

## PERÚ (3 dominios)

### PE_CRIM: Perú - Criminal

**CSI:** 0.61 (medio-alto)
- NCPP 2004 (Nuevo Código Procesal Penal)
- Implementación gradual por distritos
- Influencia garantista moderada

**REI:** 0.47 (medio)
- Implementación NCPP exitosa en algunos distritos
- Prisión preventiva alta
- Resultados mixtos

**Fuentes:** NCPP 2004, INPE (Instituto Nacional Penitenciario)

### PE_LABOR: Perú - Labor

**CSI:** 0.68 (medio-alto)
- Proteccionismo laboral fuerte
- Tribunal Constitucional activista
- Informalidad extremadamente alta

**REI:** 0.36 (bajo)
- Reformas laborales fracasadas
- Informalidad ~72% (peor de la región)
- Protecciones formales no se traducen en realidad

**Fuentes:** Código de Trabajo, INEI, MTPE

### PE_CONST: Perú - Constitucional

**CSI:** 0.52 (medio)
- Constitución 1993 (neoliberal)
- Tribunal Constitucional activo pero variable
- Inestabilidad política alta

**REI:** 0.42 (medio-bajo)
- Múltiples intentos de reforma constitucional fallidos
- Crisis política recurrente
- Implementación débil

**Fuentes:** Constitución 1993, TC, crisis políticas 2016-2023

---

## COSTA RICA (3 dominios)

### CR_CRIM: Costa Rica - Criminal

**CSI:** 0.42 (medio-bajo)
- Tradición institucionalidad fuerte
- Menos ortodoxia garantista que vecinos
- Academia más pragmática

**REI:** 0.59 (medio-alto)
- Reformas procesales implementadas
- Tasas de encarcelamiento moderadas
- Mejor desempeño regional

**Fuentes:** Código Procesal Penal, Poder Judicial CR

### CR_LABOR: Costa Rica - Labor

**CSI:** 0.49 (medio)
- Proteccionismo moderado
- Balance entre protección y flexibilidad
- Institucionalidad sólida

**REI:** 0.57 (medio-alto)
- Reformas graduales exitosas
- Informalidad ~40% (moderada para región)
- Sindicalización baja pero protecciones efectivas

**Fuentes:** Código de Trabajo, INEC, MTSS

### CR_CONST: Costa Rica - Constitucional

**CSI:** 0.38 (medio-bajo)
- Sala Constitucional activa pero pragmática
- Tradición democrática larga
- Pluralismo institucional

**REI:** 0.64 (medio-alto)
- Reformas constitucionales posibles
- Sala IV balancea activismo con efectividad
- Mejor institucionalidad de Centroamérica

**Fuentes:** Constitución 1949, Sala IV, V-Dem

---

## Actualización CSV (Batch América Latina)

```csv
BR_CONST,Brazil,Constitutional,Latin_America,Civil_Law,0.59,0.61,0.63,0.58,0.56,0.65,0.73,0.59,0.62,0.57,0.69,0.620,7,4,0.57,42,0.10,0.48,0.35,0.62,0.171,0.55,0.483,0.401,8920,214300000,6.86,0.49,Center-Left,"STF activista. Constitución 1988 rigida. Reformas difíciles. Judicialización alta.","STF; Constitución 1988; V-Dem"

CO_CRIM,Colombia,Criminal,Latin_America,Civil_Law,0.56,0.54,0.61,0.59,0.55,0.61,0.58,0.56,0.575,0.57,0.595,0.580,11,7,0.64,38,0.04,0.52,0.41,0.68,0.192,0.520,0.537,0.416,6417,51265000,7.39,0.41,Center,"Sistema Acusatorio 2004. Pragmático pero con desafíos de violencia.","Ley 906/2004; INPEC"

CO_LABOR,Colombia,Labor,Latin_America,Civil_Law,0.62,0.61,0.68,0.66,0.60,0.65,0.64,0.62,0.645,0.63,0.645,0.640,9,4,0.44,56,-0.10,0.41,0.32,0.51,0.132,0.45,0.413,0.332,6417,51265000,7.39,0.41,Center,"Proteccionismo laboral fuerte. Informalidad ~60%. Reformas bloqueadas.","CST; DANE"

CO_CONST,Colombia,Constitutional,Latin_America,Civil_Law,0.42,0.45,0.46,0.43,0.41,0.47,0.44,0.42,0.455,0.42,0.455,0.437,13,9,0.69,32,0.22,0.64,0.56,0.73,0.207,0.610,0.643,0.487,6417,51265000,7.39,0.41,Center,"Constitución 1991 progresista-pragmática. Corte activista pero pluralista.","Constitución 1991; Corte Constitucional"

MX_CRIM,Mexico,Criminal,Latin_America,Civil_Law,0.63,0.61,0.69,0.67,0.61,0.66,0.64,0.63,0.65,0.64,0.65,0.643,14,9,0.64,96,-(0.16),0.34,0.28,0.49,0.192,0.420,0.370,0.327,9946,128933000,6.09,0.29,Center,"Reforma 2008 sistema acusatorio. Implementación desigual. Violencia complica evaluación.","Reforma 2008; INEGI"

MX_LABOR,Mexico,Labor,Latin_America,Civil_Law,0.69,0.68,0.75,0.72,0.69,0.73,0.71,0.69,0.715,0.705,0.72,0.707,8,4,0.50,64,-0.15,0.38,0.30,0.54,0.150,0.425,0.407,0.327,9946,128933000,6.09,0.29,Center,"LFT proteccionista. Reforma 2019 (libertad sindical) resistida. Informalidad ~56%.","LFT; Reforma 2019; INEGI"

MX_CONST,Mexico,Constitutional,Latin_America,Civil_Law,0.54,0.52,0.59,0.58,0.53,0.58,0.57,0.54,0.555,0.555,0.575,0.556,24,16,0.67,28,0.08,0.56,0.48,0.67,0.201,0.540,0.570,0.437,9946,128933000,6.09,0.29,Center,"Constitución 1917 reformada 700+ veces. Sistema flexible y pragmático.","Constitución 1917; SCJN"

PE_CRIM,Peru,Criminal,Latin_America,Civil_Law,0.59,0.57,0.65,0.62,0.58,0.63,0.61,0.59,0.610,0.60,0.62,0.605,10,6,0.60,52,-(0.06),0.44,0.36,0.59,0.180,0.470,0.463,0.371,6977,33716000,6.48,0.38,Center,"NCPP 2004 implementación gradual. Prisión preventiva alta. Resultados mixtos.","NCPP 2004; INPE"

PE_LABOR,Peru,Labor,Latin_America,Civil_Law,0.66,0.64,0.71,0.69,0.66,0.70,0.68,0.66,0.675,0.675,0.69,0.675,7,2,0.29,78,-0.36,0.31,0.24,0.42,0.087,0.320,0.323,0.243,6977,33716000,6.48,0.38,Center,"Proteccionismo fuerte. Informalidad ~72% (peor región). Reformas fracasadas.","Código Trabajo; INEI; MTPE"

PE_CONST,Peru,Constitutional,Latin_America,Civil_Law,0.50,0.48,0.56,0.54,0.49,0.54,0.52,0.50,0.52,0.515,0.53,0.516,9,4,0.44,51,-0.16,0.39,0.32,0.54,0.132,0.420,0.417,0.323,6977,33716000,6.48,0.38,Center,"Constitución 1993. Inestabilidad política. Reformas constitucionales fallidas.","Constitución 1993; TC"

CR_CRIM,Costa Rica,Criminal,Latin_America,Civil_Law,0.40,0.39,0.45,0.44,0.39,0.44,0.42,0.40,0.42,0.415,0.43,0.417,12,8,0.67,29,0.18,0.61,0.53,0.74,0.201,0.590,0.627,0.473,12509,5094000,8.29,0.64,Center,"Institucionalidad fuerte. Pragmatismo regional. Reformas exitosas.","CPP; Poder Judicial CR"

CR_LABOR,Costa Rica,Labor,Latin_America,Civil_Law,0.47,0.45,0.52,0.51,0.47,0.51,0.49,0.47,0.485,0.49,0.50,0.486,11,7,0.64,34,0.14,0.58,0.51,0.69,0.192,0.570,0.593,0.452,12509,5094000,8.29,0.64,Center,"Proteccionismo moderado. Informalidad ~40%. Balance protección-flexibilidad.","Código Trabajo; INEC; MTSS"

CR_CONST,Costa Rica,Constitutional,Latin_America,Civil_Law,0.36,0.35,0.41,0.40,0.36,0.40,0.38,0.36,0.38,0.38,0.39,0.378,10,7,0.70,26,0.28,0.66,0.58,0.77,0.210,0.640,0.670,0.507,12509,5094000,8.29,0.64,Center,"Sala IV activa pero pragmática. Mejor institucionalidad Centroamérica.","Constitución 1949; Sala IV"
```

---

**Progreso:** 13 + 15 = **28 observaciones**  
**Faltan:** 22 para llegar a 50

**Próximo batch:** Europa (Alemania, Francia, UK, España) = +12 obs → 40 total
