# -*- coding: utf-8 -*-
"""
PoC 03 - RAG / Capa 4 de recomendaciones
OBJETIVO UNICO: verificar que, dado un factor de SHAP, la recuperacion trae
fragmentos pertinentes del corpus. NO valida la redaccion del LLM.

Pipeline: factor SHAP -> tabla de mapeo -> embedding -> busqueda vectorial -> top-k
"""
import json, time
import numpy as np
from sentence_transformers import SentenceTransformer
from corpus import CORPUS, MAPEO, RELEVANTES

TOP_K = 4
MODELO = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

print("=" * 78)
print("PoC 03 - RECUPERACION AUMENTADA (RAG) | Capa 4")
print("=" * 78)

# ---------------------------------------------------------------- PASO 1
print("\n[PASO 1] Cargando modelo de embeddings")
t0 = time.time()
enc = SentenceTransformer(MODELO)
dim = enc.get_sentence_embedding_dimension()
print(f"  modelo      : {MODELO}")
print(f"  dimensiones : {dim}")
print(f"  carga       : {time.time()-t0:.1f} s")

# ---------------------------------------------------------------- PASO 2
print(f"\n[PASO 2] Indexacion del corpus ({len(CORPUS)} fragmentos)")
t0 = time.time()
textos = [f["texto"] for f in CORPUS]
M = enc.encode(textos, normalize_embeddings=True)   # matriz (N, 384)
t_idx = time.time() - t0
print(f"  matriz      : {M.shape}  <- (fragmentos, dimensiones)")
print(f"  tiempo      : {t_idx:.2f} s  ({t_idx/len(CORPUS)*1000:.0f} ms por fragmento)")
print(f"  vector F01  : {np.round(M[0][:6], 4).tolist()} ... (378 mas)")
print("  --> esto se hace UNA VEZ. En produccion vive en conocimiento.fragmentos")


def recuperar(frase, k=TOP_K):
    """Equivalente Python de:  ORDER BY embedding <=> %s LIMIT k"""
    q = enc.encode([frase], normalize_embeddings=True)[0]
    sim = M @ q                      # coseno (vectores normalizados)
    idx = np.argsort(-sim)[:k]
    return [(CORPUS[i], float(sim[i])) for i in idx]


# ---------------------------------------------------------------- PASO 3
print("\n[PASO 3] Simulacion de salida de SHAP (contrato de la capa 3)")
shap_out = {
    "probabilidad_riesgo": 0.78,
    "factores": [
        {"variable": "gasto_mensual_promedio", "shap_value":  0.21, "valor": 900.0},
        {"variable": "num_creditos_activos",   "shap_value":  0.15, "valor": 4},
        {"variable": "ingreso_peor_mes",       "shap_value":  0.12, "valor": 640.0},
        {"variable": "ahorro_mensual",         "shap_value": -0.09, "valor": 290.0},
    ],
}
for f in shap_out["factores"]:
    print(f"  {f['variable']:<24} shap={f['shap_value']:+.2f}  valor={f['valor']}")

# ---------------------------------------------------------------- PASO 4
print("\n[PASO 4] Recuperacion por factor")
recuperados = {}
for f in shap_out["factores"]:
    var = f["variable"]
    frase = MAPEO[var]
    hits = recuperar(frase)
    recuperados[var] = hits
    print(f"\n  {var}")
    print(f"    consulta : \"{frase}\"")
    for frag, s in hits:
        ok = "OK " if frag["id"] in RELEVANTES[var] else ("!! " if frag["tema"] == "DISTRACTOR" else "-- ")
        print(f"    {ok}{frag['id']}  sim={s:.4f}  [{frag['fuente']} p.{frag['pagina']}]")
        print(f"        {frag['texto'][:88]}...")

# ---------------------------------------------------------------- PASO 5
print("\n" + "=" * 78)
print("[PASO 5] METRICAS DE RECUPERACION (las 8 variables mapeadas)")
print("=" * 78)


def evaluar(usar_mapeo):
    prec, rec, mrr, distr = [], [], [], 0
    for var, rel in RELEVANTES.items():
        consulta = MAPEO[var] if usar_mapeo else var
        hits = recuperar(consulta)
        ids = [h[0]["id"] for h in hits]
        aciertos = [i for i in ids if i in rel]
        prec.append(len(aciertos) / TOP_K)
        rec.append(len(aciertos) / len(rel))
        rr = next((1 / (p + 1) for p, i in enumerate(ids) if i in rel), 0.0)
        mrr.append(rr)
        distr += sum(1 for h in hits if h[0]["tema"] == "DISTRACTOR")
    return float(np.mean(prec)), float(np.mean(rec)), float(np.mean(mrr)), distr


metricas = {}
print(f"\n{'':<34}{'P@4':>8}{'R@4':>8}{'MRR':>8}{'distract.':>11}")
for etiqueta, clave, flag in [("CON tabla de mapeo", "con_mapeo", True),
                              ("SIN mapeo (nombre de columna)", "sin_mapeo", False)]:
    p, r, m, d = evaluar(flag)
    metricas[clave] = {"p_at_4": round(p, 3), "r_at_4": round(r, 3), "mrr": round(m, 3),
                       "distractores_recuperados": d, "total_recuperados": TOP_K * len(RELEVANTES)}
    print(f"{etiqueta:<34}{p:>8.3f}{r:>8.3f}{m:>8.3f}{d:>8} / {TOP_K*len(RELEVANTES)}")

