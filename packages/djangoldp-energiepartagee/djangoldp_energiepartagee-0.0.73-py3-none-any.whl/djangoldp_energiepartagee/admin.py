from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin
from djangoldp.models import Model
from djangoldp_energiepartagee.models import Actor, Contribution, Region, College, Regionalnetwork, Interventionzone, Legalstructure, Collegeepa, Paymentmethod, Profile, Integrationstep, Relatedactor

class EPModelAdmin(DjangoLDPAdmin):
    readonly_fields=('urlid',)


class ActorAdmin(EPModelAdmin):
    list_display = ('shortname', 'longname', 'updatedate', 'createdate')
    search_fields = ['shortname', 'longname']


class RelatedactorAdmin(EPModelAdmin):
    search_fields = ['actor__longname', 'actor__shortname', 'user__first_name', 'user__last_name', 'user__email']


class ContributionAdmin(EPModelAdmin):
    list_display = ('actor', 'year', 'updatedate', 'createdate')
    search_fields = ['actor__longname','actor__shortname']

admin.site.register(Actor, ActorAdmin)
admin.site.register(Contribution, ContributionAdmin)
admin.site.register(Region, EPModelAdmin)
admin.site.register(College, EPModelAdmin)
admin.site.register(Regionalnetwork, EPModelAdmin)
admin.site.register(Interventionzone, EPModelAdmin)
admin.site.register(Legalstructure, EPModelAdmin)
admin.site.register(Collegeepa, EPModelAdmin)
admin.site.register(Paymentmethod, EPModelAdmin)
admin.site.register(Profile, EPModelAdmin)
admin.site.register(Integrationstep, EPModelAdmin)
admin.site.register(Relatedactor, RelatedactorAdmin)
