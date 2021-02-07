from django.utils import timezone
from .forms import CamegDrugServedForm, DistrictForm, DrugStockAdjustmentForm, IhDrugServedForm, MonthForm, PatientDrugServedForm, DrugStockForm, DrugForm, DrugSupplierForm, CategoryForm, SiteForm, TranslationForm, YearForm
from .models import VariousParameters, CamegDrugServed, DrugStockAdjustment, IhDrugServed, District, Drug, Category, DrugStock, DrugSupplier, Etats, Month, PatientDrugServed, ServedEtats, Site, Translation, Year
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .templatetags.functions_extras import YearErrorMessage, sha1Hash, sha256Hash, DateErrorMessage, IntegrityErrorMessage, LanguageChangedMessage, PageNotFoundMessage, ParameterErrorMessage, RequestHaveErrorMessage, SaisieErrorMessage, SuccessDeleteMessage, SuccessSaveMessage, SuccessUpdateMessage, UserIsConnect, convert_date, get_previous_month, situation, substract_day_month_year, to_int, trans, url_matched
from django.db.models import Q, Sum
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def Pagination(request, data, num = 10):
        paginator = Paginator(data, num)
        page = request.GET.get('page')
        try:
            paginate = paginator.page(to_int(page))
            return paginate
        except:
            paginate = paginator.page(1)
            return paginate
        # except PageNotAnInteger:
        #     paginate = paginator.page(1)
        #     return paginate
        # except EmptyPage:
        #     paginate = paginator.page(paginator.num_pages)
        #     return paginate

def returnDataorNot(Table, data, cible="", ext=""):
    # try:
        if cible != "":
            if data != None and data != "":
                t = Table.objects.get(pk=data)
                if cible == "site":
                    return t.site
                elif cible == "district":
                    return t.district
                elif cible == "drug":
                    return t.drug
                else:
                    return t
            return ext
        else:
            if data != None and data != "":
                return Table.objects.filter(pk=data)
            else:
                return ext
    # except:
    #     return ext

def getFilterByQCalculation(data, start, default):
    if data != None and data != "":
        return start
    else:
        return default

def return_if_or_else(value1, value2):
    if value1 != None and value1 != "":
        return value1
    else:
        return value2

