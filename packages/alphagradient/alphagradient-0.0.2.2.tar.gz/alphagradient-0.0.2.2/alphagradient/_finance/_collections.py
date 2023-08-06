# -*- coding: utf-8 -*-
"""AG module containing classes for holding and organizing assets

Todo:
    * Fix basket.validate_resolution to actually validate resolutions
        that are not timedelta objects
    * Baskets need to be called environments
"""
# Standard imports
from __future__ import annotations

from numbers import Number
from datetime import datetime, time, timedelta
from weakref import WeakValueDictionary as WeakDict
from enum import Enum, auto
from urllib import request
from collections import OrderedDict, deque
from copy import copy
from pathlib import Path
import io
import os
import math


# Third Party imports
from pathos.multiprocessing import ProcessingPool as Pool
from p_tqdm import p_map
import yfinance as yf
import yfinance.shared as shared
import pandas as pd
import numpy as np
import tqdm

# Local Imports
from .. import utils
from ._asset import Asset, types
from ._portfolio import Portfolio
from ._standard import Currency, Stock
from .._data import AssetData

# Typing
from typing import (
    Any,
    Callable,
    Iterable,
    Optional,
    Union,
    Literal,
    Type,
    TypeVar,
    no_type_check,
    overload,
)

from typing_extensions import TypeAlias

from ..utils import TimeLike, DateOrTime, DatetimeLike, to_datetime

Bindable = Union[Asset, Portfolio]
"""AG Objects that can be bound to environments"""

Trackable = Union[Iterable[Bindable], Bindable]
"""Objects acceptable for Environment's 'track' functionality"""

TimeLike_T = TypeVar("TimeLike_T", time, str)
"""A TimeLike TypeVar"""

_FilterExpression: TypeAlias = "FilterExpression"
"""Type alias for filter expressions"""

ValidFilter = Union[_FilterExpression, dict[str, Stock], list[str], list[Stock]]
"""Objects that are valid filters for Universes"""


