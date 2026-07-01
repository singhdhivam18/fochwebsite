# FOCH Project — GitHub Push Guide
# Repo: https://github.com/singhdhivam18/fochwebsite

## FILES CHANGED IN THIS UPDATE
- coreapp/middleware.py  ← NEW file
- coreapp/views.py       ← UPDATED (middleware decorators + session tracking)
- coreapp/urls.py        ← UPDATED (new route names + logout route)

## WHAT CHANGED (Summary for Root/Team)
1. Added session-based authentication (middleware.py)
2. login_user now sets request.session so auth works
3. Fixed register.html template name (was missing .html)
4. Fixed attendance_exixting typo → attendance_existing
5. Fixed insert_data/update_student_data: created_by now from session, not hardcoded 'admin'
6. generate_volunteer_code: created_by now from session
7. Renamed: dashboard → get_dashboard, report → expense_report_page (old names kept as aliases)
8. Added logout_user endpoint

## STEP-BY-STEP PUSH COMMANDS

### If you already have the repo cloned locally:

    cd path\to\fochwebsite          # Windows
    cd path/to/fochwebsite          # Mac/Linux

    # Copy the 3 new/updated files into the repo:
    # (replace the existing coreapp/views.py and coreapp/urls.py)
    # (add the new coreapp/middleware.py)

    git status                      # check what changed
    git add coreapp/middleware.py
    git add coreapp/views.py
    git add coreapp/urls.py
    git commit -m "feat: add middleware auth, fix session tracking, fix typos"
    git push origin main

### If you have NOT cloned the repo yet:

    git clone https://github.com/singhdhivam18/fochwebsite.git
    cd fochwebsite

    # Copy the 3 files into coreapp/ folder, then:
    git add coreapp/middleware.py
    git add coreapp/views.py
    git add coreapp/urls.py
    git commit -m "feat: add middleware auth, fix session tracking, fix typos"
    git push origin main

## NOTES
- DO NOT push config.ini — it has passwords!
- DO NOT push db.sqlite3
- The alias names (dashboard, report, attendance_exixting) are kept in views.py
  so existing frontend JS that calls old API names still works.
