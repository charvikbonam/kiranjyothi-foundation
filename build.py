#!/usr/bin/env python3
"""
Kiranjyothi Research Foundation - site builder.

Edit source/config.json (phone, email, Telegram...) and the page text below, then run:
    python3 source/build.py
It writes 12 self-contained .html files (CSS + JS inside each) into the site folder.
You can also skip this script and edit the .html files directly.
"""
import json, os, sys
import html as htmllib

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SRC)
cfg = json.load(open(os.path.join(SRC, 'config.json'), encoding='utf-8'))
CSS = open(os.path.join(SRC, 'style.css'), encoding='utf-8').read()
JS = open(os.path.join(SRC, 'app.js'), encoding='utf-8').read()

FILL = lambda t: '<mark class="fill">[FILL: %s]</mark>' % t

SEED = [
 {"id":"20-years-of-service","title":"Two decades of service: Kiranjyothi turns 20","category":"general","date":"2024-07-26",
  "summary":"On 26 July 2024 the Foundation completed 20 years of service to students, farmers and elders.",
  "body":"Since 26 July 2004 the Kiranjyothi Research Foundation has worked quietly for education, skill development and rural welfare.\n\nTwenty years on, the work continues with the same spirit: Live and Let Live.\n\n[Owner: replace this text with the story of the anniversary event, guests who attended and what was announced.]",
  "images":["images/building.jpg"]},
 {"id":"ms-excel-competition-2024","title":"MS Excel Competition for students","category":"academic","date":"2024-03-26",
  "summary":"A one-hour MS Excel competition at the school campus with cash prizes for the top three.",
  "body":"The Kiranjyothi Skill Development Academy held an MS Excel competition on 26 March 2024 at the school campus. The test lasted 1 hour.\n\nPrizes: 1st Rs. 1,500, 2nd Rs. 1,000 and 3rd Rs. 500.\n\n[Owner: add winners' names, number of participants and photos.]",
  "images":["images/computer-lab.jpg"]},
 {"id":"technical-lecture-cloud-devops-2024","title":"Technical lecture: Cloud, AWS, SQL, DevOps and Python","category":"startups","date":"2024-03-26",
  "summary":"An employability session where an experienced IT professional oriented youth on cloud, AWS/SQL, DevOps and Python.",
  "body":"On Sunday 26 March 2024 (9:00 am to 4:00 pm) the Skill Development Academy hosted a technical lecture session titled 'An orientation session on Cloud Transformation, AWS/SQL, DevOps and Python'.\n\nThe resource person is a software professional with more than 8 years of experience who has trained over 2000 students.\n\n[Owner: add the speaker's full name, attendance and photos.]",
  "images":["images/classroom.jpg"]},
 {"id":"interview-gd-workshop-2023","title":"How to Succeed in Interview and Group Discussion","category":"startups","date":"2023-10-22",
  "summary":"A Sunday workshop by an expert team from Hyderabad on interviews, group discussion, resumes and personality development.",
  "body":"On 22 October 2023 (Sunday, 9:00 am to 6:00 pm) a renowned expert team from Hyderabad conducted a full-day programme.\n\nTopics: how to do an interview and group discussion effectively, tips for good communication, resume writing and interview preparation, personality development and career guidance.\n\n[Owner: add photos and feedback from participants.]",
  "images":["images/scholarship-handover.jpg"]},
 {"id":"elders-distribution-programme","title":"Support and distribution programme for the elderly","category":"social","date":"2024-01-15",
  "summary":"Clothes and essentials were distributed to old-aged people of the village.",
  "body":"The Foundation regularly distributes clothes and accessories to elderly people, honouring them with respect.\n\n[Owner: add the exact date, place and number of beneficiaries, then replace this note.]",
  "images":["images/elderly-distribution.jpg"]},
 {"id":"founder-with-children","title":"Our founder with the children of the village","category":"academic","date":"2004-12-01",
  "summary":"From the early years: books, notebooks and encouragement for children who needed them most.",
  "body":"From the very beginning, the Foundation's family has stood beside children and parents who could not afford school supplies.\n\n[Owner: replace this with the story behind this photograph.]",
  "images":["images/founder-with-children.jpg"]}
]

# ---------- chrome ----------
LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><g stroke="#f5b400" stroke-width="3" stroke-linecap="round"><path d="M32 4v8M15 9l4 7M49 9l-4 7M5 22l8 3M59 22l-8 3"/></g>'
        '<circle cx="32" cy="27" r="9" fill="#f5b400"/><path d="M6 34c10-3 20-1 26 5 6-6 16-8 26-5v20c-10-3-20-1-26 5-6-6-16-8-26-5z" fill="#0b3a8c"/>'
        '<path d="M32 39v20" stroke="#fff" stroke-width="2"/></svg>')