class Environment:
    """
    An AlphaGradient virtual environment instance

    This object essentially represents an isolated financial
    environment that ensures all instantiated assets/objects are
    compatible with eachother and are valuated at the same moment in
    time.

    Environments should be used in algorithms for creating isolated
    financial environments that keep AG objects conveniently
    accessible in one place.

    Other attributes not included in the list below include all
    instantiable asset types (eg. environment.stock, environment.call, etc.),
    which will return a dictionary of assets of that type which exist
    in this Environment, where keys are the asset.key. These attributes
    double as functions for instantiation of that asset type within
    the Environment. Instantiating an asset by calling these attributes
    will take/accept the same arguments for instantiation as when
    instantiated normally through alphagradient.finance.

    Similarly to how the the global types enum works, environments also
    permit attribute access of specific assets when accessed as the
    attribute of a type (eg. environment.stock.SPY will access SPY, if this
    environment is tracking it).

    Environments can also directly access the attributes of their portfolios
    with attribute access. When an environment keeps track of multiple
    portfolios, accessing the portfolio attribute will instead return
    a dictionary corresponding to that attribute, where keys are the
    portfolio names and values are the respective attribute.

    Parameters:
        assets:
            An asset or iterable of assets to be trakced by this environment

        portfolios:
            A portfolio or iterable of portfolios to be tracked by this
            environment

        base:
            Controls the default base currency for all assets and portfolios
            instantiated in this environment. Defaults to the current global base
            at the time of instantiation (typically USD)

        time_control:
            Controls how env.start and env.end properties function. When passed
            as "any" (default), start and end are the min and max available start
            and end of all tracked datasets, respectively. When time_control is
            passed as "all", min and max are flipped (start is the max of all
            dataset start dates, end is the min of all dataset end dates)

        force:
            Whether or not to force the creation of new assets when their
            instantiation fails due to data errors. For example, calling
            env.Stock("MYSTOCK") will faill if no data is available locally or
            online for such a ticker. However, force=True will guarantee that
            the stock instantiated with a fake dataset.

    Attributes:
        date (datetime):
            This environment's current date (the last valuation date of all
            currently tracked AlphaGradient objects). Any assets that are newly
            instantiated inside of this environment will automatically be
            valuated on this date

        start (datetime):
            This environment's start date, which all tracked assets will
            valuate to if no steps have been taken. environment.date returns
            to this date when reset is called.

        end (datetime):
            This environment's end date, which algorithms will use as a default
            to determine when backtesting should end if none is provided.

        resolution (timedelta):
            The default period of time inbetween timesteps.

        base (str):
            The base currency used by this environment represented as a currency
            code. All newly tracked/insantiated assets and objects will use
            this currency as a default base if none are provided during
            intantiation

        assets (list[Asset]):
            A list of assets currently within or tracked by this environment.

        portfolios (dict[str, Portfolio]):
            A dictionary of portfolios in which keys are the portfolio names,
            which are provided during instantiation. If no names are provided,
            defaults to "MAIN", then "P0", "P1", "P2", ..., "PN"

        status (Environment.Status):
            A member of the Status enum which corresponds to how many portfolios
            this environment is currently tracking. Controls behavior of
            environment bound methods that facilitate portfolio transactions
            such as buy, sell, short, and cover.
    """

    class Status(Enum):
        """
        Denotes an environment's portfolio status, controlling environment
        bound methods for portfolio transactions

        Status indicates how many portfolios belong to this environment.
        Environments without a portfolio will not be able to perform portfolio
        bound methods. Environments with a single portfolio will autonatically
        route all portfolio methods to the bound portoflio. Environments with
        multiple portfolios require calls to portfolio bound methods to specify
        the name of the portfolio on which the transaction is to be executed.
        If no name is specified, attempt to perform the transaction on a
        portfolio named "MAIN", if one exists.

        Attributes:
            NONE:
                This Environment has NO portfolios, and is therefore incabable
                of accepting/rerouting calls to portfolios made directly on
                the environment object. This is a legacy option, as current
                Environment objects automatically instantiate a portfolio
                if none are passed.

            SINGLE:
                This Environment only tracks a single intantiated portfolio,
                which is bound to the environments 'main' attribute (accessible
                at env.main). Portfolio calls made on the environment will be
                automatically redirected to the main portfolio automatically.

            MULTIPLE:
                This Environment tracks multiple portfolios. When Portfolio
                calls are made on the environment, they accept a "name="
                keyword argument that allows the user to specify the tracked
                portfolio on which they would like to execute the transaction.
                By default, calls are rerouted to the main portfolio should a
                name fail to be specified.

        Examples:

            .. code:: python

                # A portfolio with only a single tracked portfolio
                spy = ag.Stock("SPY")
                single_env = ag.Environment(assets=[spy])

                # A portfolio with multiple tracked portfolios
                main_portfolio = ag.Portfolio(1_000_000, name="MAIN", base="USD")
                alt_portfolio = ag.Portfolio(1_000_000, name="ALT", base="JPY")
                multiple_env = ag.Environment(
                    assets=[spy],
                    portfolios=[main_portfolio, alt_portfolio]
                )

            .. code:: pycon

                >>> single_env.NONE
                False

                >>> single_env.SINGLE
                True

                >>> single_env.MULTIPLE
                False

                >>> multiple_env.NONE
                False

                >>> multiple_env.SINGLE
                False

                >>> multiple_env.MULTIPLE
                True

                >>> # Buying 10 shares of spy on the main portfolio
                >>> single_env.buy(spy, 10)
                >>> multiple_env.buy(spy, 10)

                >>> # Buying 10 shares of spy on the alternate portfolio
                >>> multiple_env.buy(spy, 10, name="ALT")

        """

        NONE = auto()
        SINGLE = auto()
        MULTIPLE = auto()

        @classmethod
        def get(cls, n: int) -> Environment.Status:
            """Returns the appropriate status member based on the
            quantity of portfolios passsed"""
            if n == 0:
                return cls.NONE
            elif n == 1:
                return cls.SINGLE
            else:
                return cls.MULTIPLE

    class AssetDict(WeakDict):
        """
        A weakref dictionary of assets belonging to one asset
        subclass. Allows environments attribute access to specific asset
        classes, as well as asset instantiation

        Examples:
            .. code:: python

                import alphagradient as ag

                env = ag.Environment()
                for ticker in ["SPY", "DIA", "QQQ"]:
                    env.stock(ticker)

            .. code:: pycon

                >>> env.stock
                {'SPY': <STOCK SPY: $146.84 /share>, 'DIA': <STOCK DIA: $114.66 /share>, 'QQQ': <STOCK QQQ: $92.62 /share>}

                >>> env.stock.spy
                <STOCK SPY: $146.84 /share>
        """

        def __init__(self, cls, env: Environment) -> None:
            self._name = cls.__name__
            self.c = cls
            self._env = env
            super().__init__()

        def __call__(self, *args: Any, **kwargs: Any) -> None:
            force = self._env.force
            if kwargs.get("force"):
                force = kwargs["force"]
                kwargs.pop("force")
            new = self.c(*args, force=force, **kwargs)
            new._valuate()
            self[new.name] = new
            return new

        def __setitem__(self, key: str, value: Asset) -> None:
            self._env._assets.append(value)
            super().__setitem__(key, value)

        def __str__(self) -> str:
            return str(dict(self))

        def __repr__(self) -> str:
            return self.__str__()

        def __getattr__(self, attr) -> Asset:
            try:
                return self[attr.upper()]
            except KeyError:
                raise AttributeError(
                    f"AlphaGradient Environment has no \
                                     {attr.capitalize()} instance {attr}"
                )

    def __init__(
        self,
        assets: Optional[Iterable[Asset]] = None,
        portfolios: Optional[Iterable[Portfolio]] = None,
        base: Optional[str] = None,
        time_control: Literal["any", "all"] = "any",
        force: bool = False,
    ) -> None:

        # Add tracking functionality for portfolios so they can be accepted as
        # a single argument
        self._assets: list[Asset] = []
        if isinstance(assets, dict):
            assets = list(assets.values())
        self.track([] if assets is None else assets)
        self._portfolios: list[Portfolio] = (
            []
            if portfolios is None
            else (
                [portfolios] if isinstance(portfolios, Portfolio) else list(portfolios)
            )
        )

        # Controlling how self.start, self.end, and self.resolution are determined
        if time_control == "any":
            self._guarantee_inclusion = False
        elif time_control == "all":
            self._guarantee_inclusion = True
        else:
            raise ValueError(
                f"time_control argument must be one of 'any' or 'all', received {time_control}"
            )

        # Initializing other attributes
        self._base: Currency = (
            self._global_base if not isinstance(base, Currency) else base
        )
        self._times: list[time] = []
        self._time_index: int = 0
        self.force: bool = force

        # Remove this in next update
        self._synced: bool = False

        # Creating the main portfolio if one is not provided.
        if portfolios is None:
            self.main = self.portfolio(0)
        else:
            self.main = self._portfolios[0]

    def __getattr__(self, attr: str) -> Any:
        """
        TODO: To make Environments' function more analogous to the global
        environment, we should require that constructor calls are capitalized,
        similar to instantiating the class normally. env.stock should not be
        callable, or at the very least, env.Stock should ALSO be callable to
        instantiate a local instance of the stock.
        """
        instantiable = {c.__name__.lower(): c for c in types.instantiable()}
        if attr in instantiable:
            assetdict = self.AssetDict(instantiable[attr], self)
            setattr(self, attr, assetdict)
            return assetdict
        elif attr in self.Status._member_names_:
            return self.status is self.Status[attr]
        elif getattr(Portfolio, attr, False):
            return self._redirect(attr)
        else:
            raise AttributeError(
                f"AlphaGradient Environment object has no attribute {attr}"
            )

    def __contains__(self, other: object) -> bool:
        if isinstance(other, Asset):
            return other in self._assets
        elif isinstance(other, Portfolio):
            return other in self._portfolios
        else:
            return other in [asset.name for asset in self._assets]

    @property
    def start(self) -> datetime:
        """
        The starting date of the environment based on all asset datasets
        currently instantiated and tracked

        When time control is "any" (default), returns the minimum of all asset
        dataset starting dates, such that the start date is determined by the
        lowest start date of **any** of the datasets. This means that the start
        date will potentially precede the available date ranges of other
        instantiated datasets.

        If "all" is passed in for time_control instead, returns the max of all
        asset dataset starting dates, such that **all** datasets must have
        'started' prior to  the start date, and are all included in the data.
        """
        data = [dataset.first for dataset in self.data()]
        method = min if self._guarantee_inclusion else max
        return method(data) if data else self._global_start

    @property
    def end(self) -> datetime:
        """
        The ending date of the environment based on all asset datasets currently
        instantiated and tracked

        When time control is "any" (default), returns the maximum of all asset
        dataset ending dates, such that the end date is determined by the
        highest end date of **any** of the datasets. This means that the end
        date will potentially exceed the available date ranges of other
        instantiated datasets.

        If "all" is passed in for time_control instead, returns the min of all
        asset dataset ending dates, such that **all** datasets must have data
        which meets or exceeds the end date (and are therefore included in the
        data)
        """
        data = [dataset.last for dataset in self.data()]
        method = max if self._guarantee_inclusion else min
        return method(data) if data else self._global_end

    @property
    def date(self) -> datetime:
        """The environmen's current date"""
        return self._date

    @property
    def resolution(self) -> timedelta:
        """
        The minimum dataset resolution based on all currently instantiated and
        tracked asset datasets.
        """
        data = [dataset.resolution for dataset in self.data()]
        return min(data) if data else self._global_res

    @property
    def base(self) -> Currency:
        """The default currency for assets/portfolios in this environment. If
        instantiated without an argument explicitly determining otherwise, new
        assets and portfolios instantiated in this environment will use this
        currency as their base."""
        return self._base

    @base.setter
    def base(self, code: str) -> None:
        if Currency.validate_code(code, error=True):
            self._base = Currency(code)

    @property
    def assets(self) -> list[Asset]:
        """A list of assets currently tracked by this environment"""
        return self._assets

    @property
    def portfolios(self) -> dict[str, Portfolio]:
        """A dictionary of portfolios tracked by this environment, with their
        respective names as keys"""
        return {p.name: p for p in self._portfolios}

    @property
    def status(self) -> Environment.Status:
        """The current portfolio status of this environment. Determines how
        portfolio calls on the environment are rerouted."""
        return self.Status.get(len(self.portfolios))

    @property
    def times(self) -> list[time]:
        """
        A list of times that should be evaluated when using this environment
        In an algorith.

        When empty, algorithms will dynamically determine the next
        available/best time step **at every time step**. This is VERY
        computationally expensive. It is therefore recommended that algorithms
        call env.finalize() during their setup so that this object is properly
        set before algorithm runtime.
        """
        return self._times

    @property
    def open(self) -> bool:
        """Whether or not the environment is 'open' (**any** of its tracked
        assets are available to be traded)"""
        return any(asset.open for asset in self.assets)

    @no_type_check
    def track(self, *to_track: Trackable) -> None:
        """
        For all bindables in * to_track, adds them to this environment

        TODO: TYPING FOR THIS IS BUSTED BECAUSE IT CURRENTLY ONLY HANDLES ASSETS

        Parameters:
            *to_track:
                A bindable object or iterable of bindable objects, all of which
                will become bound to this environment object,
        """
        for trackable in to_track:
            assets = [trackable] if isinstance(trackable, Asset) else list(trackable)
            if all(isinstance(asset, Asset) for asset in assets):
                for asset in assets:
                    getattr(self, asset.type.name.lower())[asset.name] = asset

    def portfolio(
        self, initial: float, name: Optional[str] = None, base: Optional[str] = None
    ) -> Portfolio:
        """
        Instantiates a portfolio within this environment

        Parameters:
            initial:
                The initial quantity of the base currency

            name:
                This portfolio's name, used for indexing and rerouting Portfolio
                calls made on the environment

            base:
                A currency code representing this portfolio's base currency.
                Uses the environments base currency as a default if none is
                provided.

        Returns:
            Returns a new portfolio based on the inputs, and adds it to this
            environment's tracked portfolios
        """
        if base is None:
            base = self.base.code
        Currency.validate_code(base, error=True)
        _name: Union[Environment, str] = self if name is None else name
        new = Portfolio(initial, _name, base)
        self._portfolios.append(new)
        return new

    @overload
    def data(self, dtype: Literal["list"] = "list") -> list[AssetData]:
        ...

    @overload
    def data(self, dtype: Literal["dict"]) -> dict[str, AssetData]:
        ...

    def data(self, dtype="list"):
        """Returns all of the datasets in the assets tracked by this environment

        TODO: THIS WOULD PROBABLY MAKE MORE SENSE AS A PROPERTY CALLED DATASETS
        OR SOMETHING... FREQUENTLY USED FOR ITERATING THROUGH AVAILABLE DATA.
        COULD EVEN MAKE SENSE AS A GENERATOR...

        Parameters:
            dtype (str | type):
                The dtype of the returned data object

        Returns:
            data (dict | list):
                Returns a list or dict of asset datasets, depending on the
                dtype input

        Raises:
            ValueError: When the dtype input is unrecognized/invalid
        """
        if dtype in [dict, "dict"]:
            return {asset.key: asset.data for asset in self.assets if asset.data}
        elif dtype in [list, "list"]:
            return [asset.data for asset in self.assets if asset.data]
        else:
            raise ValueError(
                f"Unsupported type {dtype=}. Environment data "
                "can only be returned as a list or a "
                "dictionary"
            )

    def finalize(
        self,
        include: Iterable[Type] = None,
        exclude: Iterable[Type] = None,
        manual: Iterable[TimeLike_T] = None,
    ) -> None:
        """
        Vastly improves efficiency of self.next()

        Improves the efficiency of self.next() by determining a set of relevant
        times for the currently instantiated assets, and iterating across those
        for time steps rather than dynamically determing the next time step
        after each step

        Should only be called after all assets containing new relevant
        timestamps have been instantiated. Creating assets with novel and
        necessary valuation points will result in them being ignored by calls
        to next()

        Paramaters:
            include:
                A list of asset types to include in the determination of the
                relevant times. Only assets types included in this list are
                used to determine what times are 'relvant', and will be added
                to the environment's 'times' attribute.

            exclude:
                A list of asset types to exclude in the determination of the
                relevant times. Asset types included in this list are only
                used to determine what to exlude if the 'include' parameter
                has not been specified.

            manual:
                Automatically overrides include and exlcude arguments. Takes
                a list of timelike arguments (either as strings or actual python
                time objets) and uses those as the environment's relevant times.
                useful for when you want evaluate an algorithm at a different
                resolution than the data. For examples, passing manual =
                ["9:30 AM", "4:00 PM"] will ensure that the algorithms using
                this environment will only valuate at 9:30:00 and 16:00:00 each
                day, even if the data has a 15m resolution.

        """
        if manual:
            self._times = [utils.to_time(t) for t in manual]
        else:
            self._times = [t for data in self.data() for t in data.get_times()]

        self._times = sorted(set(self._times))
        self._reset_time_index()

    def sync(self, date: Optional[DatetimeLike] = None) -> None:
        """Syncs all alphagradient objects in this environment to the given datetime

        Valuates all assets to the given date, and sets the date of all
        portfolios to the given date. This only occurs for objects
        within this environment, rather than globally. Date defaults to
        environment's current date if none is provided

        Args:
            date (datetime): The date to sync to

        Returns:
            None (NoneType): Modifies this environment in place
        """
        if date is None:
            self._date = self.start
        else:
            self._date = to_datetime(date)

        def sync_asset(asset):
            if getattr(asset, "reset", False):
                asset.reset()
            asset._valuate()

        def sync_portfolio(portfolio):
            portfolio.reset()

        if self._portfolios:
            deque(map(sync_portfolio, self._portfolios), maxlen=0)

        if self.assets:
            deque(map(sync_asset, self.assets), maxlen=0)

        self._synced = False

    def optimal_start(
        self, end: Optional[DatetimeLike] = None, t: Optional[TimeLike] = "9:30 AM"
    ) -> datetime:
        """
        Returns the optimal starting time for this environment based on
        currently instantiated and tracked assets

        Returns a backtest starting datetime that:
            * Is guaranteed to be within the date range of all intantiated assets
            * | Is guaranteed to have ample time for calculations of historical
              | volatility, beta, percent change etc. BEFORE the start date
            * Automatically adjusts to accomodate shorter ending periods

        Parameters:
            end (DatetimeLike):
                The end point which provides context for the optimal start. The
                optimal starting point for an algorithm will be different
                depending on when the backtest is ending.

            t (Optional[TimeLike]):
                The time time of day of the returned optimal start date.

        Returns:
            An optimal start date for a backtest using this environment.
        """
        data = list(self.data())
        if not data:
            return self.start

        max_start = max([dataset.first for dataset in data])
        min_end = min([dataset.last for dataset in data])

        return utils.optimal_start(
            start=self.start, max_start=max_start, min_end=min_end, end=end, t=t
        )

    def autosync(self) -> None:
        """Automatically syncs this environment to the optimal start time"""
        self.sync(self.optimal_start())

    def step(self, delta: Union[DateOrTime, timedelta, float] = None) -> None:
        """
        Takes a single time step in this environment, moving all
        alphagradient objects forward by the given delta

        The function that should be called in algorithms to iterate
        forward in time after everything has been accomplished and
        evaluated in the current period. Automatically moves all ag
        objects in this environment forward in time by the given delta,
        which defaults to the environment.resolution if none is provided.

        Parameters:
            delta:
                The magnitude of the time step taken
        """

        # Want to use the default resolution for this environment as a the step size if None
        self._date += (
            self.resolution if delta is None else utils.to_step(self.date, delta)
        )

        # Valuating assets at the new date, calling step hook
        for asset in self._assets:
            asset._valuate()
            asset._step(self.date)

        # Updating portfolio value histories at new time step
        for portfolio in self._portfolios:
            portfolio.update_positions()
            portfolio.update_history()

        for algo in types.algorithm.instances.values():
            if algo.env is self:
                algo.stats._update()

        # Cleaning out expired assets
        self._assets = [asset for asset in self.assets if not asset.expired]

    def next(self, make_step: bool = True) -> datetime:
        """
        Automatically updates this environment and all of its tracked assets
        to the next point of valuation

        env.next() automatically determines the next optimal point of valuation
        by dynamically calculating the next available datapoint for each
        instantiated asset dataset. If self.times has been defined
        (self.finalize() has been called), instead uses self.times to determine
        the next optimal valuation period.

        If make_step is passed as True (default), automatically jumps to the
        next time period before returning it.

        Parameters:
            make_step:
                Whether or not to automatically make the time step (iterate to
                the next datetime) when called. Defaults to True

        Returns:
            The next optimal starting date
        """

        nextt = self.date

        # Operating procedures for when finalize() has been called on an environment
        if self.times:

            # Reset the time index after syncing or initialization
            if not self._synced:
                self._reset_time_index()
                self._synced = True

            # The new index is the next in order
            new_index = self._time_index + 1

            # Reset the index when we get to the end of a day, add one day to the valuation date
            if new_index >= len(self._times):
                nextt += timedelta(days=1)
                new_index = 0

            # Setting the time of to the time at the new (next) index
            nextt = utils.set_time(nextt, self._times[new_index])

            # Updating the time index
            self._time_index = new_index

        # Dynamically determining the next best valuation time at every time step; very costly
        else:
            nextt = min([asset.next for asset in self.assets])

        # Perform the step function if requested
        if make_step:
            self.step(nextt)

        return nextt

    def _reset_time_index(self) -> None:
        """Resets the to what it should be after syncing or initialization"""

        # We only want to compare the time
        current = self.date.time()
        for i, t in enumerate(self._times):

            # Conditions for stopping point
            if current < t:

                # In this case, the proper index is the last index of times (the previous day)
                if i == 0:
                    self._time_index = len(self.times) - 1
                else:
                    self._time_index = i - 1
                break

        # If the current time is greater than all times, we must progress to the next day
        else:
            self._time_index = 0

    def buy(self, asset: Asset, quantity: float, name: str = None) -> None:
        """Buys an asset using this environment's main portfolio, unless
        specified otherwise.

        TODO: ALL OF THESE FUNCTIONS (BUY, SELL, SHORT, COVER) ARE LIKELY
        SUFFICIENTLY COVERED BY _redirect. SHOULD PROBABLY BE DELETED.
        ALSO, CONSIDER MAKING TRANSACTIONS RETURN THE POSITION THAT THEY
        CREATE OR ALTER. EG, return new_position

        Creates a long position in the given asset with a purchase
        volume given by 'quantity' within the respective portfolio

        Parameters:
            asset:
                The asset in which to create a long position

            quantity:
                The purchase quantity

            name:
                The name of the Portfolio where the transaction will take place

        Raises:
            ValueError:
                If environment has no active portfolios, or if name
                is not specified when there are multiple portfolios none
                of which are named "MAIN"
        """
        # Transactions require a portfolio
        if self.NONE:
            raise ValueError(
                "This environment has no active portfolios. "
                "Please instantiate one in order to make "
                "transactions"
            )

        # Transaction can only refer to one portfolio
        elif self.SINGLE:
            portfolio = self._portfolios[0]
            portfolio.buy(asset, quantity)

        # Portfolio of transaction must be specified
        elif self.MULTIPLE:

            # Default to main if none is provided
            if name is None:
                try:
                    self.portfolios["MAIN"].buy(asset, quantity)
                except KeyError:
                    raise ValueError(
                        "This environment has multiple "
                        "portfolios. The portfolio name "
                        "for this transaction must be "
                        "specified"
                    )

            # Try to access portfolio by name
            else:
                try:
                    portfolio = self.portfolios[name]
                    portfolio.buy(asset, quantity)
                except KeyError:
                    raise ValueError(
                        f"Environment has no portfolio "
                        "instance named "
                        f"{name.__repr__()}"
                    )

    def sell(self, asset: Asset, quantity: float, name: str = None) -> None:
        """
        Sells an asset using this environment's main portfolio, unless
        specified otherwise.

        Decrements a long position in the given asset by 'quantity'.
        Maximum sale quantity is the amount owned by the portfolio.

        Parameters:
            asset:
                The asset of the corresponding decremented position

            quantity:
                The sale quantity

            name:
                The name of the Portfolio where the transaction will take place

        Raises:
            ValueError:
                If environment has no active portfolios, or if name
                is not specified when there are multiple portfolios none
                of which are named "MAIN"
        """
        # Transactions require a portfolio
        if self.NONE:
            raise ValueError(
                "This environment has no active portfolios. "
                "Please instantiate one in order to make "
                "transactions"
            )

        # Transaction can only refer to one portfolio
        elif self.SINGLE:
            portfolio = self._portfolios[0]
            portfolio.sell(asset, quantity)

        # Portfolio of transaction must be specified
        elif self.MULTIPLE:

            # Default to main if none is provided
            if name is None:
                try:
                    self.portfolios["MAIN"].sell(asset, quantity)
                except KeyError:
                    raise ValueError(
                        "This environment has multiple "
                        "portfolios. The portfolio name "
                        "for this transaction must be "
                        "specified"
                    )

            # Try to access portfolio by name
            else:
                try:
                    portfolio = self.portfolios[name]
                    portfolio.sell(asset, quantity)
                except KeyError:
                    raise ValueError(
                        f"Environment has no portfolio "
                        "instance named "
                        f"{name.__repr__()}"
                    )

    def short(self, asset: Asset, quantity: float, name: str = None) -> None:
        """
        Shorts an asset using this environment's main portfolio, unless
        specified otherwise.

        Creates a short position in the given asset with a short sale
        volume given by 'quantity' within the respective portfolio

        Paramters:
            asset:
                The asset in which to create a short position

            quantity:
                The short sale quantity

            name:
                The name of the Portfolio where the transaction will take place

        Raises:
            ValueError:
                If environment has no active portfolios, or if name
                is not specified when there are multiple portfolios
                none of which are named "MAIN"
        """
        # Transactions require a portfolio
        if self.NONE:
            raise ValueError(
                "This environment has no active portfolios. "
                "Please instantiate one in order to make "
                "transactions"
            )

        # Transaction can only refer to one portfolio
        elif self.SINGLE:
            portfolio = self._portfolios[0]
            portfolio.short(asset, quantity)

        # Portfolio of transaction must be specified
        elif self.MULTIPLE:

            # Default to main if none is provided
            if name is None:
                try:
                    self.portfolios["MAIN"].short(asset, quantity)
                except KeyError:
                    raise ValueError(
                        "This environment has multiple "
                        "portfolios. The portfolio name "
                        "for this transaction must be "
                        "specified"
                    )

            # Try to access portfolio by name
            else:
                try:
                    portfolio = self.portfolios[name]
                    portfolio.short(asset, quantity)
                except KeyError:
                    raise ValueError(
                        f"Environment has no portfolio "
                        "instance named "
                        f"{name.__repr__()}"
                    )

    def cover(self, asset: Asset, quantity: float, name: str = None) -> None:
        """
        Covers the short sale of an asset using this environment's main
        portfolio, unless specified otherwise.

        Decrements a long position in the given asset by 'quantity'.
        Maximum sale quantity is the amount owned by the portfolio.

        Parameters:
            asset:
                The asset of the corresponding decremented position

            quantity:
                The sale quantity

            name:
                The name of the Portfolio where the transaction will take place

        Raises:
            ValueError:
                If environment has no active portfolios, or if name
                is not specified when there are multiple portfolios
                none of which are named "MAIN"
        """
        # Transactions require a portfolio
        if self.NONE:
            raise ValueError(
                "This environment has no active portfolios. "
                "Please instantiate one in order to make "
                "transactions"
            )

        # Transaction can only refer to one portfolio
        elif self.SINGLE:
            portfolio = self._portfolios[0]
            portfolio.cover(asset, quantity)

        # Portfolio of transaction must be specified
        elif self.MULTIPLE:

            # Default to main if none is provided
            if name is None:
                try:
                    self.portfolios["MAIN"].cover(asset, quantity)
                except KeyError:
                    raise ValueError(
                        "This environment has multiple "
                        "portfolios. The portfolio name "
                        "for this transaction must be "
                        "specified"
                    )

            # Try to access portfolio by name
            else:
                try:
                    portfolio = self.portfolios[name]
                    portfolio.cover(asset, quantity)
                except KeyError:
                    raise ValueError(
                        f"Environment has no portfolio "
                        "instance named "
                        f"{name.__repr__()}"
                    )

    def _redirect(self, attr: str) -> Any:
        """
        Redirects attribute access to a the proper portfolio when
        user attempts to access portfolio attributes through the
        environment

        Examples:

            .. code:: pycon

                >>> # Buys 10 shares of spy on the env.main portfolio
                >>> env.buy(spy, 10)

                >>> # Buys 10 shares of spy on the "ALT" portfolio
                >>> env.buy(spy, 10, name="ALT")

        Parameters:
            attr:
                The attribute being accessed

        Returns:
            The attribute on the respective portfolio

        Raises:
            AttributeError:
                When the attribute does not exist
        """

        # No portfolios are present
        if self.NONE:
            raise AttributeError(
                f"Environment has no active portfolios. "
                "Must instantiate at least one "
                "portfolio to access portfolio "
                f"attribute {attr}"
            )

        # At least one portfolio is present
        else:

            # Attemting to access the attribute on the main portfolio
            try:
                obj = getattr(self.main, attr)

                # All portfolio method calls performed on the environment object should be routed
                # to the main portfolio, even if multiple portfolios are presently tracked
                if self.SINGLE or utils.is_func(obj):
                    return obj

                # If the attribute being accessed is not a callable, return a dictionary where keys
                # are portfolio names and values are the attribute being accessed on each portfolio
                else:
                    return {
                        name: getattr(p, attr) for name, p in self.portfolios.items()
                    }

            # Reroute attribute errors back to the environment object
            except AttributeError as e:
                raise AttributeError(
                    f"AlphaGradient Environment object has no attribute {attr}"
                )


