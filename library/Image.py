import wx
class BitmapImage():
    def create(path, width, height):
        bmp = wx.Bitmap(path)
        image = wx.ImageFromBitmap(bmp)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        bmp = wx.BitmapFromImage(image)
        return bmp