@login_required
def DrugServedData(request):
    rp = request.POST
    rpg = request.POST.get
    rsg = request.session.get
    saveanother = False

    if request.session.get("saveanother") == True:
        saveanother = request.session.get("saveanother")
        request.session["saveanother"] = False

    if url_matched(request.path, "cameg"):
        DataInstance = CamegDrugServed
        form = CamegDrugServedForm(rp)
        PageModelObject = CamegDrugServed.objects
        PageModel = "cameg"
    elif url_matched(request.path, "ih"):
        DataInstance = IhDrugServed
        form = IhDrugServedForm(rp)
        PageModelObject = IhDrugServed.objects
        PageModel = "ih"
    elif url_matched(request.path, "patient"):
        DataInstance = PatientDrugServed
        form = PatientDrugServedForm(rp)
        PageModelObject = PatientDrugServed.objects
        PageModel = "patient"
    elif url_matched(request.path, "stock"):
        DataInstance = DrugStock
        form = DrugStockForm(rp)
        PageModelObject = DrugStock.objects
        PageModel = "stock"
    elif url_matched(request.path, "stock_adjustment"):
        DataInstance = DrugStockAdjustment
        form = DrugStockAdjustmentForm(rp)
        PageModelObject = DrugStockAdjustment.objects
        PageModel = "stock_adjustment"
    else:
        messages.info(request, PageNotFoundMessage(request))
        return HttpResponseRedirect(reverse('home'))

    f_district = District.objects.all()
    f_drug = Drug.objects.filter(is_available = True).order_by('id')
    f_drug_supplier = DrugSupplier.objects.all()

    e_site = e_site_v = ""

    if rsg('from') != None and rsg('from') != "":
        s_date_from = rsg('from')
    else:
        s_date_from = rpg('from')

    if rsg('to') != None and rsg('to') != "":
        s_date_to = rsg('to')
    else:
        s_date_to = rpg('to')

    if rpg('f_district') != None and rpg('f_district') != "":
        f_site = Site.objects.filter(district=rpg('f_district'))
    else:
        f_site = ""

    if rsg('drug_supplier') != None and rsg('drug_supplier') != "":
        s_drug_supplier = rsg('drug_supplier')
        s_drug_supplier_v = returnDataorNot(DrugSupplier, rsg('drug_supplier'), 'drug_supplier', ext="tout fournisseur")
    else:
        s_drug_supplier = rpg('f_drug_supplier')
        s_drug_supplier_v = returnDataorNot(DrugSupplier, rpg('f_drug_supplier'), 'drug_supplier', ext="tout fournisseur")

    if rsg('district') != None and rsg('district') != "":
        s_district = rsg('district')
        s_district_v = returnDataorNot(District, rsg('district'), 'district', ext="tout district")
        f_site = Site.objects.filter(district=rsg('district'))
    else:
        s_district = rpg('f_district')
        s_district_v = returnDataorNot(District, rpg('f_district'), 'district', ext="tout district")
        if rpg('f_district') != None and rpg('f_district') != "":
            f_site = Site.objects.filter(district=rpg('f_district'))
        else:
            f_site = ""

    if rsg('site') != None and rsg('site') != "":
        s_site = rsg('site')
        s_site_v = returnDataorNot(Site, rsg('site'), 'site', ext="tout site")
    else:
        s_site = rpg('f_site')
        s_site_v = returnDataorNot(Site, rpg('f_site'), 'site', ext="tout site")

    if rsg('drug') != None and rsg('drug') != "":
        s_drug = rsg('drug')
        s_drug_v = returnDataorNot(Drug, rsg('drug'), 'drug', ext="tout médicament")
    else:
        s_drug = rpg('f_drug')
        s_drug_v = returnDataorNot(Drug, rpg('f_drug'), 'drug', ext="tout médicament")
    
    if rsg('drug_source') != None and rsg('drug_source') != "":
        s_drug_source  = rsg('drug_source')
    else:
        s_drug_source = rpg('f_drug_source')

    total_amount = ""

    if rpg('data_filter') != "" and rpg('data_filter') != None:
        s_date_from = request.session['from'] = rpg('from')
        s_date_to = request.session['to'] = rpg('to')
        s_site = request.session['site'] = rpg('f_site')
        s_drug = request.session['drug'] = rpg('f_drug')
        s_district = request.session['district'] = rpg('f_district')
        s_drug_supplier = request.session['drug_supplier'] = rpg('f_drug_supplier')
        s_drug_source = request.session['drug_source'] = rpg('f_drug_source')

        # if rpg('f_district') != None and rpg('f_district') != "":
        #     f_site = Site.objects.filter(district=rpg('f_district'))
        # else:
        #     f_site = ""

        if url_matched(request.path, PageModel):
            if rpg("from") != "" and rpg("to") != "" and rpg("from") != None and rpg("to") != None:
                _from = getFilterByQCalculation(rpg("from"), Q(date__gte=rpg("from")), Q(date__isnull=False))
                _to = getFilterByQCalculation(rpg("to"), Q(date__lte=rpg("to")), Q(date__isnull=False))
                _drug = getFilterByQCalculation(rpg("f_drug"), Q(drug=rpg("f_drug")), Q(drug__isnull=False))
                   
                if PageModel == "patient":   
                    datas = PageModelObject.filter(_from,_to,_drug).order_by('-created_at')
                elif PageModel == "stock":   
                    _drug_supplier = getFilterByQCalculation(rpg("f_drug_supplier"), Q(drug_supplier=rpg("f_drug_supplier")), Q(drug_supplier__isnull=False))
                    datas = PageModelObject.filter(_from,_to,_drug,_drug_supplier).order_by('-created_at')
                elif PageModel == "stock_adjustment":
                    _drug_source = getFilterByQCalculation(rpg("f_drug_source"), Q(drug_supplier=rpg("f_drug_source")), Q(drug_source__isnull=False))
                    datas = PageModelObject.filter(_from,_to,_drug,_drug_source).order_by('-created_at')
                else:
                    _district = getFilterByQCalculation(rpg("f_district"), Q(district=rpg("f_district")), Q(district__isnull=False))
                    _site = getFilterByQCalculation(rpg("f_site"), Q(site=rpg("f_site")), Q(site__isnull = False))
                    datas = PageModelObject.filter(_from,_to,_drug,_district,_site).order_by('-created_at')
            else:
                messages.error(request, DateErrorMessage(request))
                datas = PageModelObject.all().order_by('-created_at')[0:0]
        else:
            messages.info(request, RequestHaveErrorMessage(request))
            e_site = s_site            
            e_site_v = s_site_v
            datas = PageModelObject.all().order_by('-created_at')
    else:
        if rsg('from') != "" and rsg('to') != "" and rsg('from') != None and rsg('to') != None:
            _from = getFilterByQCalculation(rsg("from"), Q(date__gte=rsg("from")), Q(date__isnull=False))
            _to = getFilterByQCalculation(rsg("to"), Q(date__lte=rsg("to")), Q(date__isnull=False))
            _drug = getFilterByQCalculation(rsg("drug"), Q(drug=rsg("drug")), Q(drug__isnull=False))
            
            if PageModel == "patient":   
                datas = PageModelObject.filter(_from,_to,_drug).order_by('-created_at')
            elif PageModel == "stock":   
                _drug_supplier = getFilterByQCalculation(rsg("drug_supplier"), Q(drug_supplier=rsg("drug_supplier")), Q(drug_supplier__isnull=False))
                datas = PageModelObject.filter(_from,_to,_drug,_drug_supplier).order_by('-created_at')
            elif PageModel == "stock_adjustment":
                _drug_source = getFilterByQCalculation(rsg("drug_source"), Q(drug_supplier=rsg("drug_source")), Q(drug_source__isnull=False))
                datas = PageModelObject.filter(_from,_to,_drug,_drug_source).order_by('-created_at')
            else:
                _district = getFilterByQCalculation(rsg("district"), Q(district=rsg("district")), Q(district__isnull=False))
                _site = getFilterByQCalculation(rsg("site"), Q(site=rsg("site")), Q(site__isnull = False))
                datas = PageModelObject.filter(_from,_to,_drug,_district,_site).order_by('-created_at')
        else:
            datas = PageModelObject.all().order_by('-created_at')
    #         # datas = PageModelObject.all().order_by('-created_at')[0:100]

    # if PageModel != "patient" and PageModel != "stock" and PageModel != "stock_adjustment":
    #     total_amount = PageModelObject.all().aggregate(Sum('total_amount'))['total_amount__sum']

    # total_amount = total_amount


            
    if PageModel != "patient" and PageModel != "stock" and PageModel != "stock_adjustment":
        total_amount = datas.aggregate(Sum('total_amount'))['total_amount__sum']
    total_amount = total_amount

    # d = DataInstance.objects.all()
    # n = e = 0
    # for x in d:
    #     try:
    #         cg = get_object_or_404(DataInstance, id=str(to_int(x.id)))
    #         if DataInstance.objects.filter(id = sha1Hash(sha256Hash(request.user.id, timezone.now(), to_int(x.id)), to_int(x.id))).exists():
    #             f = to_int(x.id) * 2
    #             cg.id = sha1Hash(sha256Hash(request.user.id, timezone.now(), f), to_int(x.id))
    #             e += 1
    #         else:
    #             cg.id = sha1Hash(sha256Hash(request.user.id, timezone.now(), to_int(x.id)), to_int(x.id))
    #             n += 1
    #         cg.save()
    #     except:
    #         pass
    # messages.info(request, "total affecté: (existe:" + str(e) + '; new' + str(n) + ' )')
    # return HttpResponseRedirect(reverse('home'))

    # d = 0
    # try:
    #     d = DataInstance.objects.filter(date__isnull=True).count
    #     DataInstance.objects.filter(date__isnull=True).delete()
    # except:
    #     pass
    # messages.info(request, "total affecté: " + str(d))
    # return HttpResponseRedirect(reverse('home'))

    paginate = Pagination(request, datas)

    return render(request, 'pages/'+ PageModel +'.html', {
        'form': form, 'paginate': paginate,
        'f_drug': f_drug, 'f_district':f_district, 'f_site': f_site, 'f_drug_supplier': f_drug_supplier,
        's_date_from': s_date_from, 's_date_to':s_date_to, 's_drug': s_drug, 's_district':s_district, 
        's_site': s_site, 's_drug_supplier': s_drug_supplier, "e_site_v":e_site_v,
        's_drug_v': s_drug_v, 's_district_v':s_district_v, 's_site_v': s_site_v, 's_drug_supplier_v': s_drug_supplier_v,
        'total_amount': total_amount, 'e_site': e_site, 'saveanother': saveanother, 's_drug_source': s_drug_source, 
        })

