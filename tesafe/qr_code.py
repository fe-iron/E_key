import qrcode

def generate_qr(email, password, domain){
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    data =''
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(str(email)+str(password)+".png")
}