print("\n  P@4 = de los 4 traidos, cuantos son pertinentes")
print("  R@4 = de los pertinentes que existen, cuantos se trajeron")
print("  MRR = que tan arriba aparece el primer acierto (1.0 = primer puesto)")

# ---------------------------------------------------------------- PASO 5b
print("\n" + "=" * 78)
print("[PASO 5b] TECHO TEORICO, DISTRACTORES Y UMBRAL DE CORTE (con mapeo)")
print("=" * 78)
techo = float(np.mean([min(len(r), TOP_K) / TOP_K for r in RELEVANTES.values()]))
print(f"  Techo teorico de P@4 con este corpus: {techo:.3f}")
sim_dist, sim_ok, primeros_errados = [], [], []
for var, rel in RELEVANTES.items():
    hits = recuperar(MAPEO[var])
    if hits[0][0]["id"] not in rel:
        primeros_errados.append({"variable": var, "primero": hits[0][0]["id"], "esperado": sorted(rel)})
    for frag, s in hits:
        if frag["tema"] == "DISTRACTOR":
            sim_dist.append(s)
            print(f"  distractor: {var:<24} -> {frag['id']} {frag['fuente']}  sim={s:.3f}")
        elif frag["id"] in rel:
            sim_ok.append(s)
print(f"  Similitud de distractores recuperados : {min(sim_dist):.3f} a {max(sim_dist):.3f}")
print(f"  Similitud de fragmentos pertinentes   : {min(sim_ok):.3f} a {max(sim_ok):.3f}")
for e in primeros_errados:
    print(f"  Primer resultado equivocado: {e['variable']:<24} 1ro={e['primero']} esperado={e['esperado']}")

# ---------------------------------------------------------------- PASO 6
print("\n" + "=" * 78)
print("[PASO 6] PROMPT ENSAMBLADO (lo unico que vera el LLM)")
print("=" * 78)

bloques, fuentes = [], []
for var, hits in recuperados.items():
    for frag, s in hits[:2]:
        ref = f"[{frag['fuente']}, p.{frag['pagina']}]"
        bloques.append(f"{ref} {frag['texto']}")
        if ref not in fuentes:
            fuentes.append(ref)

caso = "\n".join(
    f"- {f['variable']} = {f['valor']} (SHAP {f['shap_value']:+.2f})"
    for f in shap_out["factores"]
)

PROMPT = f"""Eres un asesor financiero para mujeres emprendedoras del sector MYPE en Peru.

REGLAS ESTRICTAS:
- Usa UNICAMENTE la informacion del CONTEXTO.
- Si el CONTEXTO no cubre un factor, escribe exactamente:
  "No hay informacion suficiente en la base de conocimiento."
- Prohibido usar conocimiento propio o cifras que no esten en el CONTEXTO.
- Cita la fuente entre corchetes en cada recomendacion.
- Responde solo con JSON valido.

CONTEXTO:
{chr(10).join(bloques)}

CASO (riesgo estimado: {shap_out['probabilidad_riesgo']:.0%}):
{caso}

FORMATO: {{"recomendaciones":[{{"factor":"","accion":"","fuente":""}}]}}"""

print(PROMPT[:1500])
print("  ...")
print(f"\n  tamano del prompt : {len(PROMPT)} caracteres (~{len(PROMPT)//4} tokens)")
print(f"  fuentes citables  : {len(fuentes)}")
print("  --> el LLM NO consulta la base. Solo recibe este string.")

# ---------------------------------------------------------------- PASO 7
salida = {
    "poc": "03_rag_retrieval",
    "objetivo": "verificar pertinencia de la recuperacion por factor SHAP",
    "modelo_embeddings": MODELO,
    "dimensiones": dim,
    "fragmentos_indexados": len(CORPUS),
    "top_k": TOP_K,
    "metricas": metricas,
    "techo_teorico_p_at_4": round(techo, 3),
    "similitud_distractores": [round(min(sim_dist), 3), round(max(sim_dist), 3)],
    "similitud_pertinentes": [round(min(sim_ok), 3), round(max(sim_ok), 3)],
    "primeros_resultados_equivocados": primeros_errados,
    "probabilidad_riesgo": shap_out["probabilidad_riesgo"],
    "recuperacion": {
        var: [{"id": f["id"], "similitud": round(s, 4),
               "fuente": f["fuente"], "pagina": f["pagina"]} for f, s in hits]
        for var, hits in recuperados.items()
    },
    "prompt_caracteres": len(PROMPT),
    "fuentes_citables": fuentes,
}
with open("resultado_poc_rag.json", "w", encoding="utf-8") as fh:
    json.dump(salida, fh, ensure_ascii=False, indent=2)
print("\n[PASO 7] Archivo generado: resultado_poc_rag.json")
print("=" * 78)
