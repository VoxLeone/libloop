## 🌍 Real-World Use Cases for `Flow`

Let's explore **real-world scenarios** where your `Flow` class (from `libloop`) could elegantly replace traditional loops and make the code more readable and declarative.
---

### 1. **Filtering Sensor Readings (IoT or Hardware Logs)**

Suppose you're processing temperature readings and only care about spikes above 75°F, but want to ignore the first 100 readings (warm-up period), and only analyze the first 10 significant spikes:

```python
from libloop.flow import Flow

def is_spike(temp):
    return temp > 75

readings = get_temperature_log()  # returns a long iterable of floats

spikes = (
    Flow(readings)
    .shed(100)           # ignore initial warm-up
    .sift(is_spike)      # only keep significant spikes
    .drip(10)            # only take the first 10
    .list()
)

print(spikes)
```

---

### 2. **Processing Usernames from a CSV (Data Cleaning)**

Suppose you're importing usernames, want to skip the header row, drop any with digits, and lowercase the first 5 valid ones:

```python
import re
from libloop.flow import Flow

def is_valid(username):
    return not re.search(r'\d', username)

with open("users.csv") as f:
    usernames = (line.strip().split(",")[0] for line in f)

cleaned = (
    Flow(usernames)
    .shed(1)               # skip header
    .sift(is_valid)
    .morph(str.lower)
    .drip(5)
    .list()
)

print(cleaned)
```

---

### 3. **Combining and Filtering Event Logs (Log Processing)**

Say you have multiple log files and want to merge them, drop lines that include `DEBUG`, and take the first 20 meaningful entries:

```python
from libloop.flow import Flow

def is_interesting(line):
    return "DEBUG" not in line

log1 = open("app.log")
log2 = open("worker.log")

events = (
    Flow(log1)
    .join(log2)
    .sift(is_interesting)
    .drip(20)
    .list()
)

for event in events:
    print(event.strip())
```

---

### 4. **Simple Recommendation System (Personalization)**

You want to recommend products to a user: filter out already purchased items, convert to display format, and show the top 3:

```python
from libloop.flow import Flow

all_items = get_all_items()
purchased_ids = {item.id for item in get_user_purchases()}

def not_purchased(item):
    return item.id not in purchased_ids

def to_display(item):
    return f"{item.name} (${item.price})"

suggestions = (
    Flow(all_items)
    .sift(not_purchased)
    .morph(to_display)
    .drip(3)
    .list()
)

print("You might like:")
for suggestion in suggestions:
    print("–", suggestion)
```

---

### 5. **Quick Email Preview from Raw Email Data**

Parse the first few subject lines from a raw stream of email data:

```python
from libloop.flow import Flow

def extract_subject(line):
    if line.startswith("Subject:"):
        return line[8:].strip()

emails = read_mbox("mailbox.mbox")

subjects = (
    Flow(emails)
    .morph(extract_subject)
    .sift(lambda x: x)      # remove None or empty
    .drip(5)
    .list()
)

print("Recent subjects:")
for s in subjects:
    print("-", s)
```

---

These examples show how `Flow` replaces **nested loops, counters, and conditions** with a more fluent and readable pipeline.

Would you like one tailored for a specific domain—like finance, gaming, NLP, or web dev?
