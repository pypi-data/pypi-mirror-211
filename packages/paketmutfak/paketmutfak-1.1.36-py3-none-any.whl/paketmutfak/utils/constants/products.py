from dataclasses import dataclass
from typing import Union, List


@dataclass
class PlatformOption:
    name: str
    platform_product_id: str
    platform_option_id: str
    price: str
    type: str
    pm_restaurant_id: str
    platform_name: str
    id: str


@dataclass
class PlatformProduct:
    id: str
    platform_product_id: str
    name: str
    description: str
    price: str
    title: str
    pm_restaurant_id: str
    status: bool
    platform_name: str
    preparation_time: Union[str, None] = None


@dataclass
class PMProductExtraIngredients:
    id: str
    name: str
    price: float


@dataclass
class PMProductRemovedIngredients:
    id: str
    name: str


@dataclass
class PMOption:
    option_id: str
    product_id: str
    category_name: str
    name: str
    quantity: int
    price: float
    options: List['PMOption']
    excluded: bool


@dataclass
class PMProduct:
    id: str
    name: str
    note: str
    price: float
    hash_id: str
    options: List[PMOption]
    quantity: int
    unit_price: float
    extra_ingredients: List[PMProductExtraIngredients]
    removed_ingredients: List[PMProductRemovedIngredients]


@dataclass
class PmRegion:
    region: str
    full_address: str
    longitude: float
    latitude: float


@dataclass
class PmAddress:
    address_id: str
    city: str
    door_number: str
    district: str
    latitude: float
    longitude: float
    address_description: str
    company: str
    full_address: str
    neighborhood: str
    floor: str
    street: str
    apartment_number: str

#
@dataclass
class PmPlatform:
    platform_code: str
    platform_confirmation_code: str
    platform_delivery_price: float
    platform_name: str
    platform_user_id: str


@dataclass
class PmPayment:
    payment_location: str
    payment_method: str


@dataclass
class PmOrder:
    order_contents: List
    order_note: str
    order_type: str
    promotions: List


@dataclass
class PmPrice:
    discount_price: float
    total_price: float


@dataclass
class PmScheduled:
    is_scheduled_order: str
    scheduled_display_date: str


@dataclass
class PmBrand:
    pm_restaurant_id: str
    has_restaurant_transfer_payment: int
    brand_name: str


@dataclass
class PMCustomerInfo:
    email: str
    full_name: str
    address: PmAddress
    phone: List
    customer_type: str


@dataclass
class PMFormat:
    delivery_method: str
    original_request: dict
    verification_code: str
    customer_info: PMCustomerInfo
    region: PmRegion
    slack_channel_id: str
