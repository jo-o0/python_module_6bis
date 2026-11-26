# Code Nexus

> One Python module, five exercises, one single idea repeated at five depths:
> **capability over identity.** Ask what something can *do*, never what it *is*.
> This README is your map: definitions first, then a guide to each exercise,
> then fun facts and a run-cheatsheet at the back.

---

## PART 1 — Definitions

Everything below shows up in every exercise. Learn these once, use them five times.

**Class** — a blueprint for objects. Describes what data an object holds (attributes) and what it can do (methods).

**Inheritance** — a child class is born owning everything the parent has. Mom hands you her recipe book: you didn't write it, but every dish is yours to cook.

**Overriding** — rewriting an inherited method in the child class. Your spicier version of mom's pasta. From then on, YOUR version runs for your objects.

**super()** — knocking on mom's door. Calls the parent's version of the method from inside your override. `super().__init__(...)` is its most common job: letting the parent set up its part of the object before you add yours.

**Abstract Base Class (ABC)** — a blueprint that can't be built. Created with `class Thing(ABC)`. The cooking academy: it sells a syllabus, not food.

**@abstractmethod** — the decorator that turns a method into a requirement. Any class with even one abstract method cannot be instantiated, and any child that doesn't implement ALL of them is also abstract. The bouncer at the academy's door.

**The three bouncer rules:**
1. A class with an abstract method can't be instantiated (Python crashes *early*, at creation, instead of exploding later when the empty method is called).
2. A child missing any abstract method is also abstract — the bouncer checks the kids too.
3. A child that implements them all is welcome. That's the whole mechanic.

**Polymorphism** — "many shapes, one call." Different objects answer the *same method name* each in their own voice. The caller doesn't know or care which concrete class it holds — it just calls the method, and the object decides what happens.

**Encapsulation** — private state (`self._stored`), public windows (`pending`). The kitchen is private; the waiter reads the ticket number on the wall without entering the pantry.

**Exception** — a controlled explosion. Python stops the normal flow and travels up the call stack looking for a `try/except` that handles it. A custom exception class (like `EmptyBufferError`) lets callers catch *exactly* your error and nothing else.

**raise vs print** — `raise` is a conversation: the caller can react, catch, log, protect the stream. `print` inside a processor is a monologue: it evaporates into stdout. Also: a `print` inside an exception *class body* fires once at import time — never when the exception is raised. Spooky and useless.

**Guard clause** — handle the special case first, `return` immediately, and let the happy path march forward flat and un-indented. Anti-else-pyramid medicine.

**Type hints** — annotations like `data: Any` or `-> bool`. Python **ignores them at runtime**; their whole job is static checking (mypy reads them and catches crimes before the program starts). They are a contract for humans and checkers, not enforcement for the interpreter.

**Any** — the "I genuinely don't know what arrives" type. Validators receive `Any` because they can't predict the data. Everything narrower is a guess that will eventually reject something legitimate.

**isinstance(x, T)** — "is x's passport from country T?" Identity checking. Contrast with the *dare* below.

**Structural thinking (the dare)** — never ask "are you a number?", try `float(data)` and see if it works. Asking if someone speaks the language instead of checking their passport. A passport can be fake; speaking the language is the real test. This module prefers the dare everywhere untrusted data appears.

**typing.Protocol** — a *structural contract*: a class that declares method signatures but is **never inherited**. Anything implementing those signatures is accepted automatically. ABC says "sign the contract"; Protocol says "prove it." Both constrain what a class must provide — opposite doors, same goal.

**Duck typing** — "if it walks like a duck and quacks like a duck..." Behavior-based acceptance. The type checker verifies capability, not lineage. That's how plugin systems let strangers plug in without asking permission.

**@property** — a method wearing an attribute's clothes. Decorate with `@property` and callers read `obj.pending` with no parentheses. Public window, private kitchen.

**`__init__` (method) vs `__init__.py` (file)** — cousins, not twins. The *method* initializes one object's state (birth certificate, instance variables), called automatically after the object is created. The *file* initializes a *package* — makes a folder importable, runs once on first import. Both are setup rituals; one dresses an object, the other dresses a folder.

**FIFO** — First In, First Out. A queue: the oldest item leaves first (`pop(0)`). A stack would be last-in-first-out (`pop()` from the end) — one digit of difference, opposite behavior.