TG_ICON = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.9 3.6 2.7 11c-1.3.5-1.3 1.3-.2 1.6l4.9 1.5 1.9 5.7c.2.6.4.8.9.8.4 0 .6-.2.9-.5l2.3-2.2 4.8 3.5c.9.5 1.5.2 1.7-.8l3.2-15.1c.3-1.3-.5-1.9-1.7-1.4zM8.6 13.5l9.9-6.2c.5-.3.9-.1.5.2l-8.1 7.3-.3 3.4-2-4.7z"/></svg>'

INIT = [
 ('academic.html','🎓','Academic Initiatives'),
 ('social-service.html','🤝','Social Service Initiatives'),
 ('spiritual.html','🕉️','Spiritual Initiatives'),
 ('agricultural.html','🌾','Agricultural Initiatives'),
 ('family-counselling.html','👨‍👩‍👧','Family & Child Counselling'),
 ('startups-internships.html','🚀','Startups & Internships'),
]

def header(active):
    dd = ''.join('<a href="%s">%s %s</a>' % (u, i, t) for u, i, t in INIT)
    on = lambda f: ' class="active"' if active == f else ''
    init_on = ' active' if active in [u for u, _, _ in INIT] else ''
    return ('<div class="strip"><div class="wrap"><span>Regd. No. %%regNo%% · Dated %%regDate%%</span>'
            '<span>📞 <a href="tel:%%phoneTel%%">%%phone%%</a> &nbsp;·&nbsp; ✈️ <a data-tg href="#">Telegram</a></span></div></div>'
            '<header class="site"><div class="wrap"><a class="brand" href="index.html">' + LOGO +
            '<span><b>Kiranjyothi</b><small>Research Foundation</small></span></a>'
            '<div class="hd-right"><button class="lang-btn" id="langBtn" type="button">తెలుగు</button><button class="burger" aria-label="Menu" aria-expanded="false">☰</button></div>'
            '<nav class="main"><a href="index.html"' + on('index.html') + '>Home</a><a href="about.html"' + on('about.html') + '>About Us</a>'
            '<div class="dd' + init_on + '"><button type="button">Our Initiatives ▾</button><div class="menu">' + dd + '</div></div>'
            '<a href="achievements.html"' + on('achievements.html') + '>Achievements</a><a href="contact.html"' + on('contact.html') + '>Contact Us</a></nav></div></header>')

def footer():
    links = ''.join('<a href="%s">%s</a>' % (u, t) for u, _, t in INIT)
    return ('<footer class="site"><div class="wrap"><div class="cols"><div><div class="brand" style="color:#fff;margin-bottom:14px">' + LOGO +
            '<span><b style="font-size:1.35rem">Kiranjyothi</b><small>Research Foundation</small></span></div>'
            '<p>%%tagline%%. Serving students, farmers, families and elders since %%founded%%.</p><p class="te" style="margin-top:10px">%%orgNameTe%%</p></div>'
            '<div><h4>Explore</h4><a href="index.html">Home</a><a href="about.html">About Us</a><a href="achievements.html">Achievements</a><a href="contact.html">Contact Us</a></div>'
            '<div><h4>Initiatives</h4>' + links + '</div>'
            '<div><h4>Reach us</h4><p>📍 %%address%%</p><p>📞 <a style="display:inline" href="tel:%%phoneTel%%">%%phone%%</a></p><p>✉️ <a style="display:inline" href="mailto:%%email%%">%%email%%</a></p>'
            '<p><a data-tg href="#">✈️ Message on Telegram</a></p></div></div>'
            '<div class="legal"><span>© <span id="yr"></span> %%orgName%% · Regd. No. %%regNo%%</span><span><em>Together for a Brighter Future…</em> · <a style="display:inline;opacity:.5" href="admin.html">Admin</a></span></div></div></footer>'
            '<a class="tg-float" data-tg href="#" aria-label="Message us on Telegram">' + TG_ICON + '<span>Chat on Telegram</span></a>'
            '<div class="lightbox" role="dialog" aria-label="Image viewer"></div>'
            '<script>document.getElementById("yr").textContent=new Date().getFullYear()</script>')

def page(fname, title, desc, body, active=None, extra_head='', noindex=False):
    html = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>' + title + ' — %%orgName%%</title><meta name="description" content="' + desc + '">'
            + ('<meta name="robots" content="noindex,nofollow">' if noindex else '') +
            '<link rel="icon" href="data:image/svg+xml,' + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%230b3a8c'/%3E%3Ccircle cx='32' cy='28' r='10' fill='%23f5b400'/%3E%3C/svg%3E" + '">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;1,9..144,600&family=Noto+Sans+Telugu:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
            '<style>\n' + CSS + '\n</style></head><body>\n' + header(active) + '\n<main>' + body + '</main>\n' + footer() +
            '\n<script>window.KRF_CONFIG=' + json.dumps(cfg_public, ensure_ascii=False) + ';window.KRF_SEED=' + json.dumps(SEED, ensure_ascii=False) + ';</script>\n'
            '<script>\n' + JS + '\n</script></body></html>')
    for k, v in cfg.items():
        html = html.replace('%%' + k + '%%', str(v))
    html = html.replace('%%phoneTel%%', ''.join(c for c in cfg['phone'] if c.isdigit() or c == '+'))
    open(os.path.join(OUT, fname), 'w', encoding='utf-8').write(html)
    print('wrote', fname)

