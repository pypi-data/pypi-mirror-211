from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "oarepo_vocabularies_search": "./js/oarepo_vocabularies_ui/search/index.js",
                "oarepo_vocabularies_ui_components": "./js/oarepo_vocabularies_ui/custom-components.js",
            },
            dependencies={},
            devDependencies={},
            aliases={
                "@translations/oarepo_vocabularies_ui": "./translations/oarepo_vocabularies_ui",
            },
        )
    },
)
