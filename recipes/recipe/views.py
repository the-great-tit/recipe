from rest_framework.views import APIView
from rest_framework.response import Response


class RecipesView(APIView):
    @staticmethod
    def get(request):
        content = {'message': 'Hello, World!'}
        return Response(content)
