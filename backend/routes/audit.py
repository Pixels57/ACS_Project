"""
Audit routes
VULNERABLE: Misconfigured access permissions
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.audit import AuditRecord
from typing import Optional

router = APIRouter()


@router.get("")
async def get_audit_logs(
    user: Optional[int] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
    # VULNERABLE: No authorization check - any authenticated user can access
):
    """
    Get audit logs
    VULNERABLE: Missing access control - should require admin role
    """
    query = db.query(AuditRecord)
    
    if user:
        query = query.filter(AuditRecord.actor_id == user)
    
    audit_records = query.order_by(AuditRecord.timestamp.desc()).limit(100).all()
    
    return [
        {
            "id": record.id,
            "actor_id": record.actor_id,
            "action": record.action,
            "target": record.target,
            "timestamp": record.timestamp.isoformat(),
            "details": record.details
        }
        for record in audit_records
    ]

