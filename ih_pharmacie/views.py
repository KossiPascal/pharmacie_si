from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from med.models import District, Site, Translation
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from med.templatetags.functions_extras import trans
from django.http import HttpResponseRedirect

# from django.template import Context,loader

def home(request):
    return render(request, 'home.html', {})

def error404(request, exception=None):
    return render(request, '404.html')

def error500(request, exception=None):
    return render(request, '500.html') 

# @csrf_exempt
def csrf_failure(request, reason=""):
    # messages.error(request, trans("La vérification CSRF a échoué. Le cookie CSRF n'est pas défini. Demande abandonnée",request))
    error = trans("La vérification CSRF a échoué. Le cookie CSRF n'est pas défini. Demande abandonnée",request)
    logout(request)
    return render(request, 'auths/login.html', {'error': error,})


@login_required
def siteAjax(request):
    if request.is_ajax and request.method == "POST":
        district_id = request.POST.get('data_id')
        if District.objects.filter(id=district_id).exists():
            Sites = Site.objects.filter(district=district_id)
            data = []
            for site in Sites:
                data.append({site.id:site.site})
            return JsonResponse({"valid":True,"data": data}, status=200)
        else:
            return JsonResponse({"valid":False}, status=400)
    return JsonResponse({"valid": False}, status=400)


@login_required
def TranslationAjax(request):
    if request.is_ajax and request.method == "POST":
        search = request.POST.get('data_val')
        from django.db.models import Q

        if Translation.objects.filter(Q(trans_fr__icontains=search) | Q(trans_en__icontains=search)).exists():
            datas = Translation.objects.filter(Q(trans_fr__icontains=search) | Q(trans_en__icontains=search)).order_by('id')
            dataAppend = []
            for data in datas:
                dataAppend.append({'id': data.id, 'trans_fr': data.trans_fr, 'trans_en': data.trans_en, 'acronym_fr': data.acronym_fr, 'acronym_en': data.acronym_en})
            return JsonResponse({"valid": True, "datas": dataAppend}, status=200)
        else:
            return JsonResponse({"valid": False}, status=400)
    return JsonResponse({"valid": False}, status=400)
# def error404(request, exception=None):
#     template = loader.get_template('404.html')
#     context = Context({'message':'All: %s' % request,})
#     return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)
