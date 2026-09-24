from qr_code import QrCode

qr = QrCode.New("", inErrorCorrectionMode='H', inMask=2)
qr.Generate()
qr.image.show()