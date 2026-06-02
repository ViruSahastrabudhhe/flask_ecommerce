from enum import Enum

class RoleTypes(Enum):
    ADMIN = "Admin"
    SELLER = "Seller"
    BUYER = "Buyer"

class StoreAddressTypes(Enum):
    SHIPPING = "Shipping"
    BILLING = "Billing"
    WAREHOUSE = "Warehouse"
    PICKUP = "Pickup"

class StoreStatusTypes(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"