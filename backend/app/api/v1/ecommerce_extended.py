"""Extended ecommerce API endpoints for shipping, inventory, wishlists, and returns (async).

Access rules:
- Shipping addresses, wishlists and wishlist items belong to the signed-in user.
- Shipments, tracking events, inventory reports, return approvals, receipts and refunds are administrator operations.
- Shipment tracking, order returns and return requests are visible to the order's owner and to administrators.
- Records a caller may not see answer 404, so the API does not reveal whether another user's record exists.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import is_admin, require_admin
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.ecommerce import Product
from app.models.ecommerce_extended import InventoryStatus, ReturnReason, ShippingCarrier
from app.models.user import User
from app.services.ecommerce_extended_service import (
    InventoryService,
    ReturnService,
    ShippingService,
    WishlistService,
    order_owner_id,
    return_order_owner_id,
    shipment_order_owner_id,
)
from app.utils.exceptions import NotFoundError

router = APIRouter()

require_fulfilment_admin = require_admin("ecommerce")


# ============================================================================
# SCHEMAS
# ============================================================================

class ShippingAddressRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    street_address: str = Field(min_length=1, max_length=255)
    city: str = Field(min_length=1, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    postal_code: str = Field(min_length=1, max_length=20)
    country: str = Field(min_length=1, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    is_default: bool = False


class ShippingAddressResponse(ShippingAddressRequest):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ShipmentRequest(BaseModel):
    carrier: ShippingCarrier
    tracking_number: str = Field(min_length=1, max_length=100)
    base_rate: Decimal = Field(ge=0)
    total_cost: Decimal = Field(ge=0)


class ShipmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    carrier: ShippingCarrier
    tracking_number: Optional[str]
    status: Optional[str]
    base_rate: Optional[Decimal]
    total_cost: Optional[Decimal]
    estimated_delivery_date: Optional[datetime]
    created_at: Optional[datetime]
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]


class TrackingEventRequest(BaseModel):
    status: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    location: Optional[str] = Field(default=None, max_length=255)
    timestamp: Optional[datetime] = None


class TrackingEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    shipment_id: int
    status: str
    description: Optional[str]
    location: Optional[str]
    timestamp: datetime


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity_on_hand: int
    quantity_reserved: int
    quantity_available: int
    reorder_level: int
    reorder_quantity: int
    status: InventoryStatus


class WishlistRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: bool = False


class WishlistResponse(WishlistRequest):
    model_config = ConfigDict(from_attributes=True)

    id: int
    share_token: str


class WishlistItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    wishlist_id: int
    product_id: int
    priority: int
    notes: Optional[str]
    added_at: Optional[datetime]


class ReturnRequest(BaseModel):
    order_item_id: Optional[int] = None
    reason: ReturnReason
    reason_details: Optional[str] = None
    quantity_requested: int = Field(ge=1)


class ReturnResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    order_item_id: Optional[int]
    rma_number: Optional[str]
    reason: ReturnReason
    reason_details: Optional[str]
    status: str
    quantity_requested: int
    quantity_received: Optional[int]
    refund_amount: Optional[Decimal]
    refund_method: Optional[str]
    created_at: Optional[datetime]
    approved_at: Optional[datetime]
    received_at: Optional[datetime]
    refunded_at: Optional[datetime]


# ============================================================================
# ACCESS HELPERS
# ============================================================================

async def _is_ecommerce_admin(session: AsyncSession, user: User) -> bool:
    return await is_admin(session, user.id, "ecommerce")


async def _may_see_order(session: AsyncSession, user: User, owner_id: Optional[int]) -> bool:
    """The order's owner and administrators may see its records; everyone else gets a 404."""
    return owner_id is not None and (owner_id == user.id or await _is_ecommerce_admin(session, user))


# ============================================================================
# SHIPPING & FULFILLMENT (MODULE 106)
# ============================================================================

