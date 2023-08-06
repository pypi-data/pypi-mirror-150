import os

AUTH_MIDDLEWARE = [
    "paradoxdjango.contrib.sessions.middleware.SessionMiddleware",
    "paradoxdjango.contrib.auth.middleware.AuthenticationMiddleware",
]

AUTH_TEMPLATES = [
    {
        "BACKEND": "paradoxdjango.template.backends.paradoxdjango.DjangoTemplates",
        "DIRS": [os.path.join(os.path.dirname(__file__), "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "paradoxdjango.template.context_processors.request",
                "paradoxdjango.contrib.auth.context_processors.auth",
                "paradoxdjango.contrib.messages.context_processors.messages",
            ],
        },
    }
]
