from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from products.models import Category, Product


@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
    })
    price = fields.FloatField()

    class Index:
        name = settings.ELASTICSEARCH_PRODUCT_INDEX
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Product
        fields = (
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
        )
        related_models = (Category,)

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.products.all()
        return None
