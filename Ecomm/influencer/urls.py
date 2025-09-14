from django.urls import path
from .views import *
urlpatterns = [

    path('influencer/frzn/', InfluViewuu.as_view(), name='register'),

    path('backend/influencers/', influencer_list, name='influencer_list'),
    path('backend/influencer/profile/', influencer_profile_edit, name='influencer_profile_edit'),
    path('backend/influencers/add/', add_influencer, name='add_influencer'),
    path('backend/influencers/edit/<int:influencer_id>/', edit_influencer, name='edit_influencer'),
    path('backend/influencers/delete/<int:influencer_id>/', delete_influencer, name='delete_influencer'),
    path('backend/influencers/view/<int:influencer_id>/', view_influencer, name='view_influencer'),
    path('backend/influencers/update/<int:influencer_id>/', update_influencer, name='update_influencer'),
    path('backend/influencers/activate/<int:influencer_id>/', activate_influencer, name='activate_influencer'),
    path('backend/influencers/deactivate/<int:influencer_id>/', deactivate_influencer, name='deactivate_influencer'),

    path('backend/influencer/login/', influencer_login, name='influencer/login'),
    path('backend/influencer/dashboard/', influencer_dashboard, name='influencer_dashboard'),
    path('backend/influencer/influencer_transation_list/', influencer_transaction_list, name='influencer_transation_list'),
    path('backend/influencer/logout/', influlogout_view, name='influencer/logout'),

    path('backend/influencer/verify-email/', influencer_verify_phone, name='influencer/verify_email'),
    path('backend/influencer/verify-otp/', influencer_verify_otp, name='influencer/verify_otp'),
    path('backend/influencer/change-password/', influencer_change_password, name='influencer/change_password'),

    path('backend/influencer/sell_list/', sell_report, name='influencer_sell_list'),
    path('backend/influencer/sell-items/<str:date>/<int:user_id>/', sell_items_view, name='sell_items_view'),

    path('backend/influencer/commission-report/', commission_report, name='commission_report'),

    path('backend/influencer/withdraw/', withdraw_request_view, name='withdraw_request'),
    path('backend/withdraw/requests/', withdraw_request_list, name='withdraw_request_list'),
    path('backend/approve-withdraw/<int:request_id>/', approve_withdraw_request, name='approve_withdraw_request'),
    path('backend/approve-withdrawal/<int:request_id>/', approve_withdrawal, name='approve_withdrawal'),
    path('backend/reject-withdrawal/<int:request_id>/', reject_withdrawal, name='reject_withdrawal'),


]
