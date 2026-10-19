KIRANJYOTHI RESEARCH FOUNDATION - WEBSITE
=========================================
Open index.html in a browser to preview. Upload the whole folder to any web host to publish.

PAGES (each is ONE html file with its CSS + JS inside)
  index.html, about.html, academic.html, social-service.html, spiritual.html,
  agricultural.html, family-counselling.html, startups-internships.html,
  achievements.html (list), achievement.html (opens one achievement: ?id=...),
  contact.html, admin.html (owner login)

FILL IN YOUR DETAILS
  Yellow "[FILL: ...]" tags mark text you must replace with your LibreOffice content.
  Two ways to edit:
   A) Edit the .html files directly (search for FILL), or
   B) Edit source/config.json (phone, email, address, Telegram) and the text in
      source/build.py, then run:  python3 source/build.py   (rebuilds all pages)

TELEGRAM
  1. Chat button: set telegramUsername in config.json.
  2. Contact form -> your Telegram: create a bot with @BotFather, put the token in
     telegramBotToken, send your bot a message, and put your chat id in telegramChatId
     (find it at https://api.telegram.org/bot<TOKEN>/getUpdates).
  NOTE: a token in a website is visible to anyone who views the source. For a public site
  use telegramProxyUrl (a tiny Cloudflare Worker / server that holds the token) instead.

ADMIN PANEL (admin.html, password in config.json -> adminPassword)
  Add / edit / delete achievements with photos. Each one gets its own page automatically.
  Achievements save in the browser you use. To publish to ALL visitors:
  click "Export achievements.json" and replace data/achievements.json on your host.
  The password is checked in the browser, so it is a convenience lock, not real security.

IMAGES: images/ folder. Replace files with real photos using the same names.
