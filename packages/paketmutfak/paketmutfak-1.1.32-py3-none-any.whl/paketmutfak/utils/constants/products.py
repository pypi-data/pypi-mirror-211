from dataclasses import dataclass
from typing import Union, List
from decimal import Decimal


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


@dataclass
class PMCustomerInfo:
    email: str
    full_name: str
    address: PmAddress
    phone: List


@dataclass
class PMFormat:
    address_id: str
    customer_type: str
    delivery_method: str
    discount_price: Decimal
    order_contents: list
    order_note: str
    order_type: str
    original_request: dict
    payment_location: str
    payment_method: str
    platform_code: str
    platform_confirmation_code: str
    platform_delivery_price: Decimal
    platform_name: str
    pm_restaurant_id: str
    promotions: list
    total_price: Decimal
    is_scheduled_order: bool
    scheduled_display_date: str
    verification_code: str
    has_restaurant_transfer_payment: int
    platform_user_id: str
    customer_info: PMCustomerInfo
    region: PmRegion