cfg_public = {k: cfg[k] for k in ['orgName', 'founded', 'telegramUsername', 'telegramBotToken', 'telegramChatId', 'telegramProxyUrl', 'adminPassword']}

def hero(title, lead, img, eyebrow, crumb=None, small=True, ctas='', te_title=None, te_lead=None):
    return ('<section class="hero%s"><div class="bg" style="background-image:url(%s)"></div><div class="wrap">' % (' small' if small else '', img)
            + ('<div class="crumbs"><a href="index.html">Home</a> / %s</div>' % crumb if crumb else '')
            + '<span class="eyebrow">%s</span><h1%s>%s</h1><p class="lead"%s>%s</p>%s</div></section>' % (eyebrow, ' data-te="%s"' % htmllib.escape(te_title) if te_title else '', title, ' data-te="%s"' % htmllib.escape(te_lead) if te_lead else '', lead, ctas))

def gallery(items):
    return '<div class="gallery">' + ''.join('<figure class="rv"><img loading="lazy" src="%s" alt="%s"><figcaption>%s</figcaption></figure>' % (s, c, c) for s, c in items) + '</div>'

CTA = ('<section class="band"><div class="wrap" style="text-align:center;display:grid;gap:18px;justify-items:center"><h2>Be part of the change</h2>'
       '<p class="lead">Volunteer, donate or simply say hello. Message us on Telegram and we will reply personally.</p>'
       '<div style="display:flex;gap:14px;flex-wrap:wrap;justify-content:center"><a class="btn tg" data-tg href="#">✈️ Message on Telegram</a><a class="btn primary" href="contact.html">Contact us</a></div></div></section>')

def latest(cat, title='Latest achievements'):
    return ('<section><div class="wrap"><div class="sec-head"><span class="eyebrow">Recent work</span><h2>%s</h2></div>'
            '<div class="grid g3" data-achievements data-cat="%s" data-limit="3"></div>'
            '<p style="margin-top:26px"><a class="btn blue" href="achievements.html">See all achievements →</a></p></div></section>') % (title, cat)

def cat_page(fname, title, te, icon, cat, img, lead, intro, items, gal, quote, qsrc):
    body = hero(title, lead, img, '%s %s' % (icon, te), crumb=title)
    body += ('<section><div class="wrap split"><div class="essay rv">' + ''.join('<p>%s</p>' % p for p in intro) + '</div>'
             '<div class="photo rv"><img src="%s" alt="%s"><span class="tag">%s</span></div></div></section>' % (gal[0][0], title, gal[0][1]))
    body += ('<section class="soft"><div class="wrap"><div class="sec-head center"><span class="eyebrow">What we do</span><h2>Our work in %s</h2></div><div class="grid g3">' % title.split(' ')[0].lower()
             + ''.join('<div class="card rv"><div class="ico">%s</div><h3>%s</h3><p>%s</p></div>' % i for i in items) + '</div></div></section>')
    body += '<section class="band"><div class="wrap"><blockquote class="quote rv">“%s”<small>%s</small></blockquote></div></section>' % (quote, qsrc)
    if len(gal) > 1:
        body += '<section><div class="wrap"><div class="sec-head"><span class="eyebrow">Gallery</span><h2>Moments from the field</h2></div>' + gallery(gal) + '</div></section>'
    body += latest(cat) + CTA
    page(fname, title, lead, body, active=fname)

# ---------- HOME ----------
home = hero('Lighting the way for <em>villages</em>, one child at a time.',
            'For over %%founded%% … for two decades the Kiranjyothi Research Foundation has stood for education, employment skills, spiritual care and rural development.'.replace('For over %%founded%% … for', 'For'),
            'images/building.jpg', 'Since %%founded%% · For Academic &amp; Rural Development', small=False, te_title='గ్రామాలకు <em>వెలుగు</em>, ప్రతి బిడ్డకు ఒక కొత్త దారి.', te_lead='రెండు దశాబ్దాలుగా కిరణ్‌జ్యోతి రీసర్చ్ ఫౌండేషన్ విద్య, ఉపాధి నైపుణ్యాలు, ఆధ్యాత్మిక సంరక్షణ మరియు గ్రామీణాభివృద్ధికి అంకితమై ఉంది.',
            ctas='<div class="ctas"><a class="btn primary" href="about.html">Our story</a><a class="btn ghost" href="achievements.html">See achievements</a><a class="btn tg" data-tg href="#">✈️ Telegram</a></div>')