@login_required
def CamegDataCreateUpdateDelete(request, id='0', delete='0'):
    rp = request.POST
    rpg = request.POST.get
    form = CamegDrugServedForm(rp)
    Sites = Site.objects.filter(district=rpg('district'))
    e_site = ""
    Error = Update = False
    cameg = CamegDrugServed()
    message = SuccessSaveMessage(request)
 
    if delete == '0':
        if id != '0':
            cameg = get_object_or_404(CamegDrugServed, id=id)
            form = CamegDrugServedForm(rp or None, instance=cameg)
            e_site = cameg.site
            Sites = Site.objects.filter(district=cameg.district.id)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('saveAndAddAnother') != ""  and rpg('saveAndAddAnother') != None:
            request.session["saveanother"] = True

        if rpg('save') != "" and rpg('save') != None or rpg('saveAndAddAnother') != ""  and rpg('saveAndAddAnother') != None:
            if form.is_valid():
                try:
                    if id == '0':
                        cameg.id = sha1Hash(sha256Hash(request.user.id, timezone.now(), rpg('quantity_served')), rpg('quantity_served'))
                    cameg.date = rpg('date')
                    cameg.drug = Drug.objects.get(pk=rpg('drug'))
                    cameg.district = District.objects.get(pk=rpg('district'))
                    cameg.site = Site.objects.get(pk=rpg('site'))
                    if rpg('save') == "enrégistrer" or rpg('save') == "save" or rpg('saveAndAddAnother') != ""  and rpg('saveAndAddAnother') != None:
                        cameg.created_at = timezone.now()
                        cameg.created_by = User.objects.get(pk=request.user.id)
                    if rpg('save') == "modifier" or rpg('save') == "update":
                        cameg.updated_at = timezone.now()
                        cameg.updated_by = User.objects.get(pk=request.user.id)
                    if rpg('quantity_ordered') == '':
                        cameg.quantity_ordered = rpg('quantity_served')
                    else:
                        cameg.quantity_ordered = rpg('quantity_ordered')
                    cameg.quantity_served = rpg('quantity_served')
                    cameg.unit_price = rpg('unit_price')
                    cameg.total_amount = rpg('total_amount')
                    cameg.save()

                    if rpg('save') == "enrégistrer" or rpg('save') == "save" or rpg('saveAndAddAnother') != ""  and rpg('saveAndAddAnother') != None:
                        if rpg('add_to_stock') == 'on':
                            stock = DrugStock()
                            stock.id = sha1Hash(sha256Hash(request.user.id, timezone.now(), rpg('quantity_served')), rpg('quantity_served'))
                            stock.date = rpg('date')
                            stock.drug = Drug.objects.get(pk=rpg('drug'))
                            stock.drug_supplier = DrugSupplier.objects.get(pk='1')
                            if rpg('stock_quantity') != None and rpg('stock_quantity') != "":
                                stock.stock_quantity = rpg('stock_quantity')
                            else:
                                stock.stock_quantity = rpg('quantity_served')
                            stock.created_at = timezone.now()
                            stock.created_by = User.objects.get(pk=request.user.id)
                            stock.save()
                            
                    if rpg('add_to_stock') == 'on':
                        messages.success(request, trans('sauvegardé et ajouté au stock', request))
                    else:
                        messages.info(request, message)

                    return HttpResponseRedirect(reverse('cameg'))
                except:
                    messages.error(request, SaisieErrorMessage(request))
                    e_site = Site.objects.get(pk=to_int(rpg('site')))
                    Error = True
            else:
                messages.error(request, ParameterErrorMessage(request))
                pass
    else:
        try:
            CamegDrugServed.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('cameg'))

    return render(request, 'pages/cameg.html', {'form': form, 'Update': Update, 'cameg_nav': True, 'e_site': e_site, 'Sites': Sites, 'Error': Error})
 
@login_required
def IhDataCreateUpdateDelete(request, id='0', delete='0'):
    rp = request.POST
    rpg = request.POST.get
    form = IhDrugServedForm(rp)
    Sites = Site.objects.filter(district=rpg('district'))
    e_site = None
    Error = Update = False
    ih = IhDrugServed()
    message = SuccessSaveMessage(request)

    try:
        del request.session['datas']
        request.session['datas'] = ""
    except:
        pass

    if delete == '0':
        if id != '0':
            ih = get_object_or_404(IhDrugServed, id=id)
            message = SuccessUpdateMessage(request)
            form = IhDrugServedForm(rp or None, instance=ih)
            # datas = IhDrugServed.objects.filter(pk=id)
            e_site = ih.site
            Sites = Site.objects.filter(district=ih.district.id)
            Update = True

        if rpg('saveAndAddAnother') != ""  and rpg('saveAndAddAnother') != None:
            request.session["saveanother"] = True

        if rpg('save') != "" and rpg('save') != None or rpg('saveAndAddAnother') != ""  and rpg('saveAndAddAnother') != None:
            if form.is_valid():
                try:
                    if id == '0':
                        ih.id = sha1Hash(sha256Hash(request.user.id, timezone.now(), rpg('quantity_served')), rpg('quantity_served'))
                    ih.date = rpg('date')
                    ih.drug = Drug.objects.get(pk=rpg('drug'))
                    ih.district = District.objects.get(pk=rpg('district'))
                    ih.site = Site.objects.get(pk=rpg('site'))
                    if rpg('save') == "enrégistrer" or rpg('save') == "save" or rpg('saveAndAddAnother') != ""  and rpg('saveAndAddAnother') != None:
                        ih.created_at = timezone.now()
                        ih.created_by = User.objects.get(pk=request.user.id)
                    if rpg('save') == "modifier" or rpg('save') == "update":
                        ih.updated_at = timezone.now()
                        ih.updated_by = User.objects.get(pk=request.user.id)
                    if rpg('quantity_ordered') == '':
                        ih.quantity_ordered = rpg('quantity_served')
                    else:
                        ih.quantity_ordered = rpg('quantity_ordered')
                    ih.quantity_served = rpg('quantity_served')
                    ih.unit_price = rpg('unit_price')
                    ih.total_amount = rpg('total_amount')
                    ih.save()
                    messages.info(request, message)
                    return HttpResponseRedirect(reverse('ih'))
                except:
                    messages.error(request, SaisieErrorMessage(request))
                    e_site = Site.objects.get(pk=to_int(rpg('site')))
                    Error = True
            else:
                messages.error(request, ParameterErrorMessage(request))
                pass
    else:
        try:
            IhDrugServed.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('ih'))
    return render(request, 'pages/ih.html', {'form': form, 'Update': Update, 'ih_nav': True, 'e_site': e_site, 'Sites': Sites, 'Error': Error})

@login_required
def PatientDataCreateUpdateDelete(request, id='0', delete='0'):
    rp = request.POST
    rpg = request.POST.get
    form = PatientDrugServedForm(rp)
    Update = Error = False
    patient = PatientDrugServed()
    message = SuccessSaveMessage(request)

    if delete == '0':
        if id != '0':
            patient = get_object_or_404(PatientDrugServed, id=id)
            form = PatientDrugServedForm(rp or None, instance=patient)
            datas = PatientDrugServed.objects.filter(pk=id)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                try:
                    if id == '0':
                        patient.id = sha1Hash(sha256Hash(request.user.id, timezone.now(), rpg('quantity_served')), rpg('quantity_served'))
                    patient.date = rpg('date')
                    patient.drug = Drug.objects.get(pk=rpg('drug'))
                    patient.patient_fullname = rpg('patient_fullname')
                    if rpg('save') == "enrégistrer" or rpg('save') == "save":
                        patient.created_at = timezone.now()
                        patient.created_by = User.objects.get(pk=request.user.id)
                    if rpg('save') == "modifier" or rpg('save') == "update":
                        patient.updated_at = timezone.now()
                        patient.updated_by = User.objects.get(pk=request.user.id)
                    patient.quantity_served = rpg('quantity_served')
                    patient.quantity_source = rpg('quantity_source')
                    patient.save()
                    messages.info(request, message)
                    return HttpResponseRedirect(reverse('patient'))
                except:
                    messages.error(request, SaisieErrorMessage(request))
                    Error = True
    else:
        try:
            PatientDrugServed.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('patient'))

    return render(request, 'pages/patient.html', {'form': form, 'Update': Update, 'Error': Error})

