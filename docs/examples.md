## 💰 Finance Example: Detecting Sudden Stock Price Drops

Imagine you're analyzing intraday stock prices and want to:

* Ignore the first few readings (low liquidity at open),
* Detect when the price drops by more than 2% compared to the previous one,
* Take the first 3 such "alert-worthy" events.

```python
from libloop.flow import Flow

def price_drops(prices):
    previous = None
    for price in prices:
        if previous is not None and (price < previous * 0.98):
            yield (previous, price)
        previous = price

prices = get_intraday_prices("AAPL")  # returns a list or generator of floats

alerts = (
    Flow(prices)
    .shed(15)                       # skip first 15 ticks
    .morph(lambda p: round(p, 2))  # round prices
    .morph(price_drops)            # detect drops (as generator)
    .spill()                       # flatten result of yield tuples
    .drip(3)
    .list()
)

print("⚠️ Sudden drops detected:")
for before, after in alerts:
    print(f"From ${before} → ${after} ({round((after - before)/before*100, 2)}%)")
```

> Here, `.morph(price_drops).spill()` lets us yield multiple values per input—like `flatMap` in FP.

---

## 🧠 NLP Example: Finding Long, Unique Keywords

Suppose you have a bunch of user reviews or articles. You want to:

* Tokenize words,
* Filter out short or stop words,
* Lowercase and deduplicate,
* Take the top 10 interesting terms.

```python
from libloop.flow import Flow

stopwords = {"the", "and", "of", "to", "a", "in", "it", "is", "that"}

def tokenize(text):
    return (word.strip(".,!?") for word in text.split())

corpus = [
    "The service in the restaurant was outstanding and prompt.",
    "I loved the ambiance and the way the food was presented.",
    "The waiter was courteous and attentive.",
    "Portions were generous, and everything tasted authentic."
]

keywords = (
    Flow(corpus)
    .spill(tokenize)              # flatten all words from sentences
    .morph(str.lower)
    .sift(lambda w: w not in stopwords and len(w) > 5)
    .distinct()                   # remove duplicates
    .drip(10)
    .list()
)

print("📝 Top keywords:")
for word in keywords:
    print("-", word)
```

> `.spill()` here breaks up each sentence into its words and flattens them into a single flow. `.distinct()` removes repetition, giving you a clean keyword list.

---

