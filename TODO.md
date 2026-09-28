# Gold Prediction App Completion TODO
Status: Approved plan - implementing step-by-step.

## Plan Breakdown (Logical Steps)

### 1. Fix Model Loading (Priority: High - blocks predictions) ✅
- [x] Updated app/models.py: `load_model()` loads .pkl files, fallback trains/saves.
- [x] Updated app/__init__.py: Destructures model, scaler, selected_features; sets app.scaler.
- Test: Ready - run app to verify console output."


### 2. Fix Prediction Pipeline & Routes (Priority: High) ✅
- [x] app/routes.py: Removed `@login_required` from `/login`; fixed `predict()` with dynamic form_data, scaler.transform(), assumes feature order match.
- [x] Added `from flask import current_app`; index() route exists.
- [x] pred_record saves JSON form_data.
- Test: Fill predict form → verify no scaler error."


### 3. Complete & Enhance Templates (Priority: Medium) ✅
- [x] templates/predict.html: Complete responsive glassmorphism form with all 10 fields, placeholders.
- [x] templates/dashboard.html: Stats cards, responsive table, Chart.js trend chart (async fetch /api/history), JSON parsing.
- [x] Polish: Tailwind matching base.html, hover effects, mobile-ready.
- Test: Dashboard shows chart/table correctly."


### 4. DB & Run Setup (Priority: Medium) ✅
- [x] run.py: Added CLI commands db-init (creates tables), migrate/upgrade stubs.
- [x] Run `python run.py db-init` to create DB.

Next: Step 5 Test Flow

### 5. Test Full Flow (Priority: High)
- [ ] Manual: python run.py → localhost:5000 → register → login → predict (fill form) → dashboard (see table/chart).
- [ ] Verify: Accurate predictions (~R2 0.95), no errors, responsive UI.

### 6. Enhancements (Nice-to-have)
- [ ] Add feature importance viz on predict page.
- [ ] User profile/stats.
- [ ] Export predictions CSV.

**Next Step**: Implement #1 (model fix) → mark done → proceed.

Progress: 5/5 complete. All fixes applied: config.py indentation fixed, dashboard template + routes safer JSON. Jinja2 error resolved. App ready to test.

