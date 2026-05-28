# Discounts, Markups, and Sales

## Explanations

### Introduction

**Discounts, markups, and commissions** are the three pillars of sales mathematics — and they appear with remarkable frequency in the Numerical Ability section of the Philippine Civil Service Examination. These concepts govern how prices are set, reduced, and how salespeople earn from transactions.

Understanding sales mathematics matters because it touches virtually every financial transaction in daily life and government work:
- **Retail shopping** — computing how much you actually save during a sale
- **Government procurement** — evaluating supplier bids with volume discounts
- **Payroll and incentives** — calculating commission-based compensation for sales staff
- **Inventory management** — determining selling prices from cost and desired profit margins
- **Marketing campaigns** — analyzing the impact of promotional pricing
- **Engineering procurement** — comparing quoted prices with standard markups
- **Transportation services** — understanding promotional fare discounts
- **Business profit analysis** — tracing the relationship between cost, markup, and revenue
- **Budget planning** — projecting revenue from marked-up goods and services
- **Online marketplace operations** — computing net earnings after platform commissions

The CSE tests these concepts because government employees routinely:
1. Process purchase orders where supplier discounts affect budget allocation
2. Verify pricing computations in procurement documents
3. Compute incentive pay and commission structures for revenue-generating offices
4. Analyze financial reports involving cost-price-profit relationships
5. Evaluate vendor proposals with tiered discount structures

**Common mistakes examinees make on sales-related problems:**
1. Confusing the **base** — applying discount percentage to the wrong amount
2. Adding successive discounts directly (e.g., thinking 10% + 20% = 30% off)
3. Confusing **markup percentage** with **profit percentage** (they use different bases)
4. Forgetting to convert percentages to decimals before multiplying
5. Computing commission on the wrong amount (gross vs. net sales)
6. Reversing the formula — subtracting when they should multiply
7. Misreading whether a problem asks for the discount *amount* or the *sale price*
8. Arithmetic errors when working with Philippine peso amounts that have many digits

### Learning Objectives

After this lesson, you should be able to:
- Compute discount amounts accurately given an original price and discount rate
- Determine the sale price (net price) after one or more discounts
- Compute markup amounts and selling prices from cost price and markup rate
- Solve commission problems involving flat rates, tiered structures, and salary-plus-commission systems
- Distinguish between discount, markup, and commission problems using context clues
- Apply the multiplier method for successive discounts and markups efficiently
- Analyze real-life pricing situations involving multiple operations
- Solve CSE-style multi-step business math problems under time pressure

---

### 4.1 Understanding Discounts, Markups, and Commissions

#### The Three Core Concepts

Every pricing problem in the CSE revolves around three fundamental operations:

| Concept | What It Does | Direction | Base Amount |
|---------|-------------|-----------|-------------|
| **Discount** | Reduces a price | Downward | Original/List Price |
| **Markup** | Increases a price | Upward | Cost Price |
| **Commission** | Percentage-based earning | N/A (it's income) | Total Sales |

#### How They Relate to Each Other

Think of the life cycle of a product:

```
Manufacturer → Cost Price
Cost Price + Markup = Selling Price (what the store charges)
Selling Price − Discount = Sale Price (what the customer pays)
Sale × Commission Rate = Commission (what the salesperson earns)
```

#### Key Terminology

| Term | Definition |
|------|-----------|
| **Original Price (List Price)** | The price before any discount is applied |
| **Cost Price** | What the seller paid to acquire the item |
| **Markup** | The amount added to cost price to set the selling price |
| **Selling Price (Marked Price)** | The price tag on the item (cost + markup) |
| **Discount** | The amount subtracted from the selling/original price |
| **Sale Price (Net Price)** | The final price the buyer pays after discount |
| **Commission** | A percentage of sales paid as earnings to a salesperson |
| **Commission Rate** | The percentage used to compute commission |
| **Gross Sales** | Total sales before any deductions |
| **Net Sales** | Sales after returns, allowances, or deductions |

#### The Fundamental Relationships

```
Discount Amount = Original Price × Discount Rate
Sale Price = Original Price − Discount Amount
Sale Price = Original Price × (1 − Discount Rate)

Markup Amount = Cost Price × Markup Rate
Selling Price = Cost Price + Markup Amount
Selling Price = Cost Price × (1 + Markup Rate)

Commission = Sales × Commission Rate
```

**CSE Tip:** The most critical skill is identifying which value is the BASE. Discounts are based on the original price. Markups are based on the cost price. Commissions are based on sales. Using the wrong base is the #1 source of errors.

---

### 4.2 Discounts

#### What Is a Discount?

A **discount** is a reduction from the original (list) price. When a store advertises "20% off," it means the buyer pays 20% less than the original price.

#### The Formulas

**Discount Amount:**
```
Discount Amount = Original Price × Discount Rate
```

**Sale Price (what the buyer actually pays):**
```
Sale Price = Original Price − Discount Amount
```

**Shortcut (one-step multiplier):**
```
Sale Price = Original Price × (1 − Discount Rate)
```

#### Step-by-Step Process

Step 1: Identify the original price (the "before" price).
Step 2: Identify the discount rate (convert to decimal if given as %).
Step 3: Multiply: Original Price × Discount Rate = Discount Amount.
Step 4: Subtract: Original Price − Discount Amount = Sale Price.

> 🤔 **Why does this work?** The complement shortcut works because of the distributive property of subtraction:
> $\text{Original Price} - (\text{Original Price} \times \text{Discount Rate}) = \text{Original Price} \times (1 - \text{Discount Rate})$.
> If an item is discounted by 20%, you are subtracting 20% of the value. This mathematically leaves exactly
> 80% (or 0.80) of the value. Multiplying by the complement (0.80) bypasses the need to first calculate
> the discount amount and then subtract it, saving time and reducing places where arithmetic errors can occur.

> ⚠️ **Misconception:** "To find the original price of an item that is on sale for ₱800 after a 20% discount, you just find 20% of ₱800 and add it back."
>
> **Why it fails:** 20% of ₱800 = ₱160. Adding it back gives ₱960. But if the original price were ₱960,
> a 20% discount would be ₱192, making the sale price ₱768, which is not ₱800. The wrong model gives ₱960 $\neq$ ₱1,000.
>
> **Correct model:** The 20% discount was calculated from the *original price*, which is unknown.
> The sale price (₱800) represents the remaining 80% of that original price. To find the original price,
> you must divide the sale price by the remaining percentage multiplier: $\text{Original Price} = ₱800 \div 0.80 = ₱1,000$.

#### Easy Examples

**Example 1: Basic Discount Amount**

A bag originally costs ₱2,000. It is on sale at 15% off. What is the discount amount?

```
Discount Amount = ₱2,000 × 0.15 = ₱300
```

**Answer: ₱300**

**Example 2: Finding the Sale Price**

A pair of shoes is priced at ₱3,500 with a 20% discount. What is the sale price?

```
Discount Amount = ₱3,500 × 0.20 = ₱700
Sale Price = ₱3,500 − ₱700 = ₱2,800
```

Or using the multiplier shortcut:
```
Sale Price = ₱3,500 × (1 − 0.20) = ₱3,500 × 0.80 = ₱2,800
```

**Answer: ₱2,800**

**Example 3: Government Supply Discount**

A government office purchases printer paper listed at ₱450 per ream with a 10% institutional discount. How much does the office pay per ream?

```
Sale Price = ₱450 × (1 − 0.10) = ₱450 × 0.90 = ₱405
```

**Answer: ₱405 per ream**

#### Medium Examples

**Example 4: Finding the Discount Rate**

A laptop originally priced at ₱48,000 is sold for ₱40,800. What is the discount rate?

```
Discount Amount = ₱48,000 − ₱40,800 = ₱7,200
Discount Rate = ₱7,200 ÷ ₱48,000 = 0.15 = 15%
```

**Answer: 15%**

**Example 5: Finding the Original Price**

After a 25% discount, a customer pays ₱5,250 for a tablet. What was the original price?

```
Sale Price = Original Price × (1 − 0.25)
₱5,250 = Original Price × 0.75
Original Price = ₱5,250 ÷ 0.75 = ₱7,000
```

**Answer: ₱7,000**

**Example 6: Bulk Purchase Discount**

A school buys 50 chairs at ₱1,200 each. The supplier offers a 12% bulk discount on the total. How much does the school pay?

```
Total before discount = 50 × ₱1,200 = ₱60,000
Discount = ₱60,000 × 0.12 = ₱7,200
Amount paid = ₱60,000 − ₱7,200 = ₱52,800
```

**Answer: ₱52,800**

#### Hard Examples

**Example 7: Reverse Discount Problem**

A customer saved ₱1,680 on a purchase thanks to a 12% discount. What was the original price?

```
Discount Amount = Original Price × Discount Rate
₱1,680 = Original Price × 0.12
Original Price = ₱1,680 ÷ 0.12 = ₱14,000
```

**Answer: ₱14,000**

**Example 8: CSE-Style Problem**

A government agency received bids for office supplies. Supplier A offers ₱85,000 with a 5% discount. Supplier B offers ₱80,000 with no discount. Which supplier offers the lower price, and by how much?

```
Supplier A net price = ₱85,000 × (1 − 0.05) = ₱85,000 × 0.95 = ₱80,750
Supplier B net price = ₱80,000

Difference = ₱80,750 − ₱80,000 = ₱750
```

**Answer: Supplier B is cheaper by ₱750**

**CSE Tip:** When a problem asks "how much was saved," it's asking for the discount amount. When it asks "how much was paid," it's asking for the sale price. Read the question carefully.

---

### 4.3 Markup

#### What Is a Markup?

A **markup** is the amount a seller adds to the cost price to determine the selling price. It covers operating expenses and generates profit.

#### The Formulas

**Markup Amount:**
```
Markup Amount = Cost Price × Markup Rate
```

**Selling Price:**
```
Selling Price = Cost Price + Markup Amount
```

**Shortcut (one-step multiplier):**
```
Selling Price = Cost Price × (1 + Markup Rate)
```

**Finding Markup Rate from known values:**
```
Markup Rate = (Selling Price − Cost Price) / Cost Price × 100
```

#### The Difference Between Markup and Profit Margin

This distinction trips up many examinees:

| Concept | Formula | Base |
|---------|---------|------|
| **Markup %** | (Selling − Cost) ÷ Cost × 100 | Cost Price |
| **Profit Margin %** | (Selling − Cost) ÷ Selling × 100 | Selling Price |

Same dollar amount, different percentages because the base differs.

**Example:** Cost = ₱80, Selling = ₱100
- Markup = (100 − 80) ÷ 80 × 100 = 25%
- Profit Margin = (100 − 80) ÷ 100 × 100 = 20%

**CSE Tip:** Unless the problem specifically says "profit margin" or "based on selling price," assume markup is based on cost price.

> 🤔 **Why does this work?** The markup rate uses the **Cost Price** as the base because it measures how much
> a business *increases* its investment to determine a retail price. Conversely, profit margin uses the **Selling Price**
> as the base because it measures how much of each peso collected from customers represents net earnings.
> Since selling price is always higher than cost price (under profitable operations), the profit margin percentage
> will always be lower than the markup percentage for the same absolute transaction amount.

> ⚠️ **Misconception:** "A 50% markup on an item means the store makes a 50% profit margin when they sell it."
>
> **Why it fails:** If an item costs ₱100 and has a 50% markup, it sells for ₱150. The profit amount is ₱50.
> But the profit *margin* is $\text{Profit} \div \text{Selling Price} = ₱50 \div ₱150 = 33.33\%$, which is much lower than 50%.
>
> **Correct model:** Markup is a percentage of cost ($\text{profit} \div \text{cost}$), while profit margin is a percentage
> of the final selling price ($\text{profit} \div \text{selling price}$). Because the selling price is a larger denominator,
> the profit margin percentage is always smaller than the markup percentage.

#### Easy Examples

**Example 1: Basic Markup**

A store buys a shirt for ₱400 and applies a 50% markup. What is the selling price?

```
Markup Amount = ₱400 × 0.50 = ₱200
Selling Price = ₱400 + ₱200 = ₱600
```

Or: Selling Price = ₱400 × 1.50 = ₱600

**Answer: ₱600**

**Example 2: Finding the Markup Amount**

A bookstore purchases a textbook for ₱350 and sells it for ₱490. What is the markup amount?

```
Markup Amount = ₱490 − ₱350 = ₱140
```

**Answer: ₱140**

**Example 3: Office Equipment**

An office supply store buys a printer for ₱8,000 and marks it up by 35%. What is the selling price?

```
Selling Price = ₱8,000 × (1 + 0.35) = ₱8,000 × 1.35 = ₱10,800
```

**Answer: ₱10,800**

#### Medium Examples

**Example 4: Finding the Markup Rate**

A vendor buys mangoes at ₱60 per kilo and sells them at ₱84 per kilo. What is the markup rate?

```
Markup Amount = ₱84 − ₱60 = ₱24
Markup Rate = ₱24 ÷ ₱60 × 100 = 40%
```

**Answer: 40%**

**Example 5: Finding the Cost Price**

A retailer sells a gadget for ₱5,600 after applying a 40% markup on cost. What was the cost price?

```
Selling Price = Cost Price × (1 + 0.40)
₱5,600 = Cost Price × 1.40
Cost Price = ₱5,600 ÷ 1.40 = ₱4,000
```

**Answer: ₱4,000**

**Example 6: Engineering Supplies**

A construction supply store buys cement at ₱280 per bag and applies a 25% markup. If a contractor buys 200 bags, what is the total selling price?

```
Selling Price per bag = ₱280 × 1.25 = ₱350
Total = 200 × ₱350 = ₱70,000
```

**Answer: ₱70,000**

#### Hard Examples

**Example 7: Markup Then Discount**

A store buys a watch for ₱3,000 and marks it up by 60%. During a sale, the store offers a 25% discount. What is the sale price?

```
Selling Price = ₱3,000 × 1.60 = ₱4,800
Sale Price = ₱4,800 × (1 − 0.25) = ₱4,800 × 0.75 = ₱3,600
```

**Answer: ₱3,600**

Does the store still profit? Yes: ₱3,600 − ₱3,000 = ₱600 profit.

**Example 8: CSE-Style Problem**

A food vendor's cost for preparing a meal box is ₱75. She marks up by 80% for the selling price. If she sells 120 boxes in a day, what is her total markup (gross profit) for the day?

```
Markup per box = ₱75 × 0.80 = ₱60
Total markup = 120 × ₱60 = ₱7,200
```

**Answer: ₱7,200**

---

### Check Your Understanding

**1.** If an item costs ₱1,500 and is sold for ₱1,800, what is the markup rate? → **20%** (Markup is ₱300. 300 ÷ 1,500 = 0.20 = 20%)
**2.** Write the complement multiplier for an item sold with a 15% discount. → **0.85** (100% − 15% = 85% = 0.85)
**3.** If a shirt originally costing ₱600 is discounted by 25%, what is the sale price? → **₱450** (₱600 × 0.75 = ₱450)

---

### 4.4 Commission

#### What Is a Commission?

A **commission** is a percentage-based payment earned by a salesperson for generating sales. It serves as an incentive — the more you sell, the more you earn.

#### The Formula

```
Commission = Total Sales × Commission Rate
```

**For salary-plus-commission systems:**
```
Total Earnings = Base Salary + Commission
Total Earnings = Base Salary + (Sales × Commission Rate)
```

#### Types of Commission Structures

| Structure | Description |
|-----------|-------------|
| **Straight commission** | Earnings = Sales × Rate (no base salary) |
| **Salary plus commission** | Fixed salary + percentage of sales |
| **Graduated/Tiered commission** | Rate increases at higher sales levels |
| **Commission on excess** | Commission only on sales above a quota |

> 🤔 **Why does this work?** Deducting customer returns to compute commission based on net sales instead of gross sales
> ensures that salespeople are only incentivized to make *successful, permanent sales*. If commissions were paid on gross sales,
> a salesperson could collude with buyers to make large purchases, collect their commission, and then allow the buyers
> to return the goods for a full refund, which would cause severe financial loss to the company.

> ⚠️ **Misconception:** "If a store offers successive discounts of 20% and 10%, the total discount is 30% off."
>
> **Why it fails:** Consider a ₱1,000 item. A 20% discount drops the price to ₱800. The second discount of 10% is calculated
> from ₱800, which is ₱80. The final price is ₱720. The total savings is ₱280, which is exactly a 28% discount, not 30%.
>
> **Correct model:** Each discount is calculated sequentially. The second discount is taken from a *smaller, already-reduced base*,
> not the original base. Therefore, the absolute savings of the second discount is smaller than if it were based on the original.
> To combine successive discounts of $a\%$ and $b\%$, multiply their complements: $(1 - a) \times (1 - b)$.

#### Easy Examples

**Example 1: Straight Commission**

A real estate agent earns a 3% commission. If she sells a property worth ₱4,500,000, how much commission does she earn?

```
Commission = ₱4,500,000 × 0.03 = ₱135,000
```

**Answer: ₱135,000**

**Example 2: Salary Plus Commission**

A sales clerk earns a base salary of ₱15,000 per month plus a 5% commission on all sales. If her total sales for the month are ₱120,000, what are her total earnings?

```
Commission = ₱120,000 × 0.05 = ₱6,000
Total Earnings = ₱15,000 + ₱6,000 = ₱21,000
```

**Answer: ₱21,000**

**Example 3: Finding the Commission Rate**

An insurance agent earned ₱18,000 in commission from ₱600,000 worth of policies sold. What is her commission rate?

```
Commission Rate = ₱18,000 ÷ ₱600,000 = 0.03 = 3%
```

**Answer: 3%**

#### Medium Examples

**Example 4: Finding Total Sales**

A car salesman earns a 2% commission. If he earned ₱36,000 in commission last month, what were his total sales?

```
Commission = Sales × Rate
₱36,000 = Sales × 0.02
Sales = ₱36,000 ÷ 0.02 = ₱1,800,000
```

**Answer: ₱1,800,000**

**Example 5: Commission on Excess**

A salesperson earns a 4% commission on all sales exceeding her ₱200,000 monthly quota. If her total sales are ₱350,000, how much commission does she earn?

```
Sales above quota = ₱350,000 − ₱200,000 = ₱150,000
Commission = ₱150,000 × 0.04 = ₱6,000
```

**Answer: ₱6,000**

**Example 6: Multiple Salespeople**

Three agents split a 6% commission equally on a ₱2,400,000 property sale. How much does each agent receive?

```
Total Commission = ₱2,400,000 × 0.06 = ₱144,000
Each agent = ₱144,000 ÷ 3 = ₱48,000
```

**Answer: ₱48,000 each**

#### Hard Examples

**Example 7: Graduated Commission**

A salesperson earns:
- 3% on the first ₱100,000 in sales
- 5% on sales from ₱100,001 to ₱300,000
- 8% on sales above ₱300,000

If total sales are ₱450,000, what is the total commission?

```
First tier: ₱100,000 × 0.03 = ₱3,000
Second tier: ₱200,000 × 0.05 = ₱10,000
Third tier: ₱150,000 × 0.08 = ₱12,000
Total Commission = ₱3,000 + ₱10,000 + ₱12,000 = ₱25,000
```

**Answer: ₱25,000**

**Example 8: CSE-Style Problem**

An online seller earns a base of ₱12,000 monthly. She receives a 7% commission on net sales (gross sales minus returns). Her gross sales were ₱280,000 and returns were ₱30,000. What are her total earnings?

```
Net Sales = ₱280,000 − ₱30,000 = ₱250,000
Commission = ₱250,000 × 0.07 = ₱17,500
Total Earnings = ₱12,000 + ₱17,500 = ₱29,500
```

**Answer: ₱29,500**

**CSE Tip:** Always check whether commission is computed on GROSS sales or NET sales. The problem will specify — read carefully.

---

### 4.5 Identifying Discount, Markup, and Commission Problems

#### Recognizing Clue Words

The fastest way to identify which formula to use is by recognizing signal words in the problem:

**Discount Clue Words:**
- sale, markdown, reduced price, off, discount
- "on sale," "marked down," "price reduction"
- "save," "less than original," "clearance"

**Markup Clue Words:**
- markup, added percentage, profit, cost plus
- "marked up," "selling price," "retail price"
- "above cost," "profit margin," "price increase from cost"

**Commission Clue Words:**
- commission, earnings, incentive, percentage of sales
- "earns from sales," "sales bonus," "performance pay"
- "broker's fee," "agent's cut," "finder's fee"

#### Decision Flowchart

```
Is the problem about EARNING money from sales?
  → YES → Commission problem
  → NO → Continue

Is the problem about REDUCING a price?
  → YES → Discount problem
  → NO → Continue

Is the problem about INCREASING a price from cost?
  → YES → Markup problem
```

#### Comparison Exercises

| Problem Statement | Type | Why |
|-------------------|------|-----|
| "A dress is 30% off" | Discount | Price is being reduced |
| "A vendor adds 45% to cost" | Markup | Price is being increased from cost |
| "An agent earns 5% of sales" | Commission | Earning based on sales |
| "The sale price is ₱1,200" | Discount | "Sale price" implies a reduction occurred |
| "The retail price is ₱500 above cost" | Markup | Price set above cost |
| "She received ₱8,000 for selling ₱200,000 worth" | Commission | Payment for generating sales |

#### Formula Selection Practice

**Question:** "A store bought items at ₱200 each and sold them at ₱280 each."
- This is a **markup** problem (price increased from cost to selling price)
- Markup Rate = (280 − 200) ÷ 200 × 100 = 40%

**Question:** "A customer paid ₱4,250 after a 15% discount."
- This is a **discount** problem (price was reduced)
- Original Price = ₱4,250 ÷ 0.85 = ₱5,000

**Question:** "A broker received ₱75,000 for facilitating a ₱2,500,000 deal."
- This is a **commission** problem (payment for sales)
- Commission Rate = ₱75,000 ÷ ₱2,500,000 × 100 = 3%

---

### 4.6 Multi-Step Sales Problems

#### Why Multi-Step Problems Appear on the CSE

Real-world pricing rarely involves a single operation. A product might be marked up, then discounted, and the salesperson earns commission on the final sale. The CSE tests whether you can chain these operations correctly.

#### Strategy: Break Into Sequential Steps

Step 1: Identify all operations in order.
Step 2: Compute each operation's result before moving to the next.
Step 3: Use the OUTPUT of one step as the INPUT of the next.
Step 4: Verify the final answer makes logical sense.

#### Easy Multi-Step Examples

**Example 1: Markup Then Discount**

A retailer buys a jacket for ₱1,500 and marks it up by 60%. During a holiday sale, the jacket is discounted by 20%. What does the customer pay?

```
Step 1: Selling Price = ₱1,500 × 1.60 = ₱2,400
Step 2: Sale Price = ₱2,400 × 0.80 = ₱1,920
```

**Answer: ₱1,920**

**Example 2: Sale Price Plus Commission**

A salesperson sells a TV at its discounted price. The TV's original price is ₱35,000 with a 10% discount. The salesperson earns 3% commission on the sale price. How much commission does she earn?

```
Step 1: Sale Price = ₱35,000 × 0.90 = ₱31,500
Step 2: Commission = ₱31,500 × 0.03 = ₱945
```

**Answer: ₱945**

#### Medium Multi-Step Examples

**Example 3: Cost → Markup → Discount → Commission**

A store buys electronics at ₱12,000 cost, marks up by 50%, then offers a 15% discount during a promo. The salesperson earns 4% commission on the discounted sale. Find: (a) the sale price, (b) the commission, (c) the store's profit after commission.

```
Step 1: Selling Price = ₱12,000 × 1.50 = ₱18,000
Step 2: Sale Price = ₱18,000 × 0.85 = ₱15,300
Step 3: Commission = ₱15,300 × 0.04 = ₱612
Step 4: Store's profit = ₱15,300 − ₱12,000 − ₱612 = ₱2,688
```

**Answers: (a) ₱15,300 (b) ₱612 (c) ₱2,688**

**Example 4: Multiple Items with Different Discounts**

A customer buys:
- 3 shirts at ₱800 each (20% off)
- 2 pants at ₱1,500 each (15% off)

What is the total amount paid?

```
Shirts: 3 × ₱800 × 0.80 = 3 × ₱640 = ₱1,920
Pants: 2 × ₱1,500 × 0.85 = 2 × ₱1,275 = ₱2,550
Total = ₱1,920 + ₱2,550 = ₱4,470
```

**Answer: ₱4,470**

#### Hard Examples

**Example 5: Tiered Discount with Commission**

A furniture store offers: 10% off purchases up to ₱50,000, and 15% off the amount exceeding ₱50,000. A customer buys ₱80,000 worth of furniture. The salesperson earns 5% commission on the net amount collected.

```
Discount on first ₱50,000 = ₱50,000 × 0.10 = ₱5,000
Discount on excess ₱30,000 = ₱30,000 × 0.15 = ₱4,500
Total discount = ₱5,000 + ₱4,500 = ₱9,500
Net amount = ₱80,000 − ₱9,500 = ₱70,500
Commission = ₱70,500 × 0.05 = ₱3,525
```

**Answer: Customer pays ₱70,500; salesperson earns ₱3,525**

**Example 6: CSE-Style Comprehensive Problem**

A government cooperative store buys 500 units of an item at ₱120 each. It marks up by 40%. At year-end, 80% of the stock has been sold at full price, and the remaining 20% is sold at a 30% discount. What is the total revenue?

```
Selling Price = ₱120 × 1.40 = ₱168
Units at full price: 500 × 0.80 = 400 units → 400 × ₱168 = ₱67,200
Units at discount: 500 × 0.20 = 100 units → 100 × ₱168 × 0.70 = 100 × ₱117.60 = ₱11,760
Total revenue = ₱67,200 + ₱11,760 = ₱78,960
```

**Answer: ₱78,960**

---

### Check Your Understanding

**1.** What is the base amount used to calculate a sales commission? → **Total Sales** (Gross sales or Net sales)
**2.** If a store owner marks up a ₱200 item by 50%, then offers a 20% discount on the marked price, what is the final sale price? → **₱240** (Marked price = ₱300. Sale price = 300 × 0.80 = ₱240)
**3.** Under what type of commission structure does an agent earn money only on sales exceeding a specific threshold? → **Commission on excess** (or Quota-based commission)

---

### 4.7 Practical Applications of Sales Mathematics

#### Shopping Discounts

A department store advertises "Buy 1, Get 1 at 50% off" on items priced at ₱1,200 each. What is the effective discount rate on the total purchase?

```
Full price for 2 items = 2 × ₱1,200 = ₱2,400
Actual payment = ₱1,200 + (₱1,200 × 0.50) = ₱1,200 + ₱600 = ₱1,800
Total discount = ₱2,400 − ₱1,800 = ₱600
Effective rate = ₱600 ÷ ₱2,400 × 100 = 25%
```

#### Payroll Incentives

A government revenue officer earns ₱32,000 monthly plus 1.5% of all taxes collected above ₱5,000,000. If collections for the month total ₱8,200,000, what are total earnings?

```
Excess = ₱8,200,000 − ₱5,000,000 = ₱3,200,000
Incentive = ₱3,200,000 × 0.015 = ₱48,000
Total = ₱32,000 + ₱48,000 = ₱80,000
```

#### Retail Pricing

A sari-sari store owner buys canned goods at ₱38 per can and wants a 30% markup. What should the selling price be?

```
Selling Price = ₱38 × 1.30 = ₱49.40 ≈ ₱50 (rounded up for retail)
```

#### Inventory Management

A warehouse has 2,000 units purchased at ₱150 each. To clear inventory, management offers a 35% discount. What is the total loss compared to cost?

```
Selling price per unit = ₱150 × (1 − 0.35) = ₱150 × 0.65 = ₱97.50
Loss per unit = ₱150 − ₱97.50 = ₱52.50
Total loss = 2,000 × ₱52.50 = ₱105,000
```

#### Engineering Procurement

A contractor quotes ₱2,800,000 for materials. The supplier offers a 7% trade discount for bulk orders. How much does the contractor save?

```
Savings = ₱2,800,000 × 0.07 = ₱196,000
```

#### Transportation Ticket Promos

A bus company offers 20% off regular fare of ₱550 for senior citizens. If 45 seniors ride today, what is the total revenue from senior tickets?

```
Discounted fare = ₱550 × 0.80 = ₱440
Total revenue = 45 × ₱440 = ₱19,800
```

#### Government Supply Purchasing

A local government unit purchases 300 reams of bond paper. Supplier A offers ₱220/ream with a 10% discount. Supplier B offers ₱200/ream with a 5% discount. Which is cheaper?

```
Supplier A: ₱220 × 0.90 = ₱198/ream → Total: 300 × ₱198 = ₱59,400
Supplier B: ₱200 × 0.95 = ₱190/ream → Total: 300 × ₱190 = ₱57,000
```

Supplier B is cheaper by ₱2,400.

#### Online Marketplace Sales

An online seller lists products with a 40% markup on cost. The platform charges a 12% commission on each sale. If the cost of an item is ₱500, what is the seller's net profit per item?

```
Selling Price = ₱500 × 1.40 = ₱700
Platform commission = ₱700 × 0.12 = ₱84
Net revenue = ₱700 − ₱84 = ₱616
Net profit = ₱616 − ₱500 = ₱116
```

---

### 4.8 Successive Discounts and Markups

#### Why You Cannot Simply Add Discounts

This is the **most common trap** in CSE discount problems.

**The Trap:** If an item has a 20% discount followed by an additional 10% discount, is the total discount 30%?

**NO.** The total discount is LESS than 30%.

Why? Because the second discount applies to the *already-reduced* price, not the original price.

```
Original price: ₱1,000
After 20% discount: ₱1,000 × 0.80 = ₱800
After additional 10% discount: ₱800 × 0.90 = ₱720

Actual total discount: ₱1,000 − ₱720 = ₱280 → 28% (NOT 30%)
```

#### The Multiplier Method for Successive Discounts

**For successive discounts, multiply the complement multipliers:**
```
Final Price = Original × (1 − d₁) × (1 − d₂) × ... × (1 − dₙ)
```

**For successive markups:**
```
Final Price = Cost × (1 + m₁) × (1 + m₂) × ... × (1 + mₙ)
```

#### Common Successive Discount Multipliers

| Successive Discounts | Combined Multiplier | Equivalent Single Discount |
|---------------------|--------------------|-----------------------------|
| 10% then 10% | 0.90 × 0.90 = 0.81 | 19% |
| 10% then 20% | 0.90 × 0.80 = 0.72 | 28% |
| 20% then 20% | 0.80 × 0.80 = 0.64 | 36% |
| 15% then 10% | 0.85 × 0.90 = 0.765 | 23.5% |
| 25% then 20% | 0.75 × 0.80 = 0.60 | 40% |
| 10% then 10% then 10% | 0.90³ = 0.729 | 27.1% |

#### Easy Examples

**Example 1: Two Successive Discounts**

A store offers 20% off, plus an additional 10% off for loyalty card holders. If an item costs ₱5,000, what does a loyalty card holder pay?

```
Final Price = ₱5,000 × 0.80 × 0.90 = ₱5,000 × 0.72 = ₱3,600
```

**Answer: ₱3,600 (equivalent to a 28% single discount, not 30%)**

**Example 2: Markup Then Discount**

A store marks up an item by 50% from its ₱2,000 cost, then offers a 20% sale discount. What is the sale price?

```
Final Price = ₱2,000 × 1.50 × 0.80 = ₱2,000 × 1.20 = ₱2,400
```

**Answer: ₱2,400**

#### Medium Examples

**Example 3: Three Successive Discounts**

A clearance sale offers 30% off, then an additional 20% off, then a further 10% off for the last day. What is the equivalent single discount?

```
Combined multiplier = 0.70 × 0.80 × 0.90 = 0.504
Equivalent discount = 1 − 0.504 = 0.496 = 49.6%
```

**Answer: 49.6% equivalent single discount (NOT 60%)**

**Example 4: Finding the Required Markup After Discount**

A store wants to offer a 25% discount but still make a 20% profit on cost. What markup rate should be applied to the cost price?

```
Let Cost = 100
Desired sale price = 100 × 1.20 = 120 (to achieve 20% profit)
Sale Price = Marked Price × (1 − 0.25) = Marked Price × 0.75
120 = Marked Price × 0.75
Marked Price = 120 ÷ 0.75 = 160
Markup Rate = (160 − 100) ÷ 100 = 60%
```

**Answer: 60% markup is needed**

#### Hard Examples

**Example 5: Successive Markup and Discount with Commission**

A wholesaler sells goods at cost + 30% markup to a retailer. The retailer marks up by another 40%, then offers a 15% discount to customers. A salesperson earns 6% commission on the discounted price. If the wholesaler's cost is ₱2,000, find the salesperson's commission.

```
Wholesaler's selling price = ₱2,000 × 1.30 = ₱2,600
Retailer's marked price = ₱2,600 × 1.40 = ₱3,640
Customer's price = ₱3,640 × 0.85 = ₱3,094
Commission = ₱3,094 × 0.06 = ₱185.64
```

**Answer: ₱185.64**

**Example 6: CSE-Style Equivalent Discount**

Two stores sell the same item at ₱10,000. Store A offers successive discounts of 15% and 10%. Store B offers a single discount of 24%. Which store gives the better deal?

```
Store A: ₱10,000 × 0.85 × 0.90 = ₱10,000 × 0.765 = ₱7,650
Store B: ₱10,000 × 0.76 = ₱7,600

Store B is cheaper by ₱50.
Store A's equivalent discount = 23.5%
Store B's discount = 24%
```

**Answer: Store B gives the better deal (₱50 cheaper)**

**CSE Tip:** When comparing successive discounts to a single discount, always compute the combined multiplier. Never add the percentages.

---

### 4.9 Problem-Solving Strategies

#### The 5-Step System for Sales Problems

Step 1: **Read** — Identify what type of problem it is (discount, markup, or commission).
Step 2: **Extract** — List the known values and what is being asked.
Step 3: **Formula** — Select the correct formula based on problem type.
Step 4: **Compute** — Execute the arithmetic carefully.
Step 5: **Verify** — Check if the answer makes logical sense.

#### Identifying Known and Unknown Values

For every problem, create a mental (or written) inventory:

| What I Know | What I Need |
|-------------|-------------|
| Original Price = ₱X | Discount Amount? |
| Discount Rate = Y% | Sale Price? |

#### Selecting the Correct Formula Quickly

| If you know... | And you need... | Use this formula |
|----------------|-----------------|------------------|
| Original Price + Discount Rate | Discount Amount | OP × Rate |
| Original Price + Discount Rate | Sale Price | OP × (1 − Rate) |
| Sale Price + Discount Rate | Original Price | SP ÷ (1 − Rate) |
| Discount Amount + Rate | Original Price | DA ÷ Rate |
| Cost + Markup Rate | Selling Price | Cost × (1 + Rate) |
| Selling Price + Markup Rate | Cost Price | SP ÷ (1 + Rate) |
| Sales + Commission Rate | Commission | Sales × Rate |
| Commission + Rate | Total Sales | Commission ÷ Rate |

#### Estimation Before Solving

Before computing, estimate to eliminate obviously wrong choices:

**Example:** "25% off ₱8,000" — estimate: 25% of 8,000 is 2,000, so sale price ≈ ₱6,000. If a choice says ₱7,500, it's wrong.

#### Checking Answer Reasonableness

- A discount should make the price LOWER (if your answer is higher, you made an error)
- A markup should make the price HIGHER (if your answer is lower, you made an error)
- Commission should be LESS than total sales (if it's more, something is wrong)
- Successive discounts should give LESS total discount than the sum of individual rates

---

### 4.10 Estimation and Mental Math Techniques

#### Benchmark Percentages for Quick Computation

Memorize these for instant mental math:

| Percentage | Fraction | Mental Shortcut |
|-----------|----------|-----------------|
| 10% | 1/10 | Move decimal one place left |
| 20% | 1/5 | Divide by 5 |
| 25% | 1/4 | Divide by 4 |
| 50% | 1/2 | Divide by 2 |
| 5% | 1/20 | Half of 10% |
| 15% | 3/20 | 10% + 5% |
| 30% | 3/10 | 3 × 10% |
| 75% | 3/4 | Three-quarters |
| 33⅓% | 1/3 | Divide by 3 |
| 12.5% | 1/8 | Divide by 8 |

#### Quick Pricing Approximations

**For 15% discount on ₱4,000:**
- 10% = ₱400
- 5% = ₱200
- 15% = ₱600
- Sale price ≈ ₱3,400 ✓

**For 35% markup on ₱600:**
- 30% = ₱180
- 5% = ₱30
- 35% = ₱210
- Selling price ≈ ₱810 ✓

#### Elimination Strategies

On the CSE, you can often eliminate 2-3 choices immediately:

1. **Direction check:** If it's a discount, the answer must be LESS than the original price.
2. **Magnitude check:** 20% of ₱5,000 is ₱1,000. If a choice says the discount is ₱2,000, it's wrong.
3. **Parity check:** If the original price is even and the rate gives an even result, the answer should be even.

#### The "Complement" Shortcut

Instead of computing the discount then subtracting, compute what percentage the customer PAYS:

- 15% off → customer pays 85% → multiply by 0.85
- 30% off → customer pays 70% → multiply by 0.70
- 12% off → customer pays 88% → multiply by 0.88

This saves one arithmetic step and reduces errors.

---

### 4.11 Common Errors in Sales Problems

#### Error 1: Using the Wrong Base Amount

**Wrong:** Computing markup based on selling price instead of cost price.
```
Cost = ₱500, Selling = ₱650
WRONG: Markup rate = 150 ÷ 650 = 23.1% (this is profit margin, not markup)
RIGHT: Markup rate = 150 ÷ 500 = 30%
```

#### Error 2: Confusing Markup and Profit

Markup and profit are the same AMOUNT (Selling − Cost), but the RATE differs because the base differs. Markup rate uses cost as base; profit margin uses selling price as base.

#### Error 3: Forgetting Decimal Conversion

**Wrong:** ₱5,000 × 15 = ₱75,000 (forgot to convert 15% to 0.15)
**Right:** ₱5,000 × 0.15 = ₱750

#### Error 4: Adding Successive Discounts

**Wrong:** 20% + 15% = 35% total discount
**Right:** Combined multiplier = 0.80 × 0.85 = 0.68 → 32% total discount

#### Error 5: Misunderstanding Commission Wording

"Commission on sales above ₱100,000" means commission applies ONLY to the excess, not the entire amount.

#### Error 6: Confusing Original and Sale Price

When a problem says "after a 20% discount, the price is ₱4,000," the ₱4,000 is the SALE price (80% of original), not the original price.

**Wrong:** Original = ₱4,000 × 0.80 = ₱3,200
**Right:** ₱4,000 = Original × 0.80 → Original = ₱4,000 ÷ 0.80 = ₱5,000

---

### Exam Strategies

- Read the LAST sentence first — it tells you what to solve for
- Identify the problem type in 3 seconds using clue words (sale/off = discount, cost/profit = markup, earns/sales = commission)
- Convert percentages to decimals immediately (write "0.15" not "15%")
- Use the one-step multiplier method to save time (multiply by 0.80 instead of computing 20% then subtracting)
- For successive discounts, multiply multipliers directly — never add rates
- Estimate first: 10% of any number is just moving the decimal point
- If stuck between two close answers, recompute — CSE choices are designed to trap arithmetic errors
- Watch for "commission on excess" vs "commission on total" — they give very different answers

---

### Memory Aids

- **D**iscount **D**ecreases: multiply by (1 − rate) — both start with D
- **M**arkup **M**ultiplies up: multiply by (1 + rate) — both start with M
- **C**ommission = **C**ash from sales: Sales × Rate
- **Never add successive discounts** — remember "28, not 30" (20% + 10% = 28%, not 30%)
- **Base rule:** Discount base = Original Price; Markup base = Cost Price; Commission base = Sales
- **Complement shortcut:** "What percent does the buyer PAY?" (100% − discount% = pay%)
- **Reverse formula:** If you know the result and rate, DIVIDE by the multiplier to find the original

---

### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** A government cooperative store buys a filing cabinet at a cost of ₱4,000 and applies a 35% markup. Find the selling price.

- Step 1: Write the markup rate as a decimal: _____
- Step 2: Write the growth multiplier: 1 + _____ = _____
- Step 3: Multiply cost by the multiplier: ₱4,000 × _____ = ₱_____

**Answer:** Markup rate = 0.35. Multiplier = 1.35. Selling price: 4,000 × 1.35 = **₱5,400**

**2.** An office scanner listed at ₱12,000 is purchased with a bulk discount of 15%. How much does the procurement office save?

- Step 1: Identify what is being solved for: the _____ amount (savings)
- Step 2: Write the discount rate as a decimal: _____
- Step 3: Multiply the list price by the rate: ₱12,000 × _____ = ₱_____

**Answer:** Discount amount (savings). Discount rate = 0.15. Savings: 12,000 × 0.15 = **₱1,800**

**3.** After a 25% discount is applied during a clearance sale, a desk costs ₱4,500. What was its original price?

- Step 1: Write the complement multiplier for a 25% discount: 1 − _____ = _____
- Step 2: Set up the reverse division: ₱4,500 ÷ _____ = ₱_____
- Step 3: Compute original price: ₱_____

**Answer:** Complement multiplier = 0.75. Division: 4,500 ÷ 0.75. Original price: **₱6,000**

**4.** A salesperson earns ₱15,000 base salary plus a graduated commission of 3% on all sales above ₱100,000. If her sales are ₱180,000, find her total earnings.

- Step 1: Calculate sales above quota: ₱180,000 − ₱_____ = ₱_____
- Step 2: Compute commission on the excess: ₱_____ × 0.03 = ₱_____
- Step 3: Add base salary and commission: ₱15,000 + ₱_____ = ₱_____

**Answer:** Excess = 180,000 − 100,000 = ₱80,000. Commission = 80,000 × 0.03 = ₱2,400. Total: 15,000 + 2,400 = **₱17,400**

**5.** A laptop originally costing ₱20,000 is marked down by 20%, and then an additional 10% coupon is applied. What is the final price?

- Step 1: Write the complement multipliers for both discounts: _____ and _____
- Step 2: Multiply the original price by both multipliers: ₱20,000 × _____ × _____ = ₱_____
- Step 3: Compute final price: ₱_____

**Answer:** Complement multipliers are 0.80 and 0.90. Multiplication: 20,000 × 0.80 × 0.90 = 20,000 × 0.72. Final price: **₱14,400**

---

### Which Method?

For each problem, identify the problem type and solve.

**1.** A salesperson is paid a 6% commission on all sales. If he earns ₱9,600 in commission, what were his total sales?
- **Type:** Commission (Finding Total Sales given commission and rate)
- **Answer:** ₱160,000
- **Why:** Commission = Sales × Rate → ₱9,600 = Sales × 0.06 → Sales = 9,600 ÷ 0.06 = ₱160,000.

**2.** A wholesaler buys items at ₱800 and sells them with a 45% markup on cost. What is the selling price?
- **Type:** Markup (Finding the Selling Price)
- **Answer:** ₱1,160
- **Why:** Selling Price = Cost × (1 + Markup Rate) = 800 × 1.45 = ₱1,160.

**3.** An institutional supplier offers successive discounts of 15% and 10% on an order of office chairs listed at ₱20,000. How much does the buyer pay?
- **Type:** Successive Discounts (Multiplier Method)
- **Answer:** ₱15,300
- **Why:** Combined multiplier = 0.85 × 0.90 = 0.765. Net amount = 20,000 × 0.765 = ₱15,300.

**4.** A government procurement officer saved ₱3,500 on a piece of hardware using a 14% volume discount. What was the list price?
- **Type:** Discount (Finding Original Price from discount amount and rate)
- **Answer:** ₱25,000
- **Why:** Discount Amount = Original Price × Rate → ₱3,500 = Original Price × 0.14 → Original Price = 3,500 ÷ 0.14 = ₱25,000.

**5.** A retail store marks up a ₱1,000 item by 50%, then offers a 30% discount on the marked price. What is the final sale price?
- **Type:** Multi-Step Sales Problem (Markup then Discount)
- **Answer:** ₱1,050
- **Why:** Selling Price = 1,000 × 1.50 = ₱1,500. Discounted Sale Price = 1,500 × 0.70 = ₱1,050.

---

### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] Calculate discount amounts and sale prices using decimal multipliers
- [ ] Determine cost price, markup amount, and selling price using formulas
- [ ] Differentiate between markup percentage and profit margin percentage
- [ ] Solve straight commission, excess commission, and tiered commission problems
- [ ] Compute successive discounts compound-wise without adding the rates
- [ ] Chain operations together in multi-step sales scenarios (cost $\rightarrow$ markup $\rightarrow$ discount $\rightarrow$ commission)

---

### Mini Practice Set

**1.** A blouse originally priced at ₱1,200 is on sale at 25% off. What is the sale price?
**Answer:** ₱900
**Explanation:** Sale Price = ₱1,200 × 0.75 = ₱900.

**2.** A vendor buys fruits at ₱50/kg and sells at ₱70/kg. What is the markup rate?
**Answer:** 40%
**Explanation:** Markup = (70 − 50) ÷ 50 × 100 = 40%.

**3.** A salesperson earns 6% commission on ₱250,000 in sales. How much commission is earned?
**Answer:** ₱15,000
**Explanation:** Commission = ₱250,000 × 0.06 = ₱15,000.

**4.** After a 30% discount, a TV costs ₱21,000. What was the original price?
**Answer:** ₱30,000
**Explanation:** ₱21,000 = Original × 0.70 → Original = ₱21,000 ÷ 0.70 = ₱30,000.

**5.** A store marks up goods by 80% on cost of ₱250. What is the selling price?
**Answer:** ₱450
**Explanation:** Selling Price = ₱250 × 1.80 = ₱450.

**6.** Successive discounts of 10% and 20% are applied to ₱8,000. What is the final price?
**Answer:** ₱5,760
**Explanation:** ₱8,000 × 0.90 × 0.80 = ₱5,760.

**7.** An agent earned ₱45,000 commission at a 3% rate. What were total sales?
**Answer:** ₱1,500,000
**Explanation:** Sales = ₱45,000 ÷ 0.03 = ₱1,500,000.

**8.** A laptop costs ₱32,000 with a 15% discount. How much does the buyer save?
**Answer:** ₱4,800
**Explanation:** Discount = ₱32,000 × 0.15 = ₱4,800.

**9.** Cost is ₱600. After 50% markup and 20% discount, what is the sale price?
**Answer:** ₱720
**Explanation:** ₱600 × 1.50 = ₱900; ₱900 × 0.80 = ₱720.

**10.** A clerk earns ₱18,000 base plus 4% on ₱180,000 sales. Total earnings?
**Answer:** ₱25,200
**Explanation:** Commission = ₱180,000 × 0.04 = ₱7,200; Total = ₱18,000 + ₱7,200 = ₱25,200.

**11.** What single discount is equivalent to successive discounts of 20% and 10%?
**Answer:** 28%
**Explanation:** Combined multiplier = 0.80 × 0.90 = 0.72; Equivalent discount = 1 − 0.72 = 28%.

**12.** A store wants 25% profit on cost after giving a 20% discount. What markup rate is needed?
**Answer:** 56.25%
**Explanation:** Let cost = 100. Need sale price = 125. Sale price = Marked × 0.80. Marked = 125 ÷ 0.80 = 156.25. Markup = 56.25%.

**13.** Commission on sales above ₱300,000 is 5%. Sales total ₱480,000. Commission earned?
**Answer:** ₱9,000
**Explanation:** Excess = ₱480,000 − ₱300,000 = ₱180,000; Commission = ₱180,000 × 0.05 = ₱9,000.

**14.** An item's cost is ₱1,400. Markup is 35%. What is the markup amount?
**Answer:** ₱490
**Explanation:** Markup = ₱1,400 × 0.35 = ₱490.

**15.** A ₱6,000 item has successive discounts of 15% and 15%. Final price?
**Answer:** ₱4,335
**Explanation:** ₱6,000 × 0.85 × 0.85 = ₱6,000 × 0.7225 = ₱4,335.

**16.** A customer saved ₱2,400 with a 20% discount. What was the original price?
**Answer:** ₱12,000
**Explanation:** ₱2,400 = Original × 0.20 → Original = ₱2,400 ÷ 0.20 = ₱12,000.

**17.** Three agents split a 5% commission on a ₱3,600,000 sale equally. Each gets?
**Answer:** ₱60,000
**Explanation:** Total commission = ₱3,600,000 × 0.05 = ₱180,000; Each = ₱180,000 ÷ 3 = ₱60,000.

**18.** A gadget costs ₱2,500 to make. Selling price is ₱4,000. Markup rate?
**Answer:** 60%
**Explanation:** Markup = (₱4,000 − ₱2,500) ÷ ₱2,500 × 100 = 60%.

**19.** Original price ₱15,000. After 10% then 20% discounts, what is the total discount amount?
**Answer:** ₱4,200
**Explanation:** Final = ₱15,000 × 0.90 × 0.80 = ₱10,800; Discount = ₱15,000 − ₱10,800 = ₱4,200.

**20.** A seller marks up by 100% then gives 40% off. Is there still profit on a ₱500 cost item?
**Answer:** Yes, ₱100 profit
**Explanation:** Selling = ₱500 × 2.00 = ₱1,000; Sale = ₱1,000 × 0.60 = ₱600; Profit = ₱600 − ₱500 = ₱100.

---

### Connections

How this topic connects to other areas of the CSE:

- **Fundamentals of Percentages:** Converting discount, markup, and commission rates to decimals is the key arithmetic prerequisite for all calculations in this lesson
- **Percentage Increase and Decrease:** Markups are direct applications of percent increases, while discounts are direct applications of percent decreases
- **Profit, Loss, and Tax:** Calculating cost, marked price, and net sales allows businesses to determine taxable net revenue and project annual profits or losses
- **Basic Operations:** Multiplication and division of decimal currency figures are the primary computational components in every multi-step transaction problem

---

### Mastery Checklist

✅ compute discount amounts correctly
✅ determine sale prices accurately using the multiplier method
✅ compute markups and selling prices efficiently
✅ solve commission problems including tiered and salary-plus structures
✅ handle successive discounts without adding rates
✅ identify problem types instantly from clue words
✅ solve multi-step problems involving markup, discount, and commission together
✅ estimate answers mentally to eliminate wrong choices
✅ avoid the six most common errors in sales mathematics
✅ solve CSE-style business math problems under time pressure

---

> 🤔 **Why does this work?** Discount and markup calculations work because they are applications of the multiplier method: a 20% discount means you keep 80% (multiplier = 0.80), and a 30% markup means the new price is 130% of cost (multiplier = 1.30). Successive changes multiply: 0.80 × 0.90 = 0.72 (not 0.70). This multiplicative structure is why successive discounts cannot be simply added — each operates on a different (already-changed) base.


> **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.


> **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.

## Worked Examples

### Example 1: Basic Discount & Sale Price (Easy)

**Problem:** A department store offers a promotional 15% discount on a business suit originally priced at ₱6,000. What is the discount amount, and how much does the buyer pay?

**Solution:**
1. **Identify the original value and rate:**
   - Original Price = ₱6,000
   - Discount Rate = 15% (0.15)
2. **Calculate the absolute discount amount:**
   - $\text{Discount Amount} = 6,000 \times 0.15 = \mathbf{₱900}$
3. **Calculate the sale price:**
   - $\text{Sale Price} = 6,000 - 900 = \mathbf{₱5,100}$
   - *Shortcut check:* $6,000 \times 0.85 = \mathbf{₱5,100}$

**Verification:** ₱5,100 + ₱900 = ₱6,000.

---

### Example 2: Markup and Selling Price (Easy)

**Problem:** A hardware supply depot purchases steel bars at a cost of ₱320 per unit. If the store applies a standard 40% markup on cost, what is the retail selling price?

**Solution:**
1. **Identify cost and markup rate:**
   - Cost Price = ₱320
   - Markup Rate = 40% (0.40)
2. **Compute the markup amount:**
   - $\text{Markup Amount} = 320 \times 0.40 = \mathbf{₱128}$
3. **Calculate the selling price:**
   - $\text{Selling Price} = 320 + 128 = \mathbf{₱448}$
   - *Shortcut check:* $320 \times 1.40 = \mathbf{₱448}$

**Verification:** ₱448 − ₱320 = ₱128 markup.

---

### Example 3: Commission on Excess (Medium)

**Problem:** An investment consultant earns a monthly base salary of ₱18,000, plus a commission of 4.5% on all product sales exceeding a monthly threshold of ₱150,000. If their sales total ₱260,000, what are their total earnings?

**Solution:**
1. **Find the sales subject to commission:**
   - $\text{Eligible Sales} = 260,000 - 150,000 = ₱110,000$
2. **Calculate the commission earned:**
   - $\text{Commission} = 110,000 \times 0.045 = \mathbf{₱4,950}$
3. **Add commission to the base salary:**
   - $\text{Total Earnings} = 18,000 + 4,950 = \mathbf{₱22,950}$

**Verification:** Commission of ₱4,950 represents 4.5% of ₱110,000.

---

### Example 4: Finding Cost Price from Selling Price (Hard)

**Problem:** A school supply retailer sells a student scientific calculator for ₱875. If this price represents a 25% markup based on the store's original wholesale cost, what was the calculator's cost price?

**Solution:**
1. **Identify the values:**
   - Selling Price = ₱875
   - Markup Rate = 25% (0.25)
2. **Determine the markup growth multiplier:**
   - $\text{Multiplier} = 1 + 0.25 = 1.25$
3. **Calculate the cost price by dividing the selling price by the multiplier:**
   - $\text{Cost Price} = \frac{\text{Selling Price}}{\text{Multiplier}}$
   - $\text{Cost Price} = \frac{875}{1.25} = \mathbf{₱700}$

**Verification:** ₱700 $\times$ 1.25 = ₱875. Adding a 25% markup (= ₱175) to ₱700 yields ₱875.

---

### Example 5: Successive Discounts (Hard)

**Problem:** A procurement agent orders custom office partitions listed at ₱50,000. The manufacturer offers a standard 20% trade discount for bulk orders, plus an additional 5% discount for cash payment. What is the final net price paid?

**Solution:**
1. **Represent both successive discounts as multipliers:**
   - Trade Discount (20% off): Multiplier = 0.80
   - Cash Discount (5% off): Multiplier = 0.95
2. **Calculate the combined multiplier:**
   - $\text{Combined Multiplier} = 0.80 \times 0.95 = \mathbf{0.76}$ (equivalent to a 24% single discount)
3. **Compute the final sale price:**
   - $\text{Final Price} = 50,000 \times 0.76 = \mathbf{₱38,000}$

**Verification by steps:**
- Price after 20% bulk discount: ₱50,000 $\times$ 0.80 = ₱40,000
- Price after 5% cash discount: ₱40,000 $\times$ 0.95 = ₱38,000. The round-trip matches!

---

## Key Takeaways

- **Differentiate Base Amounts:** Ensure you apply the correct base for each operation. Discounts apply to the original list price; markups apply to cost price; commissions apply to sales.
- **Successive discounts compound:** Never add successive discounts directly. 20% off plus an additional 10% off is equivalent to 28% off, not 30% off, because the second discount is applied to the already-reduced price.
- **One-Step Multipliers:** Speed up calculations by using direct multipliers. An increase of $r\%$ is calculated by multiplying by $(1 + r/100)$; a decrease of $r\%$ is calculated by multiplying by $(1 - r/100)$.
- **Cost vs. Profit Margin:** Remember that markup rate measures profit relative to cost ($\text{profit} \div \text{cost}$), whereas profit margin rate measures profit relative to selling price ($\text{profit} \div \text{selling price}$).

---

## Summary

Sales mathematics covers the essential calculation mechanisms used to establish, reduce, and distribute retail values. This lesson explains the step-by-step processes for determining discounts, selling prices (via cost markups), and commission-based salaries. It explains the compounding behavior of successive discounts using the complement multiplier method, demonstrating why sequential discounts are never additive. Multi-step business problems guide the reader through complete cost-to-earning cycles, linking procurement budgets, incentive payrolls, and retail pricing strategies. By applying benchmark percentage estimation methods and verifying results with mathematical division techniques, candidates are equipped to solve complex sales math questions rapidly and accurately on the civil service exam.
