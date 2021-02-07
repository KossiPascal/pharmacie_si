import hashlib
from django import template
from django.contrib.auth.models import User
from django.utils import formats
from datetime import datetime
from med.models import Drug, Month, Year, District, Site, Translation, VariousParameters, CamegDrugServed, DrugStock, IhDrugServed, PatientDrugServed, DrugStockAdjustment

from django.http.response import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.urls.base import reverse
from django.contrib import messages

register = template.Library()


# def set_cookie(response, key, value, days_expire=7):
#     import datetime as dt

#     if days_expire is None:
#         max_age = 365 * 24 * 60 * 60  # one year
#     else:
#         max_age = days_expire * 24 * 60 * 60
#     expires = dt.datetime.strftime(dt.datetime.utcnow() + dt.timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
#     response.set_cookie(
#         key,
#         value,
#         max_age=max_age,
#         expires=expires,
#         domain=settings.SESSION_COOKIE_DOMAIN or None,
#         secure=settings.SESSION_COOKIE_SECURE or None,
#     )
 

@register.filter(is_safe=True, name="available_quantity")
def available_quantity(drug_id, source):
    """available_quantity for drug"""
    # drug = Drug.objects.all()
    from django.db.models import Sum
    
    if source == 'cameg':
        cameg = CamegDrugServed.objects.filter(drug = drug_id).aggregate(Sum('quantity_served'))['quantity_served__sum']
        patient_cameg = PatientDrugServed.objects.filter(drug = drug_id, quantity_source = 'cameg').aggregate(Sum('quantity_served'))['quantity_served__sum'] 
        stock_cameg= DrugStock.objects.filter(drug = drug_id, drug_supplier = 1).aggregate(Sum('stock_quantity'))['stock_quantity__sum']
        stock_adjustement_cameg = DrugStockAdjustment.objects.filter(drug = drug_id, drug_source = 'cameg').aggregate(Sum('stock_adjustment_quantity'))['stock_adjustment_quantity__sum']
        return to_int(stock_cameg) + to_int(stock_adjustement_cameg) - to_int(cameg) - to_int(patient_cameg)
    elif source == 'ih':
        ih = IhDrugServed.objects.filter(drug = drug_id).aggregate(Sum('quantity_served'))['quantity_served__sum']
        patient_ih = PatientDrugServed.objects.filter(drug = drug_id, quantity_source = 'ih').aggregate(Sum('quantity_served'))['quantity_served__sum']
        stock_ih= DrugStock.objects.filter(drug = drug_id).exclude(drug_supplier = 1).aggregate(Sum('stock_quantity'))['stock_quantity__sum']
        stock_adjustement_ih = DrugStockAdjustment.objects.filter(drug = drug_id, drug_source = 'ih').aggregate(Sum('stock_adjustment_quantity'))['stock_adjustment_quantity__sum']
        return to_int(stock_ih) + to_int(stock_adjustement_ih) - to_int(ih) - to_int(patient_ih)
    else:
        return 0


@register.filter(is_safe=True, name="get_items")
def get_items(value, arg):
    """get_items."""
    data = value[0]
    return data.items()

    
@register.filter(is_safe=True, name="substract")
def substract(x,y):
    return x - y

@register.filter(is_safe=True, name="aggragate_sum")
def aggragate_sum(value1, value2):
    """show month label."""
    if value1 != None and value1 != "" and value2 != None and value2 != "":
        d = to_int(value1) + to_int(value2)
        return d
    return ""

@register.filter(is_safe=True, name="get_label")
def get_label(value, arg):
    """show month label."""
    if value != None and value != "":
        v = int(float(value))
        try:
            if arg == 'month':
                return Month.objects.get(pk=v).month
            if arg == 'year':
                return Year.objects.get(pk=v).year
            if arg == 'drug':
                return Drug.objects.get(pk=v).drug
            if arg == 'district':
                return District.objects.get(pk=v).district
            if arg == 'site':
                return Site.objects.get(pk=v).site
            return ""
        except:
            return ""
    return ""

@register.filter(is_safe=True, name="year_label")
def year_label(value, args=""):
    """show year label."""
    if value != None and value != "":
        v = int(float(value))
        try:
            y = Year.objects.get(pk=v).month
            return y
        except:
            return ""
    return ""

@register.filter(is_safe=True, name="to_int")
def to_int(value):
    """Convert to integer."""
    if value == None or value == "":
        return 0
    return int(float(value))

@register.filter(is_safe=True, name="previous_month")
def get_previous_month(value, arg = ''):
    """Convert to integer."""
    try:
        if arg == "int":
            if to_int(value) == 1:
                return 12
            else:
                v = to_int(value) - 1
                return v
        else:
            if to_int(value) == 1:
                return str(12)
            else:
                v = to_int(value) - 1
                if v < 10:
                    return '0' + str(v)
                else:
                    return str(v)
            
    except:
        return ""

