# App Studio decisions

The durable agreement between learner and AI. Update only agreed decisions and
actual evidence; pending is a valid state. Keep explanations/help in
[LEARNING.md](LEARNING.md), not a second copy here.

## Current stage

- **Current feature:** APP-003.
- **Status:** Three stages implemented and locally checked; synthetic keep decisions made. Actual GitHub state is linked per issue below.
- **Next step:** Review the APP-003 PR and its actual checks/state; deployment is a later agreed scope.
- **Implementation marker:** `studio.json` now declares `implemented_through: 3`; the untouched template starts at 0.

This repository owns application code. Server/proxy changes and production
deployment are outside these three local-development lessons. Prepared helpers
are reusable foundations, not evidence that unfinished routes are implemented.

## APP-001 · Branded homepage

**Scope:** make the neutral FastAPI homepage express one chosen identity with
a simple original SVG mark, coherent copy, navigation and shared style tokens.
Keep account actions honest about their unfinished state.

| Decision | Agreement |
|---|---|
| Visitor and concrete use situation | Students wanting a small change of scene between busy days; unvalidated hypothesis |
| Reused IS117 brand, or name / promise / primary archetype | AI-suggested Field Notes / Small detours. Fresh perspectives. / Explorer, adopted in simulation |
| One visible choice and visitor benefit | Warm paper and uncluttered layout; synthetic learner predicts a break from school and an easier choice |
| Own issue / branch / PR | [Issue #1](https://github.com/kaw393939/is373-app-trial-1027/issues/1), feat/app-001; [PR #2](https://github.com/kaw393939/is373-app-trial-1027/pull/2) |

**Keep when:** the agreed identity is visible and usable at desktop/narrow widths;
full foundation + APP-001 checks pass; AI review and the learner's actual check
interpretation/browser observation/keep reason are recorded; reviewed evidence
and verified GitHub state are linked below.

## APP-002 · Signup, login and logout

**Scope:** add browser forms and REST behavior for member signup, login, a private
dashboard and logout backed by SQLite. Reuse the prepared password/JWT/CSRF/session
helpers; keep data local. New accounts cannot choose their role.

| Decision | Agreement |
|---|---|
| Expected public/private behavior and account flow | Public member-only signup; private API401 before login and200 after; browser redirects to login; logout revokes server session |
| Valid and rejected cases to demonstrate | Valid signup/login; duplicate/invalid signup, wrong credentials, missing CSRF, anonymous/revoked/expired session; restart persistence |
| Own issue / branch / PR | [Issue #3](https://github.com/kaw393939/is373-app-trial-1027/issues/3), feat/app-002; [PR #4](https://github.com/kaw393939/is373-app-trial-1027/pull/4) |

**Keep when:** the agreed forms/API work; duplicate/invalid signup and wrong
credentials are rejected; passwords are hashed; authentication uses validated,
expiring JWTs with protected cookies and CSRF; private requests require a live
session and logout revokes it. Full cumulative checks, AI review, actual learner
contributions and GitHub state are recorded. This is not a production-security certification.

## APP-003 · Server-enforced roles

**Scope:** enforce a small member/admin boundary in the API and browser. Assign
roles only through the trusted local terminal command; use current server-side
permissions, including for an existing session after a role change.

| Visitor | Homepage | Member area | Admin area/API |
|---|---|---|---|
| Anonymous | Allowed | Login required | Login required |
| Member | Allowed | Allowed | Forbidden |
| Admin | Allowed | Allowed | Allowed |

| Decision | Agreement |
|---|---|
| Intended admin-only result | Small admin page and JSON confirmation; current database role enforced on every request |
| Actual allowed/denied request evidence | Anonymous401, member403, admin200 at API; browser login redirect/member denial/admin page; immediate downgrade |
| Own issue / branch / PR | [Issue #5](https://github.com/kaw393939/is373-app-trial-1027/issues/5), feat/app-003; [PR #6](https://github.com/kaw393939/is373-app-trial-1027/pull/6) |

**Keep when:** a direct request cannot bypass the role boundary, role changes
take effect as specified, new signup remains member-only, and full cumulative
checks plus AI review pass. Link the learner's actual interpretation/observation,
reviewed record and verified GitHub result. Hidden navigation alone is insufficient.

## Evidence

Link actual files/checks and the student's own issues/PRs. No fabricated URLs,
customer research or claims that a timestamp proves learning.

| Feature | Files / own issue / PR | Actual checks and learner observations | Kept / GitHub state |
|---|---|---|---|
| APP-001 | [Own issue #1](https://github.com/kaw393939/is373-app-trial-1027/issues/1); app/brand.json, app/templates/home.html, app/static/logo.svg; upstream example adopted | Full Black/Pylint, 93 foundation + 2 homepage + 2 actual Chromium checks passed. Synthetic inspection led to a clearer honest CTA; see LEARNING | Merged [PR #2](https://github.com/kaw393939/is373-app-trial-1027/pull/2), issue closed, selected merge checks passed; historical status exported upstream |
| APP-002 | [Own issue #3](https://github.com/kaw393939/is373-app-trial-1027/issues/3); app/features/accounts.py, signup/login/dashboard templates; upstream example adopted | Full Black/Pylint,98 foundation + 14 contracts + 2 Chromium journeys passed; real manual account journey; synthetic explanations in LEARNING | Merged [PR #4](https://github.com/kaw393939/is373-app-trial-1027/pull/4), issue closed, selected merge checks passed; historical status exported upstream |
| APP-003 | [Own issue #5](https://github.com/kaw393939/is373-app-trial-1027/issues/5); app/features/roles.py, admin/access-denied templates; upstream example adopted | Full Black/Pylint, 98 foundation + 18 contracts + 2 Chromium journeys passed; actual CLI/browser role changes, synthetic explanation in LEARNING | Reviewed keep record before publication; issue/PR hold actual GitHub state |

The instructor's reference branches show possible implementations. They do not
establish this repository's completion or the learner's own reasoning.
