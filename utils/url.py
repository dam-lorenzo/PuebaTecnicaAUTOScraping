

class URL():
    BASE        = 'https://www.hiperlibertad.com.ar/'
    CATEGORIES  = 'https://www.hiperlibertad.com.ar/api/catalog_system/pub/category/tree/50'
    PRODUCTS    = 'https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/{slug}?O=OrderByTopSaleDESC&_from=0&_to=23&ft&sc=1'

    @classmethod
    def get_products_url(cls, slug):
        return cls.PRODUCTS.format(slug=slug)