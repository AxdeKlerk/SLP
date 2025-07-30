Security Bug
**Bug:**
Accidentally committed the Django SECRET_KEY to *GitHub* in a public repository.

**Fix:**

Regenerated a new secure key using *Django*’s         get_random_secret_key()

Created a .env file to store the new SECRET_KEY

Installed python-decouple to read environment variables securely

Updated settings.py to load the secret key with:
SECRET_KEY = config('SECRET_KEY')

Added .env to .gitignore to prevent future leaks

**Lesson Learned:**

Secrets should never be hardcoded in settings.py or committed to version control. Using a .env file and decouple ensures sensitive information stays secure and separate from code.
Always check for secrets before pushing to *GitHub*, and use .gitignore to protect .env files automatically.
