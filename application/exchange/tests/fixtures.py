from django.conf import settings

fixtures = {
    'import.xml': settings.BASE_DIR / 'application/exchange/fixtures/testing/import.xml',
    'offers.xml': settings.BASE_DIR / 'application/exchange/fixtures/testing/offers.xml',
    '3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg': settings.BASE_DIR / 'application/exchange/fixtures/testing/3cb3474f'
                                                                    '-d9a8-11e9-81dc-2c4d5446690f.jpg',
    '3cb3474f-d9a8-11e9-81dc-2c4d5446690f_1.jpg': settings.BASE_DIR / 'application/exchange/fixtures/testing/3cb3474f'
                                                                    '-d9a8-11e9-81dc-2c4d5446690f_1.jpg',
    '3cb3474f-d9a8-11e9-81dc-2c4d5446690f_2.jpg': settings.BASE_DIR / 'application/exchange/fixtures/testing/3cb3474f'
                                                                    '-d9a8-11e9-81dc-2c4d5446690f_2.jpg',
    'import.xml.part0': settings.BASE_DIR / 'application/exchange/fixtures/testing/import.xml.part0',
    'import.xml.part1': settings.BASE_DIR / 'application/exchange/fixtures/testing/import.xml.part1',
    'image-files': settings.BASE_DIR / 'application/exchange/fixtures/testing/image-files/'
}
