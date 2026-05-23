# Scale and Map Problems

## Explanations

### Introduction

A **scale** is a ratio that relates a measurement on a drawing, map, or model to the corresponding measurement in real life. When you see "1:50,000" printed on a road map, it means that every 1 unit of length on the map corresponds to 50,000 of the same units in reality. Scale problems ask you to move between these two worlds — the miniature representation and the full-size reality.

**Scale and map problems** appear consistently in the Philippine Civil Service Examination because they test:
- Proportional reasoning — the core mathematical skill behind ratios
- Unit conversion — a practical skill every government employee needs
- Multi-step problem solving — combining operations in sequence
- Spatial and quantitative literacy — interpreting maps, blueprints, and technical drawings

**Where scales are used in real life:**
- **Road maps and GPS navigation** — computing travel distances between cities
- **Architecture and engineering** — reading floor plans and structural blueprints
- **Urban planning** — designing city layouts, zoning maps, lot subdivisions
- **Construction** — interpreting site plans and elevation drawings
- **Land surveying** — converting cadastral map measurements to actual land areas
- **Military and disaster response** — plotting coordinates and distances on tactical maps
- **Transportation planning** — route design, road network analysis
- **Government infrastructure projects** — DPWH road plans, DENR land-use maps

**Common mistakes examinees make:**
1. Forgetting to convert units before or after applying the scale ratio
2. Reversing the scale — treating map distance as actual distance and vice versa
3. Setting up the proportion incorrectly (flipping numerator and denominator)
4. Mixing metric and English units without converting
5. Skipping simplification, leading to arithmetic errors with large numbers
6. Misreading the scale format (confusing "1 cm = 5 km" with "1:5")
7. Failing to check whether the answer is reasonable (e.g., getting 0.002 km for a city-to-city distance)

---

### Learning Objectives

After this lesson, you should be able to:
- Interpret map scales correctly in all common formats
- Identify and simplify scale ratios
- Convert map distances into actual (real-world) distances
- Convert actual distances into map (drawing) distances
- Perform unit conversions accurately within scale problems
- Solve multi-step scale and map problems involving combined operations
- Apply estimation and mental math to verify answers quickly
- Solve CSE-style scale and map questions efficiently under time pressure

---

### 4.1 What Is a Scale?

A **scale** is a ratio that expresses the relationship between a distance on a representation (map, blueprint, model) and the corresponding distance in reality.

**Core idea:** Real-world objects are too large to draw at full size. A scale shrinks them proportionally so that every measurement on the drawing maintains the same ratio to the real measurement.

#### The Scale Ratio

A scale of **1:50,000** means:

> For every **1 unit** measured on the map, the actual distance is **50,000 of the same units** in reality.

- 1 cm on the map = 50,000 cm in reality
- 1 inch on the map = 50,000 inches in reality
- 1 mm on the map = 50,000 mm in reality

The units on both sides of the ratio are always the **same** — this is critical. The scale ratio is dimensionless (unit-free) until you assign a specific unit to work with.

#### Why Scales Exist

| Without Scale | With Scale |
|--------------|-----------|
| A 10 km road would need a 10 km long drawing | A 10 km road fits in 20 cm on paper (at 1:50,000) |
| A building floor plan would be 30 m wide | A floor plan fits on an A3 sheet (at 1:100) |
| A country map would span hundreds of kilometers | A country fits on a single page (at 1:5,000,000) |

#### Interpreting Scale Statements

| Scale Expression | Meaning |
|-----------------|---------|
| 1:1,000 | 1 unit on drawing = 1,000 units in reality |
| 1:50,000 | 1 unit on map = 50,000 units in reality |
| 1:1 | Full size (no reduction) |
| 2:1 | Enlarged — drawing is 2× actual size (used for small components) |

**Key insight:** The larger the second number, the more the real world has been "shrunk" to fit on paper. A 1:1,000,000 map covers a much larger area than a 1:1,000 map of the same paper size.

---

### 4.2 Types of Scale Representation

Scales appear in three common formats. You must recognize all three because CSE questions may use any of them.

#### 1. Ratio Scale (Representative Fraction)

Written as a pure ratio with no units:

- **1:25,000**
- **1:100**
- **1:500,000**

This is the most common format in exam questions. Both numbers are in the same unit (whichever you choose to work with).

#### 2. Written (Verbal/Statement) Scale

Expressed as a sentence relating two different units:

- "1 cm represents 5 km"
- "1 inch represents 10 miles"
- "2 cm represents 1 km"

This format explicitly states the units, which makes unit conversion part of the problem.

#### 3. Graphic (Bar) Scale

A labeled line segment printed on the map itself:

```
|----|----|----|----|
0    5   10   15   20 km
```

Each segment represents a fixed real-world distance. Even if the map is photocopied at a different size, the bar scale remains accurate (unlike ratio scales, which become invalid if the map is resized).

#### Comparison Table

| Format | Example | Units Stated? | Survives Resizing? |
|--------|---------|--------------|-------------------|
| Ratio | 1:50,000 | No (same unit implied) | No |
| Written | 1 cm = 2 km | Yes (different units) | No |
| Graphic | Bar with markings | Yes (on the bar) | Yes |

#### Converting Between Formats

**Written → Ratio:**
"1 cm represents 5 km"
→ Convert 5 km to cm: 5 × 100,000 = 500,000 cm
→ Ratio scale: **1:500,000**

**Ratio → Written:**
1:25,000
→ 1 cm = 25,000 cm = 250 m = 0.25 km
→ Written: "1 cm represents 0.25 km" or "4 cm represents 1 km"

---

### 4.3 Understanding Scale Ratios

#### Reading the Ratio

A scale ratio has two parts:

```
Map Distance : Actual Distance
     1       :     50,000
```

- The **left number** (usually 1) represents the measurement on the map/drawing
- The **right number** represents the corresponding measurement in reality
- Both are in the **same unit**

#### Simplifying Scale Ratios

Sometimes scales are given in non-simplified form:

- **2 cm : 10 km** → Convert to same units: 2 cm : 1,000,000 cm → Simplify: 1:500,000
- **5 mm : 1 km** → 5 mm : 1,000,000 mm → 1:200,000
- **3 inches : 15 miles** → This stays as a written scale unless you convert

#### Why Units Must Match

The ratio 1:50,000 is meaningless if the left side is in centimeters and the right side is in kilometers — those are different magnitudes. Always ensure both sides use the same unit before simplifying.

**Example:** A map states "2 cm represents 8 km." What is the ratio scale?

Step 1: Convert 8 km to cm → 8 × 100,000 = 800,000 cm
Step 2: Write the ratio → 2:800,000
Step 3: Simplify → 1:400,000

---

### 4.4 Converting Map Distance to Actual Distance

This is the most common type of scale problem: you measure a distance on the map and need to find the real-world distance.

#### The Formula

```
Actual Distance = Map Distance × Scale Factor
```

Where the **Scale Factor** is the second number in the ratio (when the first number is 1).

Alternatively, set up a proportion:

```
Map Distance       1
────────────── = ──────
Actual Distance   Scale
```

#### Step-by-Step Procedure

1. **Identify the scale** (e.g., 1:50,000)
2. **Identify the map distance** (e.g., 4 cm)
3. **Multiply:** 4 × 50,000 = 200,000 cm
4. **Convert to useful units:** 200,000 cm ÷ 100,000 = 2 km
5. **Check reasonableness:** Is 2 km a reasonable distance between two nearby towns? Yes.

#### Worked Examples

**Example 1 (Easy):**
Scale: 1:100,000. Two cities are 3.5 cm apart on the map. Find the actual distance.

- Actual = 3.5 × 100,000 = 350,000 cm
- Convert: 350,000 ÷ 100,000 = **3.5 km**

**Example 2 (Medium):**
Scale: "1 cm represents 2.5 km." A road measures 7.2 cm on the map. Find the actual length.

- Actual = 7.2 × 2.5 = **18 km**
- (No extra conversion needed — the written scale already gives km directly)

**Example 3 (Hard):**
Scale: 1:250,000. A river measures 12.4 cm on the map. Express the actual length in kilometers.

- Actual = 12.4 × 250,000 = 3,100,000 cm
- Convert: 3,100,000 ÷ 100,000 = **31 km**

---

### 4.5 Converting Actual Distance to Map Distance

The reverse problem: you know the real-world distance and need to find how long it would be on the map.

#### The Formula

```
Map Distance = Actual Distance ÷ Scale Factor
```

Or equivalently:

```
Map Distance = Actual Distance × (1 / Scale Factor)
```

#### Step-by-Step Procedure