@login_required
def StockDataCreateUpdateDelete(request, id='0', delete='0'):
    rp = request.POST
    rpg = request.POST.get
    form = DrugStockForm(rp)
    PageModel = "stock"
    Error = Update = False
    stock = DrugStock()
    message = SuccessSaveMessage(request)
    
    if delete == '0':
        if id != '0':
            stock = get_object_or_404(DrugStock, id=id)
            form = DrugStockForm(rp or None, instance=stock)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                try:
                    if id == '0':
                        stock.id = sha1Hash(sha256Hash(request.user.id, timezone.now(), rpg('stock_quantity')), rpg('stock_quantity'))
                    stock.date = rpg('date')
                    stock.drug = Drug.objects.get(pk=rpg('drug'))
                    stock.drug_supplier = DrugSupplier.objects.get(pk=rpg('drug_supplier'))
                    stock.stock_quantity = rpg('stock_quantity')
                    if rpg('save') == "enrégistrer" or rpg('save') == "save":
                        stock.created_at = timezone.now()
                        stock.created_by = User.objects.get(pk=request.user.id)
                    if rpg('save') == "modifier" or rpg('save') == "update":
                        stock.updated_at = timezone.now()
                        stock.updated_by = User.objects.get(pk=request.user.id)
                    stock.save()
                    messages.info(request, message)
                    return HttpResponseRedirect(reverse('stock'))
                except:
                    messages.error(request, SaisieErrorMessage(request))
                    Error = True
    else:
        try:
            DrugStock.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('stock'))

    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'Error': Error,  'Update': Update})

@login_required
def StockAdjustmentDataCreateUpdateDelete(request, id='0', delete='0'):
    rp = request.POST
    rpg = request.POST.get
    form = DrugStockAdjustmentForm(rp)
    PageModel = "stock_adjustment"
    Error = Update = False
    stock_adjustment = DrugStockAdjustment()
    message = SuccessSaveMessage(request)
    datas = DrugStockAdjustment.objects.all().order_by('-created_at')
    if delete == '0':
        if id != '0':
            stock_adjustment = get_object_or_404(DrugStockAdjustment, id=id)
            form = DrugStockAdjustmentForm(rp or None, instance=stock_adjustment)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                try:
                    if id == '0':
                        stock_adjustment.id = sha1Hash(sha256Hash(request.user.id, timezone.now(), rpg('stock_adjustment_quantity')),rpg('drug_source'))
                    stock_adjustment.date = rpg('date')
                    stock_adjustment.drug = Drug.objects.get(pk=rpg('drug'))
                    stock_adjustment.drug_source = rpg('drug_source')
                    stock_adjustment.stock_adjustment_quantity = rpg('stock_adjustment_quantity')
                    if rpg('save') == "enrégistrer" or rpg('save') == "save":
                        stock_adjustment.created_at = timezone.now()
                        stock_adjustment.created_by = User.objects.get(pk=request.user.id)
                    if rpg('save') == "modifier" or rpg('save') == "update":
                        stock_adjustment.updated_at = timezone.now()
                        stock_adjustment.updated_by = User.objects.get(pk=request.user.id)
                    stock_adjustment.save()
                    messages.info(request, message)
                    return HttpResponseRedirect(reverse('stock_adjustment'))
                except:
                    messages.error(request, SaisieErrorMessage(request))
                    Error = True
    else:
        try:
            DrugStockAdjustment.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('stock_adjustment'))

    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'Error': Error, 'datas': datas,  'Update': Update})

@login_required
def DrugDataCreateUpdateDelete(request, id=0, delete=0):
    rp = request.POST
    rpg = request.POST.get
    form = DrugForm(rp)
    PageModelObject = Drug.objects
    PageModel = "drug"
    datas = PageModelObject.all().order_by('id')
    Error = Update = noFooterNav = is_available = is_not_available = False
    drug = Drug()
    message = SuccessSaveMessage(request)
    categories = Category.objects.all()
    category = None

    if delete == 0:
        if id != 0:
            drug = get_object_or_404(Drug, id=id)
            form = DrugForm(rp or None, instance=drug)
            datas = Drug.objects.filter(pk=id)
            message = SuccessUpdateMessage(request)
            Update = noFooterNav = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                try:
                    drug.drug = rpg('drug')
                    drug.category = Category.objects.get(pk=rpg('category'))
                    if rpg('expiry_date') != None and rpg('expiry_date') != "":
                        drug.expiry_date = rpg('expiry_date')
                    if rpg('save') == "enrégistrer" or rpg('save') == "save":
                        drug.created_at = timezone.now()
                        drug.created_by = User.objects.get(pk=request.user.id)
                    if rpg('save') == "modifier" or rpg('save') == "update":
                        drug.updated_at = timezone.now()
                        drug.updated_by = User.objects.get(pk=request.user.id)
                    drug.save()
                    messages.info(request, message)
                    return HttpResponseRedirect(reverse('drug'))
                except:
                    messages.error(request, SaisieErrorMessage(request))
                    Error = True
    
        if rpg('data_filter') != "" and rpg('data_filter') != None:
            try:
                category = Category.objects.get(id=rpg("category"))
            except:
                pass
            _category = getFilterByQCalculation(rpg("category"), Q(category=rpg("category")), Q(category__isnull=False))
            if rpg("availability") == "available":
                ava = is_available = True
            else:
                ava = False
                is_not_available = True
            _available = getFilterByQCalculation(rpg("availability"), Q(is_available=ava), Q(is_available__isnull=False))
                    
            datas = PageModelObject.filter(_category,_available).order_by('id')


    else:
        try:
            Drug.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('drug'))
 
    # paginate = Pagination(request, datas)
    paginate = datas

    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'paginate': paginate, 'Error': Error, 'Update': Update, 'noFooterNav': noFooterNav, 'categories': categories, 'is_available': is_available, 'is_not_available': is_not_available, 'category': category})

@login_required
def DrugSupplierDataCreateUpdateDelete(request, id=0, delete=0):
    rp = request.POST
    rpg = request.POST.get
    form = DrugSupplierForm(rp)
    PageModelObject = DrugSupplier.objects
    PageModel = "drug_supplier"
    datas = PageModelObject.all().order_by('id')
    Update = noFooterNav = False
    drug_supplier = DrugSupplier()
    message = SuccessSaveMessage(request)
    if delete == 0:
        if id != 0:
            drug_supplier = get_object_or_404(DrugSupplier, id=id)
            form = DrugSupplierForm(rp or None, instance=drug_supplier)
            datas = DrugSupplier.objects.filter(pk=id)
            message = SuccessUpdateMessage(request)
            Update = noFooterNav = True
            
        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                drug_supplier.drug_supplier = rpg('drug_supplier')
                if rpg('save') == "enrégistrer" or rpg('save') == "save":
                    drug_supplier.created_at = timezone.now()
                    drug_supplier.created_by = User.objects.get(pk=request.user.id)
                if rpg('save') == "modifier" or rpg('save') == "update":
                    drug_supplier.updated_at = timezone.now()
                    drug_supplier.updated_by = User.objects.get(pk=request.user.id)
                drug_supplier.save()
                messages.info(request, message)
                return HttpResponseRedirect(reverse('drug_supplier'))
    else:
        try:
            DrugSupplier.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('drug_supplier'))

    paginate = Pagination(request, datas)

    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'paginate': paginate, 'Update': Update, 'noFooterNav': noFooterNav, })