# Using a protected keyword, attr must be set outside of the class
setattr(Environment, "type", types.environment)
setattr(types.environment, "c", Environment)


def _get_exchange_info() -> pd.DataFrame:
    """
    Returns a dataframe of exchange listings for initializing the Universe class

    Called upon initialization of the Universe class, updates the stock listings
    that are available by default when gathering stock data from the internet

    Returns:
        A dataframe of all available stock listings
    """

    # Getting updated stock listings
    base = "ftp://ftp.nasdaqtrader.com/symboldirectory/"
    dfs: list[pd.DataFrame] = []
    for file in ["nasdaqlisted.txt", "otherlisted.txt"]:
        _data = io.StringIO(request.urlopen(f"{base}{file}").read().decode())
        data = pd.read_csv(_data, sep="|")
        dfs.append(data[:-1])

    # Dropping test stocks
    dfs = [df[df["Test Issue"] == "N"].drop("Test Issue", axis=1) for df in dfs]

    # Unpacking the dfs
    nasdaq, other = dfs

    # Adding Exchange info for nasdaq listings, dropping columns that dont match
    nasdaq["Exchange"] = "NASDAQ"
    nasdaq.drop(
        ["Market Category", "Financial Status", "NextShares"], axis=1, inplace=True
    )

    # Converting exchange info to human-readable format
    converter = {"A": "NYSEMKT", "N": "NYSE", "P": "NYSEARCA", "Z": "BATS", "V": "IEXG"}
    other["Exchange"] = other["Exchange"].map(lambda s: converter[s])

    # Dropping unnecessary data, matching column labels
    other.drop(["CQS Symbol", "NASDAQ Symbol"], axis=1, inplace=True)
    other.rename({"ACT Symbol": "Symbol"}, axis=1, inplace=True)

    # Joining frames
    data = pd.concat(dfs).sort_values("Symbol")

    return data.reset_index(drop=True)


