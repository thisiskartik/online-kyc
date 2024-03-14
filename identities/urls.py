from django.urls import path
from identities.views import upload_face_image, upload_signature_image, upload_aadhar_image, upload_pan_image

urlpatterns = [
    path('<str:identity_id>/face/', upload_face_image),
    path('<str:identity_id>/signature/', upload_signature_image),
    path('<str:identity_id>/aadhar/', upload_aadhar_image),
    path('<str:identity_id>/pan/', upload_pan_image)
]