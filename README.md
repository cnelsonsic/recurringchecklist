# Recurring Checklist
A dumb-as-rocks recurring checklist manager.

You can add events and set them to repeat a number of days after completion.
```python
>>> add("Scrub toilets", interval=14)
```

Then you can flag it as completed, for now.
```python
>>> complete("Scrub toilets")
```

It will show up in the listing as to be done in its next interval.
```python
>>> checklist()
['[ ] Scrub toilets (in 13 days.)']
```
