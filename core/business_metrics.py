from datetime import datetime
from typing import Optional


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None


def get_quarter(date_obj: datetime):
    return (date_obj.month - 1) // 3 + 1


def filter_deals(deals, user_query):
    """
    Filters deals by:
    - Open status only (pipeline logic)
    - Quarter if specified in query
    """

    filtered = []

    query_lower = user_query.lower()
    quarter_filter = None
    year_filter = None

    if "q1" in query_lower:
        quarter_filter = 1
    elif "q2" in query_lower:
        quarter_filter = 2
    elif "q3" in query_lower:
        quarter_filter = 3
    elif "q4" in query_lower:
        quarter_filter = 4
    elif "this quarter" in query_lower:
        now = datetime.now()
        quarter_filter = get_quarter(now)
        year_filter = now.year

    for deal in deals:

        # Only Open deals = active pipeline
        status = (deal.get("color_mm0yrwc6") or "").lower()
        if status != "open":
            continue

        close_date_str = deal.get("date_mm0ymted")
        close_date = parse_date(close_date_str)

        if quarter_filter:
            if not close_date:
                continue

            if get_quarter(close_date) != quarter_filter:
                continue

            if year_filter and close_date.year != year_filter:
                continue

        filtered.append(deal)

    return filtered


def calculate_pipeline_by_sector(deals):
    sector_totals = {}
    missing_close_dates = 0
    total_pipeline = 0.0

    for deal in deals:
        sector = (deal.get("color_mm0yscsw") or "Unknown").strip().lower()
        revenue_raw = deal.get("numeric_mm0yrkb5")
        close_date = deal.get("date_mm0ymted")

        revenue = 0.0
        if revenue_raw:
            try:
                revenue = float(str(revenue_raw).replace(",", "").replace("$", ""))
            except:
                revenue = 0.0

        if not close_date:
            missing_close_dates += 1

        total_pipeline += revenue
        sector_totals[sector] = sector_totals.get(sector, 0) + revenue

    total_deals = len(deals)
    average_deal_size = total_pipeline / total_deals if total_deals > 0 else 0

    # Top 3 sector concentration
    sorted_sectors = sorted(sector_totals.items(), key=lambda x: x[1], reverse=True)
    top_three_total = sum([s[1] for s in sorted_sectors[:3]])
    concentration_ratio = (top_three_total / total_pipeline * 100) if total_pipeline > 0 else 0

    return {
        "pipeline_by_sector": sector_totals,
        "missing_close_dates": missing_close_dates,
        "total_pipeline": total_pipeline,
        "total_deals": total_deals,
        "average_deal_size": average_deal_size,
        "top_3_sector_concentration_percent": concentration_ratio
    }