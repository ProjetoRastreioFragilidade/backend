#from django.conf import settings
from ppsus_app.models import User

#if Account.objects.count() == 0:
#for user in settings.ADMINS:
username = 'teste'
password = 'bhr326126'
#print('Creating account for %s (%s)' % (username, email))
admin = User.objects.create_superuser(
    username=username, 
    password=password, 
    first_name='Bruno', 
    last_name='Rasteiro', 
    posto_id=1)
admin.is_active = True
admin.is_admin = True
admin.save()

print("#############")
print("Super User criado")
print(admin)
print("#############")

#else:
#    print('Admin accounts can only be initialized if no Accounts exist')