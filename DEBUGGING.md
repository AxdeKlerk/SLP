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

### Offcanvas Navigation Error

**Bug:**  
The navigation links inside the mobile offcanvas menu would not redirect properly. Clicking them closed the menu but did not trigger navigation, even though the same links in the inline (desktop) menu worked fine.  

**Fix:**  
Removed the `data-bs-dismiss="offcanvas"` attribute from each `<a>` tag inside the offcanvas. This attribute was closing the drawer but also blocking the link’s natural navigation behaviour.  

**Lesson Learned:**  
If links inside a *Bootstrap* offcanvas are meant to load a new page (like *Django* `{% url %}` links), there is no need for `data-bs-dismiss`. The page reload will automatically hide the offcanvas, so adding dismissal attributes can actually break expected link behaviour.  

## Runtime Error

**Bug:**

*Cloudinary* image uploads failed in the *Django* admin panel. The error traceback ended with:
    `ValueError: Must supply api_key`
Even though the .env file included separate CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET variables, they were not being read correctly.

**Fix:**

Instead of using the dictionary-style CLOUDINARY_STORAGE = {...} config in settings.py, I used the unified CLOUDINARY_URL format in .env, like so:
    `CLOUDINARY_URL=cloudinary://<API_KEY>:<API_SECRET>@<CLOUD_NAME>`
I also made sure to load this into the environment using *python-dotenv*, like this:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')

    CLOUDINARY_URL = os.getenv(`CLOUDINARY_URL`)
    if CLOUDINARY_URL:
    os.environ[CLOUDINARY_URL] = CLOUDINARY_URL
I then removed the old cloudinary.config() and CLOUDINARY_STORAGE = { ... } blocks to avoid conflicts with cloudinary_storage.

**Lesson Learned:**

*Cloudinary* prefers the all-in-one CLOUDINARY_URL format, and it must be present in os.environ before *Django* tries to use it. If you’re using *python-decouple*, it won’t export variables to os.environ automatically, which breaks *Cloudinary* unless you handle it manually. *python-dotenv* with *os.getenv()* works better in this case.

## Template Logic — Navbar active state (dropdown parent)

**Bug:**
Initially the `Events` navbar item wasn't staying highlighted once one of the dropdown items were selected. I then hard coded the `Events` navbar item as `active` and realised that the issue was with the relationship between parent and child items.

**Fix:**
I removed the hard-coded `active` from the parent toggle and marked the parent/children `active`:

`{% if url_name == 'events' or url_name == 'previous_events' %}active{% endif %}` based on the current view name with a request resolver above: `{% with url_name=request.resolver_match.url_name %}` and added the `active` status to my css to increase specifity.

**Lesson Learned:**

Don’t hard-code active on nav items; compute it from the current route. For dropdowns, the parent’s state should reflect child activity (via request.resolver_match.url_name) and keep CSS specific but simple; Bootstrap’s defaults can override you unless your rules target the right elements.

## Logic Bug

**Bug:**

I noticed that my Roxoff event cards were appearing on the Upcoming Gigs page. This wasn’t supposed to happen — Roxoff events should only be shown on their own dedicated template `(roxoff.html)`, not mixed in with regular events.

**Fix:**

I realised I needed a way to clearly separate Roxoff events from regular ones. So I added a new event_type field to the Event model with `regular` and `roxoff` choices. Then I updated the view for the Upcoming Gigs page `(events_view)` to exclude Roxoff events:

`events = Event.objects.filter(gig_date__gte=today).exclude(event_type='roxoff').order_by('gig_date')`

**Lesson Learned:**

It’s better to explicitly separate types of events in the model using a dedicated field like event_type. That way, filtering them in views is more reliable and readable than trying to guess based on other values like roxoff_day. It also makes future development easier, especially if I need more event types later.

## Routing Error

**Bug:**
The venue search was returning a 404 error after submitting a search term. The artist search worked perfectly, even though the structure for both was identical in urls.py, views.py, and JavaScript. Visiting a URL like /venue/2/ returned a 404, but /artist/5/ did not.

**Fix:**
The issue was caused by relying on both root-level and namespaced includes for the products app in config/urls.py. At one point, both of these were present:

`path('', include('apps.products.urls')),`
`path('products/', include('apps.products.urls', namespace='products')),`

This meant some views worked at /artist/5/ (because of the root include), while others like /venue/2/ failed (due to inconsistent includes or redirects).
Once the root-level include was removed for clarity and consistency, all routes required the /products/ prefix. The fix involved two changes:

Removed the root include:

`path('', include('apps.products.urls')),`  # removed

Updated JS redirects to include the /products/ prefix:

window.location.href = `/products/venue/${data.id}/`;
window.location.href = `/products/artist/${data.id}/`;

**Lesson Learned:**
When using app-level namespacing `(namespace='products')`, routes must consistently match the URL prefix (/products/...). Having both root-level and prefixed includes causes unpredictable routing. Always verify that JavaScript redirects match your configured URL patterns.

## Navigation Highlight Issue

**Bug:**

The *Search* navbar item did not stay highlighted when navigating to either the artist or venue detail page (`artist_detail`, `venue_detail`). The expected behavior was for the *Search* tab to be marked active when the user was on these pages, just like the *Events* tab behaves when on related event pages.

**Fix:**  
I identified that the condition checking the *Search* tab for `artist_search` and `venue_search` was incorrect because those were not the actual view names. Instead, the actual view names were `artist_detail` and `venue_detail`. I updated the navbar to use these correct names.

**Lesson Learned:**  
When using `url_name` for template conditions, it’s essential to ensure I’m checking against the correct view name. I learned to debug this by printing `url_name` in the template using:

<p style="color:red; font-size:12px">
  url_name = {{ request.resolver_match.url_name }}
</p>

This helped me verify the actual names *Django* was using for each page. Always ensure the condition matches the exact value of `url_name` for the intended behavior.

## Template/Context Error

**Bug:**

The size dropdown wasn’t showing any options in the merch detail page. Clicking the button made the dropdown appear, but it was empty. The issue was that I tried looping with `{% for s in size_choices %}` and using `{{ s }}`, but my model’s choices actually return two values `(key, label)`. Because of that, nothing was rendered in the `<ul>`.

**Fix:**

I updated my `MerchDetailVie`w to pass size_choices into the context. Then in my template, I switched from using `{{ s }}` to the correct `{{ key }} and {{ label }}`. Finally, I matched the *Size JS* to the same pattern as the *Quantity JS*, so both dropdowns behave consistently.

**Lesson Learned:**

I need to remember that *Django* model field choices always give back `(key, label)` pairs, not a single value. If I try to loop with the wrong variable, the template will silently fail and look like “nothing happened.” Next time, I’ll check what data type a loop is actually returning before writing the template logic, and I’ll keep dropdown JS patterns consistent across all fields.


