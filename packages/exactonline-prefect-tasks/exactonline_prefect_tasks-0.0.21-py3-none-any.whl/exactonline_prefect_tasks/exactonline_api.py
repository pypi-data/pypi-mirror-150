# vim: set ts=8 sw=4 sts=4 et ai tw=79:
"""
Override for ExactAPi class. Removes Autorefresh class.
"""
from exactonline.rawapi import ExactRawApi

from exactonline.api.unwrap import Unwrap
from exactonline.api.v1division import V1Division

from exactonline.api.bankaccounts import BankAccounts
from exactonline.api.contacts import Contacts
from exactonline.api.invoices import Invoices
from exactonline.api.ledgeraccounts import LedgerAccounts
from exactonline.api.quotations import Quotations
from exactonline.api.receivables import Receivables
from exactonline.api.relations import Relations
from exactonline.api.vatcodes import VatCodes


class ExactOnlineApi(
    # Talk to /api/v1/{division} directly.
    V1Division,
    # Strip the surrounding "d" and "results" dictionary
    # items.
    Unwrap,
    # The base class comes last: talk to /api.
    ExactRawApi
):
    bankaccounts = BankAccounts.as_property()
    contacts = Contacts.as_property()
    invoices = Invoices.as_property()
    ledgeraccounts = LedgerAccounts.as_property()
    quotations = Quotations.as_property()
    receivables = Receivables.as_property()
    relations = Relations.as_property()
    vatcodes = VatCodes.as_property()
