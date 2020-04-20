import math

from arrplat.config import DEFAULT_PAGE_SIZE


class Page(object):
    items = []
    previous_page = None
    next_page = None
    has_previous = 1
    previous_items = None
    has_next = False
    page_size = DEFAULT_PAGE_SIZE
    total = 0
    page = 1

    def __init__(self, items, page, page_size, total):
        self.items = items
        self.previous_page = None
        self.next_page = None
        self.page_size = page_size
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.total = total
        self.page = int(math.ceil(total / float(page_size)))
        if self.page < 1:
            self.page = 1


def paginate(query, page, page_size):
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        raise AttributeError('page_size needs to be >= 1')
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    # We remove the ordering of the query since it doesn't matter for getting a count and
    # might have performance implications as discussed on this Flask-SqlAlchemy issue
    # https://github.com/mitsuhiko/flask-sqlalchemy/issues/100
    total = query.order_by(None).count()
    return Page(items, page, page_size, total)
