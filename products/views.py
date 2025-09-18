from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer
from products.documents import ProductDocument


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.setdefault('request', self.request)
        return context

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response({'count': 0, 'results': []})

        search = (
            ProductDocument.search()
            .query(
                'multi_match',
                query=query,
                fields=['title^3', 'description', 'category.title'],
                fuzziness='AUTO',
            )
            .sort('-created_at')
        )

        try:
            response = search[:50].execute()
        except Exception:
            return Response(
                {'count': 0, 'results': [], 'detail': 'Search service unavailable.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        hit_ids = [int(hit.meta.id) for hit in response]

        products = (
            Product.objects.filter(id__in=hit_ids)
            .select_related('category')
        )
        products_by_id = {product.id: product for product in products}
        ordered_products = [products_by_id[product_id] for product_id in hit_ids if product_id in products_by_id]

        serializer = self.get_serializer(ordered_products, many=True)
        return Response({'count': len(ordered_products), 'results': serializer.data})
