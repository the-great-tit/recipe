from rest_framework.views import APIView
from rest_framework.response import Response


class RecipesView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
