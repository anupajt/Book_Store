# context_processors.py

from admin_panel.models import Category

def categories(request):
    # Retrieve all categories from the database
    all_categories = Category.objects.all()
    num_categories = all_categories.count()
    category_indices = list(range(num_categories))
    return {'all_categories': all_categories, 'num_categories': category_indices}