@register.filter(is_safe=True, name="meg_by_arg")
def meg_by_arg(id):
    try:
        return Drug.objects.get(pk=id)
    except:
        return 0

@register.filter(is_safe=True, name="separate_millier")
def separate_millier(n, sep=" "):
    """separate data with arg"""
    if n == None or n == "":
        return 0
    s = str(n)
    l = len(s)
    d = l/3
    for i in range(1, to_int(d)+1):
        s = s[:l-3*i] + sep + s[l-3*i:]
    return s

@register.filter(is_safe=True, name="url_matched")
def url_matched(url, arg=""):
    """Return True if split url matched arg"""
    try:
        page1 = url.split('/')[2]
        try:
            page2 = url.split('/')[3]
        except:
            page2 = ""
        if arg != "":
            if page1 == arg or page2 == arg and page2 != "":
                return True 
            else:
                return False
        else:
            if page2 != "":
                return page2
            else:
                return page1
    except:
        return False

@register.filter(is_safe=True, name="time_diff")
def time_diff(value):
    """Convert to integer and add 5"""
    ds = int(formats.date_format(datetime.now(), 'YmdHis'))
    de = int(formats.date_format(value, 'YmdHis'))
    r = ds - de
    return r
    return int(float(value)) - 5

@register.filter(is_safe=True, name="convert_date")
def convert_date(date_value, args='en'):
    """ Return date in all  with args  """
    if date_value == None or date_value == "":
        return ""

    date_str = str(date_value)
    arg = str(args)

    try:
        if int(len(date_str)) == 7:
            date = datetime.strptime(date_str, "%Y-%m")
        elif int(len(date_str)) == 10:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        elif int(len(date_str)) == 13:
            date = datetime.strptime(date_str, "%Y-%m-%d %H")
        elif int(len(date_str)) == 16:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        elif int(len(date_str)) == 19:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        elif int(len(date_str)) >= 21 and int(len(date_str)) <= 26:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
        else:
            date = 0
    except:
        date = 0


    if date != 0:
        """ Return True data """
        if int(date.month) < 10:
            month = "0" + str(date.month)
        else:
            month = str(date.month)

        if int(date.day) < 10:
            day = "0" + str(date.day)
        else:
            day = str(date.day)

        if arg == "FDTE":
            """ Return full date with time in English format """
            return str(date.year) + "-" + str(month) + "-" + str(day) + str(date.hour) + ":" + str(date.minute) + ":" + str(date.second)
        elif arg == "FDTF":
            """ Return full date with time in french format """
            return str(day) + "/" + str(month) + "/" + str(date.year) + str(date.hour) + ":" + str(date.minute) + ":" + str(date.second)
        elif arg == "fr" or arg == "(fr)":
            """ Return date in french format """
            return str(day) + "/" + str(month) + "/" + str(date.year)
        elif arg == "Y":
            """ Return Year """
            return str(date.year)
        elif arg == "m":
            """ Return Str Month Id """
            return str(month)
        elif arg == "mFr":
            """ Return Int Month Id """
            return int(date.month)
        elif arg == "M":
            """ Return Month Label """
            return get_label(str(month), 'month')
        elif arg == "d":
            """ Return day """
            return str(day)
        elif arg == "H":
            """ Return Hour """
            return str(date.hour)
        elif arg == "mm":
            """ Return Minute """
            return str(date.minute)
        elif arg == "S":
            """ Return Second """
            return str(date.second)
        elif arg == "f":
            """ Return Microsecond """
            return str(date.microsecond)
        elif arg == "FH":
            """ Return full Hour """
            return str(date.hour) + ":" + str(date.minute) + ":" + str(date.second)
        elif arg == "en" or arg == "(en)":
            """ Return date in english format """
            return str(date.year) + "-" + str(month) + "-" + str(day)
        else:
            """ Return date in english format """
            return str(date.year) + "-" + str(month) + "-" + str(day)


    else:
        """ Return False data """
        return ""

