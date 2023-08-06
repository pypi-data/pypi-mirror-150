# django-webpack-pages

Use webpack with your multi-page, multilingual django webapp.

Put the following in your settings file:

```python
WEBPACK_PAGES = {
    "CRITICAL_CSS_ENABLED": True,
    "ROOT_PAGE_DIR": osp.join(BASE_DIR, "pages"),
    "STATICFILE_BUNDLES_BASE": "bundles/{locale}/",  # should end in /
}
```

Using `webpack_loader.contrib.pages` you can register entrypoints for corresponding pages in templates.

At the top of your individual page, do:

```jinja2
{% extends "layout.jinja" %}
{% do register_entrypoint("myapp/dashboard") %}
```

In the layout's (base template's) head, place the following:

```jinja2
<!DOCTYPE html>
{% do register_entrypoint("main") %}
<html lang="{{ LANGUAGE_CODE }}">
<head>
  ...
  {{ render_css() }}
</head>
<body>
  ...
  {{ render_js() }}
</body>
```

This will load the registered entrypoints in order (`main`, then `myapp/dashboard`) and automatically inject
the webpack-generated css and js. It also supports critical css injection upon first request visits.
