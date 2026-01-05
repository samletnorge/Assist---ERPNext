# Copyright (c) 2026, samletnorge and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MarketplaceListing(Document):
    def validate(self):
        """Validate the marketplace listing before saving."""
        if not self.currency:
            self.currency = frappe.defaults.get_global_default("currency") or "NOK"
        
        if self.status == "Posted" and not self.posted_on:
            self.posted_on = frappe.utils.now()
    
    def before_submit(self):
        """Actions before submitting the listing."""
        self.status = "Posted"
        if not self.posted_on:
            self.posted_on = frappe.utils.now()
