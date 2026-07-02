#!/usr/bin/env python3
"""FULL milestone-based content, faithful to the cronología doc (year -> milestones),
bilingual ES/EN, each writeup paired with its attached photos. Emits tools/years.json.

Photos are read from ~/Downloads/puna-fotos and web-optimized into ../assets/ (cached).
Run:  python3 tools/content_full.py     ->  writes tools/years.json
"""
import pathlib, json, unicodedata, re, hashlib, subprocess
SRC   = pathlib.Path.home()/"Downloads"/"puna-fotos"
ROOT  = pathlib.Path(__file__).parent.parent
ASSETS= ROOT/"assets"; ASSETS.mkdir(exist_ok=True)
EXTS  = ["jpg","jpeg","png","JPG","JPEG","PNG","heic","HEIC","Heic","jpG"]

def _slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+','-',s).strip('-').lower() or 'x'
def opt(src: pathlib.Path):
    rel=src.relative_to(SRC)
    parent=_slug("-".join(rel.parent.parts)) if rel.parent.parts else "root"
    safe=f"assets/{parent}__{_slug(rel.stem)}.jpg"
    dst=ROOT/safe
    if not dst.exists():
        dst.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(["sips","--resampleWidth","1300","-s","format","jpeg","-s","formatOptions","62",
                        str(src),"--out",str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return safe
def _pick(folder, stem):
    base=SRC/folder
    for e in EXTS:
        hits=sorted(base.glob(f"**/{stem}.{e}"))
        if hits: return hits[0]
    return None
def N(folder, triples):
    out=[]
    for stem,es,en in triples:
        p=_pick(folder,stem)
        if p: out.append({"u":opt(p),"es":es,"en":en})
        else: print("  MISSING",folder,stem)
    return out
def DIRECT(rel, es, en):
    p=SRC/rel
    return [{"u":opt(p),"es":es,"en":en}] if p.exists() else (print("  MISSING",rel) or [])
def ORD(folder, caps):
    base=SRC/folder; d=base
    if base.exists():
        for s in sorted(base.iterdir()):
            if s.is_dir() and 'selecc' in s.name.lower(): d=s; break
    files=[f for f in sorted(d.glob("*")) if f.suffix.lower() in (".jpg",".jpeg",".png",".heic")][:len(caps)] if d.exists() else []
    return [{"u":opt(f),"es":es,"en":en} for f,(es,en) in zip(files,caps)]
def ALL(folder, es, en):  # grab every image in a folder (filenames don't matter)
    d=SRC/folder
    if not d.exists(): return []
    fs=[f for f in sorted(d.iterdir()) if f.suffix.lower() in (".jpg",".jpeg",".png",".heic")]
    return [{"u":opt(f),"es":es,"en":en} for f in fs]

VID={"sausalito":{"u":"assets/videos/sausalito-agua.mp4","es":"Mujeres de Sausalito cuentan la situación con el agua en su comunidad","en":"Women of Sausalito describe the water situation in their community"},
     "santaana":{"u":"assets/videos/santa-ana.mp4","es":"Actividad en la comunidad de Santa Ana","en":"Activity in the community of Santa Ana"}}

YMETA={
 "2020":("#ff5a4a","Nuestros orígenes","Our beginnings",
   "En el contexto de la pandemia de COVID-19, el encuentro entre Yamil, Victoria y Pablo terminaría dando origen a Fundación Puna y a las primeras redes de trabajo colectivo de la organización junto a las comunidades de su provincia.",
   "Amid the COVID-19 pandemic, the meeting of Yamil, Victoria and Pablo would give rise to Fundación Puna and to the organization's first networks of collective work alongside the communities of its province."),
 "2021":("#7ba551","Primeros recorridos territoriales","First territorial journeys",
   "Con la reapertura de rutas, se organiza el primer viaje a las comunidades de la cuenca de Salinas Grandes. A partir de una colecta solidaria se reunieron útiles escolares y alimentos para recorrer siete comunidades de Jujuy en un solo fin de semana, visibilizando las desigualdades estructurales en torno al agua, la infraestructura y los derechos básicos.",
   "As the roads reopened, the first trip to the communities of the Salinas Grandes basin was organized. A solidarity drive gathered school supplies and food to visit seven communities of Jujuy in a single weekend, making visible the structural inequalities around water, infrastructure and basic rights."),
 "2022":("#ff914d","Un año de consolidación","A year of consolidation",
   "La Fundación se enfoca en fortalecer su identidad. Con el aporte de Lorenzo Ramicone se desarrolla el logotipo y la identidad visual. Se sostienen las acciones educativas a distancia y la difusión de las problemáticas de las comunidades de la Puna: un año de base para ordenar y proyectar a futuro.",
   "The Foundation focuses on strengthening its identity. With Lorenzo Ramicone's contribution, the logo and visual identity take shape. Remote education and outreach about the Puna communities' struggles continue — a foundational year to organize and look ahead."),
 "2023":("#79408d","Reforma inconstitucional","Unconstitutional reform",
   "El 2023 estuvo marcado por un fuerte conflicto social, político e institucional a partir de una reforma de la constitución provincial que restringía el derecho a la protesta y la propiedad comunitaria de la tierra. La defensa del territorio, el agua y los derechos humanos toman un rol protagónico dentro de la Fundación.",
   "2023 was marked by intense social, political and institutional conflict over a provincial constitutional reform that restricted the right to protest and communal land ownership. The defense of territory, water and human rights took center stage for the Foundation."),
 "2024":("#9e69b1","Lucha, cultura y crecimiento","Struggle, culture and growth",
   "Una etapa de mayor consolidación que combina el trabajo territorial con la articulación política, el fortalecimiento cultural y nuevas iniciativas. La educación continúa como eje, con clases de inglés y espacios vinculados a derechos humanos.",
   "A stage of greater consolidation combining territorial work with political articulation, cultural strengthening and new initiatives. Education remains a core axis, with English classes and human-rights spaces."),
 "2025":("#6492d8","Expansión y articulación internacional","International expansion and alliances",
   "El año de la proyección internacional y la intervención judicial. La Fundación llevó reclamos socioambientales al Parlamento Europeo y sumó alianzas clave con organismos de derechos humanos como el SERPAJ, mientras diversificaba el trabajo territorial hacia la salud comunitaria y la universidad pública.",
   "The year of international projection and judicial intervention. The Foundation brought socio-environmental claims to the European Parliament and forged key alliances with human-rights bodies such as SERPAJ, while diversifying territorial work toward community health and the public university."),
 "2026":("#78677e","Lo que viene","What's next",
   "Una nueva etapa de crecimiento: se reactivan y profundizan las acciones en territorio mientras se consolidan redes de cooperación internacional. Pronto, más novedades.",
   "A new stage of growth: territorial action is renewed and deepened while international cooperation networks consolidate. More coming soon."),
}

# ---------------- milestones (in doc order) ----------------
MILES=[
 # ===== 2020 =====
 {"y":"2020","t_es":"Apoyo educativo durante la pandemia","t_en":"Educational support during the pandemic",
  "x_es":"Durante la pandemia, Yamil Alejo, un joven estudiante de ingeniería oriundo de Barrancas, regresa a su comunidad y detecta una problemática urgente: la falta de conectividad estaba dejando a muchos niños y jóvenes fuera del sistema educativo. Frente a esa realidad, comienza a organizar clases de apoyo y acompañamiento escolar utilizando los recursos que tenía a mano —celulares, cuadernos y espacios comunitarios— para sostener redes educativas y que muchos estudiantes pudieran continuar aprendiendo en medio del aislamiento.",
  "x_en":"During the pandemic, Yamil Alejo, a young engineering student from Barrancas, returns to his community and spots an urgent problem: the lack of connectivity was leaving many children and youth outside the school system. In response, he begins organizing tutoring and school support using whatever was at hand —phones, notebooks and community spaces— to sustain learning networks so that many students could keep learning through the isolation.",
  "ph":N("2020",[("Yamil 01","Nota periodística sobre las clases de apoyo de Yamil","News feature on Yamil's tutoring"),
                 ("Yamil 02","Clases de apoyo escolar durante el aislamiento","School tutoring during the isolation")])},
 {"y":"2020","t_es":"Salud y territorio durante la pandemia","t_en":"Health and territory during the pandemic",
  "x_es":"En ese mismo contexto, Victoria Araya, una estudiante de medicina, decide regresar a Jujuy con la intención de reconectar con sus orígenes. Al volver, se suma como voluntaria al sistema de salud, donde recorre muchos pueblos de la Quebrada y la Puna jujeña. A través de esa experiencia comienza a evidenciar que la urgencia no era solamente el COVID-19, sino también desigualdades estructurales mucho más profundas: la falta de agua, de acceso a la educación, de conectividad y de derechos básicos en muchas comunidades de la provincia.",
  "x_en":"In that same context, Victoria Araya, a medical student, decides to return to Jujuy to reconnect with her roots. Back home, she volunteers in the health system, traveling through many villages of the Quebrada and the Jujuy Puna. Through that experience she begins to see that the emergency was not only COVID-19, but far deeper structural inequalities: the lack of water, education, connectivity and basic rights in many communities of the province.",
  "ph":N("2020",[("IMG_3788","Victoria Araya recorriendo los pueblos de la Quebrada y la Puna","Victoria Araya visiting the villages of the Quebrada and Puna"),
                 ("Victoria 01","Voluntarios de salud frente al Hospital de Susques","Health volunteers in front of the Susques Hospital"),
                 ("Victoria 02","Victoria Araya, voluntaria de salud en la Puna","Victoria Araya, health volunteer in the Puna")])},
 {"y":"2020","t_es":"El encuentro entre Victoria, Yamil y Pablo","t_en":"The meeting of Victoria, Yamil and Pablo",
  "x_es":"En 2020, en medio de la pandemia, los caminos de Victoria Araya, Yamil Alejo y Pablo Agüero se cruzan a partir de las iniciativas comunitarias que cada uno venía impulsando por separado en Jujuy. El encuentro entre los tres permitió unir fuerzas, miradas y formas de organización que terminarían dando origen a Fundación Puna. Desde entonces, Victoria, Yamil y Pablo continúan integrando la organización como sus miembros fundadores.",
  "x_en":"In 2020, mid-pandemic, the paths of Victoria Araya, Yamil Alejo and Pablo Agüero cross through the community initiatives each had been driving separately in Jujuy. Their meeting joined forces, perspectives and ways of organizing that would give rise to Fundación Puna. Since then, Victoria, Yamil and Pablo remain part of the organization as its founding members.",
  "ph":N("2020",[("Victoria 03","Victoria, Yamil y Pablo — miembros fundadores de Fundación Puna","Victoria, Yamil and Pablo — founding members of Fundación Puna")])},
 # ===== 2021 =====
 {"y":"2021","t_es":"Organización colectiva","t_en":"Collective organizing",
  "x_es":"Antes del viaje, Fundación Puna impulsa una colecta junto a voluntarios, familias y redes cercanas. Olga Cabrera, anciana originaria del pueblo de Volcán y abuela de Victoria Araya, tuvo un rol fundamental sugiriendo ideas y ayudando a armar cada bolsita con útiles, golosinas y materiales destinados a los niños de cada comunidad. Ese trabajo, sostenido desde el cuidado y la dedicación, también formó parte del espíritu colectivo de Puna.",
  "x_en":"Before the trip, Fundación Puna runs a collection with volunteers, families and close networks. Olga Cabrera —an elder from the town of Volcán and Victoria Araya's grandmother— played a key role suggesting ideas and helping assemble each bag of supplies, treats and materials for the children of every community. That work, grounded in care and dedication, was also part of Puna's collective spirit.",
  "ph":ORD("2021/pre viaje a la puna ",[("Donaciones recolectadas","Donations gathered"),
        ("Victoria y Olga preparando todo para el viaje","Victoria and Olga getting everything ready for the trip"),
        ("Olga limpiando y ordenando donaciones","Olga cleaning and sorting the donations"),
        ("Cronograma del viaje","The trip schedule")])},
 {"y":"2021","t_es":"Santuario de Tres Pozos","t_en":"Santuario de Tres Pozos",
  "x_es":"La primera parada del recorrido fue el Santuario de Tres Pozos, hogar de Verónica Chávez, quien hasta el día de hoy sigue siendo una referente para nuestra Fundación. La comunidad recibió al equipo con mate cocido y tortillas; durante la jornada se realizaron juegos, actividades recreativas y entrega de útiles escolares y regalos.",
  "x_en":"The first stop of the journey was the Santuario de Tres Pozos, home of Verónica Chávez, still a key reference for our Foundation today. The community welcomed the team with mate cocido and tortillas; the day was filled with games, activities and the handing out of school supplies and gifts.",
  "ph":ORD("2021/Santuario de Tres pozos ",[("Merienda en Tres Pozos","Afternoon snack at Tres Pozos")]*4+
       [("Tortilla a la parrilla en Tres Pozos","Grilled tortilla at Tres Pozos"),
        ("Victoria Araya con niñas de la comunidad","Victoria Araya with girls from the community"),
        ("Pablo Agüero en la comunidad de Tres Pozos","Pablo Agüero in the community of Tres Pozos")])},
 {"y":"2021","t_es":"Rinconadillas","t_en":"Rinconadillas",
  "x_es":"El viaje continuó en Rinconadillas, una comunidad especialmente significativa para Yamil Alejo: lo vio crecer, allí viven sus abuelos maternos y transcurrió gran parte de su infancia. La comunidad organizó un almuerzo colectivo y espacios de encuentro junto al equipo de Fundación Puna.",
  "x_en":"The journey continued in Rinconadillas, a community especially meaningful to Yamil Alejo: it watched him grow up, his maternal grandparents live there and much of his childhood took place there. The community organized a shared lunch and gatherings with the Fundación Puna team.",
  "ph":ORD("2021/Rinconadillas",[("Victoria con niñas de Rinconadillas","Victoria with girls from Rinconadillas"),
        ("Llegada de Fundación Puna a Rinconadillas","Fundación Puna arrives in Rinconadillas"),
        ("Llegada de Fundación Puna a Rinconadillas","Fundación Puna arrives in Rinconadillas"),
        ("Almuerzo comunitario","Community lunch"),("Hojas de coca","Coca leaves"),
        ("Partido de fútbol en las alturas","Football match in the highlands"),
        ("Partido de fútbol en las alturas","Football match in the highlands"),
        ("Paisaje llegando a Rinconadillas","Landscape on the way to Rinconadillas"),
        ("Paisaje de Rinconadillas","Rinconadillas landscape")])},
 {"y":"2021","t_es":"San Francisco de Alfarcito","t_en":"San Francisco de Alfarcito",
  "x_es":"En Alfarcito pudimos conocer experiencias de organización vinculadas al trabajo local y al cuidado del territorio, además de recorrer espacios productivos comunitarios que mostraron otra realidad dentro de la región.",
  "x_en":"In Alfarcito we got to know experiences of local organizing and care for the territory, and visited community productive spaces that showed another reality within the region.",
  "ph":N("2021/San Francisco de Alfarcito",[("4","Paisaje de Alfarcito","Alfarcito landscape"),
        ("5","Paisaje de Alfarcito","Alfarcito landscape"),("1","Caminata por Alfarcito","Walking through Alfarcito"),
        ("2","Alfarcito","Alfarcito")])},
 {"y":"2021","t_es":"Sausalito · la cuestión del agua","t_en":"Sausalito · the water question",
  "x_es":"La visita a Sausalito marcó uno de los momentos más movilizantes del recorrido. La falta de acceso al agua potable atravesaba la vida cotidiana de toda la comunidad. El contraste con otras localidades evidenció las profundas desigualdades dentro de la misma región y reforzó la necesidad de incorporar la problemática del agua como uno de los ejes centrales del trabajo de Fundación Puna.",
  "x_en":"The visit to Sausalito was one of the most moving moments of the journey. The lack of access to drinking water shaped the daily life of the whole community. The contrast with other towns exposed the deep inequalities within the same region and reinforced the need to make water one of the central axes of Fundación Puna's work.",
  "video":VID["sausalito"],
  "ph":N("2021/Sausalito",[("WhatsApp Image 2026-06-30 at 13.57.42","Voluntarios de Fundación Puna en una cena en Sausalito","Fundación Puna volunteers at a dinner in Sausalito"),
        ("WhatsApp Image 2026-06-30 at 13.56.51","Victoria Araya junto a las mujeres de la comunidad de Sausalito","Victoria Araya with the women of the Sausalito community")])},
 {"y":"2021","t_es":"Tusaquillas","t_en":"Tusaquillas",
  "x_es":"En Tusaquillas, el encuentro permitió continuar fortaleciendo vínculos y conocer de cerca las dificultades cotidianas vinculadas al acceso a recursos básicos y a los espacios para las infancias.",
  "x_en":"In Tusaquillas, the gathering allowed us to keep strengthening bonds and to see up close the everyday difficulties tied to access to basic resources and to spaces for children.",
  "ph":N("2021/Tusaquillas",[("IMG_0344","Merienda en Tusaquillas","Snack in Tusaquillas"),
        ("IMG_0349","Voluntarios de Fundación Puna en Tusaquillas","Fundación Puna volunteers in Tusaquillas"),
        ("IMG_0357","Entrega de donaciones en Tusaquillas","Handing out donations in Tusaquillas"),
        ("IMG_0365","Victoria Araya junto a la comunidad de Tusaquillas","Victoria Araya with the community of Tusaquillas"),
        ("IMG_0374","Escuela de Tusaquillas","School of Tusaquillas"),
        ("IMG_0336","Paisaje de Tusaquillas","Tusaquillas landscape"),
        ("IMG_0395","Victoria Araya junto a la comunidad de Tusaquillas","Victoria Araya with the community of Tusaquillas")])},
 {"y":"2021","t_es":"Santa Ana","t_en":"Santa Ana",
  "x_es":"En Santa Ana se realizaron actividades junto a niños y familias, espacios de encuentro comunitario y entrega de útiles y materiales escolares.",
  "x_en":"In Santa Ana, activities were held with children and families, community gatherings and the handing out of school supplies and materials.",
  "video":VID["santaana"],
  "ph":N("2021/Santa Ana",[("IMG_0444","Actividad en la comunidad de Santa Ana","Activity in the community of Santa Ana"),
        ("IMG_0450","Actividad en la comunidad de Santa Ana","Activity in the community of Santa Ana"),
        ("IMG_0500","Voluntarios de Fundación Puna en Santa Ana","Fundación Puna volunteers in Santa Ana"),
        ("IMG_0434","Actividad en la comunidad de Santa Ana","Activity in the community of Santa Ana"),
        ("IMG_0429","Actividad en la comunidad de Santa Ana","Activity in the community of Santa Ana"),
        ("IMG_0509","Paisaje de Santa Ana","Santa Ana landscape")])},
 {"y":"2021","t_es":"Barrancas","t_en":"Barrancas",
  "x_es":"El recorrido finalizó en Barrancas, comunidad natal de Yamil Alejo y lugar donde habían comenzado las primeras redes de acompañamiento educativo durante la pandemia. La jornada incluyó meriendas, juegos y espacios comunitarios que cerraron el viaje reafirmando el vínculo entre Fundación Puna y las comunidades de la región.",
  "x_en":"The route ended in Barrancas, Yamil Alejo's home community and the place where the first educational-support networks had begun during the pandemic. The day included snacks, games and community spaces that closed the trip, reaffirming the bond between Fundación Puna and the region's communities.",
  "ph":N("2021/Barrancas",[("IMG_0592","Actividad en la comunidad de Barrancas","Activity in the community of Barrancas"),
        ("IMG_0593","Actividad en la comunidad de Barrancas","Activity in the community of Barrancas"),
        ("IMG_0594","Actividad en la comunidad de Barrancas","Activity in the community of Barrancas"),
        ("IMG_0626","Voluntarios de Fundación Puna en Barrancas","Fundación Puna volunteers in Barrancas"),
        ("IMG_0527","Paisaje de Barrancas","Barrancas landscape"),
        ("IMG_0577","Actividad en la comunidad de Barrancas","Activity in the community of Barrancas"),
        ("IMG_0581","Actividad en la comunidad de Barrancas","Activity in the community of Barrancas"),
        ("IMG_0618","Actividad en la comunidad de Barrancas","Activity in the community of Barrancas")])},
 {"y":"2021","t_es":"Regreso a Rinconadillas y Ojo de Agua","t_en":"Return to Rinconadillas and Ojo de Agua",
  "x_es":"Hacia finales de 2021, Fundación Puna realiza un nuevo viaje a la región, fortaleciendo los vínculos construidos durante los primeros recorridos. El viaje incluyó una segunda visita a Rinconadillas y un recorrido por Ojo del Agua, donde el equipo conoció de cerca las dificultades cotidianas vinculadas al acceso al agua. El encuentro con familias que debían recolectarla manualmente reforzó aún más la importancia de esta problemática dentro del trabajo de la fundación.",
  "x_en":"Toward the end of 2021, Fundación Puna made a new trip to the region, strengthening the bonds built during the first journeys. The trip included a second visit to Rinconadillas and a stop at Ojo del Agua, where the team saw up close the everyday difficulties tied to water access. Meeting families who had to collect it by hand further reinforced the importance of this issue in the foundation's work.",
  "ph":N("2021/Rinconadillas la vuelta (fin de año)",
       [("IMG_1071","Victoria Araya y Jeremy Munson en Rinconadillas","Victoria Araya and Jeremy Munson in Rinconadillas"),
        ("IMG_1111","Victoria Araya y Jeremy Munson en Rinconadillas","Victoria Araya and Jeremy Munson in Rinconadillas"),
        ("IMG_1224","Victoria Araya y Jeremy Munson en Rinconadillas","Victoria Araya and Jeremy Munson in Rinconadillas"),
        ("IMG_1214","Retiro de agua en Rinconadillas","Collecting water in Rinconadillas"),
        ("IMG_1267","Actividad en Rinconadillas","Activity in Rinconadillas"),
        ("IMG_1188","Paisaje de Rinconadillas","Rinconadillas landscape")])},
 {"y":"2021","t_es":"Clases de inglés online","t_en":"Online English classes",
  "x_es":"En esta etapa se suma como miembro Jeremy Munson, quien comienza a colaborar impulsando clases de inglés para jóvenes de las comunidades con las que Fundación Puna trabaja.",
  "x_en":"In this period Jeremy Munson joins as a member, beginning to collaborate by driving English classes for youth in the communities Fundación Puna works with.",
  "ph":N("2021/Rinconadillas la vuelta (fin de año)",[("IMG_8734","Victoria Araya y Jeremy Munson — clases de inglés online","Victoria Araya and Jeremy Munson — online English classes")])},
 # ===== 2022 =====
 {"y":"2022","t_es":"Identidad visual","t_en":"Visual identity",
  "x_es":"Durante este año la Fundación se enfocó en fortalecer su identidad. Con el aporte de Lorenzo Ramicone se desarrolla el logotipo y la identidad visual, dando forma a una imagen más clara y coherente. A la par, se sostienen las acciones educativas a distancia y la difusión de las problemáticas que atraviesan las comunidades de la Puna. Así, 2022 se vuelve un año de base para ordenar y proyectar a futuro.",
  "x_en":"During this year the Foundation focused on strengthening its identity. With Lorenzo Ramicone's contribution, the logo and visual identity are developed, giving shape to a clearer, more coherent image. In parallel, remote education and outreach about the Puna communities' struggles continue. Thus 2022 becomes a foundational year to organize and project into the future.",
  "ph":DIRECT("2022/Victoria y Yamil .JPG","Victoria y Yamil","Victoria and Yamil")},
 # ===== 2023 =====
 {"y":"2023","t_es":"Corte y permanencia en Purmamarca","t_en":"Blockade and encampment in Purmamarca",
  "x_es":"En junio, en Purmamarca, tuvo lugar uno de los episodios más significativos: el corte y permanencia en la Ruta Nacional 9, que duró más de dos meses. Comunidades indígenas, docentes y trabajadores se manifestaron en defensa de sus derechos y la respuesta estatal fue represiva, con balas de goma, gases lacrimógenos y detenciones constantes. Fundación Puna acompañó de cerca a muchas de las víctimas ofreciendo apoyo económico y logístico.",
  "x_en":"In June, in Purmamarca, one of the most significant episodes took place: the blockade and encampment on National Route 9, which lasted more than two months. Indigenous communities, teachers and workers demonstrated in defense of their rights and the state response was repressive, with rubber bullets, tear gas and constant detentions. Fundación Puna accompanied many of the victims with financial and logistical support.",
  "ph":N("2023",[("9B3F8A62-E2CA-4605-89C6-16B8DA8B6EB8","Corte y permanencia en Purmamarca","Blockade and encampment in Purmamarca"),
        ("IMG_7113","Victoria Araya en la posta de salud del corte de Purmamarca","Victoria Araya at the blockade's first-aid post"),
        ("IMG_5171","Victoria Araya en el corte de Purmamarca","Victoria Araya at the Purmamarca blockade"),
        ("IMG-20230701-WA0352","Mural en la Ruta Nacional 9","Mural on National Route 9"),
        ("IMG_7302","Corte y permanencia en Purmamarca","Blockade and encampment in Purmamarca"),
        ("IMG_7309","Jeremy Munson en el corte de Purmamarca","Jeremy Munson at the Purmamarca blockade")])},
 {"y":"2023","t_es":"Apoyo ante la represión — Lian Lamas","t_en":"Support amid the repression — Lian Lamas",
  "x_es":"La violencia estatal dejó heridas físicas y emocionales profundas. Entre los casos más graves se encuentran Lian Lamas, un joven de 17 años que perdió un ojo tras recibir un disparo policial, y Joel Paredes, quien también sufrió daños irreparables. Frente a estas situaciones, Fundación Puna acompañó a las víctimas ofreciendo apoyo económico y logístico, y dando hospedaje en Buenos Aires para sus consultas médicas.",
  "x_en":"State violence left deep physical and emotional wounds. Among the gravest cases are Lian Lamas, a 17-year-old who lost an eye after a police shot, and Joel Paredes, who also suffered irreparable damage. In response, Fundación Puna accompanied the victims with financial and logistical support, and hosted them in Buenos Aires for their medical care.",
  "ph":N("2023/Lian Lamas",[("IMG_8362","Lian Lamas","Lian Lamas"),
        ("IMG_7865","Lian Lamas en la casa de Fundación Puna en Buenos Aires","Lian Lamas at Fundación Puna's house in Buenos Aires"),
        ("b73d1497-0b61-408b-8388-d77a2c226fcf","Lian Lamas con Estela de Carlotto","Lian Lamas with Estela de Carlotto")])},
 {"y":"2023","t_es":"Tercer Malón de la Paz","t_en":"Third Malón de la Paz",
  "x_es":"Frente a la gravedad de la situación, más de 400 comunidades originarias se organizaron en el Tercer Malón de la Paz, una movilización histórica que recorrió más de 1.800 km desde La Quiaca hasta Buenos Aires para llevar el reclamo a la Corte Suprema de Justicia. Yamil Alejo asumió un rol de liderazgo entre los jóvenes del movimiento. Fundación Puna colaboró en la logística, el apoyo en la posta de salud y la visibilización del conflicto a nivel nacional e internacional.",
  "x_en":"Given the gravity of the situation, more than 400 Indigenous communities organized the Third Malón de la Paz, a historic mobilization that traveled over 1,800 km from La Quiaca to Buenos Aires to bring their claim to the Supreme Court of Justice. Yamil Alejo took on a leadership role among the movement's youth. Fundación Puna supported logistics, the first-aid post and national and international visibility of the conflict.",
  "ph":N("2023/Tercer Malon de la Paz en Buenos Aires (yamil)",
       [("IMG-20230729-WA0065","El Tercer Malón de la Paz en Buenos Aires","The Third Malón de la Paz in Buenos Aires"),
        ("IMG-20230729-WA0075","El Tercer Malón de la Paz en Buenos Aires","The Third Malón de la Paz in Buenos Aires"),
        ("IMG-20230729-WA0077","El Tercer Malón de la Paz en Buenos Aires","The Third Malón de la Paz in Buenos Aires"),
        ("IMG_4358","Yamil Alejo en el Tercer Malón de la Paz","Yamil Alejo at the Third Malón de la Paz")])},
 {"y":"2023","t_es":"Verónica Chávez y James Cameron","t_en":"Verónica Chávez and James Cameron",
  "x_es":"Con el acompañamiento de Fundación Puna, Verónica Chávez, representante de la Comunidad Santuario Tres Pozos, se reunió en Buenos Aires con el cineasta y activista ambiental James Cameron, y expuso de primera mano cómo el avance de la extracción de litio afecta los territorios, el acceso al agua y las formas de vida en la Puna. Victoria Araya participó como traductora, proyectando la voz de la comunidad a escala internacional.",
  "x_en":"With Fundación Puna's support, Verónica Chávez, representative of the Santuario Tres Pozos community, met in Buenos Aires with filmmaker and environmental activist James Cameron, and showed first-hand how the advance of lithium extraction affects the territories, water access and ways of life in the Puna. Victoria Araya took part as translator, projecting the community's voice on an international scale.",
  "ph":N("2023-cameron",[("2","Verónica Chávez con James Cameron","Verónica Chávez with James Cameron"),
        ("1","Verónica Chávez con James Cameron","Verónica Chávez with James Cameron"),
        ("3","Reunión con Victoria Araya como traductora","Meeting with Victoria Araya as translator"),
        ("4","Verónica Chávez con Victoria Araya en Aeroparque","Verónica Chávez with Victoria Araya at Aeroparque"),
        ("5","Recorte de noticia","News clipping")])},
 # ===== 2024 =====
 {"y":"2024","t_es":"En las calles","t_en":"In the streets",
  "x_es":"En enero, Fundación Puna reafirma su compromiso con las comunidades de Salinas Grandes acompañando al Tercer Malón de la Paz en el rechazo al DNU 70/2023 impulsado por el gobierno nacional. La participación en movilizaciones y espacios de protesta forma parte de una continuidad en la defensa de derechos, especialmente en relación con el territorio, el agua y las condiciones de vida de las comunidades.",
  "x_en":"In January, Fundación Puna reaffirms its commitment to the Salinas Grandes communities by accompanying the Third Malón de la Paz in rejecting the national government's Decree 70/2023. Taking part in mobilizations and protests is part of a continuity in defending rights, especially around territory, water and the communities' living conditions.",
  "ph":N("2024",[("IMG_3427","Victoria Araya y Yamil Alejo en la marcha en San Salvador de Jujuy","Victoria Araya and Yamil Alejo at the march in San Salvador de Jujuy"),
        ("IMG_3440","Reunión de Fundación Puna con miembros del Tercer Malón de la Paz","Fundación Puna meeting with members of the Third Malón de la Paz")])},
 {"y":"2024","t_es":"Cumbre del Agua","t_en":"Water Summit",
  "x_es":"La defensa del agua se consolida como una prioridad. En marzo, Fundación Puna participa en la Cumbre del Agua, un espacio de encuentro entre comunidades originarias, especialistas y activistas, donde se comparten estrategias para proteger los recursos hídricos frente al avance de políticas extractivas.",
  "x_en":"The defense of water consolidates as a priority. In March, Fundación Puna takes part in the Water Summit, a gathering of Indigenous communities, specialists and activists where strategies are shared to protect water resources against the advance of extractive policies.",
  "ph":N("2024",[("IMG_9906","Acuerdo de trabajo con la comunidad de Tres Pozos","Working agreement with the Tres Pozos community"),
        ("07d1d7a0-0fb7-40e6-870d-3d4de718aa14","Pedido de apoyo de la Cumbre del Agua a Fundación Puna","The Water Summit's request for support to Fundación Puna")])},
 {"y":"2024","t_es":"Cultura en comunidad","t_en":"Culture in community",
  "x_es":"La cultura y el vínculo con las comunidades ocupan un lugar central. En febrero, el equipo participa del desentierro de carnaval en la comunidad de Angosto El Pérchel, una ceremonia ancestral que marca el inicio del carnaval andino y refuerza la conexión con la tierra y la vida comunitaria. Además, Fundación Puna visita nuevamente a la comunidad de Rinconadillas.",
  "x_en":"Culture and the bond with the communities take a central place. In February, the team takes part in the carnival 'unearthing' in the community of Angosto El Pérchel, an ancestral ceremony that marks the start of the Andean carnival and reinforces the connection with the land and community life. Fundación Puna also visits the Rinconadillas community again.",
  "ph":N("2024",[("IMG_7540","Paisaje de la Puna jujeña","Landscape of the Jujuy Puna"),
        ("IMG_7675","Desentierro de carnaval en Angosto El Pérchel","Carnival 'unearthing' in Angosto El Pérchel"),
        ("IMG_9087","Carnaval andino","Andean carnival"),
        ("IMG_7593","Visita a la comunidad de Rinconadillas","Visit to the Rinconadillas community")])},
 {"y":"2024","t_es":"Activismo ambiental con Carola Rackete y Bojana Novakovic","t_en":"Environmental activism with Carola Rackete and Bojana Novakovic",
  "x_es":"Hacia octubre, la dimensión internacional vuelve a tomar fuerza con la visita de la eurodiputada Carola Rackete y la actriz y activista serbia Bojana Novakovic, quienes recorren la región y se vinculan con las comunidades en el marco de sus agendas de activismo ambiental. Su presencia aporta visibilidad y un gesto de acompañamiento que refuerza la importancia de las redes globales en la defensa del territorio.",
  "x_en":"Toward October, the international dimension gains strength again with the visit of MEP Carola Rackete and the Serbian actress and activist Bojana Novakovic, who tour the region and connect with the communities as part of their environmental-activism agendas. Their presence brings visibility and a gesture of solidarity that reinforces the importance of global networks in defending the territory.",
  "ph":N("2024/Carola y bojana",[("IMG_7781","Victoria Araya y Verónica Chávez con Bojana Novakovic en las Salinas","Victoria Araya and Verónica Chávez with Bojana Novakovic at the Salinas"),
        ("IMG_7737","Fundación Puna con Carola Rackete, Bojana Novakovic y miembros en la Cuenca de Salinas Grandes","Fundación Puna with Carola Rackete, Bojana Novakovic and members in the Salinas Grandes basin"),
        ("IMG_7839","Salinas Grandes","Salinas Grandes"),
        ("IMG_7753","Recorrido junto a las comunidades","Touring alongside the communities"),
        ("IMG_9238","Salinas Grandes","Salinas Grandes")])},
 # ===== 2025 =====
 {"y":"2025","t_es":"Cumbre de Energías Limpias · Parlamento Europeo","t_en":"Clean Energy Summit · European Parliament",
  "x_es":"Fundación Puna gestiona la participación de referentes comunitarios en una cumbre sobre energías limpias en el Parlamento Europeo: Verónica Chávez (cuenca de Salinas Grandes, Jujuy), Ñushpi Quilla Mayhuay Alancay (Malargüe, Mendoza) y Sergio Martínez (Andalgalá). Cada uno lleva una realidad distinta atravesada por un mismo eje: la defensa del agua y del territorio frente al avance extractivo, poniendo en el centro del debate las tensiones entre el discurso de las energías 'limpias' y sus impactos concretos en los territorios. Sol Felicitas Araya, del área de comunicación, realiza un informe audiovisual que reúne testimonios e imágenes del territorio para amplificar estas voces.",
  "x_en":"Fundación Puna arranges the participation of community leaders in a clean-energy summit at the European Parliament: Verónica Chávez (Salinas Grandes basin, Jujuy), Ñushpi Quilla Mayhuay Alancay (Malargüe, Mendoza) and Sergio Martínez (Andalgalá). Each brings a distinct reality tied to a shared axis: the defense of water and territory against extractive expansion, bringing to the center of the debate the tensions between the discourse of 'clean' energy and its concrete impacts. Sol Felicitas Araya, from communications, produces a short film gathering testimonies and images of the territory to amplify these voices.",
  "ph":N("2025",[("IMG_1995","Ñushpi y Victoria en el Parlamento Europeo","Ñushpi and Victoria at the European Parliament"),
        ("IMG_1978","Ñushpi, Verónica y Victoria en el Parlamento Europeo con Carola Rackete","Ñushpi, Verónica and Victoria at the European Parliament with Carola Rackete"),
        ("IMG_1963","Verónica y Victoria en el Parlamento Europeo","Verónica and Victoria at the European Parliament"),
        ("IMG_1926","Ñushpi, Verónica y Victoria en Europa","Ñushpi, Verónica and Victoria in Europe"),
        ("IMG_0686","Victoria y Jeremy con Verónica en Europa","Victoria and Jeremy with Verónica in Europe")])},
 {"y":"2025","t_es":"Alianza con el SERPAJ","t_en":"Alliance with SERPAJ",
  "x_es":"En paralelo, Fundación Puna firma un convenio de trabajo con el Servicio Paz y Justicia (SERPAJ), organización fundada por Adolfo Pérez Esquivel. Este acuerdo fortalece una línea de acción orientada a la cooperación en conflictos territoriales, ampliando las redes de articulación y consolidando un perfil más internacionalista.",
  "x_en":"In parallel, Fundación Puna signs a working agreement with Servicio Paz y Justicia (SERPAJ), the organization founded by Adolfo Pérez Esquivel. This agreement strengthens a line of action oriented to cooperation on territorial conflicts, expanding networks and consolidating a more internationalist profile.",
  "ph":N("2025",[("IMG_3912","Victoria Araya con Adolfo Pérez Esquivel","Victoria Araya with Adolfo Pérez Esquivel"),
        ("IMG_3846","Victoria Araya con los miembros del SERPAJ","Victoria Araya with the members of SERPAJ"),
        ("IMG_3923","Firma del convenio entre Fundación Puna y SERPAJ","Signing of the agreement between Fundación Puna and SERPAJ")])},
 {"y":"2025","t_es":"Jornadas de Plantas Medicinales","t_en":"Medicinal Plants gatherings",
  "x_es":"Los pasados 9 y 10 de octubre, las instalaciones del Club Vial 6 fueron sede de las 1ras Jornadas de Cannabis y Plantas Medicinales de la provincia —organizadas junto al programa de radio cannábico 'La Rama que Llama'—, un importante espacio de encuentro, debate e intercambio de conocimientos, libre y gratuito. El evento marcó un hito al ser declarado de interés legislativo, un reconocimiento que subraya la urgencia y la relevancia de abordar esta temática de forma seria, interdisciplinaria y abierta a la comunidad. La iniciativa contó con el acompañamiento de la Universidad Nacional de Jujuy (UNJu): se destacó la presencia de autoridades institucionales, con la participación especial de la Dra. en Antropología Liliana Bergessio, reafirmando el compromiso de la universidad pública con espacios académicos que promuevan el pensamiento crítico y el abordaje de temáticas de impacto social.",
  "x_en":"On October 9–10, the Club Vial 6 hosted the province's 1st Cannabis and Medicinal Plants Conference —organized together with the cannabis radio program 'La Rama que Llama'— a major, free and open space for gathering, debate and knowledge-sharing. The event was a milestone, declared of legislative interest, a recognition that underscores the urgency and relevance of addressing this topic seriously, across disciplines and open to the community. The initiative was accompanied by the National University of Jujuy (UNJu): institutional authorities took part, notably Dr. Liliana Bergessio (Anthropology), reaffirming the public university's commitment to academic spaces that foster critical thinking and socially impactful themes.",
  "ph":ALL("2025-jornadas","1ras Jornadas de Cannabis y Plantas Medicinales — Club Vial 6 (9–10 de octubre 2025)","1st Cannabis & Medicinal Plants Conference — Club Vial 6 (Oct 9–10, 2025)")},
 {"y":"2025","t_es":"Amicus Curiae en el caso de la niña Cielo","t_en":"Amicus Curiae in the case of the child Cielo",
  "x_es":"Fundación Puna articuló una red de organizaciones nacionales e internacionales de derechos humanos, que incluyó al Cyrus R. Vance Center for International Justice (NYC Bar Association) y al Servicio Paz y Justicia (SERPAJ). Esta alianza estratégica intervino institucionalmente mediante la figura de Amicus Curiae en el caso de la niña Cielo (Chaco), promoviendo la correcta aplicación de los estándares de protección de la niñez y la perspectiva de género ante el sistema judicial argentino.",
  "x_en":"Fundación Puna convened a network of national and international human-rights organizations, including the Cyrus R. Vance Center for International Justice (NYC Bar Association) and Servicio Paz y Justicia (SERPAJ). This strategic alliance intervened institutionally through the figure of Amicus Curiae in the case of the child Cielo (Chaco), promoting the correct application of child-protection standards and a gender perspective before the Argentine judicial system.",
  "ph":[]},
]

# per-section location -> mini map (lat, lon, place_es, place_en). Only where a real place exists.
LOC={
 "Apoyo educativo durante la pandemia":(-23.20,-65.95,"Barrancas, Jujuy","Barrancas, Jujuy"),
 "Salud y territorio durante la pandemia":(-23.42,-66.57,"Susques, Jujuy","Susques, Jujuy"),
 "Organización colectiva":(-23.92,-65.47,"Volcán, Jujuy","Volcán, Jujuy"),
 "Santuario de Tres Pozos":(-23.63,-65.75,"Santuario de Tres Pozos, Jujuy","Santuario de Tres Pozos, Jujuy"),
 "Rinconadillas":(-23.66,-65.70,"Rinconadillas, Jujuy","Rinconadillas, Jujuy"),
 "San Francisco de Alfarcito":(-23.83,-65.50,"San Francisco de Alfarcito, Jujuy","San Francisco de Alfarcito, Jujuy"),
 "Sausalito · la cuestión del agua":(-23.55,-65.72,"Sausalito, Jujuy","Sausalito, Jujuy"),
 "Tusaquillas":(-22.95,-65.95,"Tusaquillas, Jujuy","Tusaquillas, Jujuy"),
 "Santa Ana":(-23.33,-65.30,"Santa Ana, Jujuy","Santa Ana, Jujuy"),
 "Barrancas":(-23.20,-65.95,"Barrancas, Jujuy","Barrancas, Jujuy"),
 "Regreso a Rinconadillas y Ojo de Agua":(-23.66,-65.70,"Rinconadillas · Ojo de Agua, Jujuy","Rinconadillas · Ojo de Agua, Jujuy"),
 "Corte y permanencia en Purmamarca":(-23.745,-65.50,"Purmamarca, Jujuy","Purmamarca, Jujuy"),
 "Apoyo ante la represión — Lian Lamas":(-34.60,-58.38,"Buenos Aires","Buenos Aires"),
 "Tercer Malón de la Paz":(-34.60,-58.38,"Buenos Aires","Buenos Aires"),
 "Verónica Chávez y James Cameron":(-34.60,-58.38,"Buenos Aires","Buenos Aires"),
 "En las calles":(-24.185,-65.297,"San Salvador de Jujuy","San Salvador de Jujuy"),
 "Cumbre del Agua":(-24.185,-65.297,"San Salvador de Jujuy","San Salvador de Jujuy"),
 "Cultura en comunidad":(-23.78,-65.45,"Angosto El Pérchel, Jujuy","Angosto El Pérchel, Jujuy"),
 "Activismo ambiental con Carola Rackete y Bojana Novakovic":(-23.62,-65.80,"Salinas Grandes, Jujuy","Salinas Grandes, Jujuy"),
 "Cumbre de Energías Limpias · Parlamento Europeo":(50.8503,4.3517,"Bruselas, Europa","Brussels, Europe"),
 "Alianza con el SERPAJ":(-34.60,-58.38,"Buenos Aires","Buenos Aires"),
 "Jornadas de Plantas Medicinales":(-24.185,-65.297,"San Salvador de Jujuy","San Salvador de Jujuy"),
 "Amicus Curiae en el caso de la niña Cielo":(-27.45,-58.98,"Chaco","Chaco"),
}
# group -> years.json (structure generate_b.py expects)
order=["2020","2021","2022","2023","2024","2025"]  # 2026 added in January
YEARS=[]
for y in order:
    c,les,len_,ies,ien=YMETA[y]
    items=[]
    for m in MILES:
        if m["y"]!=y: continue
        it={"t_es":m["t_es"],"t_en":m["t_en"],"sub_es":"","sub_en":"",
            "text_es":m["x_es"],"text_en":m["x_en"],"photos":m["ph"],"video":m.get("video")}
        L=LOC.get(m["t_es"])
        if L: it["loc"]={"lat":L[0],"lon":L[1],"es":L[2],"en":L[3]}
        items.append(it)
    if y=="2023":  # James Cameron section first on the 2023 page
        items.sort(key=lambda it: 0 if "Cameron" in it["t_es"] else 1)
    YEARS.append({"year":y,"color":c,"label_es":les,"label_en":len_,"intro_es":ies,"intro_en":ien,"items":items})

# Press links attached to the specific action (milestone) they document (keyed by t_es).
LINKS={
 "Cumbre de Energías Limpias · Parlamento Europeo":[
   {"es":"Denunciando en Europa desastres extractivistas en nuestro país",
    "en":"Denouncing our country's extractivist disasters, in Europe",
    "src":"argentina.indymedia.org",
    "url":"https://argentina.indymedia.org/2025/05/23/denunciando-en-europa-desastres-extractivistas-en-nuestro-pais/"}],
}
for y in YEARS:
    for it in y["items"]:
        ls=LINKS.get(it["t_es"])
        if ls: it["links"]=ls

(pathlib.Path(__file__).parent/"years.json").write_text(json.dumps(YEARS,ensure_ascii=False,indent=1))
tot=sum(len(y["items"]) for y in YEARS); ph=sum(len(it["photos"]) for y in YEARS for it in y["items"])
print(f"years.json: {len(YEARS)} years, {tot} chapters, {ph} photos")
for y in YEARS: print(f"  {y['year']}: {len(y['items'])} chapters, {sum(len(it['photos']) for it in y['items'])} photos")