home += ('<section class="stats"><div class="wrap"><div class="grid"><div class="stat"><b data-years>22</b><span>Years of service</span></div>'
         '<div class="stat"><b data-count="6">6</b><span>Focus initiatives</span></div><div class="stat"><b data-count="6">6</b><span>Computer courses</span></div>'
         '<div class="stat"><b>%%founded%%</b><span>Year of registration</span></div></div></div></section>')
home += ('<section><div class="wrap split"><div class="essay rv"><span class="eyebrow">Who we are</span><h2 style="margin:12px 0 20px">A light kindled in gratitude</h2>'
         '<p>The Kiranjyothi Research Foundation was born on 26 July 2004 from a simple idea: that those who have been lifted by their village and their parents must lift others in turn. It began as a family’s tribute to their parents and grew into a movement for education, skills and welfare.</p>'
         '<p>Guided by the principle of <em>“Live and Let Live”</em> and inspired by Swami Vivekananda, we put our energy where it matters most: a child with no notebook, a youth with no job-ready skill, a farmer with no modern know-how and an elder with no company.</p>'
         '<a class="btn blue" href="about.html">Read our full story →</a></div>'
         '<div class="photo rv"><img src="images/founder-with-children.jpg" alt="Founder with village children"><span class="tag">Where it began</span></div></div></section>')
focus = [('academic.html','Academic Initiatives','విద్యా కార్యక్రమాలు','Scholarships, books, computers and career guidance for students.','linear-gradient(135deg,#0b3a8c,#1f6fe0)','01'),
         ('social-service.html','Social Service','సామాజిక సేవ','Welfare for elders, the needy and the whole village.','linear-gradient(135deg,#1e9e5a,#0f6e3a)','02'),
         ('spiritual.html','Spiritual Initiatives','ఆధ్యాత్మిక కార్యక్రమాలు','Peace, satsang and companionship for senior citizens.','linear-gradient(135deg,#f28c00,#c25f00)','03'),
         ('agricultural.html','Agricultural Initiatives','వ్యవసాయ కార్యక్రమాలు','Modern farming knowledge and cottage-industry support.','linear-gradient(135deg,#4a8f1d,#2c5f0d)','04'),
         ('family-counselling.html','Family &amp; Child Counselling','కుటుంబ మరియు బాల సలహా','Listening, guidance and protection for families and children.','linear-gradient(135deg,#8e44ad,#5b2a73)','05'),
         ('startups-internships.html','Startups &amp; Internships','ఉద్యోగ నైపుణ్యాలు','Employability skills, mock interviews and first jobs.','linear-gradient(135deg,#0b3a8c,#071f54)','06')]
home += ('<section class="soft"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Our focus areas</span><h2>Six initiatives, one mission</h2>'
         '<p class="lead">Every programme comes back to the same promise: Education, Empowerment, Progress.</p></div><div class="grid g3">'
         + ''.join('<a class="card focus rv" data-n="%s" style="--c:%s" href="%s"><h3>%s</h3><span class="te">%s</span><p>%s</p><span class="more">Explore →</span></a>' % (n, c, u, t, te, d) for u, t, te, d, c, n in focus)
         + '</div></div></section>')
home += ('<section class="band"><div class="wrap"><blockquote class="quote rv">“Together for a Brighter Future”<small>— the Kiranjyothi family</small></blockquote></div></section>')
home += ('<section><div class="wrap"><div class="sec-head"><span class="eyebrow">Our work in action</span><h2>Latest achievements</h2>'
         '<p class="lead">Every achievement has its own page. Tap one to read the full story.</p></div><div class="grid g3" data-achievements data-limit="3"></div>'
         '<p style="margin-top:26px"><a class="btn blue" href="achievements.html">All achievements →</a></p></div></section>')
home += ('<section class="soft"><div class="wrap"><div class="sec-head"><span class="eyebrow">Gallery</span><h2>Our campus &amp; community</h2></div>'
         + gallery([('images/building.jpg', 'Foundation building'), ('images/classroom.jpg', 'Students learning together'), ('images/library.jpg', 'Library and competitive-exam corner'),
                    ('images/computer-lab.jpg', 'Computer education lab'), ('images/scholarship-handover.jpg', 'Support handed over'), ('images/elderly-distribution.jpg', 'Care for elders')])
         + '</div></section>')
home += CTA
page('index.html', 'Home', 'Kiranjyothi Research Foundation: academic and rural development since 2004.', home, 'index.html')