@register.filter(is_safe=True, name="substract_day_month_year")
def substract_day_month_year(date, arg=''):
    """ substract day(D) or month(M) or year(Y) """
    import datetime
    from dateutil.relativedelta import relativedelta
    if date != None and date != "":
        if len(arg) == 3:
            if arg[0] == "A" or arg[0] =="S":
                if arg[2] == "D" or arg[2] == "M" or arg[2] == "Y":
                    v = to_int(arg[1])
                    d1 = datetime.datetime.strptime(str(date), "%Y-%m-%d")

                    if arg[0] == "A":  # A=Add (+)      S=Substract (-)
                        if arg[2] == "D":
                            d2 = d1 + relativedelta(days=v)
                        elif arg[2] == "M":
                            d2 = d1 + relativedelta(months=v)
                        elif arg[2] == "Y":
                            d2 = d1 + relativedelta(years=v)
                        else:
                            return ""
                    else:
                        if arg[2] == "D":
                            d2 = d1 - relativedelta(days=v)
                        elif arg[2] == "M":
                            d2 = d1 - relativedelta(months=v)
                        elif arg[2] == "Y":
                            d2 = d1 - relativedelta(years=v)
                        else:
                            return "" 


                    return datetime.datetime.strftime(d2, "%Y-%m-%d")
    return ""       

@register.filter(is_safe=True, name="situation")
def situation(real_date, date_changed, ):
    import datetime
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    real_date = str(real_date)
    date_changed = str(date_changed)

    if date >= date_changed and date < real_date:
        return 'à vider'
        dash_style = 'background-color:#bf9918; color:white; font-size:15px;padding:5px;'
    elif date < real_date:
        return 'OK'
        dash_style = 'color:green;'
    elif date >= date_changed and date > real_date and real_date != '':
        return 'Périmé'
        dash_style = 'background-color:red; color:white;padding:5px;'
    else:
        return ''

@register.filter(is_safe=True, name="situation_style")
def situation_style(data):
    if data == 'à vider':
        return 'background-color:#bf9918; color:white; font-size:15px;padding:0px 5px;'
    elif data == 'OK':
        return 'color:green;'
    elif data == 'Périmé':
        return 'background-color:red; color:white;padding:0px 5px;'
    else:
        return ""

@register.filter(is_safe=True, name="trans")
def trans(value, request):
    """translate params given into english or french"""
    if value != None and value != "":
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = request.COOKIES.get('user_id')
        try:
            lg = VariousParameters.objects.get(user_language=user_id).language
            if Translation.objects.filter(trans_en=value).exists():
                data_en = Translation.objects.get(trans_en=value)
                if data_en != None and data_en != "":
                    if lg == 'en' or lg == 'english' or lg == 'anglais':
                        return data_en.trans_en
                    elif lg == 'fr' or lg == 'french' or lg == 'français':
                        return data_en.trans_fr
                    else:
                        return data_en.trans_en
                return value
            if Translation.objects.filter(trans_fr=value).exists():
                data_fr = Translation.objects.get(trans_fr=value)
                if data_fr != None and data_fr != "":
                    if lg == 'en' or lg == 'english' or lg == 'anglais':
                        return data_fr.trans_en
                    elif lg == 'fr' or lg == 'french' or lg == 'français':
                        return data_fr.trans_fr
                    else:
                        return data_fr.trans_en
                return value
            return value
        except:
            if Translation.objects.filter(trans_en=value).exists():
                data_en = Translation.objects.get(trans_en=value)
                if data_en != None and data_en != "":
                    return data_en.trans_en
                return value
            if Translation.objects.filter(trans_fr=value).exists():
                data_fr = Translation.objects.get(trans_fr=value)
                if data_fr != None and data_fr != "":
                    return data_fr.trans_en
                return value
            return value
    return ""

@register.filter(is_safe=True, name="getTransSigle")
def getTransSigle(value, request):
    """get english or french acronym of params given"""
    if value != None and value != "":
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = request.COOKIES.get('user_id')
        try:
            if VariousParameters.objects.filter(user_language=user_id).exists():
                lg = VariousParameters.objects.get(user_language=user_id).language
                if Translation.objects.filter(trans_en=value).exists():
                    data_en = Translation.objects.get(trans_en=value)
                    if data_en != None and data_en != "":
                        if lg == 'en' or lg == 'english' or lg == 'anglais':
                            if data_en.acronym_en != None and data_en.acronym_en != "":
                                return data_en.acronym_en
                        if lg == 'fr' or lg == 'french' or lg == 'français':
                            if data_en.acronym_fr != None and data_en.acronym_fr != "":
                                return data_en.acronym_fr
                    return value

                if Translation.objects.filter(trans_fr=value).exists():
                    data_fr = Translation.objects.get(trans_fr=value)
                    if data_fr != None and data_fr != "":
                        if lg == 'fr' or lg == 'french' or lg == 'français':
                            if data_fr.acronym_fr != None and data_fr.acronym_fr != "":
                                return data_fr.acronym_fr
                        if lg == 'en' or lg == 'english' or lg == 'anglais':
                            if data_fr.acronym_en != None and data_fr.acronym_en != "":
                                return data_fr.acronym_en
                    return value
                return value
            else:
                if Translation.objects.filter(trans_en=value).exists():
                    data_en = Translation.objects.get(trans_en=value)
                    if data_en != None and data_en != "":
                        if data_en.acronym_en != None and data_en.acronym_en != "":
                            return data_en.acronym_en
                    return value
                if Translation.objects.filter(trans_fr=value).exists():
                    data_fr = Translation.objects.get(trans_fr=value)
                    if data_fr != None and data_fr != "":
                        if data_fr.acronym_fr != None and data_fr.acronym_fr != "":
                            return data_fr.acronym_en
                    return value
                return value
        except:
            if Translation.objects.filter(trans_en=value).exists():
                data_en = Translation.objects.get(trans_en=value)
                if data_en != None and data_en != "":
                    if data_en.acronym_en != None and data_en.acronym_en != "":
                        return data_en.acronym_en
                return value
            if Translation.objects.filter(trans_fr=value).exists():
                data_fr = Translation.objects.get(trans_fr=value)
                if data_fr != None and data_fr != "":
                    if data_fr.acronym_fr != None and data_fr.acronym_fr != "":
                        return data_fr.acronym_en
                return value
            return value
    return ""
    
