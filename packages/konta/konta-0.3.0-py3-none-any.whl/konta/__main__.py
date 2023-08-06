#!/usr/bin/env python3
"""Main CLI entrypoint."""

import datetime as dt
import builtins

import argparse

from konta import woob_import, woob_to_bean
from konta.config import Config
from beancount.parser import printer
from beancount.core.data import SORT_ORDER


def _parse_cli():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="konta", description="A Woob -> Beancount data pipeline."
    )
    parser.add_argument("-v", "--verbose", action="count", default=0)
    subparsers = parser.add_subparsers(
        title="Subcommands",
        description="Konta has multiples subcommands that use various Woob queries to produce Beancount directives.",
        help="sub-command help",
    )

    # * Transactions subcommand
    tx_parser = subparsers.add_parser(
        "tx",
        help="List transactions from Woob as Beancount directives. (woob bank history / woob bank coming)",
    )
    tx_parser.add_argument(
        "-d",
        "--date",
        help="Starting Date to fetch transactions from. Defaults to 1 week ago.",
        type=dt.datetime.fromisoformat,
        default=dt.datetime.today() - dt.timedelta(days=7),
    )
    # TODO: --ignored-accounts argument, with a special "*" value
    #       to ignore all by default
    # TODO: --allowed-accounts that overrides the ignored list,
    #       automatically ignores the other accounts if present
    # TODO: a flag to disable "coming" transactions.
    tx_parser.set_defaults(func=_tx_main)

    # * Balance subcommand
    balance_parser = subparsers.add_parser(
        "bal",
        help="List balances/portfolio prices from Woob investments as Beancount directives. (woob bank investment)",
    )
    balance_parser.add_argument(
        "-p",
        "--prices",
        action="store_true",
        help="Fetch the prices of the assets in the portfolios of investments.",
    )
    balance_parser.set_defaults(func=_bal_main)
    return parser.parse_args()


def _tx_main(args):
    conf = Config.from_toml()
    # TODO: Actually have a meaningful usecase for ingesting existing files
    # print(bean_import.import_data(conf.get_exising_input_paths()[0]))
    woob_txs = woob_import.import_data(args.date)
    # TODO: this processing loop should be in the library part, not the binary used just for the PoC
    beans = []
    for acc_id in woob_txs.keys():
        for tx in woob_txs[acc_id]["history"]:
            bean = woob_to_bean.woob_to_bean(
                conf,
                acc_id,
                tx,
            )
            if bean is not None:
                beans.append(bean)
        for tx in woob_txs[acc_id]["coming"]:
            bean = woob_to_bean.woob_to_bean(
                conf,
                acc_id,
                tx,
            )
            if bean is not None:
                beans.append(bean)
    beans = builtins.sorted(
        beans, key=lambda entry: (entry.date, SORT_ORDER.get(type(entry), 0))
    )
    for bean in beans:
        printer.print_entry(bean)
    pass


def _bal_main(args):
    pass


def main():
    """Handle main CLI entrypoint."""
    args = _parse_cli()
    args.func(args)


if __name__ == "__main__":
    main()
