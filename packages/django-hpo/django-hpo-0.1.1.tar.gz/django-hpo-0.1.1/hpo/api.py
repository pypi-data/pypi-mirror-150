import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from hpo.models import Phenotype
from django.conf import settings

HPO_PAGE_SIZE = getattr(settings, 'HPO_PAGE_SIZE', 25)

@login_required
def phenotype(request):
    data = 'fail'
    try:
        q = request.GET.get('term', '')
        phenotypes = list(Phenotype.objects.filter(name__icontains=q)[:HPO_PAGE_SIZE])
        results = []
        for g in phenotypes:
            phenotypes_json = {
                'id': g.id,
                'label': "%s" % g.name,
                'value': "%s" % g.name,
            }
            results.append(phenotypes_json)
        data = results
    except:
        pass
    return JsonResponse(data, safe=False)
