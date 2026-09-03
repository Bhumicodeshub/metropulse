# MetroPulse — 4-Week Pilot Designs

## Pilot 1: Off-Manhattan Demand Development (Brooklyn Focus)

**Rationale:** Manhattan captures 88.76% of all pickups; Brooklyn, despite being
NYC's most populous borough, accounts for only 0.84% of trips (854 trips/day avg,
$32.45 avg fare) — a real, quantified underserved-demand gap, not a guess.

- **Unit of analysis:** Individual driver-days, aggregated to zone-day level for
  Brooklyn's top 10 zones by existing (low) trip volume
- **Treatment:** Driver positioning incentive (bonus per completed trip originating
  in target Brooklyn zones) during identified low-coverage hours
- **Control:** Matched set of Brooklyn zones with similar baseline volume, no incentive applied
- **Primary metric:** Daily trip count in treatment zones vs control zones
- **Guardrail metrics:** Average fare (should not drop, would indicate rushed/short trips),
  driver earnings per hour (pilot should not reduce driver take-home pay),
  cross-borough trip share (should not cannibalize Manhattan demand)
- **Sample size reasoning:** Baseline Brooklyn daily volume ~854 trips/day, historical
  day-to-day variation observed across the 91-day dataset gives a working std dev
  estimate; a 4-week window (28 days) per group gives enough days to detect a
  ~15-20% shift in daily trip count at conventional significance levels, based on
  the variability already observed in daily_summary data
- **Stopping rule:** If guardrail metrics (driver earnings, average fare) drop more
  than 10% in treatment zones at any weekly checkpoint, pause and reassess
- **Decision rule:** If treatment zones show a statistically significant increase in
  trip volume (CI for the difference excludes 0) with guardrails intact after 4 weeks,
  recommend scaling to additional Brooklyn zones

---

## Pilot 2: Airport-Focused Operations (JFK/LaGuardia)

**Rationale:** Airport pickups average $76.45/trip vs $24.45 for non-airport trips —
a statistically significant +$51.99 difference (95% CI: $51.93-$52.06, confirmed via
two-sample comparison). JFK alone is the #2 busiest single pickup zone citywide
(459K trips in the study window). This is high-value, concentrated, provable demand.

- **Unit of analysis:** Hourly time-blocks at JFK and LaGuardia, compared across
  treatment vs control days
- **Treatment:** Pre-positioning drivers near airport terminals ahead of known peak
  arrival windows (identified from Investigation 1's hourly demand pattern)
- **Control:** Standard/unmanaged positioning, no pre-positioning signal sent to drivers
- **Primary metric:** Average passenger wait time proxy (time between ride request and
  pickup, if available) or trip volume captured during peak windows
- **Guardrail metrics:** Driver idle time (should not increase — pre-positioning
  shouldn't mean drivers wait longer with no fares), average fare (should hold steady,
  not indicating diverted/shorter trips)
- **Sample size reasoning:** Baseline airport volume ~8,808 trips/day with a std dev
  of ~1,218; a 4-week pilot (28 days) provides sufficient days to detect a meaningful
  (~10-15%) shift in captured peak-window volume given this variability
- **Stopping rule:** If driver idle time increases more than 15% in treatment windows
  at any weekly checkpoint, pause and reassess positioning strategy
- **Decision rule:** If treatment windows show a statistically significant increase in
  captured trip volume during peak periods, with guardrails intact, recommend
  permanent pre-positioning protocol during identified peak hours

---

## Initiatives Explicitly Ruled Out (with evidence)

- **Weather-triggered operational planning:** Rejected. Investigation 4 and the
  statistical comparison (Comparison 1) both show no significant relationship between
  precipitation and taxi demand (95% CI for the difference includes 0). Recommending
  a weather-based initiative would contradict our own evidence.
- **Transit-disruption response:** Rejected. No genuine disruption events were
  identifiable in the subway data — low-ridership days align with regular weekly
  cyclicality (Sundays, holidays), not disruptions. On these days taxi demand also
  fell (up to -38.8%), showing taxi and subway move together rather than one
  substituting for the other, so a "compensate for subway disruption" strategy has
  no supporting evidence in this data.