# ---------- ABOUT ----------
ab = hero('About Kiranjyothi', 'A foundation built on gratitude, service and the belief that no one should be left behind.', 'images/library.jpg', 'About us', crumb='About Us')
ab += ('<section><div class="wrap split"><div class="essay rv"><span class="eyebrow">Our story</span><h2 style="margin:12px 0 20px">A light kindled in gratitude</h2>'
       '<p>“Kiran” means a ray of light and “jyothi” means a flame. Together they describe what this foundation has tried to be for more than twenty years: a small, steady light in the lives of village children, young job-seekers, farmers and elders.</p>'
       '<p>On 26 July 2004 the Kiranjyothi Research Foundation was registered (Regd. No. 8/BK4/2004) with a simple resolve: to serve through education and rural development, as an expression of gratitude to the parents who raised its founding family and to the community that shaped them.</p>'
       '<p>The founder, ' + FILL("founder's full name") + ', was born into a farming family and grew up believing in the saying <em>“Krushito nasti durbhiksham”</em>: where there is hard work on the land, there is no famine. He took to heart the life-principle of <em>“Live and Let Live”</em> from childhood, found inspiration in the teachings of Swami Vivekananda, and decided to build development work in his own village in memory of his parents.</p>'
       '<p>What started with notebooks, textbooks and scholarships for children who could not afford them has grown steadily. Today the Foundation runs a library, a computer education centre and a Skill Development Academy that offers employability training, technical lectures, MS Excel contests, mock interviews and job notifications. It also reaches out to old-aged people with clothes and spiritual programmes, and to farmers with modern agricultural knowledge.</p>'
       '<p>The Foundation’s story is not about buildings or budgets. It is about the child who now reads confidently, the youth who cleared an interview, the farmer who learned a better method and the elder who no longer feels forgotten. Everything we do is summed up in one line we are proud to carry: <strong>Together for a Brighter Future.</strong></p></div>'
       '<div><div class="photo rv"><img src="images/about-poster.jpg" alt="Foundation profile in Telugu"></div><p class="note" style="margin-top:10px">Our profile in Telugu (సంస్థ ఆవిర్భావం).</p></div></div></section>')
ab += ('<section class="soft"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Our aims</span><h2>Why we exist</h2></div><div class="grid g2">'
       '<ul class="ticks" style="grid-column:1/-1;grid-template-columns:repeat(auto-fit,minmax(320px,1fr))">'
       '<li>Encourage students and build their skills through education and scholarships.</li><li>Provide education, health and social service in rural areas.</li>'
       '<li>Create employment opportunities and improve employability skills of youth.</li><li>Promote self-reliance and value-based education.</li>'
       '<li>Run welfare programmes for the Foundation’s own development and for the old-aged.</li><li>Protect the environment and promote greenery.</li>'
       '<li>Support cottage industries and bring modern agricultural methods to farmers.</li><li>Grow the habit of reading through a village library.</li></ul></div></div></section>')
ab += ('<section><div class="wrap"><div class="sec-head"><span class="eyebrow">Our journey</span><h2>Milestones</h2></div><div class="timeline">'
       '<div class="tl rv"><b>2004</b><p>The Foundation is established on 26 July and registered as 8/BK4/2004.</p></div>'
       '<div class="tl rv"><b>2004–05</b><p>First premises and first programmes: books and notebooks for children and aid for school and college fees.</p></div>'
       '<div class="tl rv"><b>2023–24</b><p>Skill Development Academy programmes: interview and group-discussion workshops, technical lectures, MS Excel competition.</p></div>'
       '<div class="tl rv"><b>2024</b><p>Two decades of service completed on 26 July 2024.</p></div>'
       '<div class="tl rv"><b>Today</b><p>Library, computer education centre and six initiatives running. ' + FILL('add newer milestones') + '</p></div></div></div></section>')
ab += ('<section class="soft"><div class="wrap"><div class="sec-head"><span class="eyebrow">Gallery</span><h2>Inside the Foundation</h2></div>'
       + gallery([('images/building.jpg', 'Our building'), ('images/library.jpg', 'Library'), ('images/computer-lab.jpg', 'Computer lab'), ('images/classroom.jpg', 'Classroom session'), ('images/brochure.jpg', 'Foundation brochure')])
       + '</div></section>')
ab += ('<section><div class="wrap"><div class="sec-head"><span class="eyebrow">Our people</span><h2>Leadership &amp; team</h2></div><div class="grid g3">'
       + ''.join('<div class="card rv"><div class="ico">👤</div><h3>%s</h3><p>%s</p></div>' % (FILL('Name'), FILL('Role, e.g. Founder / President / Secretary')) for _ in range(3))
       + '</div></div></section>')
ab += CTA
page('about.html', 'About Us', 'The story, aims and journey of the Kiranjyothi Research Foundation.', ab, 'about.html')

