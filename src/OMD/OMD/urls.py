"""OMD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from OMDApp.views.accounts_view import (LoginView, LogOut, RegisterView, RegisterDogView, RegisterSingleDogView,
                                        ProfileView, EditProfileView, EditPasswordView, UserListView, UsersDogsListView)
from OMDApp.views.dogs_view import (DogListView, ProfileDogView, EditProfileDogView, RegisterAdoptionDogView,
                                    AdoptionDogListView, AdoptionDogListFilteredView, AdoptionDog, SwitchAdoptedDogView,
                                    AdoptedDogListView, HealthBookDogView, ClinicHistoryDogView)
from OMDApp.views.turns_view import (AskForTurn, ViewAcceptedTurns, ViewPendingTurns, AcceptTurn, RejectTurn,
                                     ViewMyTurns, CancelTurn, AttendTurnView, GenerateUrgencyView, AttendUrgencyView,
                                     NewUrgencyButtonView, Evaluation, ShowFinalizedTurn)
from OMDApp.views.donations_view import (RegisterDonation , ViewCampaigns, RegisterEvent , InsertCardView, ViewMyDonations,AllDonations,
                                         ViewFinalizedCampaigns, CampaignDonations)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Accounts
    path('register/', RegisterView, name='register'),
    path('registerdog/', RegisterDogView, name='registerDog'),
    path('registersingledog', RegisterSingleDogView, name='registerSingleDog'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOut, name='logout'),
    path('profile/', ProfileView, name='profile'),
    path('editprofile/', EditProfileView.as_view(), name='editProfile'),
    path('editpassword/', EditPasswordView.as_view(), name='editPassword'),
    
    # Dogs
    path('mydogs/', DogListView.as_view(), name='my_dogs'),
    path('dog/<int:dog_id>/', ProfileDogView, name='dog_profile'),
    path('profiledog', EditProfileDogView.as_view(), name='dog_edit_profile'),
    path('healthbookdog/<int:dog_id>/', HealthBookDogView, name='dog_health_book'),
    path('clinichistorydog/<int:dog_id>/', ClinicHistoryDogView, name='dog_clinic_history'),
    
    # Dogs - Adoption
    path('registeradoptiondog/', RegisterAdoptionDogView, name='register_adoption_dog'),
    path('adoptiondoglist/', AdoptionDogListView, name='adoption_dog_list'),
    path('adoptiondoglistfiltered/', AdoptionDogListFilteredView, name='adoption_dog_list_filtered'),
    path('adoptiondog/<int:dog_id>/', AdoptionDog, name='adoption_dogs'),
    path('adoptdogswitch/<int:dog_id>/', SwitchAdoptedDogView, name='adopt_dog_switch'),
    path('adopteddogs/', AdoptedDogListView, name='adopted_dogs'),

    # Turns
    path('askforturn/', AskForTurn, name='askForTurn'),
    path('pendingturns/', ViewPendingTurns, name='pendingTurns'),
    path('acceptedturns/', ViewAcceptedTurns, name='acceptedTurns'),
    path('myturns/', ViewMyTurns, name='myTurns'),
    path('acceptingTurn/<int:turn_id>/', AcceptTurn, name='acceptTurn'),
    path('rejectingTurn/<int:turn_id>/', RejectTurn, name='rejectTurn'),
    path('cancelingTurn/<int:turn_id>/', CancelTurn, name='cancelTurn'),
    path('attendTurnView/<int:turn_id>/', AttendTurnView, name='attendTurnView'),
    path('evaluation/<int:turn_id>/', Evaluation, name='evaluation'),
    path('showFturn/<int:turn_id>/', ShowFinalizedTurn, name='showFinalizedTurn'),

    # Turns - Urgency
    path('selectUrgency/', NewUrgencyButtonView, name='selectUrgency'),
    path('selectUser/', UserListView, name='selectUser'),
    path('selectUsersDog/<int:user_id>', UsersDogsListView, name='selectUsersDog'),
    path('register/<int:urgency>/', RegisterView, name='register'),
    path('registerdog/<int:urgency>/', RegisterDogView, name='registerDog'),
    path('generateUrgency/<int:dog_id>/', GenerateUrgencyView, name='generateUrgency'),
    path('attendUrgency/<int:turn_id>/', AttendUrgencyView, name='attendUrgency'),

    # Donations
    path('registerdonation/<int:campana_id>/',RegisterDonation,name='registerDonation'), #esta es la donacion
    path('viewcampaigns/',ViewCampaigns,name='viewCampaigns'),
    path('registerevent/',RegisterEvent,name='registerEvent'),
    path('mydonations/',ViewMyDonations, name='myDonations'),
    path('listdonations/',AllDonations, name='listDonations'),
    path('listcampaigndonations/<int:campana_id>/',CampaignDonations, name='listCampaignDonations'),
    path('listFdonations/',ViewFinalizedCampaigns, name='listFinalizedDonations'),
    path('introcard/', InsertCardView , name='insertCard')
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