@login_required
def CategoryDataCreateUpdateDelete(request, id=0, delete=0):
    rp = request.POST
    rpg = request.POST.get
    form = CategoryForm(rp)
    PageModelObject = Category.objects
    PageModel = "category"
    datas = PageModelObject.all().order_by('id')
    Update = False

    if delete== 0 and delete!= None:
        if id == 0 and id != None:
            category = Category()
            message = SuccessSaveMessage(request)
        else:
            category = get_object_or_404(Category, id=id)
            form = CategoryForm(rp or None, instance=category)
            datas = Category.objects.filter(pk=id)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                category.category = rpg('category')
                category.save()
                messages.info(request, message)
                return HttpResponseRedirect(reverse('category'))
    else:
        try:
            Category.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('category'))
    
    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'datas': datas, 'Update': Update, 'noFooterNav': True, })

@login_required
def YearDataCreateUpdateDelete(request, id=0, delete=0):
    rp = request.POST
    rpg = request.POST.get
    form = YearForm(rp)
    PageModelObject = Year.objects
    PageModel = "year"
    datas = PageModelObject.all().order_by('id')
    Update = False

    if delete== 0 and delete!= None:
        if id == 0 and id != None:
            year = Year()
            message = SuccessSaveMessage(request)
        else:
            year = get_object_or_404(Year, id=id)
            form = YearForm(rp or None, instance=year)
            datas = Year.objects.filter(pk=id)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                year.year = rpg('year')
                year.save()
                messages.info(request, message)
                return HttpResponseRedirect(reverse('year'))
    else:
        try:
            Year.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('year'))
    
    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'datas': datas, 'Update': Update, 'noFooterNav': True})

@login_required
def MonthDataCreateUpdateDelete(request, id=0, delete=0):
    rp = request.POST
    rpg = request.POST.get
    form = MonthForm(rp)
    PageModelObject = Month.objects
    PageModel = "month"
    datas = PageModelObject.all().order_by('id')
    Update = False

    if delete== 0 and delete!= None:
        if id == 0 and id != None:
            month = Month()
            message = SuccessSaveMessage(request)
        else:
            month = get_object_or_404(Month, id=id)
            form = MonthForm(rp or None, instance=month)
            datas = Month.objects.filter(pk=id)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                try:
                    if PageModelObject.filter(pk=rpg('id')).exists() or PageModelObject.filter(month=rpg('month')).exists():
                        try:
                            PageModelObject.filter(pk=rpg('id')).delete()
                            PageModelObject.filter(month=rpg('month')).delete()
                        except:
                            pass
                    
                    month.id = rpg('id')
                    month.month = rpg('month')
                    month.save()
                    messages.info(request, message)  
                except:
                    messages.info(request, 'Problème avec votre donnée !!!')
                return HttpResponseRedirect(reverse('month'))
    else:
        try:
            Month.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('month'))
    
    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'datas': datas, 'Update': Update, 'noFooterNav': True, })

@login_required
def DistrictDataCreateUpdateDelete(request, id=0, delete=0):
    rp = request.POST
    rpg = request.POST.get
    form = DistrictForm(rp)
    PageModelObject = District.objects
    PageModel = "district"
    datas = PageModelObject.all().order_by('id')
    Update = False

    if delete== 0 and delete!= None:
        if id == 0 and id != None:
            district = District()
            message = SuccessSaveMessage(request)
        else:
            district = get_object_or_404(District, id=id)
            form = DistrictForm(rp or None, instance=district)
            datas = District.objects.filter(pk=id)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                district.district = rpg('district')
                district.save()
                messages.info(request, message)
                return HttpResponseRedirect(reverse('district'))
    else:
        try:
            District.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('district'))
    
    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'datas': datas, 'Update': Update, 'noFooterNav': True, })

@login_required
def SiteDataCreateUpdateDelete(request, id=0, delete=0):
    rp = request.POST
    rpg = request.POST.get
    form = SiteForm(rp)
    PageModelObject = Site.objects
    PageModel = "site"
    datas = PageModelObject.all().order_by('id')
    Update = False

    if delete== 0 and delete!= None:
        if id == 0 and id != None:
            site = Site()
            message = SuccessSaveMessage(request)
        else:
            site = get_object_or_404(Site, id=id)
            form = SiteForm(rp or None, instance=site)
            datas = Site.objects.filter(pk=id)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                site.site = rpg('site')
                site.district = District.objects.get(pk=rpg('district'))
                site.save()
                messages.info(request, message)
                return HttpResponseRedirect(reverse('site'))
    else:
        try:
            Site.objects.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('site'))
    
    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'datas': datas, 'Update': Update, 'noFooterNav': True, })

