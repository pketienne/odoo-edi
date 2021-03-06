"""Mail threads"""

from odoo import api, models


class MailThread(models.AbstractModel):
    """Mail threads

    Disable mail thread posting whenever the context parameter
    ``tracking_disable`` is set.
    """

    _inherit = 'mail.thread'

    @api.multi
    def message_post(self, *args, **kwargs):
        """Post message"""
        if self._context.get('tracking_disable'):
            return
        return super().message_post(*args, **kwargs)

    @api.multi
    def message_post_with_view(self, *args, **kwargs):
        """Post message using a view"""
        if self._context.get('tracking_disable'):
            return
        return super().message_post_with_view(*args, **kwargs)

    @api.multi
    def message_post_with_template(self, *args, **kwargs):
        """Post message using a template"""
        if self._context.get('tracking_disable'):
            return
        return super().message_post_with_template(*args, **kwargs)