**all() / any()** — `all` returns True only if EVERY boolean is true, short-circuiting at the first False (a bouncer who ends the line's night at the first fake ID). `any` is the optimist: True if at least one is true. ⚠️ Wrapping trap: inside `all()`, the condition must be the **PASS** condition. `all(v == v ...)` means "all clean"; `all(v != v ...)` means "all nan" — inverted and deadly, and it *sounds* right until you trace it.

**Vacuous truth** — `all([])` is `True`. An empty list passes every `all()` check. Owned design decision here: empty data validates as True, consistently across all processors.

**Ternary** — `value if condition else other`. A whole if-else compressed into one line; the condition gatekeeps between two values. Powers the normalization trick: `items = [data] if not isinstance(data, list) else data`.

**f-strings** — `f"..."` means "format this": `{expr}` gets evaluated and plugged in. Quote-nesting rule (pre-3.12): the inner quotes must differ from the outer ones, or the string ends early and SyntaxError city opens its gates.

**list/tuple/dict comprehension** — building a collection by describing it, not by appending in a loop: `[float(e) for e in items]`. Same loop, one line, often faster.

**Multiple inheritance** — a class with two parents: `class Shiftling(Creature, TransformCapability)`. Python walks the parents left to right (the MRO — Method Resolution Order). The capability arrives as a *mixin*: an ability, not a family.

**Abstract Factory pattern** — an ABC (`CreatureFactory`) declaring `create_base()` / `create_evolved()`; concrete factories decide which classes get born. Calling code never names a concrete entity — same trick as the DataStream never naming a concrete processor.

**Capability pattern (mixin)** — an ability kept as its own ABC (`TransformCapability`), deliberately NOT mixed into the base class. Abilities are opt-in, not mandatory. The alternative — putting `transform()` on `Creature` — would force every plain entity to implement a power it doesn't have (or inherit a lying default).

**Strategy pattern** — behavior packaged into interchangeable objects. Each strategy knows who it fits (`is_valid`) and what to do (`act`). The caller (tournament) never checks entity families — the *decision moved into the strategies*. Add a new capability, add a new strategy, zero changes to the battle code.

---

## PART 2

### The arc of the module

| Ex | File(s) | New idea |
|----|---------|----------|
| 0 | `data_processor.py` | ABC + exceptions: the contract with a bouncer |
| 1 | `data_stream.py` | Polymorphism: a conductor who trusts faces |
| 2 | `data_pipeline.py` | Protocol/duck typing: an export layer that trusts behavior |
| 3 | `ex3/` + `battle.py` + `capacitor.py` | Abstract factory + capability mixin |
| 4 | `ex4/` + `tournament.py` | Strategy pattern: decisions move into the strategies |

Each exercise *reuses* the previous one untouched. Nothing is thrown away; the idea just grows a new floor.

---

### Exercise 0 — `data_processor.py` 🏭

**What it does:** three processors (Numeric, Text, Log) that validate, ingest and store data, plus a FIFO vending machine to pull it back out.

**Run it:**
```bash
python3 data_processor.py
```

**The cast:**
- `DataProcessor(ABC)` — the parent. Abstract `validate(data: Any) -> bool` (a polite question, never raises) and abstract `ingest(data: Any) -> None` (a gate, MUST raise on invalid data). Concrete `output() -> tuple[int, str]` (checks the fridge, raises `EmptyBufferError` if empty, `pop(0)` — oldest first). Also holds `_stored` (private buffer) and `_rank` (arrival counter).
- `NumericProcessor` — dares data to `float()`. Prints integers without the `.0` (`is_integer()`).
- `TextProcessor` — `all(isinstance(elem, str) ...)`.
- `LogProcessor` — asks four questions per dict: is it a dict, has `log_level`, has `log_message`, are all values strings.
- Four custom exceptions, one per processor + `EmptyBufferError`. Specificity is kindness: catch exactly your error, never `Exception` by accident.

**The ingest recipe (all three processors):**
1. Normalize: `[data] if not isinstance(data, list) else data` — the tray trick. Downstream only ever sees batches.
2. Dual-collect: good items in one list, rejected in another.
3. Store the good (stamped with rank, ranks only tick for stored items — no gaps).
4. If anything was rejected → raise the custom exception with the rejected list in the message. Best effort with a full report: good data kept, bad data reported loudly, no silent loss.

**Key detail:** validate and ingest must ask the *same question* — one source of truth per processor. Every disagreement is a crack garbage can slip through.

---

### Exercise 1 — `data_stream.py` 🚂

**What it does:** a `DataStream` that routes mixed data to the right processor without knowing any processor's dialect, and reports lifetime vs inventory.

**Run it:**
```bash
python3 data_stream.py
```

**What changed from ex0:** only the validators. They now accept one item OR a list (normalize, then run the same dare, plural). Same logic, looped — no new rules. The example stream sends lists as elements, so this upgrade is mandatory, not decorative.

**The DataStream:**
- `_processors: list[DataProcessor]` + `_totals: dict[str, int]` (the ledger, seeded at registration).
- `register_processor(proc)` — appends and seeds its ledger entry at 0.
- `process_stream(stream)` — for each element, walk processors in registration order; **first** `validate` that says True claims it (ingest, count, `break`). No takers → print the orphan error line. Registration order = priority order.
- `print_processors_stats()` — guard clause first (no processors → message, return). Then per processor TWO numbers:
  - **total** = the stream's ledger. Lifetime items routed. Only ever grows.
  - **remaining** = the processor's inventory (`proc.pending`). Breathes: grows on ingest, shrinks on output.

**The flag pattern (and its two traps):** `routed = False` resets per element, BEFORE the inner loop; set True on claim; the `if not routed:` error check lives at OUTER loop level, after the inner loop finishes. Wrong nesting = poisoned flags or premature panic. Indentation is logic.

**The demo's money shot:** consume 3/2/1 items, print stats again — totals frozen (8/3/2), remaining dropped (1/1/1). If both numbers move, something's wrong: consumption never touches the ledger.

---

### Exercise 2 — `data_pipeline.py` 🔌

**What it does:** same stream, now with an export layer. Plugins format the output; the stream feeds them.

**Run it:**
```bash
python3 data_pipeline.py
```

**The new pieces:**
- `ExportPlugin(Protocol)` — declares `process_output(self, data: list[tuple[int, str]]) -> None`. Never inherited, never instantiated. A contract that trusts faces.
- `CsvExportPlugin` — inherits from **nothing**. Collects the values (`elem[1]`), `",".join(items)`, prints `CSV Output:` + the line. The commas ARE the CSV.
- `JsonExportPlugin` — same dance, different costume: one string per tuple shaped `"item_{rank}": "{value}"`, joined with `", "`, wrapped in `{ }`, printed after a `JSON Output:` header. The braces and quotes ARE the JSON. (Ranks are per-processor — each object owns its `_rank`.)
- `DataStream.output_pipeline(nb, plugin)` — for EACH processor: collect up to `nb` tuples via `proc.output()`, then ONE `plugin.process_output(collected)` call per processor (that's why the demo prints one line per processor).

**The drain guard:** if a buffer runs dry before `nb` pops, `except EmptyBufferError: break` — export what exists, no crash. The demo shows it twice: Log exports 2 when asked for 3 (CSV scene), and its JSON line only has `item_2`/`item_3`. A partial export beats an explosion. The ledger doesn't move either — the export only pops items out, totals count what came IN.

**Why manual strings:** the csv/json libraries are off-limits on purpose. Building the format by hand is the skill — once you've been the serializer, you understand what serializers do forever.

---

### Exercise 3 — `ex3/` + `battle.py` + `capacitor.py` 🐉

**What it does:** creature families. Who *creates* the objects (abstract factory) and how to give an entity a power without forcing it on every entity (capability mixin).

**Run it:**
```bash
python3 battle.py
python3 capacitor.py
```

**Package layout (the `ex3/` folder):**
```
ex3/
├── __init__.py      # exposes ONLY the factories — never the concrete entities
├── creature.py      # Creature(ABC) + TransformCapability(ABC)
├── creatures.py     # Flameling, Pyrodon, Shiftling, Morphagon
└── factory.py       # CreatureFactory(ABC) + the two concrete factories
```
`__init__.py` is what makes the folder a *package*: it runs once on first import and controls the public face. `battle.py` and `capacitor.py` sit at the module root, next to the package, and import like `from ex3 import FlameFactory, TransformCreatureFactory`.

**The cast:**
- `Creature(ABC)` — `name` + `ctype` attributes, abstract `attack()`, concrete `describe()` → `"Flameling is a Fire type Creature"`.
- `TransformCapability(ABC)` — abstract `transform()` + `revert()`, holds `_transformed: bool`. Deliberately NOT a Creature. An ability should not be forced onto every entity.
- `Shiftling(Creature, TransformCapability)` and `Morphagon(Creature, TransformCapability)` — multiple inheritance: the mixin brings the power, `Creature` brings the identity. While transformed, `attack()` returns the boosted line.
- `CreatureFactory(ABC)` — abstract `create_base()` / `create_evolved()`.
- `FlameFactory` → base Flameling, evolved Pyrodon. `TransformCreatureFactory` → base Shiftling, evolved Morphagon.

**Why the factory:** calling code says "give me a base creature" and never learns the concrete class. New family? New factory. Zero changes in `battle.py`.

---

### Exercise 4 — `ex4/` + `tournament.py` 🏆

**What it does:** a tournament where every opponent fights every other exactly once — and the battle code never checks what anything *is*. Strategies decide.

**Run it:**
```bash
python3 tournament.py
```

**Package layout:**
```
ex4/
├── __init__.py      # exposes the strategies
└── strategy.py      # BattleStrategy(ABC) + NormalStrategy + AggressiveStrategy
```

**The cast:**
- `BattleStrategy(ABC)` — abstract `is_valid(entity) -> bool` (is this entity suitable?) and `act(entity)` (what the tournament executes).
- `NormalStrategy` — valid for ANY entity; `act` just calls `attack()`.
- `AggressiveStrategy` — valid only for transform-capable entities: `isinstance(entity, TransformCapability)`. Never the concrete family — the capability class. `act` = transform → attack → revert.
- `act` called with an invalid entity → raise the dedicated exception with a clear message (e.g. `Invalid Creature 'Flameling' for this aggressive strategy`), and the tournament aborts mid-run.

**The tournament:** opponents are `(factory, strategy)` pairs. Build each entity via its factory, check each strategy with `is_valid`, face every pair once, apply each entity's strategy. The battle code has zero family knowledge — that's the entire point. New capability tomorrow? New strategy class, nothing else changes.

---

## PART 3 — Fun Facts / Interesting Questions 💡

**Is the DataStream an AI algorithm?**
Genuinely, yes — the routing is the Mixture-of-Experts pattern (the architecture inside models like Mixtral). Elements play the role of tokens; each processor is a specialist that only claims what it understands; the router is the stream itself. One difference: your router is hand-written rules, theirs is a learned network. Same job. One programmed, one trained.

**Why does `all([])` return True?**
Vacuous truth: "every element passes" is automatically true when there are no elements to contradict it. Same logic as "all the unicorns in this room are pink." No unicorns, no counterexample. Here it's an owned design decision: empty data validates as True, consistently everywhere.

**Why is nan the only value that isn't equal to itself?**
`nan` means "not a number" — the result of undefined math like `0/0`. It represents *failure to compute*, so IEEE decided it must never compare equal to anything, including itself — otherwise `nan == nan` would claim a failed computation succeeded. So `value != value` is a perfect nan detector, and the list version (`all(v == v ...)`) is just that check wearing a loop. The cursed-looking idiom that only the liar fails.

**What would break if transform/revert lived on Creature?**
Every plain entity (Flameling, Pyrodon) would be forced to implement a power it doesn't have — the ABC bouncer would demand it — or inherit a lying default that pretends to transform. Abilities become mandatory instead of opt-in. The capability mixin is the fix: power where it's wanted, silence where it's not.

**Why does a `print` inside an exception class body fire at import time?**
A class body runs ONCE, when Python defines the class — not when the exception is raised. The `print` isn't inside a method, so it's class-level code, and class-level code executes at definition time. If you want output when the exception happens, print where it's caught (or define `__str__`).

**Why do the JSON keys start at item_3 in the demo?**
Ranks are per-processor (each object owns its `_rank` from the parent's `__init__`). Numeric popped ranks 0–2 during the earlier CSV export, so the next item out the FIFO door is rank 3. The key is just the rank wearing an `item_` prefix.

**Why can Protocol plugins be tested without importing anything from the package?**
Because acceptance is structural, not nominal. The plugin never says "I am an ExportPlugin" — it just implements `process_output` with the right signature, and the type checker (and the stream's call) accept it. That's why third parties can extend the pipeline without touching your code.

**ABC or Protocol — which one when?**
Building a family that must share a design, where forgetting a method should crash early at instantiation? ABC. Offering an interface the outside world can implement freely, where forgetting a method should fail at type-check time instead? Protocol. Sign the contract vs prove it.

---

## PART 5 — References 📚

- [Python docs: abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [Python docs: typing — Support for type hints](https://docs.python.org/3/library/typing.html) (Protocol lives here)
- [Python docs: exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Design Patterns: Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)
- [Design Patterns: Strategy](https://refactoring.guru/design-patterns/strategy)
- Mixture-of-Experts explained: any modern MoE paper or blog — the DataStream is a hand-written one.

---

*Made with love and a concerning amount of "innit" jokes. Capability over identity, bestie — always. 💅*
