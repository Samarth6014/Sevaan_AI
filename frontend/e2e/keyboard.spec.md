# e2e plan (Playwright + axe-core), owner C
Install later: `npm i -D @playwright/test @axe-core/playwright`. Then automate:
1. Tab from page load: first stop is the skip link; Enter moves focus to #main.
2. Login, create case, accept consent, finish the chat flow using the keyboard only.
3. axe scan of /, /login, /cases, /chat/:id, /review/:id, /admin: no critical violations.
4. Toggle lite mode and record transfer size of first load (target < 200 KB [A]).
Record the manual NVDA/TalkBack pass in reports/a11y_walkthrough.md.
