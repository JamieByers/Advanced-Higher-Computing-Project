class Product:
    def __init__(
        self,
        title: str = "",
        price: float = 0.0,
        buyer_protection_price: float = 0.0,
        postage: float = 0.0,
        brand: str = "",
        colour: str = "",
        size: str = "",
        quality: str = "",
        condition: str = "",
        location: str = "",
        payment_options: str = "",
        views: int = 0,
        description: str = "",
        url: str = "",
        uploaded: str = "",
        other_data: list[str] = []
    ):
        self.title = title
        self.price = price
        self.buyer_protection_price = buyer_protection_price
        self.postage = postage
        self.brand = brand
        self.size = size
        self.quality = quality
        self.condition = condition
        self.location = location
        self.payment_options = payment_options
        self.views = views
        self.description = description
        self.url = url
        self.colour = colour
        self.uploaded = uploaded
        self.other_data = other_data if other_data is not None else []