# ---------- CATEGORY PAGES ----------
cat_page('academic.html', 'Academic Initiatives', 'విద్యా కార్యక్రమాలు', '🎓', 'academic', 'images/classroom.jpg',
 'Helping every child stay in school, grow in confidence and reach for competitive exams and careers.',
 ['Education is where our work began. From the first notebooks handed to children in 2004 to today’s library and computer lab, the Foundation has made sure that money is never the reason a bright child drops out.',
  'We reward merit, support fees, give out textbooks and run career counselling so students know their options. ' + FILL('add numbers or special programmes')],
 [('🏅', 'Scholarships to poor students', 'Financial help for students from low-income families.'),
  ('🇮🇳', 'Independence Day scholarships', 'Scholarships for merit-rank students, awarded on Independence Day.'),
  ('💰', 'School & college fee support', 'Direct help towards fees so studies are never interrupted.'),
  ('📚', 'Textbooks & notebooks', 'Free books and stationery for children who need them.'),
  ('🧭', 'Career counselling & guidance', 'Guidance on skills, knowledge and a competitive spirit.'),
  ('💻', 'Laptops & computers', 'Computers and laptops for needy students, plus a computer lab with Basic Computer, MS Office, Typing, Internet, Tally and Graphic Design courses.'),
  ('🏆', 'Merit appreciation', 'Recognising bright students to inspire others.'),
  ('📖', 'Library & competitive exams corner', 'A village library with shelves for competitive-exam preparation.'),
  ('⌨️', 'MS Excel competition', 'Contests with cash prizes that make learning exciting.')],
 [('images/library.jpg', 'Library & competitive exams corner'), ('images/computer-lab.jpg', 'Computer education lab'), ('images/classroom.jpg', 'Students in a session'), ('images/scholarship-handover.jpg', 'Support handed over')],
 'Knowledge builds a better tomorrow.', 'Wall message in our classroom')

cat_page('social-service.html', 'Social Service Initiatives', 'సామాజిక సేవ', '🤝', 'social', 'images/elderly-distribution.jpg',
 'Standing beside the elderly, the needy and the whole village in everyday life and in hard times.',
 ['Service to society is the second pillar of the Foundation. We believe a village is only as strong as its weakest member, so we reach out with practical help and visible respect.',
  'Our social service work includes distribution of clothes and essentials to elderly people, community welfare, and environmental care through greenery drives. ' + FILL('add health camps, relief work, tree-plantation drives')],
 [('👵', 'Clothes & accessories for the elderly', 'Distribution of clothes and essentials to old-aged people.'),
  ('🏘️', 'Community welfare', 'Village-level welfare programmes for families in need.'),
  ('🌳', 'Environment & greenery', 'Protecting the environment and promoting tree plantation.'),
  ('🩺', 'Medical support', 'Health support and awareness for the needy. ' + FILL('camp details')),
  ('🍲', 'Relief in emergencies', FILL('describe relief work')),
  ('🙌', 'Volunteer network', 'Young volunteers who give time to community work.')],
 [('images/elderly-distribution.jpg', 'Distribution for the elderly'), ('images/building.jpg', 'Foundation building'), ('images/scholarship-handover.jpg', 'Helping hands')],
 'Live and Let Live.', 'The Foundation’s guiding principle')

cat_page('spiritual.html', 'Spiritual Initiatives', 'ఆధ్యాత్మిక కార్యక్రమాలు', '🕉️', 'spiritual', 'images/building.jpg',
 'Peace of mind, companionship and dignity for our senior citizens.',
 ['The Foundation draws its spiritual strength from the teachings of Swami Vivekananda: that service to people is service to God. For the older members of our community, we organise spiritual gatherings where they feel valued, heard and at peace.',
  'These programmes also give young people the chance to sit with and learn from their elders. ' + FILL('add details: bhajans, satsang, pravachanam, festival celebrations')],
 [('🙏', 'Spiritual programmes for old-aged people', 'Regular gatherings for prayer, discourse and fellowship.'),
  ('📿', 'Satsang & bhajans', FILL('schedule')),
  ('🎉', 'Festival celebrations', FILL('festivals celebrated')),
  ('📖', 'Values from Swami Vivekananda', 'Talks and reading that nurture character and service.'),
  ('🩺', 'Medical & spiritual care', 'Health checks and companionship together for our elders.'),
  ('🧘', 'Meditation & wellbeing', FILL('yoga/meditation sessions'))],
 [('images/building.jpg', 'Foundation building'), ('images/elderly-distribution.jpg', 'With our elders')],
 'Arise, awake and stop not till the goal is reached.', 'Swami Vivekananda')

cat_page('agricultural.html', 'Agricultural Initiatives', 'వ్యవసాయ కార్యక్రమాలు', '🌾', 'agri', 'images/classroom.jpg',
 'Bringing modern, sustainable farming know-how and cottage-industry support to the farmers who feed us.',
 ['Our founder grew up in a farming family and lives by the saying “Krushito nasti durbhiksham”, meaning there is no famine where there is farming. That belief drives our agricultural work.',
  'We teach farmers modern, scientific methods and help rural families start cottage industries so that the village earns from many sources. ' + FILL('add training camps, demonstrations, tie-ups')],
 [('🧑‍🌾', 'Modern farming awareness', 'Training farmers in modern agricultural technology.'),
  ('🌱', 'Cottage industries support', 'Helping rural families start and run small industries.'),
  ('💧', 'Water & soil care', FILL('details')),
  ('🧪', 'Research & innovation', 'Field-level research for rural development.'),
  ('🤝', 'Farmer meetings', FILL('details')),
  ('📈', 'Market linkages', FILL('details'))],
 [('images/classroom.jpg', 'Community learning session'), ('images/brochure.jpg', 'Foundation brochure')],
 'Krushito nasti durbhiksham.', 'Where there is farming, there is no famine')