class Universe(dict):
    """
    A collection of stocks that can be efficiently filtered

    Special dictionaries that provide functionality for filtering thousands of
    stocks to meet a set of selection criteria

    Examples:

        .. code:: python

            uni = ag.Universe("all")

            # Selection will contain only Stocks whose beta is positive, and
            # whose value is more than 100 (of their base currency)
            selection = uni.filter[uni.beta > 0, uni.value > 100]

    Parameters:
        tickers:
            What tickers to include in the Universe's total pool. This can be
            passed in as a long string of tickers separated by spaces, a list
            of tickers, a stock object, or a list of stock objects. One can also
            pass in a float to instantiate a universe of exactly that many
            tickers, grabbed from a list of supported tickers (sorted
            alphabetically). Finally, one can pass in literals "local" or
            "all", which will intantiate ALL available tickers either locally
            (in persistent storage) or online, respectively.

        refresh:
            If true, this Universe will reinstantiate all tickers (even those
            with persistent storage available) from online data, 'refreshing'
            them.

        verbose:
            Defaults to True. Outputs Universe initialization performance
            metrics and progress.

    Attributes:
        verbose (bool):
            Whether or not universe functions (including initialization) will
            print their status/progress to stdout

        refresh (bool):
            Whether or not the universe will prefer to gather data from onlne,
            even if it is present locally

        tickers (list[str]):
            A list of stock tickers that are currently included in / tracked
            by this universe

        coverage (float):
            A value indicating the proportion of available stocks that are
            present in this universe

        supported (list[str]):
            A list of stock exhanges which Universes currently support
            filtering by explicitly during instantiation. Includes literals
            "NYSE", "NYSEARCA", "NASDAQ" and more.
    """

    _exchange_info: pd.DataFrame = pd.DataFrame()
    _eipath = Path(__file__).parent.joinpath("exchange_info.p")
    try:
        raise Exception
        _exchange_info = _get_exchange_info()
        with open(_eipath, "wb") as f:
            _exchange_info.to_pickle(f)
    except Exception as e:
        _exchange_info = pd.read_pickle(_eipath)

    def __init__(
        self,
        tickers: Union[float, Stock, str, list[str], list[Stock]] = "local",
        refresh: bool = False,
        verbose: bool = True,
    ) -> None:
        super().__init__()
        self.verbose: bool = verbose
        self.refresh: bool = refresh
        self.print: Any = print if self.verbose else lambda *args, **kwargs: None
        self._tickers: list[str] = []
        self._errors: list[str] = []
        self.update_local()

        tickers, stock_input = self._ticker_input(tickers)
        init_message = f"Initializing Universe: {len(tickers)} Stocks"
        self.print(init_message)
        self.print(("-" * len(init_message)))
        if not stock_input:
            self.add(tickers)

        self.filter = Filter(self)

    def __getattr__(self, attr: str) -> Any:
        try:
            # This checks that the attr being accessed exists on a stock
            self.benchmark.__getattribute__(attr)
            return FilterExpression(attr)
        except AttributeError:
            raise AttributeError(f"Universe object has no attribute {attr}")

    def __contains__(self, other: object) -> bool:
        if not isinstance(other, (Stock, str)):
            return NotImplemented
        if isinstance(other, Stock):
            return other in self.values()
        else:
            return other in self.keys()

    def __copy__(self) -> Universe:
        return Universe(list(self.values()), refresh=self.refresh, verbose=False)

    def __deepcopy__(self) -> Universe:
        return self.__copy__()

    @property
    def tickers(self) -> list[str]:
        """A list of tickers currently instantiated within this universe"""
        return self._tickers

    @property
    def errors(self) -> list[str]:
        """A list of tickers that have had errors in their instantiation"""
        return self._errors

    @property
    def coverage(self) -> float:
        """The proportion of the Universe's intitial listings that remain. For
        Universe objects, this is always 1, as they have not yet been filtered"""
        return 1

    @property
    def supported(self) -> list[str]:
        """A list of supported exchanges"""
        return self._exchange_info["Exchange"].unique.to_list()

    def add(
        self,
        tickers: Union[float, Stock, str, list[str], list[Stock]],
        refresh: bool = None,
    ) -> None:
        """
        Adds new stocks/tickers to the universe.

        Parameters:
            tickers (list[str] | list[Stock]):
                A list of tickers or already instantiated stock objects to be
                added to the universe

            refresh:
                Whether or not to prefer downloading stock data online even
                when present locally. Defaults to the universe's general setting
                when none is provided.
        """
        refresh = self.refresh if refresh is None else refresh
        tickers, stock_input = self._ticker_input(tickers)
        tickers = [ticker.upper() for ticker in tickers if ticker not in self._tickers]
        self._tickers = sorted(self._tickers + tickers)
        if not stock_input:
            errors = self._get_stocks(tickers, refresh=refresh)
            for error in errors:
                self._tickers.remove(error)
                self._errors.append(error)
        self._remove_errors()

    def update_local(self) -> None:
        """Updates the locally available tickers"""
        if self.refresh:
            self.local_p = []
            self.local_csv = []
            self.local = []
        else:
            pickle_path: Path = self._global_persistent_path
            raw_path: Path = self._global_persistent_path
            self.local_p = sorted(
                [
                    f[6:-2]
                    for f in os.listdir(pickle_path)
                    if f.startswith("STOCK_") and f.endswith(".p")
                ]
            )
            self.local_csv = sorted(
                [
                    f[6:-4]
                    for f in os.listdir(raw_path)
                    if f.startswith("STOCK_") and f.endswith(".csv")
                ]
            )
            self.local = sorted(list(set(self.local_p + self.local_csv)))

    def update_tickers(self) -> None:
        """Updates the exchange info for this universe object by getting stock
        listings from the internet"""
        self._exchange_info = _get_exchange_info()
        with open(self._eipath, "wb") as f:
            self._exchange_info.to_pickle(f)

    def _ticker_input(
        self, tickers: Union[float, Stock, str, list[str], list[Stock]]
    ) -> tuple[list[str], bool]:
        """Normalizes ticker list inputs before _get_stocks is called"""
        stock_input = False
        if isinstance(tickers, str):
            if tickers.lower() == "all":
                tickers = self._exchange_info["Symbol"].to_list()
            elif tickers.lower() == "local":
                tickers = self.local
            else:
                tickers = self._get_listings(tickers)

        elif isinstance(tickers, list):
            if all(isinstance(ticker, Stock) for ticker in tickers):
                assert type(tickers) is list[Stock]
                stocks = tickers
                tickers = [stock.name for stock in stocks]
                for stock, ticker in zip(stocks, tickers):
                    self[ticker] = stock
                stock_input = True

            elif not all(isinstance(ticker, str) for ticker in tickers):
                invalid = str(
                    [
                        type(ticker)
                        for ticker in tickers
                        if type(ticker) not in [Stock, str]
                    ]
                )[1:-1]
                raise TypeError(
                    "Ticker list inputs must contain only strings or only "
                    f"Stocks. List contained: {invalid}"
                )

        elif isinstance(tickers, Stock):
            self[tickers.name] = tickers
            tickers = [tickers.name]
            stock_input = True

        elif isinstance(tickers, Number):
            n = int(tickers)
            tickers = self.local[: (n if n < len(self.local) else len(self.local))]
            if len(tickers) <= n:
                n = n if n < len(self._exchange_info) else len(self._exchange_info)
                info = self._exchange_info["Symbol"].to_list()[:n]
                i = 0
                while len(tickers) < n:
                    if info[i] not in tickers:
                        tickers.append(info[i])
                    i += 1

            tickers.sort()

        else:
            raise TypeError(
                f"Invalid input type {type(tickers).__name__} for tickers. "
                "Tickers must be a list of strings, a list of AlphaGradient "
                "Stocks, or the name of an exchange (currently supports NYSE "
                "and NASDAQ)"
            )

        # For mypy
        assert type(tickers) is list[str]

        return tickers, stock_input

    def _get_stocks(self, tickers: list[str], refresh: bool = False) -> list[str]:
        """
        Given a list of tickers (list(str)), adds all of them as entries to self

        Takes in a list of normalized tickers (list(str)) and adds them as
        entries to the dictionary, where keys are tickers and values are the
        initialized assets

        Parameters:
            tickers:
                A list of stock tickers to be added

            refresh:
                Whether to prefer online instead of local data

        Returns:
            A list of delisted tickers that have been removed from self.tickers
            because of their failure to initialize, typically from a failure to
            retrieve the data from yfinance/yahoo finance api
        """

        def get_instantiated(tickers: list[str]) -> list[str]:
            """Gets the tickers that are already instantiated in AG"""
            to_instantiate = []
            instantiated = []
            for ticker in tickers:
                if types.stock.instances.get(ticker):
                    instantiated.append(ticker)
                else:
                    to_instantiate.append(ticker)

            if instantiated:
                stock_or_stocks = "stock" if len(instantiated) == 1 else "stocks"
                is_or_are = "is" if len(instantiated) == 1 else "are"
                self.print(
                    f"[1]: adding {len(instantiated)} {stock_or_stocks} that "
                    f"{is_or_are} already instantiated"
                )
                for ticker in instantiated:
                    self[ticker] = types.stock[ticker]
            return to_instantiate

        # Ensures that we don't reinitialize stocks that already exist
        all_tickers = get_instantiated(tickers)

        # The number of columns for progress displays
        ncols = 100
        self.print(
            f"[2]: initializing {len(all_tickers)} stocks to be added to Universe"
        )

        # Separating uninitialized tickers into online and local
        local = []
        online = all_tickers[:]
        if not refresh:
            local = [ticker for ticker in all_tickers if ticker in self.local]
            online = [ticker for ticker in all_tickers if ticker not in local]

        def get_local(tickers: list[str]) -> None:
            """Gets all tickers that have data available locally"""
            self.print(f"[3]: initializing {len(tickers)} stocks from local data")
            stocks = p_map(
                lambda ticker: Stock(ticker),
                tickers,
                ncols=ncols,
                disable=(not self.verbose),
            )
            for stock in stocks:
                self[stock.name] = stock
            self.print()

        def get_online(tickers: list[str], timeout: float = 5) -> None:
            """Gets all remaining data not otherwise handled

            Args:
                tickers (list(str)): A list of tickers to be added
                timeout (Number): The amount of time to wait for each
                    stock when attempting download before considering it a failure / timeout error
            """
            self.print(f"[4]: initializing {len(tickers)} stocks from online data")
            for i, batch in enumerate(utils.auto_batch(tickers)):
                self.print(f"Batch {i + 1}: downloading {len(batch)} stocks")
                data = yf.download(
                    " ".join(batch),
                    group_by="Ticker",
                    auto_adjust=False,
                    progress=self.verbose,
                    show_errors=False,
                    timeout=timeout,
                )

                to_remove = list(shared._ERRORS.keys())
                for ticker in to_remove:
                    batch.remove(ticker)

                self.print(
                    f"Initializing {len(batch)} Stocks from downloaded batch "
                    f"({len(to_remove)} failures)"
                )

                if batch:
                    stocks = p_map(
                        lambda ticker: Stock(
                            ticker, data=data[ticker].dropna(how="all")
                        ),
                        batch,
                        ncols=ncols,
                        disable=(not self.verbose),
                    )
                else:
                    stocks = []

                for stock in stocks:
                    self[stock.name] = stock
                self.print()

        def get_online_mp(
            tickers: list[str], timeout: float = 5
        ) -> dict[str, list[str]]:
            """A version of get_online that utilizes multiprocessing"""
            size = utils.auto_batch_size(tickers)
            batches: Any = math.ceil(len(tickers) / size)
            self.print(
                f"[4]: initializing {len(tickers)} stocks from online data "
                f"({batches} batches)"
            )

            def get_batch(batch: list[str]) -> tuple[list[Stock], dict[str, list[str]]]:
                # Not sure why this is necessary... but it seems to prevent yf.download from halting
                data = yf.Ticker("SPY").history(period="1d")

                # TODO: Custom implementation of data gathering from public APIs
                # like yahoo/google finance, so that we don't have to deal with
                # stuff like this.

                # The actual data we need
                data = yf.download(
                    " ".join(batch),
                    group_by="Ticker",
                    auto_adjust=False,
                    progress=False,
                    show_errors=False,
                    timeout=timeout,
                )
                to_remove = list(shared._ERRORS.keys())
                errors = {
                    "timeout": [
                        ticker
                        for ticker, error in shared._ERRORS.items()
                        if error
                        == "No data found for this date range, symbol may be delisted"
                    ],
                    "delisted": [
                        ticker
                        for ticker, error in shared._ERRORS.items()
                        if error == "No data found, symbol may be delisted"
                    ],
                }
                for ticker in to_remove:
                    batch.remove(ticker)

                data = data.sort_index()

                return (
                    [
                        Stock(ticker, data=data[ticker].dropna(how="all"))
                        for ticker in batch
                    ],
                    errors,
                )

            batches = list(utils.auto_batch(tickers))
            stocks = p_map(get_batch, batches, ncols=ncols, disable=(not self.verbose))
            errors = {
                "delisted": [
                    error for value in stocks for error in value[1]["delisted"]
                ],
                "timeout": [error for value in stocks for error in value[1]["timeout"]],
            }
            stocks = [stock for value in stocks for stock in value[0]]
            for stock in stocks:
                self[stock.ticker] = stock

            return errors

        # If refreshing, all stocks are initialzed via newly downloaded
        # online data
        if refresh:
            errors = get_online_mp(all_tickers)

        else:
            if local:
                get_local(local)
            else:
                self.print(
                    f"[3]: no local data detected, moving on to online initialization"
                )
            if online:
                errors = get_online_mp(online)
            else:
                errors = {"delisted": [], "timeout": []}

        num_errors = len(errors["delisted"]) + len(errors["timeout"])
        delisted = errors["delisted"][:]
        timeouts = errors["timeout"][:]

        self.print(
            f"Successfully added {(len(all_tickers) - num_errors)} of "
            f"{len(all_tickers)} stocks ({len(delisted)} failures, "
            f"{len(timeouts)} timeouts, {num_errors} total errors))"
        )

        previous = []

        # Attempting timeout one more time
        # TODO: This is not a complete solution
        while timeouts:
            self.print(f"\n[5]: retrying {len(timeouts)} timeouts")
            errors = get_online_mp(timeouts, timeout=10)

            n_timeout = len(errors["timeout"])
            n_delisted = len(errors["delisted"])
            n_attempts = len(timeouts)
            n_errors = n_timeout + n_delisted
            n_success = n_attempts - n_errors
            self.print(
                f"{n_success} / {n_attempts} successful timeout reattempts "
                f"({n_delisted} failures, {n_timeout} timeouts, {n_errors} "
                "total errors)"
            )

            delisted += errors["delisted"]
            previous = timeouts[:]
            timeouts = []

            # Just retrying timeouts once before considering them failures
            for ticker in errors["timeout"]:
                if ticker in previous:
                    delisted.append(ticker)
                else:
                    timeouts.append(ticker)

        for ticker in delisted:
            all_tickers.remove(ticker)

        for ticker in all_tickers:
            types.stock.instances[ticker] = self[ticker]

        return delisted

    def _get_listings(self, exchange: str) -> list[str]:
        """Gets the listings for a particular exchange"""
        info = self._exchange_info
        return info[info["Exchange"] == exchange]["Symbol"].to_list()

    def _remove_errors(self) -> None:
        """Removes errors from list of tracked tickers"""
        for symbol in self.errors:
            ei = self._exchange_info[self._exchange_info["Symbol"] == symbol].index
            self._exchange_info.drop(ei, inplace=True)
        with open(self._eipath, "wb") as f:
            self._exchange_info.to_pickle(f)


