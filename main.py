from qr_code import QrCode

for mask in range(8):
    qr = QrCode.New("", inMask=mask)
    qr.Generate()
    qr.image.show()