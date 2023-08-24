import os
from zipline.api import order_target, record, symbol
from zipline.finance import commission, slippage

def initialize(context):
    context.sym = symbol("AAPL")
    context.i = 0

    context.set_commission(commission.PerShare(cost=0.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())

def handle_data(context, data):
    # Skip the first 60 days to get full WindowsError
    context.i += 1
    if context.i < 100:
        return

    # Computer Avgs
    short_mavg = data.history(context.sym, "price", 30, "1d").mean()
    long_mavg = data.history(context.sym, "price", 100, "1d").mean()

    # Trading logic
    # Buy when short crosses long -> upwards momentum
    # Otherwise, downwards momentum so we short
    if short_mavg > long_mavg:
        order_target(context.sym, 100)
    elif short_mavg == long_mavg:
        order_target(context.sym, 0)
    else:
        order_target(context.sym, -100)

    # Save values for later inspection
    record(
        AAPL=data.current(context.sym, "price"),
        short_mavg=short_mavg,
        long_mavg=long_mavg,
    )


# Display the results
def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    import logging

    logging.basicConfig(
        format="[%(asctime)s-%(levelname)s][%(name)s]\n %(message)s",
        level=logging.INFO,
        datafmt="%Y-%m-%dT%H:%M:%S%z",
    )

    log = logging.getLogger("Algorithm")

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel("Portfolio value (USD)")

    ax2 = fig.add_subplot(212)
    ax2.set_ylabel("Price (USD)")

    if "AAPL" in results and "short_mavg" in results and "long_mavg" in results:
        results["AAPL"].plot(ax=ax2)
        results[["short_mavg", "long_mavg"]].plot(ax=ax2)

        trans = results[[t != [] for t in results.transactions]]
        buys = trans[[t[0]["amount"] > 0 for t in trans.transactions]]
        sells = trans[[t[0]["amount"] < 0 for t in trans.transactions]]
        ax2.plot(
            buys.index,
            results.short_mavg.loc[buys.index],
            "^",
            markersize=10,
            color="m",
        )
        ax2.plot(
            sells.index,
            results.short_mavg.loc[sells.index],
            "v",
            markersize=10,
            color="k",
        )
        plt.legend(loc=0)
    else:
        msg = "AAPL, short_mavg & long_mavg data not captured using record()."
        ax2.annotate(msg, xy=(0.1, 0.5))
        log.info(msg)

    plt.show()

    if "PYTEST_CURRENT_TEST" in os.environ:
        plt.close("all")
