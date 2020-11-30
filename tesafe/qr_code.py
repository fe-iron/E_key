from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
import qrcode


def generate_qr(request):
    fname = request.POST.get('fname', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    id = request.POST.get('seller_id', None)
    domain = get_current_site(request).domain
    email = str(email).replace('.','e')
    password = str(password).replace('.','p')
    # try:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    data = 'http://' + domain + '/qr_view?fname=' + fname + '&email=' + email + '&pas=' + password + '&id=' + str(id)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save('media/qr/' + str(email) + str(password) + ".png")
    return JsonResponse({"path": 'http://' + domain + '/media/qr/'+str(email)+str(password)+".png", "msg": True}, status=200)

