from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        # Ensure Elasticsearch document registrations are loaded with the app
        try:
            import elasticsearch
            import elasticsearch_dsl

            # django-elasticsearch-dsl still imports `elasticsearch.dsl`,
            # so expose the modern package under that attribute when needed.
            if not hasattr(elasticsearch, 'dsl'):
                elasticsearch.dsl = elasticsearch_dsl

            import products.documents  # noqa: F401
        except ImportError:
            pass