cat_page('family-counselling.html', 'Family & Child Counselling', 'కుటుంబ మరియు బాల సలహా', '👨‍👩‍👧', 'family', 'images/founder-with-children.jpg',
 'A safe, caring place for families and children to be heard, guided and protected.',
 ['Strong families make strong villages. Our counselling initiative offers a listening ear and practical guidance to parents, teenagers and children who are facing stress, study pressure or difficult situations at home.',
  'Children’s protection and wellbeing are at the heart of the Foundation’s work. ' + FILL('add counsellor name(s), qualifications, timings and helpline')],
 [('👂', 'Family counselling', 'Guidance for parents and couples in difficult times.'),
  ('🧒', 'Child counselling & protection', 'A safe space for children and awareness about their rights.'),
  ('📚', 'Study & exam stress', 'Support for students under pressure.'),
  ('🧭', 'Career guidance', 'Helping young people choose the right path.'),
  ('👪', 'Parenting workshops', FILL('details')),
  ('📞', 'Helpline', FILL('phone / Telegram counselling hours'))],
 [('images/founder-with-children.jpg', 'Children of the village')],
 'Every child deserves to be heard.', 'Our promise')

cat_page('startups-internships.html', 'Startups & Internships', 'ఉద్యోగ నైపుణ్యాలు', '🚀', 'startups', 'images/computer-lab.jpg',
 'The Kiranjyothi Skill Development Academy prepares rural youth for jobs, internships and their own start-ups.',
 ['Unemployment is one of the biggest challenges for rural youth. Our Skill Development Academy bridges the gap between a degree and a job through practical, employability-focused training.',
  'The Academy runs technical lecture sessions on cloud, AWS, SQL, DevOps and Python, interview and group-discussion workshops, resume-writing sessions, mock interviews and job-vacancy notifications. ' + FILL('add internship partners and start-up mentoring')],
 [('💼', 'Employability skills', 'Communication, personality development and career guidance.'),
  ('🎤', 'Mock interviews', 'Practice interviews with feedback from experts.'),
  ('📝', 'Resume writing workshops', 'Build a professional resume that gets noticed.'),
  ('👥', 'Group discussions', 'Confidence-building group-discussion sessions.'),
  ('☁️', 'Technical lectures', 'Cloud, AWS/SQL, DevOps and Python orientation by industry professionals.'),
  ('📢', 'Job vacancy notifications', 'Timely updates on openings for our youth.'),
  ('🏢', 'Internships', 'Internship opportunities through workshops and partners. ' + FILL('partners')),
  ('💡', 'Start-up mentoring', FILL('mentoring details')),
  ('🏭', 'Cottage industries', 'Guidance to turn skills into small enterprises.')],
 [('images/computer-lab.jpg', 'Computer lab'), ('images/classroom.jpg', 'Workshop session'), ('images/scholarship-handover.jpg', 'Programme in progress')],
 'Small steps, big dreams.', 'Wall message in our computer lab')

# ---------- ACHIEVEMENTS ----------
ac = hero('Achievements', 'Every milestone, event and success story. Tap any card to open its own page.', 'images/classroom.jpg', 'Our impact', crumb='Achievements')
ac += ('<section><div class="wrap"><div class="filters" id="chips"></div><label style="max-width:420px;margin-bottom:28px">Search<input id="achSearch" type="search" placeholder="Search achievements…"></label>'
       '<div class="grid g3" id="achList"></div></div></section>' + CTA)
page('achievements.html', 'Achievements', 'All achievements of the Kiranjyothi Research Foundation.', ac, 'achievements.html')

# ---------- SINGLE ACHIEVEMENT ----------
page('achievement.html', 'Achievement', 'An achievement of the Kiranjyothi Research Foundation.',
     '<section style="padding-top:50px"><div class="wrap"><article class="article" id="article"><div class="empty">Loading…</div></article></div></section>' + CTA, 'achievements.html')

