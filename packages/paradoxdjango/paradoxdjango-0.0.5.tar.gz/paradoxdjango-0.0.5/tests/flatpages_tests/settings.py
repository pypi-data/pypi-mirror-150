import os

FLATPAGES_TEMPLATES = [
    {
        "BACKEND": "paradoxdjango.template.backends.paradoxdjango.DjangoTemplates",
        "DIRS": [os.path.join(os.path.dirname(__file__), "templates")],
        "OPTIONS": {
            "context_processors": ("paradoxdjango.contrib.auth.context_processors.auth",),
        },
    }
]
