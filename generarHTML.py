import os

base = os.getcwd()

# Detecta carpetas automáticamente
carpeta_letras = os.path.join(base, "letras")
carpeta_audios = os.path.join(base, "audios")
salida_html = os.path.join(base, "index.html")

if not os.path.exists(carpeta_letras):
    print("No se encontró la carpeta 'letras'. Crea la carpeta con tus archivos .txt")
    exit()
if not os.path.exists(carpeta_audios):
    print("No se encontró la carpeta 'audios'. Crea la carpeta con tus archivos .mp3")
    exit()

# Listar y ordenar archivos por número inicial
temas_txt = sorted([f for f in os.listdir(carpeta_letras) if f.endswith(".txt")])
temas_mp3 = sorted([f for f in os.listdir(carpeta_audios) if f.endswith(".mp3")])

# Crear diccionario de audios por número
audios_dict = {}
for mp3 in temas_mp3:
    num = mp3.split("-")[0]
    audios_dict[num] = mp3

# HTML base
html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Volumen 1 – Reparto Extra</title>
<style>
body { font-family:'Segoe UI', Arial, sans-serif; margin:0; background:#f4f4f4; color:#222; scroll-behavior:smooth; }
header { position:relative; height:400px; overflow:hidden; color:#fff; text-align:center; }
header::before { content:''; background:url('portada.jpg') center/cover no-repeat fixed; position:absolute; top:0; left:0; width:100%; height:100%; transform:translateZ(0); z-index:-2; }
header::after { content:''; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(44,62,80,0.6); z-index:-1; }
header h1 { margin:100px 0 10px; font-size:3em; text-shadow:2px 2px 8px rgba(0,0,0,0.5); }
header p { font-size:1.2em; color:#ddd; }
main { max-width:900px; margin:40px auto; padding:0 20px; }
.tema { border-radius:15px; margin-bottom:20px; overflow:hidden; transition:box-shadow 0.3s, transform 0.3s, background-color 0.3s; background:#ecf0f1; }
.tema.active { box-shadow:0 10px 25px rgba(0,0,0,0.35); transform:scale(1.02); }
.tema:nth-child(odd) .titulo-tema { background:#3498db; color:#fff; }
.tema:nth-child(even) .titulo-tema { background:#1abc9c; color:#fff; }
.titulo-tema { cursor:pointer; padding:18px 25px; font-weight:bold; font-size:1.2em; transition:background 0.3s, transform 0.2s; }
.titulo-tema:hover { opacity:0.85; transform:scale(1.02); }
.contenido-tema { padding:0 20px; max-height:0; overflow:hidden; opacity:0; transition:max-height 0.5s ease, padding 0.5s ease, opacity 0.5s ease, background-color 0.5s ease; background:#ecf0f1; }
.contenido-tema.open { padding:20px; max-height:500px; opacity:1; }
.letra { white-space:pre-wrap; background:#fff; padding:15px; border-radius:10px; max-height:220px; overflow-y:auto; margin-bottom:15px; box-shadow:inset 0 2px 5px rgba(0,0,0,0.1); }
audio { width:100%; border-radius:10px; outline:none; transition: box-shadow 0.5s ease; }
.tema.playing { box-shadow:0 0 20px #ffce54,0 0 40px #ffce54 inset; }
.vu-meter { height:6px; background:#ddd; border-radius:3px; margin-top:5px; overflow:hidden; display:flex; align-items:flex-end; }
.vu-bar { flex:1; height:100%; margin:0 1px; background:#ffce54; transition:height 0.1s linear; }
.pendiente { font-style:italic; color:#888; text-align:center; animation:parpadeo 1.5s infinite alternate; }
@keyframes parpadeo {0% {color:#888; transform:translateY(0px);}50% {color:#bbb; transform:translateY(-3px);}100% {color:#888; transform:translateY(0px);}}
</style>
</head>
<body>
<header>
<h1>Volumen 1 – Reparto Extra</h1>
<p>Álbum musical cubano · Son · Salsa · Fusión</p>
</header>
<main>
"""

# Generar bloques de temas
for txt in temas_txt:
    num = txt.split("-")[0]
    nombre = "-".join(txt.split("-")[1:]).replace(".txt","").replace("_"," ")
    ruta_txt = os.path.join(carpeta_letras, txt)
    with open(ruta_txt,"r",encoding="utf-8") as f:
        letra = f.read()
    if num in audios_dict:
        audio_file = audios_dict[num]
        bloque = f"""
<div class="tema"><div class="titulo-tema">{num} – {nombre}</div><div class="contenido-tema">
<div class="letra">{letra}</div>
<audio controls src="audios/{audio_file}"></audio>
<div class="vu-meter">{"".join(['<div class="vu-bar"></div>'*10])}</div>
</div></div>
"""
    else:
        bloque = f"""
<div class="tema"><div class="titulo-tema">{num} – {nombre}</div><div class="contenido-tema">
<div class="letra">{letra}</div>
<p class="pendiente">Audio disponible pronto</p>
</div></div>
"""
    html += bloque

# Script de interacción
html += """
<script>
const temas = document.querySelectorAll('.titulo-tema');
temas.forEach(titulo => {titulo.addEventListener('click', ()=>{
    const contenido = titulo.nextElementSibling;
    const parent = titulo.parentElement;
    document.querySelectorAll('.contenido-tema').forEach(c => c.classList.remove('open'));
    document.querySelectorAll('.tema').forEach(t => t.classList.remove('active'));
    contenido.classList.add('open'); parent.classList.add('active');});
});
const audios = document.querySelectorAll('audio');
audios.forEach(audio => {
  const bars = audio.nextElementSibling?.querySelectorAll('.vu-bar');
  audio.addEventListener('play', () => { audios.forEach(a => a.parentElement.parentElement.classList.remove('playing'));
    audio.parentElement.parentElement.classList.add('playing'); if(bars) animateVU(bars);
  });
  audio.addEventListener('pause', () => { if(bars) bars.forEach(bar => bar.style.height='0%'); audio.parentElement.parentElement.classList.remove('playing'); });
  audio.addEventListener('ended', () => { if(bars) bars.forEach(bar => bar.style.height='0%'); audio.parentElement.parentElement.classList.remove('playing'); });
});
function animateVU(bars){ bars.forEach(bar => { const h = Math.floor(Math.random()*80)+20; bar.style.height = h+'%'; }); requestAnimationFrame(()=>animateVU(bars)); }
</script>
</main>
</body>
</html>
"""

# Guardar HTML
with open(salida_html,"w",encoding="utf-8") as f:
    f.write(html)

print(f"HTML generado correctamente en '{salida_html}'")