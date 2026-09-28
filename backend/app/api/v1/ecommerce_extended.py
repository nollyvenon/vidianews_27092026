"""Extended ecommerce API endpoints for shipping, inventory, wishlists, and returns"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.services.ecommerce_extended_service import (
    ShippingService, InventoryService, WishlistService, ReturnService
)
from app.models.auth import User
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class ShippingAddressRequest(BaseModel):
    first_name: str
    last_name: str
    street_address: str
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str
    phone: Optional[str] = None
    is_default: bool = False


class ShippingAddressResponse(ShippingAddressRequest):
    id: int


class ShipmentRequest(BaseModel):
    carrier: str
    tracking_number: str
    base_rate: Decimal
    total_cost: Decimal


class TrackingEventRequest(BaseModel):
    status: str
    description: Optional[str] = None
    location: Optional[str] = None


class WishlistRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False


class WishlistResponse(WishlistRequest):
    id: int
    share_token: str


class ReturnRequest(BaseModel):
    order_item_id: Optional[int] = None
    reason: str
    reason_details: Optional[str] = None
    quantity_requested: int


# ============================================================================
# SHIPPING & FULFILLMENT (MODULE 106)
# ============================================================================

@router.post("/shipping-addresses", response_model=ShippingAddressResponse)
def create_shipping_address(
    address: ShippingAddressRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create shipping address"""
    return ShippingService.create_shipping_address(db, current_user.id, address.dict())


@router.get("/shipping-addresses", response_model=List[ShippingAddressResponse])
def get_shipping_addresses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's shipping addresses"""
    return ShippingService.get_user_shipping_addresses(db, current_user.id)


@router.post("/orders/{order_id}/shipment")
def create_shipment(
    order_id: int,
    shipment: ShipmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create shipment"""
    return ShippingService.create_shipment(db, order_id, shipment.dict())


@router.post("/shipments/{shipment_id}/tracking")
def add_tracking_event(
    shipment_id: int,
    event: TrackingEventRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add tracking event"""
    return ShippingService.add_tracking_event(db, shipment_id, event.dict())


@router.get("/shipments/{shipment_id}/tracking")
def get_shipment_tracking(
    shipment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get shipment tracking"""
    return ShippingService.get_shipment_tracking(db, shipment_id)


# ============================================================================
# INVENTORY MANAGEMENT (MODULE 107)
# ============================================================================

@router.get("/products/{product_id}/inventory")
def get_product_inventory(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get product inventory"""
    return InventoryService.get_or_create_inventory_level(db, product_id)


@router.get("/inventory/low-stock")
def get_low_stock_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get low stock products (admin only)"""
    return InventoryService.get_low_stock_products(db)


@router.get("/inventory/out-of-stock")
def get_out_of_stock_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get out of stock products (admin only)"""
    return InventoryService.get_out_of_stock_products(db)


# ============================================================================
# WISHLISTS (MODULE 109)
# ============================================================================

@router.post("/wishlists", response_model=WishlistResponse)
def create_wishlist(
    wishlist: WishlistRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create wishlist"""
    return WishlistService.create_wishlist(db, current_user.id, wishlist.dict())


@router.get("/wishlists", response_model=List[WishlistResponse])
def get_wishlists(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's wishlists"""
    return WishlistService.get_user_wishlists(db, current_user.id)


@router.get("/wishlists/{wishlist_id}")
def get_wishlist(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get wishlist"""
    wishlist = WishlistService.get_wishlist(db, wishlist_id)
    if not wishlist or wishlist.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    return wishlist


@router.get("/wishlists/share/{share_token}")
def get_shared_wishlist(
    share_token: str,
    db: Session = Depends(get_db)
):
    """Get shared wishlist"""
    wishlist = WishlistService.get_wishlist_by_share_token(db, share_token)
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    return wishlist


@router.post("/wishlists/{wishlist_id}/items/{product_id}")
def add_to_wishlist(
    wishlist_id: int,
    product_id: int,
    priority: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add product to wishlist"""
    wishlist = WishlistService.get_wishlist(db, wishlist_id)
    if not wishlist or wishlist.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    return WishlistService.add_to_wishlist(db, wishlist_id, product_id, priority)


@router.delete("/wishlist-items/{item_id}")
def remove_from_wishlist(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove item from wishlist"""
    WishlistService.remove_from_wishlist(db, item_id)
    return {"status": "success"}


@router.get("/wishlists/{wishlist_id}/items")
def get_wishlist_items(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get wishlist items"""
    wishlist = WishlistService.get_wishlist(db, wishlist_id)
    if not wishlist or wishlist.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    return WishlistService.get_wishlist_items(db, wishlist_id)


@router.get("/products/{product_id}/in-wishlist")
def check_in_wishlist(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if product is in user's wishlist"""
    is_in_wishlist = WishlistService.check_item_in_wishlist(db, current_user.id, product_id)
    return {"product_id": product_id, "in_wishlist": is_in_wishlist}


# ============================================================================
# RETURNS & REFUNDS (MODULE 110)
# ============================================================================

@router.post("/orders/{order_id}/return")
def create_return_request(
    order_id: int,
    return_req: ReturnRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create return request"""
    return_request = ReturnService.create_return_request(
        db, order_id, return_req.dict()
    )
    return return_request


@router.get("/returns/{return_id}")
def get_return_request(
    return_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get return request"""
    return_request = ReturnService.get_return_request(db, return_id)
    if not return_request:
        raise HTTPException(status_code=404, detail="Return not found")
    return return_request


@router.get("/orders/{order_id}/returns")
def get_order_returns(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get order returns"""
    return ReturnService.get_order_returns(db, order_id)


@router.post("/returns/{return_id}/approve")
def approve_return(
    return_id: int,
    refund_amount: float = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve return request"""
    ReturnService.approve_return(db, return_id, refund_amount)
    return {"status": "approved"}


@router.post("/returns/{return_id}/reject")
def reject_return(
    return_id: int,
    reason: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject return request"""
    ReturnService.reject_return(db, return_id, reason)
    return {"status": "rejected"}


@router.post("/returns/{return_id}/receive")
def receive_return(
    return_id: int,
    quantity_received: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark return as received"""
    ReturnService.receive_return(db, return_id, quantity_received)
    return {"status": "received"}


@router.post("/returns/{return_id}/refund")
def process_refund(
    return_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process refund"""
    ReturnService.process_refund(db, return_id)
    return {"status": "refunded"}


@router.get("/returns/pending")
def get_pending_returns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending returns (admin only)"""
    return ReturnService.get_pending_returns(db)