# ---------- CONTACT ----------
ct = hero('Contact Us', 'We would love to hear from you. Message us on Telegram or use the form below.', 'images/building.jpg', 'Get in touch', crumb='Contact Us')
topics = ''.join('<option>%s</option>' % t for t in ['General enquiry', 'Scholarship / education support', 'Skill development / internship', 'Volunteer with us', 'Donate', 'Family / child counselling', 'Agriculture'])
ct += ('<section><div class="wrap split"><div><span class="eyebrow">Reach us</span><h2 style="margin:12px 0 24px">Let’s talk</h2><div class="infobox">'
       '<div><span class="ico">📍</span><span><b>Address</b><br>%%address%%</span></div>'
       '<div><span class="ico">📞</span><span><b>Phone</b><br><a href="tel:%%phoneTel%%">%%phone%%</a></span></div>'
       '<div><span class="ico">✉️</span><span><b>Email</b><br><a href="mailto:%%email%%">%%email%%</a></span></div>'
       '<div><span class="ico">✈️</span><span><b>Telegram</b><br><a data-tg href="#">@%%telegramUsername%%</a></span></div>'
       '<div><span class="ico">🕘</span><span><b>Office hours</b><br>%%hours%%</span></div></div>'
       '<a class="btn tg" style="margin-top:26px" data-tg href="#">✈️ Open Telegram chat</a></div>'
       '<div class="card"><h3 style="margin-bottom:16px">Send us a message</h3><form class="f" id="contactForm">'
       '<label>Your name<input name="name" required></label><label>Phone / Telegram<input name="phone" required></label>'
       '<label>Topic<select name="topic">' + topics + '</select></label><label>Message<textarea name="message" required></textarea></label>'
       '<button class="btn blue" type="submit">Send via Telegram</button><div class="status" id="cfStatus"></div>'
       '<p class="note">Your message is delivered straight to the Foundation’s Telegram.</p></form></div></div></section>')
ct += ('<section class="soft"><div class="wrap"><div class="sec-head"><span class="eyebrow">Find us</span><h2>Our location</h2></div>'
       + ('<iframe src="%%mapEmbedUrl%%" style="border:0;width:100%;height:420px;border-radius:24px" loading="lazy" allowfullscreen></iframe>' if cfg.get('mapEmbedUrl') else
          '<div class="empty" style="grid-column:auto">Map not added yet. In Google Maps choose Share → Embed a map, copy the link inside src="…" and put it in <code>mapEmbedUrl</code> in config.json.</div>')
       + '</div></section>')
page('contact.html', 'Contact Us', 'Contact the Kiranjyothi Research Foundation.', ct, 'contact.html')

# ---------- ADMIN ----------
ad = ('<section style="padding:50px 0 90px;min-height:70vh"><div class="wrap">'
      '<div id="login" class="card" style="max-width:440px;margin:40px auto"><h2 style="font-size:1.8rem;margin-bottom:6px">Admin login</h2><p class="note" style="margin-bottom:18px">For the Foundation’s staff only.</p>'
      '<form class="f" id="loginForm"><label>Password<input type="password" id="pw" required autocomplete="current-password"></label><button class="btn blue" type="submit">Log in</button><div class="status" id="loginStatus"></div></form></div>'
      '<div id="adminApp" style="display:none"><div class="admin-bar"><div><span class="eyebrow">Admin panel</span><h1 style="font-size:2.3rem">Manage achievements</h1></div>'
      '<button class="mini" id="logout">Log out</button></div>'
      '<div class="card" style="margin-bottom:28px"><p><b>How publishing works:</b> new achievements appear instantly <b>in this browser</b>. To show them to every visitor, press <b>Export</b>, then replace the file <code>data/achievements.json</code> on your website with the downloaded one.</p></div>'
      '<div class="split" style="align-items:start;gap:32px"><div class="card"><h3 id="formTitle" style="margin-bottom:16px">Add a new achievement</h3>'
      '<form class="f" id="achForm"><label>Title<input name="title_" required maxlength="120"></label>'
      '<div class="grid g2" style="gap:14px"><label>Category<select name="cat" id="f_cat"></select></label><label>Date<input type="date" name="date" id="f_date" required></label></div>'
      '<label>Short summary (shown on the card)<textarea name="summary" style="min-height:80px" required maxlength="220"></textarea></label>'
      '<label>Full story (leave a blank line between paragraphs)<textarea name="body" style="min-height:200px" required></textarea></label>'
      '<label>Photos (the first is the cover)<input type="file" id="f_img" accept="image/*" multiple></label><div class="thumbs" id="thumbs"></div>'
      '<div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn blue" type="submit">Save achievement</button><button class="btn" type="button" id="cancelEdit" style="display:none;border-color:var(--line)">Cancel</button></div>'
      '<div class="status" id="saveStatus"></div></form></div>'
      '<div class="card"><h3>All achievements (<span id="count">0</span>)</h3><div id="list" style="margin:10px 0 20px"></div>'
      '<div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn blue" id="export" type="button">⬇ Export achievements.json</button>'
      '<label class="mini" style="display:inline-flex;cursor:pointer;color:var(--ink)">⬆ Import<input type="file" id="import" accept=".json" style="display:none"></label>'
      '<button class="mini danger" id="resetPub" type="button">Reset to published</button></div></div></div></div></div></section>')
page('admin.html', 'Admin', 'Admin panel', ad, None, noindex=True)

# data file the owner replaces on the server
json.dump(SEED, open(os.path.join(OUT, 'data', 'achievements.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done')
