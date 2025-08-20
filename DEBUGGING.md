## Security Bug

**Bug:**

Accidentally committed the *Django* SECRET_KEY to *GitHub* in the initial commit.

**Fix:**

Regenerated a new secure key using get_random_secret_key()

Stored it safely in a .env file (excluded via .gitignore)

Updated settings.py to load the key using python-decouple

Removed the entire *Git* history by deleting .git, reinitializing, and creating a fresh, secure initial commit

Force-pushed the cleaned repo to *GitHub*

**Lesson Learned:**

Even one leaked commit can expose sensitive data permanently. Using environment variables and .gitignore from the start prevents accidental leaks. Rewriting history should be done early if needed, before more commits make it harder.

## Deployment Issue

**Bug:**

After deploying to Heroku, the app crashed with an Application Error and later returned a 404 page instead of loading the homepage. The logs revealed that some environment variables were missing, and Django couldn’t find SECRET_KEY or `DATABASE_URL`. Even after fixing that, the app loaded but still returned a 404 error for all routes.

**Fix:**

Added missing environment variables to Heroku using:

    heroku config:set SECRET_KEY="your-secret-key"
    heroku config:set `DATABASE_URL`="your-database-url"

Added DISABLE_COLLECTSTATIC=1 to stop Heroku failing on missing static files during build.

The 404 error wasn’t caused by routing issues or template placement — the problem was that the templates were in the templates/ folder, but the view was trying to render core/home.html, which didn’t exist.

**Fix:**

Updated the views to match the actual template paths. Since the HTML files were directly inside templates/ (not in a core/ subfolder), we changed from:

    return render(request, 'core/home.html') to return render(request, 'home.html')

(Same for about.html and contact.html.)

**Lesson Learned:**

Heroku needs all environment variables your app depends on — even if it runs locally.

If Django throws a 404 after deployment but the URL paths look correct, double-check the template paths in your render() function.

Don't assume it's a folder problem — sometimes it's just the wrong string in the render() call.

## Database Configuration Error

### **Database Configuration Error**

**Bug:**  
The new *Heroku* app was still connected to the *PostgreSQL database* used in a previous project. This led to seeing old user data in the *Django* admin panel, even though the new app was supposed to be starting fresh. The problem occurred because the ``DATABASE_URL`` in *Heroku* was still pointing to the old *Heroku PostgreSQL* database from the previous project.

**Fix:**  
A brand-new *Supabase* database was created to replace the old *Heroku PostgreSQL* one. The *transaction pooler* connection string was copied from *Supabase* (under **Database > Connection Pooling**) and updated to include the actual password with special characters properly percent-encoded (e.g. `!` → `%21`). The connection string was set in *Heroku* and migrations were applied to initialise the new data base.

**Lesson Learned:**
When creating a new *Heroku* app, it may retain environment variables (like `DATABASE_URL`) from earlier linked services. If not explicitly changed, the app will connect to the previous database, even if the project is new. Always inspect and update `DATABASE_URL` after setting up a new deployment. Special characters in credentials must be percent-encoded to avoid connection errors.


