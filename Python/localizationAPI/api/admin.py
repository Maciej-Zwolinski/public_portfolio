from django.contrib import admin


from api.models import IPLocalization, Currency


# Register your models here.

class IPLocalizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'url')
    raw_id_fields = ('currency', )


admin.site.register(IPLocalization, IPLocalizationAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code')


admin.site.register(Currency, CurrencyAdmin)