1. **Identify the scale** (e.g., 1:50,000)
2. **Identify the actual distance** (e.g., 8 km)
3. **Convert actual distance to the same unit as the map measurement** (usually cm): 8 km = 800,000 cm
4. **Divide:** 800,000 ÷ 50,000 = 16 cm
5. **Check reasonableness:** Is 16 cm a reasonable length to measure on a map? Yes.

#### Worked Examples

**Example 1 (Easy):**
Scale: 1:25,000. The actual distance between two landmarks is 5 km. Find the map distance.

- Convert: 5 km = 500,000 cm
- Map distance = 500,000 ÷ 25,000 = **20 cm**

**Example 2 (Medium):**
Scale: "2 cm represents 3 km." The actual distance is 21 km. Find the map distance.

- Set up proportion: 2 cm / 3 km = x cm / 21 km
- Cross-multiply: x = (2 × 21) / 3 = 42 / 3 = **14 cm**

**Example 3 (Hard):**
Scale: 1:400,000. A highway is 56 km long. How many centimeters is this on the map?

- Convert: 56 km = 5,600,000 cm
- Map distance = 5,600,000 ÷ 400,000 = **14 cm**

---

### 4.6 Unit Conversions in Scale Problems

Unit conversion is where most examinees lose points. Scale problems almost always require converting between units — typically from centimeters (map measurement) to kilometers (real-world distance) or vice versa.

#### Essential Conversion Factors (Metric)

| From | To | Multiply by |
|------|-----|------------|
| 1 km | m | 1,000 |
| 1 km | cm | 100,000 |
| 1 km | mm | 1,000,000 |
| 1 m | cm | 100 |
| 1 m | mm | 1,000 |
| 1 cm | mm | 10 |

#### Essential Conversion Factors (English)

| From | To | Multiply by |
|------|-----|------------|
| 1 mile | feet | 5,280 |
| 1 mile | yards | 1,760 |
| 1 mile | inches | 63,360 |
| 1 yard | feet | 3 |
| 1 foot | inches | 12 |

#### The Critical Conversion: cm ↔ km

Since most map problems involve centimeters on the map and kilometers in reality:

- **cm to km:** divide by 100,000
- **km to cm:** multiply by 100,000

**Memory aid:** There are exactly **5 zeros** between cm and km (cm → m is ×100, m → km is ×1,000; total = 100 × 1,000 = 100,000).

#### Common Conversion Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Dividing by 1,000 to go from cm to km | That converts cm to m, not km | Divide by 100,000 |
| Multiplying by 1,000 to go from km to cm | That converts km to m, not cm | Multiply by 100,000 |
| Forgetting conversion entirely | Raw scale multiplication gives cm, not km | Always convert at the end |
| Converting before multiplying when unnecessary | Adds complexity | Convert at the step where it simplifies the math |

#### Shortcut: Direct Scale Interpretation

For common scales, memorize what 1 cm represents:

| Scale | 1 cm on map = | Useful for |
|-------|--------------|-----------|
| 1:1,000 | 10 m | Building floor plans |
| 1:10,000 | 100 m | Campus/neighborhood maps |
| 1:25,000 | 250 m | Topographic maps |
| 1:50,000 | 500 m = 0.5 km | Regional maps |
| 1:100,000 | 1 km | Provincial maps |
| 1:250,000 | 2.5 km | Island maps |
| 1:500,000 | 5 km | Country maps |
| 1:1,000,000 | 10 km | Continental maps |

---

### 4.7 Multi-Step Scale and Map Problems

CSE questions often combine scale interpretation with additional reasoning steps: computing travel time, comparing routes, finding areas, or working with multiple scales.

#### Type 1: Distance + Speed → Time

**Example:** On a map with scale 1:200,000, two towns are 6 cm apart. If a bus travels at 60 km/h, how long is the trip?

Step 1: Actual distance = 6 × 200,000 = 1,200,000 cm = 12 km
Step 2: Time = Distance ÷ Speed = 12 ÷ 60 = 0.2 hours = **12 minutes**

#### Type 2: Comparing Two Routes

**Example:** Route A measures 8 cm on a 1:50,000 map. Route B measures 5 cm on a 1:100,000 map. Which route is longer?

- Route A: 8 × 50,000 = 400,000 cm = 4 km
- Route B: 5 × 100,000 = 500,000 cm = 5 km
- **Route B is longer by 1 km**

#### Type 3: Area Problems

**Example:** A rectangular lot measures 4 cm × 3 cm on a 1:2,000 map. Find the actual area.