class Filter:
    """
    A universe's filter object that allows stock filtering

    A filter object attached to all universe objects that automatically
    processes filter expressions for its attached universe

    Thse objects are not intended to be instantiated by the end user, and only
    have utility in their attachment to a Universe object.

    Parameters:
        universe: The universe object to attach to
    """

    def __init__(self, universe: Universe) -> None:
        self.universe = universe

    def __getitem__(self, item: Any) -> Universe:
        """The standard method of operating a universe filter. Filter
        expressions should act as 'indexing' the universe"""
        if not isinstance(item, Iterable):
            item = [item]

        universe = copy(self.universe)
        for filterr in self._validate_filters(item):
            if filterr.called:
                universe = self._filter_mp(universe, filterr)
            else:
                universe = self._filter(universe, filterr)

        return universe

    @staticmethod
    def _filter_mp(universe: Universe, filterr: FilterExpression) -> UniverseView:
        """A multiprocessing version of the filter execution"""

        def process_stock(stock):
            return (stock.name, filterr._exec(stock))

        filtered: Union[dict[str, Stock], list[Stock]] = []

        with Pool() as pool:
            filtered = dict(pool.map(process_stock, universe.values()))
        filtered = [v for k, v in universe.items() if filtered[k]]
        return UniverseView(universe, filtered, filterr)

    @staticmethod
    def _filter_mp_v2(universe: Universe, filterr: FilterExpression) -> UniverseView:
        """A multiprocessing version of the filter execution that utilizes
        automatic batching of the universe's current stocks"""

        def process_batch(batch):
            return [(stock, filterr._exec(stock)) for stock in batch]

        batches = list(utils.auto_batch(list(universe.values())))
        filtered = []
        with Pool() as pool:
            filtered = pool.map(process_batch, batches)

        filtered = [stock for batch in filtered for stock, success in batch if success]

        return UniverseView(universe, filtered, filterr)

    @staticmethod
    def _filter(universe: Universe, filterr: FilterExpression) -> UniverseView:
        """Executes a filter expression on a universe

        Executes a single filter expression on this filter's universe,
        returning a universe view that is the result of the filter

        Parameters:
            universe (Universe | UniverseView):
                The universe to filter

            filterr (FilterExpression):
                The expression to apply

        Returns:
            The filtered universe object
        """
        filtered = [v for v in universe.values() if filterr._exec(v)]
        return UniverseView(universe, filtered, filterr)

    @staticmethod
    def _validate_filters(filters: Iterable[ValidFilter]) -> list[FilterExpression]:
        """Validates that all objects in a filter indexing operation are valid
        filters or filter expressions"""

        def validate(filterr):
            if isinstance(filterr, list):
                if all(isinstance(obj, str) for obj in filterr):
                    filterr = FilterExpression(filterr, special="strlist")

                elif all(isinstance(obj, Stock) for obj in filterr):
                    filterr = FilterExpression(filterr, special="stocklist")

            elif isinstance(filterr, dict):
                if all(
                    ((isinstance(k, str), isinstance(v, Stock)) == (True, True))
                    for k, v in filterr.items()
                ):
                    filterr = FilterExpression(filterr, special="dict")

            if not isinstance(filterr, FilterExpression):
                raise TypeError(f"Invalid filter {filterr}")

            return filterr

        return [validate(filterr) for filterr in filters]


