# What I checked, and what the agent got wrong

## What the agent got wrong

Honestly, I didn't catch a clear mistake in the code itself. Everything the agent
produced compiled, the tests turned green, and verify.py confirmed it. But "I didn't
catch a bug" doesn't mean I just rubber-stamped it — I made sure I understood each
change before I accepted it.

The one thing I pushed back on mentally was the km-to-miles conversion. The agent said
the constant was backwards — MILES_PER_KM = 1.609 was being used as a multiplier when
it should be a divisor. I didn't just take its word for it. I checked: 1 mile is about
1.609 km, so to go from km to miles you divide, not multiply. 100 km / 1.609 = 62.1
miles, which is right. The old code would have printed 160.9 miles for a 100 km
distance, which is obviously wrong. Once I worked it out myself I was confident the fix
was correct.

## What I checked before I accepted its work

For the wear bug: I read the before and after in km_wachter.py myself. The old code did
`km_since_service // interval` — integer floor division — which means anything under
15,000 km would come out as 0. A car at 14,900 km would look 0% worn. The fix switches
to `(km_since_service / interval) * 100`, which gives 99.3% for that same car. That
makes sense. I then ran pytest and saw both km_wachter tests go green.

For the missing-reading bug: I traced through what the old code did step by step. It
called `car.get("last_service_km", 0)`, so if the key was missing it treated it as 0.
A car with a 92,000 km odometer and no service record would look like it had driven
92,000 km since service — flagged as 600% worn. The fix returns False early if the key
isn't there at all, which is the right call: "we don't know" should not mean "flag it."

For the fleet report crash: the old `car_wear` did `car["last_service_km"]` with a bare
key lookup. Any car without that key would throw a KeyError and kill the nightly report.
The fix adds the same guard. I added the missing test myself (well, directed the agent
to add it) and watched it pass.

I ran `python verify.py` after every fix, not just at the end. I didn't accept "it
looks done" from the agent — I waited until verify.py printed PASS for each check.

## What the data actually said

I went in expecting total mileage or age to be the main breakdown predictors. Both came
back with a correlation of basically 0 against broke_down. The mean odometer for cars
that broke down was 53,447 km; for cars that didn't it was 53,301 km — nearly identical.
Age was the same story: median of 5 years for both groups.

What actually separated the two groups was km_since_service (correlation +0.40), then
avg_daily_km (+0.25) and load_factor (+0.22). Cars that broke down had driven about
twice as far since their last service as the ones that were fine (median 13,000 vs 6,300
km). They also tended to be driven harder each day and under heavier load.

So the thing that matters is not how old a car is or how many total km it has — it is
how overdue it is for a service combined with how hard it is being worked. That was
genuinely surprising to me and I wouldn't have guessed it without looking at the numbers.
