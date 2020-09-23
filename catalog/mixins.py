class PageTitleMixin(object):
    page_title = None
    active_tab = None

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('page_title', self.get_page_title())
        ctx.setdefault('active_tab', self.active_tab)
        return ctx
