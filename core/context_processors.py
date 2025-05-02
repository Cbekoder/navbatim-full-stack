from services.models import Category

def categories(request):
    return {
        'global_categories': Category.objects.all()
    }