Step 1: Actual length = 4 × 2,000 = 8,000 cm = 80 m
Step 2: Actual width = 3 × 2,000 = 6,000 cm = 60 m
Step 3: Area = 80 × 60 = **4,800 m²**

**Warning:** For area, the scale factor is squared. If the linear scale is 1:2,000, the area scale is 1:4,000,000. But it's safer to convert each dimension separately and then multiply.

#### Type 4: Working Backward from Travel Data

**Example:** A car travels 45 km between two cities. On the map, this distance is 9 cm. What is the map scale?

Step 1: Convert 45 km to cm → 4,500,000 cm
Step 2: Scale = 9:4,500,000 = 1:500,000

---

### 4.8 Real-Life Applications of Scale and Maps

Scale problems are not abstract math — they reflect tasks that government employees perform regularly:

| Application | Who Uses It | Scale Problem Type |
|------------|------------|-------------------|
| Road maps | DPWH engineers, LGU planners | Map → actual distance |
| GPS/navigation | Field workers, delivery personnel | Actual → map verification |
| Blueprints | Building officials, architects | Drawing → actual dimensions |
| Land titles | DENR, assessors, surveyors | Map → actual lot area |
| Disaster maps | NDRRMC, LGU responders | Evacuation route distances |
| Zoning maps | Urban planners, HLURB | Lot dimensions from plans |
| Military maps | AFP, PNP tactical units | Grid coordinates, distances |
| Classroom geography | Teachers, students | Country/world map interpretation |

#### Philippine Context Examples

- A DPWH engineer reads a 1:50,000 topographic map to estimate road construction length
- A municipal assessor measures a lot on a 1:2,000 cadastral map to verify land area
- A barangay disaster officer uses a 1:10,000 flood map to identify evacuation distances
- A DENR forester measures forest cover on a 1:250,000 land-use map

---

### 4.9 Using Diagrams, Maps, and Visual Models

#### Reading a Map Legend

Maps include legends that explain symbols and the scale. When solving problems:
1. Locate the scale (usually bottom or corner of the map)
2. Identify the format (ratio, written, or bar scale)
3. Note the units used
4. Measure the required distance using a ruler or the given measurement

#### Interpreting Bar Scales

A bar scale looks like a ruler printed on the map:

```
├────┼────┼────┼────┤
0    2    4    6    8 km
```

To use it:
- Measure the distance between two points on the map
- Compare that measurement against the bar scale
- Read off the corresponding real-world distance

**Advantage:** If the map is enlarged or reduced (photocopied), the bar scale changes proportionally, so it remains accurate.

#### Estimating from Visual Scales

When exact measurement isn't possible:
- Use the bar scale as a reference ruler
- Estimate how many "bar lengths" fit between two points
- Multiply by the distance each bar represents

---

### 4.10 Problem-Solving Strategies

#### The 5-Step System for Scale Problems

1. **READ** — Identify what's given (scale, distance) and what's asked (map or actual?)
2. **CONVERT** — Ensure units are consistent before calculating
3. **CALCULATE** — Apply the scale ratio (multiply or divide)
4. **CONVERT AGAIN** — Express the answer in the requested unit
5. **CHECK** — Is the answer reasonable? (A city-to-city distance should be in km, not mm)

#### Quick Decision: Multiply or Divide?

| If you have... | And you want... | Then... |
|---------------|----------------|---------|
| Map distance | Actual distance | **Multiply** by scale factor |
| Actual distance | Map distance | **Divide** by scale factor |

**Memory aid:** "Map is small, reality is big." Going from small to big = multiply. Going from big to small = divide.

#### Elimination Strategy for Multiple Choice

If the scale is 1:100,000 and the map distance is 6 cm:
- Actual = 6 × 100,000 = 600,000 cm = 6 km
- If choices are: (A) 0.6 km, (B) 6 km, (C) 60 km, (D) 600 km
- Immediately eliminate (A) and (D) as unreasonable
- Check your calculation → answer is (B)

---

### 4.11 Estimation and Mental Math Techniques

#### Quick Mental Conversions

