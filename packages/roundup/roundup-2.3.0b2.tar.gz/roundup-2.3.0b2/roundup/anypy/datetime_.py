try:
    from datetime import now, UTC
    def utcnow():
        return now(UTC)
except ImportError:
    import datetime
    def utcnow():
        return datetime.datetime.utcnow()

