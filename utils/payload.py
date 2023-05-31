from datetime import datetime

class Payload():
    
    def __init__(
            self,
            _id: str                    = None,
            productReference: str       = None,
            name: str                   = None,
            completeName: str           = None,
            brand: str                  = None,
            brandId: str                = None,
            categories: list            = None,
            link: str                   = None,
            description: str            = None,
            isKit: bool                 = None,
            images: list                = None,
            sellerId: str               = None,
            sellerName: str             = None,
            price: float                = None,
            listPrice: float            = None,
            priceWithoutDiscount: float = None,
            priceValidUntil: str        = None,
            stock: int                  = None,
            paymentOptions: list        = None,
            releaseDate: str            = None,
            createdAt: str              = None
        ) -> None:
        self.id                     = _id
        self.productReference       = productReference
        self.name                   = name
        self.completeName           = completeName
        self.brand                  = brand
        self.brandId                = brandId
        self.categories             = categories
        self.link                   = link
        self.description            = description
        self.isKit                  = isKit
        self.images                 = images
        self.sellerId               = sellerId
        self.sellerName             = sellerName
        self.price                  = price
        self.listPrice              = listPrice
        self.priceWithoutDiscount   = priceWithoutDiscount
        self.priceValidUntil        = priceValidUntil
        self.stock                  = stock
        self.paymentOptions         = paymentOptions
        self.releaseDate            = releaseDate
        self.createdAt              = createdAt

    def create_payload(self):
        return {
            PayloadKeys.id:               str(self.id),
            PayloadKeys.productReference: str(self.productReference),
            PayloadKeys.name:             self.name,
            PayloadKeys.completeName:     self.completeName,
            PayloadKeys.brand:            self.brand,
            PayloadKeys.brandId:          str(self.brandId),
            PayloadKeys.categories:       self.categories,
            PayloadKeys.link:             self.link,
            PayloadKeys.description:      self.description,
            PayloadKeys.isKit:            self.isKit,
            PayloadKeys.images:           self.images,
            PayloadKeys.sellerId:         str(self.sellerId),
            PayloadKeys.sellerName:       self.sellerName,
            PayloadKeys.price:            self.__clean_price(self.price),
            PayloadKeys.listPrice:        self.__clean_price(self.listPrice),
            PayloadKeys.priceWithoutDiscount: self.__clean_price(self.priceWithoutDiscount),
            PayloadKeys.priceValidUntil:  self.priceValidUntil,
            PayloadKeys.stock:            self.stock,
            PayloadKeys.paymentOptions:   self.paymentOptions,
            PayloadKeys.createdAt:        self.createdAt,
            PayloadKeys.timestamp:        datetime.now().isoformat()
        }

    def __clean_price(self, price):
        if not price:
            return
        if type(price) == str:
            return float(price.replace(',', '.'))
        else:
            return float(price)
    
class PayloadKeys():
    id                      = "Id"
    productReference        = "ProductReference"
    name                    = "Name"
    completeName            = "CompleteName"
    brand                   = "Brand"
    brandId                 = "BrandId"
    categories              = "Categories"
    link                    = "Link"
    description             = "Description"
    isKit                   = "IsKit"
    images                  = "Images"
    sellerId                = "SellerId"
    sellerName              = "SellerName"
    price                   = "Price"
    listPrice               = "ListPrice"
    priceWithoutDiscount    = "PriceWithoutDiscount"
    priceValidUntil         = "PriceValidUntil"
    stock                   = "Stock"
    paymentOptions          = "PaymentOptions"
    createdAt               = "CreatedAt"
    timestamp               = "Timestamp"
    type                    = 'Type'
    typeGroup               = 'TypeGroup'
    options                 = 'Options'
    installments            = 'Installments'
    interestRate            = 'InterestRate'
    monthlyPayment          = 'MonthlyPayment'
    total                   = 'Total'
    validUntil              = 'ValidUntil'