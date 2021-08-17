import adsk.core
from .Localization import localization as LC

app = adsk.core.Application.get()

# get user language prefernece from fusion and set locale for addin
def getUserLanguagePreference():
    #https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-b8af2def-f673-4cd4-baec-3c9912059547
    languageCode = app.preferences.generalPreferences.userLanguage

    if languageCode == 5:
        return 'de' #German
    elif languageCode == 3:
        return 'en' #English
    elif languageCode == 8:
        return 'ja' #Japanese
    elif languageCode == 0:
        return 'zh' #Chinese PRC

locale = getUserLanguagePreference()
LC.Localization(locale) 
_LCLZ = LC.Localization.getLocaleString