For scale 1:100,000:
- 1 cm = 1 km (memorize this — it's the most common exam scale)
- So 5 cm = 5 km, 3.5 cm = 3.5 km — instant answers!

For scale 1:50,000:
- 1 cm = 0.5 km
- So 8 cm = 4 km, 14 cm = 7 km

For scale 1:200,000:
- 1 cm = 2 km
- So 4 cm = 8 km, 6.5 cm = 13 km

#### Simplification Before Calculation

Instead of multiplying large numbers, simplify first:

**Example:** Scale 1:250,000, map distance = 8 cm
- Don't compute: 8 × 250,000 = 2,000,000 cm then convert
- Instead: 1 cm = 250,000 cm = 2.5 km, so 8 cm = 8 × 2.5 = **20 km**

#### Reasonableness Checks

| Context | Reasonable Distance |
|---------|-------------------|
| Two buildings in a compound | 10–500 m |
| Two barangays in a municipality | 1–10 km |
| Two municipalities in a province | 10–100 km |
| Two provinces | 50–500 km |
| Manila to Cebu | ~570 km |

If your answer doesn't fit the context, recheck your work.

---

### 4.12 Common Errors in Scale and Map Problems

| Error | Example | How to Avoid |
|-------|---------|-------------|
| Wrong unit conversion | Writing 1 km = 1,000 cm instead of 100,000 cm | Memorize: km → m (×1,000) → cm (×100) = ×100,000 |
| Reversed scale | Using map distance where actual should go | Ask: "Am I going from small to big or big to small?" |
| Proportion setup error | Writing 1/50,000 = actual/map instead of map/actual | Keep consistent: map on top, actual on bottom (or vice versa — just be consistent) |
| Forgetting to simplify | Getting 1:800,000 when asked for simplest form | Always check if both numbers share a common factor |
| Arithmetic mistakes | 7 × 50,000 = 3,500,000 → then writing 35 km instead of 3.5 km | Count zeros carefully; use estimation to verify |
| Mixing scale formats | Treating "1 cm = 5 km" as if it were 1:5 | Convert written scales to ratio form first |
| Area vs. linear confusion | Using linear scale for area without squaring | Convert each dimension separately, then multiply |
| Ignoring the question's unit | Computing in cm when the question asks for km | Read the question's unit requirement last before answering |

---

### Step-by-Step Rules Summary

#### Map → Actual Distance

1. Read the scale (e.g., 1:50,000)
2. Measure or note the map distance (e.g., 6 cm)
3. Multiply: 6 × 50,000 = 300,000 cm
4. Convert to km: 300,000 ÷ 100,000 = 3 km
5. Verify reasonableness

#### Actual → Map Distance

1. Read the scale (e.g., 1:50,000)
2. Note the actual distance (e.g., 8 km)
3. Convert to cm: 8 × 100,000 = 800,000 cm
4. Divide: 800,000 ÷ 50,000 = 16 cm
5. Verify reasonableness

#### Finding the Scale

1. Note both distances (map and actual) with their units
2. Convert both to the same unit
3. Write as a ratio: map : actual
4. Simplify to 1:n form

#### Unit Conversion Chain

```
mm → cm → m → km
 ÷10   ÷100  ÷1,000

km → m → cm → mm
 ×1,000 ×100  ×10
```

---

### Exam Strategies

1. **Memorize key equivalences:** 1:100,000 means 1 cm = 1 km. This single fact solves ~30% of scale questions instantly.

2. **Convert the scale to "1 cm = ? km" form immediately.** This makes multiplication trivial.

3. **Use estimation to eliminate choices.** If the map distance is 4 cm and the scale is 1:50,000, the answer must be around 2 km. Eliminate anything far from that.

4. **Watch for trap answers.** Examiners often include the result before unit conversion (e.g., 200,000 cm as a choice alongside 2 km).

5. **For reverse problems (actual → map), divide.** If you're getting a huge number for a map distance, you probably multiplied instead of dividing.

6. **For multi-step problems, solve one step at a time.** Don't try to combine scale conversion, unit conversion, and speed/time in one equation.

7. **Double-check which direction the question asks.** "How far apart are they in reality?" = multiply. "How long is this on the map?" = divide.

---

### Real CSE-Like Examples

#### Easy Examples

**Example 1:**
A map has a scale of 1:100,000. Two barangays are 5 cm apart on the map. What is the actual distance?

**Solution:**
- Actual = 5 × 100,000 = 500,000 cm
- Convert: 500,000 ÷ 100,000 = **5 km**
- (Shortcut: At 1:100,000, 1 cm = 1 km, so 5 cm = 5 km)

**Example 2:**
A blueprint uses a scale of 1:200. A wall measures 4 cm on the blueprint. What is the actual length of the wall?

**Solution:**
- Actual = 4 × 200 = 800 cm = **8 meters**

**Example 3:**
On a map with scale 1:50,000, what actual distance does 1 cm represent?

**Solution:**
- 1 cm = 50,000 cm = 500 m = **0.5 km**

#### Medium Examples

**Example 4:**
A map uses the scale "1 cm represents 4 km." If the actual distance between two cities is 28 km, how far apart are they on the map?

**Solution:**
- Map distance = 28 ÷ 4 = **7 cm**

**Example 5:**
On a 1:250,000 map, a road measures 9.2 cm. A car travels this road at 80 km/h. How long does the trip take?

**Solution:**
- Actual = 9.2 × 250,000 = 2,300,000 cm = 23 km
- Time = 23 ÷ 80 = 0.2875 hours = 0.2875 × 60 ≈ **17.25 minutes**

**Example 6:**
Two towns are 15 km apart. On a map, they are 6 cm apart. What is the scale of the map?

**Solution:**
- Convert 15 km to cm: 15 × 100,000 = 1,500,000 cm
- Scale = 6:1,500,000 = 1:250,000

#### Hard Examples

**Example 7:**
A rectangular park measures 3 cm × 2 cm on a 1:5,000 map. What is the actual area in square meters?

**Solution:**
- Length = 3 × 5,000 = 15,000 cm = 150 m
- Width = 2 × 5,000 = 10,000 cm = 100 m
- Area = 150 × 100 = **15,000 m²** (or 1.5 hectares)

**Example 8:**
Map A has scale 1:50,000. Map B has scale 1:200,000. A river measures 12 cm on Map A. How long would the same river measure on Map B?

**Solution:**
- Actual length = 12 × 50,000 = 600,000 cm = 6 km
- On Map B: 600,000 ÷ 200,000 = **3 cm**

**Example 9:**
A surveyor measures a lot boundary as 7.5 cm on a 1:2,000 cadastral map. The lot is rectangular with a width of 3 cm on the same map. If land costs ₱5,000 per square meter, what is the total land value?

**Solution:**
- Length = 7.5 × 2,000 = 15,000 cm = 150 m
- Width = 3 × 2,000 = 6,000 cm = 60 m
- Area = 150 × 60 = 9,000 m²
- Value = 9,000 × ₱5,000 = **₱45,000,000**

---

### Mini Practice Set (20 Questions)

**1.** Scale: 1:100,000. Map distance: 7 cm. Actual distance = ?
**Answer:** 7 km. (7 × 100,000 = 700,000 cm = 7 km)

**2.** Scale: 1:50,000. Map distance: 10 cm. Actual distance = ?
**Answer:** 5 km. (10 × 50,000 = 500,000 cm = 5 km)

**3.** Scale: 1:25,000. Actual distance: 3 km. Map distance = ?
**Answer:** 12 cm. (3 km = 300,000 cm; 300,000 ÷ 25,000 = 12 cm)

**4.** Scale: "1 cm represents 2 km." Map distance: 9 cm. Actual distance = ?
**Answer:** 18 km. (9 × 2 = 18 km)

**5.** Scale: 1:200,000. Map distance: 4.5 cm. Actual distance = ?
**Answer:** 9 km. (4.5 × 200,000 = 900,000 cm = 9 km)

**6.** Two cities are 36 km apart. Map distance: 12 cm. Scale = ?
**Answer:** 1:300,000. (36 km = 3,600,000 cm; 12:3,600,000 = 1:300,000)

**7.** Scale: 1:500,000. Actual distance: 40 km. Map distance = ?
**Answer:** 8 cm. (40 km = 4,000,000 cm; 4,000,000 ÷ 500,000 = 8 cm)

**8.** Scale: 1:10,000. A building is 3.5 cm long on the blueprint. Actual length = ?
**Answer:** 350 m. (3.5 × 10,000 = 35,000 cm = 350 m)

**9.** Scale: "2 cm represents 5 km." Actual distance: 30 km. Map distance = ?
**Answer:** 12 cm. (2/5 = x/30; x = 12 cm)

**10.** Scale: 1:75,000. Map distance: 8 cm. Actual distance in km = ?
**Answer:** 6 km. (8 × 75,000 = 600,000 cm = 6 km)

**11.** Scale: 1:1,000,000. Map distance: 2.5 cm. Actual distance = ?
**Answer:** 25 km. (2.5 × 1,000,000 = 2,500,000 cm = 25 km)

**12.** Scale: 1:40,000. Actual distance: 6 km. Map distance = ?
**Answer:** 15 cm. (6 km = 600,000 cm; 600,000 ÷ 40,000 = 15 cm)

**13.** A map states "1 cm = 500 m." What is the ratio scale?
**Answer:** 1:50,000. (500 m = 50,000 cm; ratio = 1:50,000)

**14.** Scale: 1:150,000. Map distance: 6 cm. A car travels at 90 km/h. Travel time = ?
**Answer:** 6 minutes. (Actual = 6 × 150,000 = 900,000 cm = 9 km; Time = 9 ÷ 90 = 0.1 hr = 6 min)

**15.** Scale: 1:20,000. A lot is 5 cm × 4 cm on the map. Actual area = ?
**Answer:** 40,000 m². (Length = 5 × 20,000 = 100,000 cm = 1,000 m; Width = 4 × 20,000 = 80,000 cm = 800 m; Area = 1,000 × 800 = 800,000 m²)
*Correction:* Let me recalculate. Length = 5 × 20,000 = 100,000 cm = 1,000 m; Width = 4 × 20,000 = 80,000 cm = 800 m; Area = 1,000 × 800 = **800,000 m²**

**16.** Scale: 1:250,000. Two points are 3 cm apart on the map. Express in meters.
**Answer:** 7,500 m. (3 × 250,000 = 750,000 cm = 7,500 m)

**17.** On Map A (1:100,000), a river is 8 cm. How long is it on Map B (1:400,000)?
**Answer:** 2 cm. (Actual = 8 km; Map B = 800,000 ÷ 400,000 = 2 cm)

**18.** Scale: 1:5,000. A fence measures 12 cm on the plan. Actual length in meters = ?
**Answer:** 600 m. (12 × 5,000 = 60,000 cm = 600 m)

**19.** Actual distance: 120 km. Map distance: 4 cm. Scale = ?
**Answer:** 1:3,000,000. (120 km = 12,000,000 cm; 4:12,000,000 = 1:3,000,000)

**20.** Scale: "3 cm represents 6 km." What is the ratio scale?
**Answer:** 1:200,000. (6 km = 600,000 cm; 3:600,000 = 1:200,000)

---

### Quick Recap

| Concept | Key Point |
|---------|-----------|
| Scale definition | Ratio of map distance to actual distance |
| Scale formats | Ratio (1:50,000), Written (1 cm = 5 km), Graphic (bar) |
| Map → Actual | Multiply map distance by scale factor, then convert units |
| Actual → Map | Convert actual to map units, then divide by scale factor |
| Unit conversion | 1 km = 100,000 cm (memorize the 5 zeros) |
| Multi-step | Combine scale conversion with speed/time, area, or cost calculations |
| Reasonableness | Always check if your answer makes real-world sense |

---

### Memory Aids

1. **"Five Zeros"** — 1 km = 100,000 cm. Count: 1-0-0-0-0-0. Five zeros after the 1.

2. **"Small to Big = Multiply"** — Going from map (small) to reality (big)? Multiply by the scale factor.

3. **"Big to Small = Divide"** — Going from reality (big) to map (small)? Divide by the scale factor.

4. **"1:100,000 = 1 cm per km"** — The golden ratio for quick mental math on exams.

5. **"Scale Up, Zeros Up"** — Larger scale numbers mean more zeros in your conversion. Double-check by counting zeros.

6. **"RCCCC"** — Read, Convert, Calculate, Convert, Check. The 5-step system.

7. **"Area = Square the Scale"** — For area problems, each dimension gets the scale applied separately. Don't just multiply area by the scale once.

---

### Mastery Checklist

After completing this lesson, you should be able to:

- ✅ Interpret map scales correctly in ratio, written, and graphic formats
- ✅ Identify and simplify scale ratios to standard form
- ✅ Convert map distances to actual distances using multiplication
- ✅ Convert actual distances to map distances using division
- ✅ Perform unit conversions accurately (especially cm ↔ km)
- ✅ Solve multi-step scale problems (distance + time, area, cost)
- ✅ Determine the scale given both map and actual distances
- ✅ Estimate answers mentally using memorized scale equivalences
- ✅ Eliminate unreasonable answer choices quickly
- ✅ Solve CSE scale and map questions confidently under time pressure