@login_required
def Dash(request):
    rp = request.POST
    rpg = request.POST.get
    Stock = DrugStock.objects
    CamegServed = CamegDrugServed.objects
    IhServed = IhDrugServed.objects
    Patient = PatientDrugServed.objects
    Adjustment = DrugStockAdjustment.objects
    months = Month.objects.all()
    years = Year.objects.all()
    datas = Etats.objects.filter(amount=False).order_by("n")
    total_amount_datas = Etats.objects.filter(amount=True, total_amount = True)
    single_amount_datas = Etats.objects.filter(amount=True, single_amount = True)
    

    # try:
    #     total_amount_datas = Etats.objects.get(amount=True, total_amount = True)
    # except:
    #     total_amount_datas = 0
    # try:
    #     single_amount_datas = Etats.objects.get(amount=True, single_amount = True)
    # except:
    #     single_amount_datas = 0


    try:
        DashDate = VariousParameters.objects.filter(dash_type='dash')
    except:
        DashDate = None

    try:
        if rpg('year') != None and rpg('year') != "":
            dash_year = rpg('year')
        else:
            dash_year = VariousParameters.objects.get(dash_type='dash').year
    except:
        dash_year = None

    try:
        if rpg('month') != None and rpg('month') != "":
            dash_month = rpg('month')
        else:
            dash_month = VariousParameters.objects.get(dash_type='dash').month
    except:
        dash_month = None


    if rpg('data_filter') != "" and rpg('data_filter') != None:
        if rpg('year') != None and rpg('year') != "" and rpg('month') != None and rpg('month') != "":
            # last_month = get_previous_month(rpg('month'),'int')
            last_year = to_int(rpg('year')) - 1
            this_year = to_int(rpg('year'))
            this_month = to_int(rpg('month')) 
            
            Etats.objects.all().delete()
            DashDate.delete()

            dash = VariousParameters()
            dash.year = rpg('year')
            dash.month = rpg('month')
            dash.dash_type = 'dash'
            dash.save()
            
            try:
                max_drug_id = int(Drug.objects.filter(is_available = True).order_by("-id")[0].id)
            except:
                max_drug_id = 0

            try:
                cameg_total_amount_served_last_year = to_int(CamegServed.filter(date__year__lte = last_year).aggregate(Sum('total_amount'))['total_amount__sum'])
                cameg_total_amount_served_this_year = to_int(CamegServed.filter(date__year = this_year, date__month__lte = this_month).aggregate(Sum('total_amount'))['total_amount__sum'])
                cameg_total_amount_served = cameg_total_amount_served_last_year + cameg_total_amount_served_this_year
                cameg_total_amount_served_this_month = to_int(CamegServed.filter(date__year = this_year, date__month = this_month).aggregate(Sum('total_amount'))['total_amount__sum'])

                ih_total_amount_served_last_year = to_int(IhServed.filter(date__year__lte = last_year).aggregate(Sum('total_amount'))['total_amount__sum'])
                ih_total_amount_served_this_year = to_int(IhServed.filter(date__year = this_year, date__month__lte = this_month).aggregate(Sum('total_amount'))['total_amount__sum'])
                ih_total_amount_served = ih_total_amount_served_last_year + ih_total_amount_served_this_year
                ih_total_amount_served_this_month = to_int(IhServed.filter(date__year = this_year, date__month = this_month).aggregate(Sum('total_amount'))['total_amount__sum'])
            
                total_etat = Etats()
                total_etat.cameg_served = cameg_total_amount_served
                total_etat.ih_served = ih_total_amount_served
                total_etat.amount = True
                total_etat.total_amount = True
                total_etat.save()

                single_etat = Etats()
                single_etat.cameg_served = cameg_total_amount_served_this_month
                single_etat.ih_served = ih_total_amount_served_this_month
                single_etat.amount = True
                single_etat.single_amount = True
                single_etat.save()
            except:
                pass

            for i in range(1, max_drug_id + 1):
                try:
                    etat = Etats()
                    ##############################################################################################################################
                    cameg_stock_until_last_year = to_int(Stock.filter(date__year__lte = last_year, drug_supplier=1, drug = i).aggregate(Sum('stock_quantity'))['stock_quantity__sum'])
                    cameg_stock_this_year = to_int(Stock.filter(date__year = this_year, date__month__lte = this_month, drug_supplier=1, drug = i).aggregate(Sum('stock_quantity'))['stock_quantity__sum'])
                    # cameg_stock_this_month = to_int(Stock.filter(date__year = this_year, date__month = this_month, drug_supplier=1, drug = i).aggregate(Sum('stock_quantity'))['stock_quantity__sum'])
                    cameg_stock_global = cameg_stock_until_last_year + cameg_stock_this_year
                    #####################
                    # cameg_stock_adjustment_until_last_year = to_int(Adjustment.filter(date__year__lte = last_year, drug_source='cameg', drug = i).aggregate(Sum('stock_adjustment_quantity'))['stock_adjustment_quantity__sum'])
                    # cameg_stock_adjustment_this_year = to_int(Adjustment.filter(date__year = this_year, date__month__lte = this_month, drug_source='cameg', drug = i).aggregate(Sum('stock_adjustment_quantity'))['stock_adjustment_quantity__sum'])
                    # cameg_stock_adjustment_this_month = to_int(Adjustment.filter(date__year = this_year, date__month = this_month, drug_source='cameg', drug = i).aggregate(Sum('stock_adjustment_quantity'))['stock_adjustment_quantity__sum'])
                    cameg_stock_adjustment_global = cameg_stock_until_last_year + cameg_stock_this_year
                    #####################
                    cameg_served_until_last_year = to_int(CamegServed.filter(date__year__lte = last_year, drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    cameg_served_this_year = to_int(CamegServed.filter(date__year = this_year, date__month__lte = this_month, drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    cameg_served_this_month = to_int(CamegServed.filter(date__year = this_year, date__month = this_month, drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    cameg_served_global = cameg_served_until_last_year + cameg_served_this_year
                    #####################
                    # cameg_patient_served_until_last_year = to_int(Patient.filter(date__year__lte = last_year, quantity_source='cameg', drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    # cameg_patient_served_this_year = to_int(Patient.filter(date__year = this_year, date__month__lte = this_month, quantity_source='cameg', drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    cameg_patient_served_this_month = to_int(Patient.filter(date__year = this_year, date__month = this_month, quantity_source='cameg', drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    cameg_patient_served_global = cameg_stock_until_last_year + cameg_stock_this_year
                    ##############################################################################################################################
                    ih_stock_until_last_year = to_int(Stock.filter(date__year__lte = last_year, drug = i).exclude(drug_supplier='1').aggregate(Sum('stock_quantity'))['stock_quantity__sum'])
                    ih_stock_this_year = to_int(Stock.filter(date__year = this_year, date__month__lte = this_month, drug = i).exclude(drug_supplier='1').aggregate(Sum('stock_quantity'))['stock_quantity__sum'])
                    # ih_stock_this_month = to_int(Stock.filter(date__year = this_year, date__month = this_month, drug = i).exclude(drug_supplier='1').aggregate(Sum('stock_quantity'))['stock_quantity__sum'])
                    ih_stock_global = ih_stock_until_last_year + ih_stock_this_year
                    #####################
                    ih_stock_adjustment_until_last_year = to_int(Adjustment.filter(date__year__lte = last_year, drug_source='ih', drug = i).aggregate(Sum('stock_adjustment_quantity'))['stock_adjustment_quantity__sum'])
                    ih_stock_adjustment_this_year = to_int(Adjustment.filter(date__year = this_year, date__month__lte = this_month, drug_source='ih', drug = i).aggregate(Sum('stock_adjustment_quantity'))['stock_adjustment_quantity__sum'])
                    # ih_stock_adjustment_this_month = to_int(Adjustment.filter(date__year = this_year, date__month = this_month, drug_source='ih', drug = i).aggregate(Sum('stock_adjustment_quantity'))['stock_adjustment_quantity__sum'])
                    ih_stock_adjustment_global = ih_stock_adjustment_until_last_year + ih_stock_adjustment_this_year
                    #####################
                    ih_served_until_last_year = to_int(IhServed.filter(date__year__lte = last_year, drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    ih_served_this_year = to_int(IhServed.filter(date__year = this_year, date__month__lte = this_month, drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    ih_served_this_month = to_int(IhServed.filter(date__year = this_year, date__month = this_month, drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    ih_served_global = ih_served_until_last_year + ih_served_this_year
                    #####################
                    ih_patient_served_until_last_year = to_int(Patient.filter(date__year__lte = last_year, quantity_source='ih', drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    ih_patient_served_this_year = to_int(Patient.filter(date__year = this_year, date__month__lte = this_month, quantity_source='ih', drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    ih_patient_served_this_month = to_int(Patient.filter(date__year = this_year, date__month = this_month, quantity_source='ih', drug = i).aggregate(Sum('quantity_served'))['quantity_served__sum'])
                    ih_patient_served_global = ih_patient_served_until_last_year + ih_patient_served_this_year
                    ##############################################################################################################################
                    cameg_real_stock = cameg_stock_global + cameg_stock_adjustment_global - (cameg_served_global - cameg_served_this_month) - (cameg_patient_served_global - cameg_patient_served_this_month) 
                    cameg_stock_remaining = cameg_real_stock - cameg_served_this_month - cameg_patient_served_this_month 
                    #####################
                    ih_real_stock = ih_stock_global + ih_stock_adjustment_global - (ih_served_global - ih_served_this_month) - (ih_patient_served_global - ih_patient_served_this_month) 
                    ih_stock_remaining = ih_real_stock - ih_served_this_month - ih_patient_served_this_month 
                    #####################
                    if cameg_stock_remaining > 0 or ih_stock_remaining > 0:
                        drug_situation = situation(Drug.objects.get(pk=i).expiry_date, substract_day_month_year(Drug.objects.get(pk=i).expiry_date, 'S3M'))
                    else:
                        drug_situation = ""
                    
                    etat.n = i
                    etat.drug = Drug.objects.get(pk=i)
                    etat.cameg_stock = cameg_real_stock
                    # etat.new_cameg_stock = cameg_stock_this_month + cameg_stock_adjustment_this_month
                    etat.ih_stock = to_int(ih_real_stock)
                    # etat.new_ih_stock =  ih_stock_this_month + ih_stock_adjustment_this_month
                    etat.cameg_served = cameg_served_this_month
                    etat.ih_served = ih_served_this_month
                    etat.patient_cameg_served = cameg_patient_served_this_month
                    etat.patient_ih_served = ih_patient_served_this_month
                    etat.cameg_stock_remaining = cameg_stock_remaining
                    etat.ih_stock_remaining = ih_stock_remaining
                    etat.expiry_date = Drug.objects.get(pk=i).expiry_date
                    etat.situation = drug_situation
                    etat.save()
                except:
                    pass
        else:
            datas = None
            messages.error(request, DateErrorMessage(request))
        return HttpResponseRedirect(reverse('dash'))
    return render(request, 'reports/dash.html', {'datas': datas, 'dash_year': dash_year, 'dash_month': dash_month, 'months': months, 'years': years, 'total_amount_datas':total_amount_datas, 'single_amount_datas':single_amount_datas, 'range': range(1, 3, 1)})

@login_required
def ServedEtat(request):
    rp = request.POST
    rpg = request.POST.get
    years = Year.objects.all()
    districts = District.objects.all()
    datas = ServedEtats.objects.filter(amount=False).order_by("n")
    datas_amount = ServedEtats.objects.filter(amount=True)
    DashDate = VariousParameters.objects.filter(dash_type='dashS')
    try:
        sites = Site.objects.filter(district=rpg('district'))
    except:
        sites = None
    try:
        dash_year = return_if_or_else(rpg('year'),VariousParameters.objects.get(dash_type='dashS').year)
    except:
        dash_year = None
    try:
        dash_district = return_if_or_else(rpg('district'),VariousParameters.objects.get(dash_type='dashS').district.id)
    except:
        dash_district = None
    try:
        dash_site = return_if_or_else(rpg('site'),VariousParameters.objects.get(dash_type='dashS').site.id)
    except:
        dash_site = None
    try:
        dash_source = return_if_or_else(rpg('data_source'),VariousParameters.objects.get(dash_type='dashS').data_source)
    except:
        dash_source = None


    if rpg('data_filter') != "" and rpg('data_filter') != None:
        if rpg('year') != None and rpg('year') != "":
            ServedEtats.objects.all().delete()
            DashDate.delete()

            dash = VariousParameters()
            dash.data_source = rpg('data_source')
            
            dash.year = return_if_or_else(rpg('year'), None)
            try:
                dash.district = District.objects.get(pk=rpg('district'))
            except:
                pass
            try:
                dash.site = Site.objects.get(pk=rpg('site'))
            except:
                pass
            dash.dash_type = 'dashS'
            dash.save()


            _district = getFilterByQCalculation(rpg('district'), Q(district=rpg('district')), Q(district__isnull=False))
            _year = getFilterByQCalculation(rpg('year'), Q(date__year=rpg('year')), Q(date__isnull=False))
            _site = getFilterByQCalculation(rpg("site"), Q(site=rpg("site")), Q(site__isnull=False))
            camegDataObject = CamegDrugServed.objects.filter(_year, _district, _site)
            ihDataObject = IhDrugServed.objects.filter(_year, _district, _site)
            max_drug_id = int(Drug.objects.all().order_by("-id")[0].id)
            line_num = 0
            
            if rpg('data_source') == "cameg":
                DataObject = camegDataObject
            elif rpg('data_source') == "ih":
                DataObject = ihDataObject
            else:
                DataObject = None

            if DataObject != None:
                try:
                    etat = ServedEtats()
                    etat.jan = to_int(DataObject.filter(date__month="01").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.fev = to_int(DataObject.filter(date__month="02").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.mar = to_int(DataObject.filter(date__month="03").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.avr = to_int(DataObject.filter(date__month="04").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.mai = to_int(DataObject.filter(date__month="05").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.jun = to_int(DataObject.filter(date__month="06").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.jul = to_int(DataObject.filter(date__month="07").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.aou = to_int(DataObject.filter(date__month="08").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.sep = to_int(DataObject.filter(date__month="09").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.ocb = to_int(DataObject.filter(date__month="10").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.nov = to_int(DataObject.filter(date__month="11").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.dec = to_int(DataObject.filter(date__month="12").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.total = to_int(DataObject.filter(date__month__gte="01", date__month__lte="12").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.amount = True
                    etat.save()
                    
                    for i in range(1, max_drug_id +1):
                        etat = ServedEtats()
                        if Drug.objects.filter(pk = i, is_available=True).exists():
                            line_num += 1 
                            etat.n = line_num
                            etat.drug = Drug.objects.get(pk=i)
                            etat.jan = to_int(DataObject.filter(drug = i).filter(date__month = "01").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.fev = to_int(DataObject.filter(drug = i).filter(date__month = "02").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.mar = to_int(DataObject.filter(drug = i).filter(date__month = "03").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.avr = to_int(DataObject.filter(drug = i).filter(date__month = "04").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.mai = to_int(DataObject.filter(drug = i).filter(date__month = "05").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.jun = to_int(DataObject.filter(drug = i).filter(date__month = "06").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.jul = to_int(DataObject.filter(drug = i).filter(date__month = "07").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.aou = to_int(DataObject.filter(drug = i).filter(date__month = "08").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.sep = to_int(DataObject.filter(drug = i).filter(date__month = "09").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.ocb = to_int(DataObject.filter(drug = i).filter(date__month = "10").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.nov = to_int(DataObject.filter(drug = i).filter(date__month = "11").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.dec = to_int(DataObject.filter(drug = i).filter(date__month = "12").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.total = to_int(DataObject.filter(drug = i).filter(date__month__gte="01", date__month__lte="12").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.amount = False
                            etat.save()
                        else:
                            pass
                except:
                    pass  
            else:
                try:
                    etat = ServedEtats()
                    etat.jan = to_int(camegDataObject.filter(date__month="01").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="01").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.fev = to_int(camegDataObject.filter(date__month="02").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="02").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.mar = to_int(camegDataObject.filter(date__month="03").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="03").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.avr = to_int(camegDataObject.filter(date__month="04").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="04").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.mai = to_int(camegDataObject.filter(date__month="05").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="05").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.jun = to_int(camegDataObject.filter(date__month="06").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="06").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.jul = to_int(camegDataObject.filter(date__month="07").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="07").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.aou = to_int(camegDataObject.filter(date__month="08").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="08").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.sep = to_int(camegDataObject.filter(date__month="09").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="09").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.ocb = to_int(camegDataObject.filter(date__month="10").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="10").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.nov = to_int(camegDataObject.filter(date__month="11").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="11").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.dec = to_int(camegDataObject.filter(date__month="12").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month="12").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.total = to_int(camegDataObject.filter(date__month__gte="01", date__month__lte="12").aggregate(Sum('total_amount'))['total_amount__sum']) + to_int(ihDataObject.filter(date__month__gte="01", date__month__lte="12").aggregate(Sum('total_amount'))['total_amount__sum'])
                    etat.amount = True
                    etat.save()
                    
                    for i in range(1, max_drug_id +1):
                        etat = ServedEtats()
                        if Drug.objects.filter(pk = i, is_available=True).exists():
                            line_num += 1 
                            etat.n = line_num
                            etat.drug = Drug.objects.get(pk=i)
                            etat.jan = to_int(camegDataObject.filter(drug = i).filter(date__month = "01").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "01").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.fev = to_int(camegDataObject.filter(drug = i).filter(date__month = "02").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "02").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.mar = to_int(camegDataObject.filter(drug = i).filter(date__month = "03").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "03").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.avr = to_int(camegDataObject.filter(drug = i).filter(date__month = "04").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "04").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.mai = to_int(camegDataObject.filter(drug = i).filter(date__month = "05").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "05").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.jun = to_int(camegDataObject.filter(drug = i).filter(date__month = "06").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "06").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.jul = to_int(camegDataObject.filter(drug = i).filter(date__month = "07").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "07").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.aou = to_int(camegDataObject.filter(drug = i).filter(date__month = "08").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "08").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.sep = to_int(camegDataObject.filter(drug = i).filter(date__month = "09").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "09").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.ocb = to_int(camegDataObject.filter(drug = i).filter(date__month = "10").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "10").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.nov = to_int(camegDataObject.filter(drug = i).filter(date__month = "11").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "11").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.dec = to_int(camegDataObject.filter(drug = i).filter(date__month = "12").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month = "12").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.total = to_int(camegDataObject.filter(drug = i).filter(date__month__gte="01", date__month__lte="12").aggregate(Sum('quantity_served'))['quantity_served__sum']) + to_int(ihDataObject.filter(drug = i).filter(date__month__gte="01", date__month__lte="12").aggregate(Sum('quantity_served'))['quantity_served__sum'])
                            etat.amount = False
                            etat.save()
                        else:
                            pass
                except:
                    pass

        else:
            pass 
            # datas = datas_amount = None
            # messages.error(request, YearErrorMessage(request))
        return HttpResponseRedirect(reverse('dashS'))

    return render(request, 'reports/dash_served.html', {'datas': datas,'datas_amount': datas_amount, 'dash_year': dash_year, 'dash_district': dash_district, 'dash_site': dash_site, 'years': years, 'districts': districts, 'sites': sites, 'dash_source': dash_source, 'range': range(1, 3, 1)})

@login_required
def TranslationDataCreateUpdateDelete(request, id=0, delete=0):
    rp = request.POST
    rpg = request.POST.get
    form = TranslationForm(rp)
    PageModelObject = Translation.objects
    PageModel = "translation"
    datas = PageModelObject.all().order_by('-id')
    Update = False

    if delete== 0 and delete!= None:
        if id == 0 and id != None:
            translation = Translation()
            message = SuccessSaveMessage(request)
        else:
            translation = get_object_or_404(Translation, id=id)
            form = TranslationForm(rp or None, instance=translation)
            datas = PageModelObject.filter(pk=id)
            message = SuccessUpdateMessage(request)
            Update = True

        if rpg('save') != "" and rpg('save') != None:
            if form.is_valid():
                # data_en = PageModelObject.filter(trans_en=rpg('trans_en')).exists()
                data_fr = PageModelObject.filter(trans_fr=rpg('trans_fr')).exists()

                # if data_en and rpg('save') != "" and rpg('save') != None:
                #     messages.error(request, "La traduction existe déja")
                if data_fr and rpg('save') == "enrégistrer" or data_fr and rpg('save') == "save":
                    messages.error(request, trans("Cette Entrée Existe déjà", request))
                else:
                    translation.acronym_fr = rpg('acronym_fr')
                    translation.acronym_en = rpg('acronym_en')
                    translation.trans_fr = rpg('trans_fr')
                    translation.trans_en = rpg('trans_en')
                    translation.save()
                    messages.info(request, message)
                    return HttpResponseRedirect(reverse('translation'))
    else:
        try:
            PageModelObject.filter(pk=delete).delete()
            messages.info(request, SuccessDeleteMessage(request))
        except IntegrityError:
            messages.error(request,IntegrityErrorMessage(request))
        return HttpResponseRedirect(reverse('translation'))
    
    paginate = Pagination(request, datas)

    return render(request, 'pages/' + PageModel + '.html', {'form': form, 'Update': Update, 'noFooterNav': True, 'text_transform': True, 'paginate': paginate})

def LanguageUpdate(request):
    language = request.POST.get('language')
    url = request.POST.get('url')
    if language != None and language != "":
        user_exist = VariousParameters.objects.filter(user_language=request.user.id).exists()
        data_exist = VariousParameters.objects.filter(user_language=request.user.id,language = language).exists()

        if user_exist:
            if data_exist:
                pass
            else:
                lg = get_object_or_404(VariousParameters, user_language=request.user.id)
                lg.language = language
                lg.save()
                messages.info(request,LanguageChangedMessage(request))
        else:
            lg= VariousParameters()
            lg.user_language = User.objects.get(pk=request.user.id)
            lg.language = language
            lg.save()
            messages.info(request,LanguageChangedMessage(request))
    response = HttpResponseRedirect(url)
    response.set_cookie(key='user_id', value=request.user.id)
    return response
