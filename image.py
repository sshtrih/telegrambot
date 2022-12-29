# from mongoengine import connect, Document, fields
#
# import io
# import PIL.Image as Image
#
# connect(db='UniversitiesPhotos', host='127.0.0.1', port=27017)
#
#
# class University(Document):
#     meta = {'collection': 'image'}
#
#     university_title = fields.StringField(required=True)
#     university_image = fields.ImageField(thumbnail_size=(300, 300, False))
#
#
# # mirea = University(university_title='mireaa')
# # my_image = open('downloads/img.png', 'rb')
# # mirea.university_image.replace(my_image, filename='mireaa.png')
# # mirea.save()
# #
# # image = University.objects(university_title='mireaa').first()
# #
# # bytes = image.university_image.thumbnail.read()
# # print(bytes)
# #
# # Image.open(io.BytesIO(bytes)).show()