@register.filter(is_safe=True, name="siteLanguage")
def siteLanguage(website, request):
    """get language of systèm choosen"""
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = request.COOKIES.get('user_id')

    if user_id != None and user_id != "":
            try:
                if VariousParameters.objects.filter(user_language=user_id).exists():
                    lg = VariousParameters.objects.get(user_language=user_id).language
                    if lg == 'en' or lg == 'english' or lg == 'anglais':
                        return '(en)'
        
                    if lg == 'fr' or lg == 'french' or lg == 'français':
                        return '(fr)'
                else:
                    return '(en)'
            except:
                return ''          
    else:
        return '(en)'

def UserIsConnect(request):
    if request.user.is_authenticated:
        messages.info(request, trans("Vous Êtes Déja Connecté!", request))
        return True
    else:
        if request.GET.get('next') != None and request.GET.get('next') != "":
            messages.error(request, trans("Authentifier Vous Pour Accéder A La Page Demandée!", request))
        else:
            pass
        return False




def sha1Hash(value1, value2='', value3=''):
    """algorithm = sha1"""
    if value2 == '' and value3 == '':
        hash = hashlib.sha1((str(value1)).encode()).hexdigest()
    else:
        hash = hashlib.sha1((str(value1) + str(value2) + str(value3)).encode()).hexdigest()
    return hash


def sha256Hash(value1, value2='', value3=''):
    """algorithm = sha256"""
    if value2 == '' and value3 == '':
        hash = hashlib.sha256((str(value1)).encode()).hexdigest()
    else:
        hash = hashlib.sha256((str(value1) + str(value2) + str(value3)).encode()).hexdigest()
    return hash


def MD5Hash(value1, value2='', value3=''):
    """algorithm = md5"""
    if value2 == '' and value3 == '':
        hash = hashlib.md5((str(value1)).encode()).hexdigest()
    else:
        hash = hashlib.md5((str(value1) + str(value2) + str(value3)).encode()).hexdigest()
    return hash








def SuccessSaveMessage(request):
    return trans("Sauvegardé avec Succès!", request)

def SuccessUpdateMessage(request):
    return trans("Modifié avec Succès!", request)

def SuccessDeleteMessage(request):
    return trans("Supprimé avec Succès!", request)

def IntegrityErrorMessage(request):
    return trans("Action Impossible, Elément utilisé dans d'autres pages", request)

def SaisieErrorMessage(request):
    return trans("Erreur de Saisie! Veuillez Revérifier SVP !!!", request)

def PageNotFoundMessage(request):
    return trans("La Page demandée n'est pas disponible pour le moment", request)

def DateErrorMessage(request):
    return trans("Renseigné correctement les dates !", request)

def YearErrorMessage(request):
    return trans("Renseigné correctement l'année !", request)

def RequestHaveErrorMessage(request):
    return trans("La Requete demandée comporte des erreurs !", request)

def LanguageChangedMessage(request):
    return trans("Langue Changée", request)

def ParameterErrorMessage(request):
    return trans("Paramettre Non Pris En Charge !", request)

def LoggedInSuccessMessage(request):
    return trans("Vous vous êtes connecté avec Succès!", request)

def InactiveAccountMessage(request):
    return trans("Votre Compte est inactif! contacter votre administrateur SVP.", request)

def IncorectLoginInfosMessage(request):
    return trans("informations d'identification incorrectes. Réessayer!", request)

def RequireAuthenticateMessage(request):
    return trans("Authentification Requise", request)

def LogoutSuccessMessage(request):
    return trans("Vous Êtes Déconnecté!", request)