class FilterExpression:
    """
    An expression compiled inside of a filter indexing operation

    An object produced by performing a boolean operation on a stock attribute,
    when the attribute is accessed from a universe object. When compiled,
    filter expressions will always produce a function that takes in a single
    stock object as an input, and produces a boolean output. Functions passed
    into a filter indexing operation that operate similarly are also valid
    filter expressions.

    For the sake of example, let x be a Universe or UniverseView (they operate
    identically when being filtered). The expression "x.beta() > 1" will
    produce a filter expression object that, when compiled, will result in a
    function whose input is a stock object and output is the boolean result of
    "stock.beta() > 1". Any expression that takes a single stock as an input
    with a boolean return is a valid expression inside of a filtering operation.
    For example, the expression "x.value" will return a filter expression whos
    attached function will evaluate the boolean of conversion of a stock's
    value -- False if the stock is worthless else True.

    Filter expression objects can only be created by accessing stock attributes
    on a universe object.

    Filter Expressions are only intended to be created by Universe and Filter
    objects. They should never be instantiated by end users.

    Parameters:
        attr:
            The stock attribute to access for each stock

        special:
            Used when creating nonstandard filter expressions
    """

    attr: str

    def __init__(
        self,
        attr: Union[str, ValidFilter],
        special: Optional[Literal["strlist", "stocklist", "dict"]] = None,
    ) -> None:
        self.operation: str = ""
        self.condition: Any = None
        self.exp: Optional[Callable] = None
        self.args: Any = None
        self.kwargs: Any = None
        self.called: bool = False
        self.is_other: bool = False

        if isinstance(attr, str):
            self.attr = attr
        else:
            self.attr = "direct"
            self.operation = "filter"
            if type(attr) is list[str]:
                self.condition = attr
            elif type(attr) is list[Stock]:
                self.condition = [stock.name for stock in attr]
            elif type(attr) is dict:
                self.condition = list(attr.keys())

        """
        if special is not None:
            self.attr = "direct"
            self.operation = "filter"
            if special == "strlist":
                self.condition = attr
            elif special == "stocklist":
                self.condition = [stock.name for stock in attr]
            elif special == "dict":
                self.condition = list(attr.keys())
        """

    def __str__(self) -> str:
        convert = {
            "__lt__": "<",
            "__le__": "<=",
            "__eq__": "==",
            "__ne__": "!=",
            "__gt__": ">",
            "__ge__": ">=",
            "filter": "filter",
        }
        attr = self.attr_string()

        if self.is_other:
            return attr

        elif self.operation is None:
            return f"if {attr}"

        return f"{attr} {convert[self.operation]} {self.condition}"

    def __hash__(self) -> int:
        kwargs = None
        if self.kwargs:
            kwargs = ((k, v) for k, v in self.kwargs)
        return (self.attr, self.args, kwargs, self.operation, self.condition).__hash__()

    def __call__(self, *args: Any, **kwargs: Any) -> FilterExpression:
        self.args = args
        self.kwargs = kwargs
        self.called = True
        return self

    def __bool__(self) -> bool:
        if self.is_other:
            return True
        raise NotImplementedError(
            f"Direct boolean conversion not currently supported for filter "
            "expressions. If checking for a false value, try "
            f"'{self.attr_string()} == False'"
        )

    def __lt__(self, other: object) -> FilterExpression:
        if self.is_other:
            return NotImplemented
        if isinstance(other, FilterExpression):
            other.is_other = True
        if not self.operation:
            self.operation = "__lt__"
        if not self.condition:
            self.condition = other
        return self

    def __le__(self, other: object) -> FilterExpression:
        if self.is_other:
            return NotImplemented
        if isinstance(other, FilterExpression):
            other.is_other = True
        if not self.operation:
            self.operation = "__le__"
        if not self.condition:
            self.condition = other
        return self

    def __eq__(self, other: object) -> FilterExpression:  # type: ignore[override]
        if self.is_other:
            return NotImplemented
        if isinstance(other, FilterExpression):
            other.is_other = True
        if not self.operation:
            self.operation = "__eq__"
        if not self.condition:
            self.condition = other
        return self

    def __ne__(self, other: object) -> FilterExpression:  # type: ignore[override]
        if self.is_other:
            return NotImplemented
        if isinstance(other, FilterExpression):
            other.is_other = True
        if not self.operation:
            self.operation = "__ne__"
        if not self.condition:
            self.condition = other
        return self

    def __gt__(self, other: object) -> FilterExpression:
        if self.is_other:
            return NotImplemented
        if isinstance(other, FilterExpression):
            other.is_other = True
        if not self.operation:
            self.operation = "__gt__"
        if not self.condition:
            self.condition = other
        return self

    def __ge__(self, other: object) -> FilterExpression:
        if self.is_other:
            return NotImplemented
        if isinstance(other, FilterExpression):
            other.is_other = True
        if not self.operation:
            self.operation = "__ge__"
        if not self.condition:
            self.condition = other
        return self

    def __contains__(self, other: object) -> FilterExpression:
        if self.is_other:
            return NotImplemented
        if isinstance(other, FilterExpression):
            other.is_other = True
        if not self.operation:
            self.operation = "__contains__"
        if not self.condition:
            self.condition = other
        return self

    def _build_attr(self) -> Callable[[Stock], Any]:
        """Builds a function for getting the attribute being accessed on the stock"""
        base = lambda stock: getattr(stock, self.attr)
        called = None
        if self.called:
            args = self.args or tuple()
            kwargs = self.kwargs or {}
            called = lambda stock: base(stock)(*args, **kwargs)
        return called or base

    def _build_condition(self) -> Callable[[Stock], Any]:
        """Builds a function for getting the condition, and accessing the
        attribute of the condition if it is another stock attr"""
        if isinstance(self.condition, FilterExpression):
            base = lambda stock: getattr(stock, self.condition.attr)
            called = None
            if self.condition.called:
                args = self.condition.args or tuple()
                kwargs = self.condition.kwargs or {}
                called = lambda stock: base(stock)(*args, **kwargs)
            return called or base
        return lambda stock: self.condition

    def _build_exp(self) -> Callable[[Stock], Any]:
        """Builds the entire function"""
        attr = self._build_attr()

        if self.operation is None:
            return attr

        condition = self._build_condition()

        base = lambda stock: getattr(attr(stock), self.operation)(condition(stock))

        checker = lambda value: False if value == NotImplemented else value

        return lambda stock: checker(base(stock))

    def _exec(self, *args: Any, **kwargs: Any) -> bool:
        """Executes the function compiled by this filter"""
        if self.exp is None:
            self.exp = self._build_exp()
        result = self.exp(*args, **kwargs)
        try:
            return bool(result)
        except TypeError as e:
            raise TypeError(
                f"Filter expression '{self}' does not return a boolean or "
                "boolean-convertible value"
            ) from e

    @no_type_check
    @staticmethod
    def from_string(string: str) -> FilterExpression:
        """
        Takes in a string of a valid filter expressions and returns it as a
        filterexpression object

        TODO: This method does not currently function as expected, needs better
        parsing. Do not use for the time being.
        """

        def is_numeric_char(char):
            return char.isnumeric or char in [".", "-"]

        def is_numeric(string):
            return all(is_numeric_char(char) for char in string)

        items = string.split(" ")
        attr = items[0]
        operation = items[1]
        condition = " ".join(items[2:])

        if condition.startswith("["):
            condition = condition[1:-1].split(" ")
            return FilterExpression(condition, special="strlist")

        elif is_numeric(condition):
            try:
                condition = float(condition)
                exp = FilterExpression(attr)
                exp.operation = operation
                exp.condition = condition
                return exp
            except ValueError:
                pass

        exp = FilterExpression(attr)
        exp.operation = operation
        exp.condition = condition

        return exp

    def attr_string(self) -> str:
        """Builds a string representation of the attribute being accessed"""
        result = f"stock.{self.attr}"
        args = ""
        kwargs = ""
        if self.args is not None:
            end = -1
            if len(self.args) < 2:
                end -= 1
            args = str(self.args)[1:end]
        if self.kwargs is not None:
            kwargs = str([f"{k}={v}" for k, v in self.kwargs.items()])[1:-1]
            called = True
        if args or kwargs:
            if args:
                result = f"{result}({args}"
                if kwargs:
                    result = f"{result}, {kwargs}"
                result += ")"
            else:
                result = f"{result}({kwargs})"
        elif self.called:
            result = f"{result}()"

        return result


