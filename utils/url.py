

class URL():
    BASE        = 'https://www.hiperlibertad.com.ar/'
    CATEGORIES  = 'https://www.hiperlibertad.com.ar/api/catalog_system/pub/category/tree/50'
    PRODUCTS    = 'https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/{slug}?O=OrderByTopSaleDESC&_from={_from}&_to={_to}&ft&sc={store}'
    STORES    = 'https://www.hiperlibertad.com.ar/institucional/sucursales'
    steps       = 23

    @classmethod
    def get_products_url(cls, slug, _from, store):
        _to = _from + cls.steps
        return cls.PRODUCTS.format(slug=slug, _from=_from, _to=_to, store=store)