@router.post("/shipping-addresses", response_model=ShippingAddressResponse, status_code=201)
async def create_shipping_address(
    address: ShippingAddressRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a shipping address for the signed-in user"""
    return await ShippingService.create_shipping_address(db, current_user.id, address.model_dump())


@router.get("/shipping-addresses", response_model=List[ShippingAddressResponse])
async def get_shipping_addresses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List the signed-in user's shipping addresses"""
    return await ShippingService.get_user_shipping_addresses(db, current_user.id)


@router.post("/orders/{order_id}/shipment", response_model=ShipmentResponse, status_code=201)
async def create_shipment(
    order_id: int,
    shipment: ShipmentRequest,
    _admin: User = Depends(require_fulfilment_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a shipment for an order (administrators only)"""
    return await ShippingService.create_shipment(db, order_id, shipment.model_dump())


@router.get("/orders/{order_id}/shipments", response_model=List[ShipmentResponse])
async def get_order_shipments(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Shipments for an order, visible to the order's owner and administrators"""
    if not await _may_see_order(db, current_user, await order_owner_id(db, order_id)):
        raise NotFoundError("Order")
    return await ShippingService.get_order_shipments(db, order_id)


@router.post("/shipments/{shipment_id}/tracking", response_model=TrackingEventResponse, status_code=201)
async def add_tracking_event(
    shipment_id: int,
    event: TrackingEventRequest,
    _admin: User = Depends(require_fulfilment_admin),
    db: AsyncSession = Depends(get_db),
):
    """Record a tracking event for a shipment (administrators only)"""
    return await ShippingService.add_tracking_event(db, shipment_id, event.model_dump())


@router.get("/shipments/{shipment_id}/tracking", response_model=List[TrackingEventResponse])
async def get_shipment_tracking(
    shipment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Tracking history for a shipment, visible to the order's owner and administrators"""
    owner_id = await shipment_order_owner_id(db, shipment_id)
    if not await _may_see_order(db, current_user, owner_id):
        raise NotFoundError("Shipment")
    return await ShippingService.get_shipment_tracking(db, shipment_id)


# ============================================================================
# INVENTORY MANAGEMENT (MODULE 107)
# ============================================================================

@router.get("/products/{product_id}/inventory", response_model=InventoryResponse)
async def get_product_inventory(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Stock level for a product"""
    if await db.get(Product, product_id) is None:
        raise NotFoundError("Product")
    return await InventoryService.get_or_create_inventory_level(db, product_id)


@router.get("/inventory/low-stock", response_model=List[InventoryResponse])
async def get_low_stock_products(
    _admin: User = Depends(require_fulfilment_admin),
    db: AsyncSession = Depends(get_db),
):
    """Products at or below their reorder level (administrators only)"""
    return await InventoryService.get_low_stock_products(db)


@router.get("/inventory/out-of-stock", response_model=List[InventoryResponse])
async def get_out_of_stock_products(
    _admin: User = Depends(require_fulfilment_admin),
    db: AsyncSession = Depends(get_db),
):
    """Products with no stock on hand (administrators only)"""
    return await InventoryService.get_out_of_stock_products(db)


# ============================================================================
# WISHLISTS (MODULE 109)
# ============================================================================

@router.post("/wishlists", response_model=WishlistResponse, status_code=201)
async def create_wishlist(
    wishlist: WishlistRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a wishlist for the signed-in user"""
    return await WishlistService.create_wishlist(db, current_user.id, wishlist.model_dump())


@router.get("/wishlists", response_model=List[WishlistResponse])
async def get_wishlists(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List the signed-in user's wishlists"""
    return await WishlistService.get_user_wishlists(db, current_user.id)


@router.get("/wishlists/share/{share_token}", response_model=WishlistResponse)
async def get_shared_wishlist(
    share_token: str,
    db: AsyncSession = Depends(get_db),
):
    """A public wishlist, by its share token"""
    wishlist = await WishlistService.get_wishlist_by_share_token(db, share_token)
    if wishlist is None:
        raise NotFoundError("Wishlist")
    return wishlist


@router.get("/wishlists/{wishlist_id}", response_model=WishlistResponse)
async def get_wishlist(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """One of the signed-in user's wishlists"""
    wishlist = await WishlistService.get_wishlist(db, wishlist_id)
    if wishlist is None or wishlist.user_id != current_user.id:
        raise NotFoundError("Wishlist")
    return wishlist


@router.post("/wishlists/{wishlist_id}/items/{product_id}", response_model=WishlistItemResponse, status_code=201)
async def add_to_wishlist(
    wishlist_id: int,
    product_id: int,
    priority: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a product to one of the signed-in user's wishlists"""
    wishlist = await WishlistService.get_wishlist(db, wishlist_id)
    if wishlist is None or wishlist.user_id != current_user.id:
        raise NotFoundError("Wishlist")
    return await WishlistService.add_to_wishlist(db, wishlist_id, product_id, priority)


@router.delete("/wishlist-items/{item_id}")
async def remove_from_wishlist(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove an item from the signed-in user's wishlist"""
    item = await WishlistService.get_wishlist_item(db, item_id)
    if item is None or item.wishlist.user_id != current_user.id:
        raise NotFoundError("Wishlist item")
    await WishlistService.remove_from_wishlist(db, item_id)
    return {"status": "success"}


@router.get("/wishlists/{wishlist_id}/items", response_model=List[WishlistItemResponse])
async def get_wishlist_items(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Items in one of the signed-in user's wishlists"""
    wishlist = await WishlistService.get_wishlist(db, wishlist_id)
    if wishlist is None or wishlist.user_id != current_user.id:
        raise NotFoundError("Wishlist")
    return await WishlistService.get_wishlist_items(db, wishlist_id)


@router.get("/products/{product_id}/in-wishlist")
async def check_in_wishlist(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Whether the signed-in user has the product on any wishlist"""
    is_in_wishlist = await WishlistService.check_item_in_wishlist(db, current_user.id, product_id)
    return {"product_id": product_id, "in_wishlist": is_in_wishlist}


# ============================================================================
# RETURNS & REFUNDS (MODULE 110)
# ============================================================================

@router.post("/orders/{order_id}/return", response_model=ReturnResponse, status_code=201)
async def create_return_request(
    order_id: int,
    return_req: ReturnRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Request a return for an order the signed-in user placed"""
    if not await _may_see_order(db, current_user, await order_owner_id(db, order_id)):
        raise NotFoundError("Order")
    return await ReturnService.create_return_request(db, order_id, return_req.model_dump())


@router.get("/returns/pending", response_model=List[ReturnResponse])
async def get_pending_returns(
    _admin: User = Depends(require_fulfilment_admin),
    db: AsyncSession = Depends(get_db),
):
    """Returns still awaiting a decision or refund (administrators only)"""
    return await ReturnService.get_pending_returns(db)


@router.get("/returns/{return_id}", response_model=ReturnResponse)
async def get_return_request(
    return_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """A return request, visible to the order's owner and administrators"""
    owner_id = await return_order_owner_id(db, return_id)
    if not await _may_see_order(db, current_user, owner_id):
        raise NotFoundError("Return request")
    return await ReturnService.get_return_request(db, return_id)


@router.get("/orders/{order_id}/returns", response_model=List[ReturnResponse])
async def get_order_returns(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return requests for an order, visible to the order's owner and administrators"""
    if not await _may_see_order(db, current_user, await order_owner_id(db, order_id)):
        raise NotFoundError("Order")
    return await ReturnService.get_order_returns(db, order_id)


@router.post("/returns/{return_id}/approve")
async def approve_return(
    return_id: int,
    refund_amount: Optional[Decimal] = Query(None, ge=0),
    _admin: User = Depends(require_fulfilment_admin),
    db: AsyncSession = Depends(get_db),
):
    """Approve a return request (administrators only)"""
    await ReturnService.approve_return(db, return_id, refund_amount)
    return {"status": "approved"}


@router.post("/returns/{return_id}/reject")
async def reject_return(
    return_id: int,
    reason: Optional[str] = Query(None, max_length=500),
    _admin: User = Depends(require_fulfilment_admin),
    db: AsyncSession = Depends(get_db),
):
    """Reject a return request before it is received (administrators only)"""
    await ReturnService.reject_return(db, return_id, reason)
    return {"status": "rejected"}


@router.post("/returns/{return_id}/receive")
async def receive_return(
    return_id: int,
    quantity_received: int = Query(..., ge=0),
    _admin: User = Depends(require_fulfilment_admin),
    db: AsyncSession = Depends(get_db),
):
    """Record the items received back for a return (administrators only)"""
    await ReturnService.receive_return(db, return_id, quantity_received)
    return {"status": "received"}


@router.post("/returns/{return_id}/refund")
async def process_refund(
    return_id: int,
    _admin: User = Depends(require_fulfilment_admin),
    db: AsyncSession = Depends(get_db),
):
    """Mark a received return as refunded (administrators only)"""
    await ReturnService.process_refund(db, return_id)
    return {"status": "refunded"}