class UniverseView(Universe):
    """A Universe with filters applied, with functionality for removing,
    adding, or changing filters applied"""

    def __init__(
        self,
        base: Universe,
        stocklist: Union[float, Stock, str, list[str], list[Stock]],
        filterr: FilterExpression,
    ) -> None:
        super().__init__(stocklist, refresh=False, verbose=False)
        if type(base) is Universe:
            self.universe = base
            self.filters = OrderedDict({filterr: len(self)})
        elif type(base) is UniverseView:
            self.universe = base.universe
            self.filters = base.filters
            self.filters[filterr] = len(self)
        else:
            raise TypeError(f"Unacceptable base for a universe view {type(base)=}")

    @property
    def coverage(self) -> float:
        """The proportion of stocks that remain in this universe compared to
        its original instance."""
        return len(self) / len(self.universe)

    @property
    def history(self) -> str:
        """A formatted string of this portfolio's filter history"""
        initial = len(self.universe)
        result = f"Universe: {initial} stocks"
        result += "\n" + ("-" * len(result))
        prev = initial
        for filterr, curr in self.filters.items():
            diff = prev - curr
            step_percentage = round((diff / prev) * 100, 3) if prev > 0 else 0
            total_percentage = (
                round((1 - (curr / initial)) * 100, 3) if initial > 0 else 0
            )
            result += f"\n{filterr.__str__()}: {curr} results"
            result += f" | {step_percentage}% ({diff}) removed"
            result += f" | {total_percentage}% ({initial - curr}) total removed"
            prev = curr

        return result


# Using a protected keyword, attr must be set outside of the class
setattr(Universe, "type", types.universe)
setattr(types.universe, "c", Universe)
