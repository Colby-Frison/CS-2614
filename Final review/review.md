# Computer Organization – Final Exam **Ultra‑Condensed Deep‑Dive**

> **Source Backbone:** *Computer System Architecture* 3e (M. Moris Mano) + all lecture decks, quiz & mid‑term keys.  Everything below is exam‑grade depth (no fluff) so you can cram efficiently tonight.

---

## Quick Navigation

1. [Logic & Digital Fundamentals](#ch1)  ▸ fast Boolean proofs, K‑maps
2. [MSI Components & Sequential Blocks](#ch2)  ▸ decoders⇆encoders, registers, counters, buses
3. [Data Representation & Computer Arithmetic](#ch3)  ▸ 2’s‑comp, IEEE‑754, overflow traps
4. [Register‑Transfer & ALU Micro‑Operations](#ch4)  ▸ RTL notations, common bus, ALU + shifter
5. [Basic Computer Design (Mano Machine)](#ch5)  ▸ instruction cycle, control logic, interrupts
6. [Night‑Before Blitz Checklist](#blitz)
7. [Formula & Opcode Sheets](#refs)

---

## 1  Logic & Digital Fundamentals (Ch 1)

### 1.1 Boolean Essentials

* **Identity**: X+0=X , X·1=X
* **Null**: X+1=1 , X·0=0
* **Idempotent**: X+X=X , X·X=X
* **Complement**: X+X′=1 , X·X′=0
* **Absorption**: X+XY=X ; X(X+Y)=X
* **Consensus**: XY+X′Z+YZ = XY + X′Z

> **Proof Trick:** Convert to consensus form → strike redundant term quickly.

### 1.2 Canonical & Standard Forms – SOP vs POS

* **Canonical Sum‑of‑Products (SOP)**: Express F as OR (Σ) of **minterms** where F=1.  For n variables, each minterm $m_i = X_0^{b_0}X_1^{b_1}…X_{n-1}^{b_{n-1}}$ appears once.
* **Canonical Product‑of‑Sums (POS)**: Express F as AND (Π) of **maxterms** where F=0.  Each maxterm $M_i = (X_0+\bar{X}_1+…)$ contains every literal once.
* **Standard (non‑canonical) SOP/POS**: Literals may be missing after algebra/K‑map simplification, yielding minimal gate cost.
* **Conversion**: Canonical SOP ↔ POS via complement: $F = Σm(…) = \overline{ΠM(…)}$ and vice versa.
* **Hardware insight**: SOP maps naturally to a two‑level AND‑OR network; POS to OR‑AND (NAND/NOR) — choose based on gate availability.

### 1.3 K‑Map Master Pattern

```
2‑var: 01/11 vertical pairing saves a literal.
3‑var: look for wrapped rectangles of 4 (edges touch).
4‑var: aim for 8‑cell ad‑jacencies (across borders).
5‑var: treat as two 4‑var maps; pair vertically between them.
```

* **Don’t‑cares (×)**: may be 0 or 1 — use to enlarge group, but **never** force inclusion if it breaks minimality.
* **Prime vs Essential implicant**: an NP‑complete cover problem, but K‑map visually reveals.

### 1.3 Sequential Core Facts

| FF     | Char. Eqn      | Excitation (to go from Q→Q⁺)                       |
| ------ | -------------- | -------------------------------------------------- |
| **D**  | Q⁺=D           | D=Q⁺                                               |
| **T**  | Q⁺=T⊕Q         | T = Q⊕Q⁺                                           |
| **JK** | Q⁺ = JQ′ + K′Q | J = Q′Q⁺, K = QQ⁺′                                 |
| **SR** | Q⁺ = S + R′Q   | Forbidden S=R=1 (gating avoided in clocked design) |

*Edge‑triggering* (Mano §1‑14): Master–slave or single‑edge avoids level‑sensitive hazards.

### 1.4 Typical Exam Prompts

1. **Prove** using Boolean algebra: $(X+Y)(X+Z)=X+YZ$
2. **Minimize** F(A,B,C,D) = Σm(0,2,5,7,8,10,13) + d(1,9)
3. **Design** a mod‑6 synchronous counter with JK FFs – produce optimum logic via excitation maps.

---

## 2  MSI Components & Sequential Blocks (Ch 2)

### 2.1 Decoder / Encoder / Priority Encoder

* **De‑Facto Equations** (3→8 example):

  * $D_0=E·A′B′C′$ … $D_7=E·ABC$
  * *Priority* adds OR tree for V=ΣIᵢ and cascades for >8 lines.

### 2.2 Multiplexer as Function Realizer

F = Σm(1,2,6,7) – with A,B as select, hook C and constants:

| Input                                                                  | I₀ | I₁ | I₂ | I₃ |
| ---------------------------------------------------------------------- | -- | -- | -- | -- |
| C                                                                      | 0  | 1  | 1  | 0  |
| Minimal exam angle: show how one 4×1 implements any 2‑var truth table. |    |    |    |    |

### 2.3 Register Transfer Hardware

* **Parallel Load**: Gating D onto FF when Load=1 using AND‑OR network.
* **Shift Register Timing**: For bidirectional 4‑bit SR: S1S0 bits control 2×1 MUX in front of each D.
* **Ring vs Johnson (twisted ring)** counters: count length n vs 2n.

### 2.4 Synchronous Counter Logic (n‑bit)

* **Toggle signal:** $T_0=1$; $T_i=\prod_{k=0}^{i-1}Q_k$
* **Prop delay:** t\_total ≈ t\_toggle + t\_FF; independent of n (advantage vs ripple).
* **Exam Trap:** Provide waveform → deduce number of FFs required for given mod.

---

## 3  Data Representation & Computer Arithmetic (Ch 3)

### 3.1 2’s‑Complement Quick Ref

* Range (n bits): $-2^{n-1}$ … $+2^{n-1}-1$.
* Subtraction **A−B**: Compute A + (\~B +1).

### 3.2 Overflow Diagnostics

| Operands sign | Sum sign | V flag       |
| ------------- | -------- | ------------ |
| same          | differs  | 1 (overflow) |
| otherwise     | –        | 0            |

**Hardware**: XOR of carry into and out of MSB.

### 3.3 Floating‑Point Edge Cases

| Case     | Exponent | Mantissa | Interpretation   |
| -------- | -------- | -------- | ---------------- |
| Zero     | 0        | 0        | ±0               |
| Denormal | 0        | ≠0       | ±0.M ×2^{1‑Bias} |
| Inf      | 255      | 0        | ±∞               |
| NaN      | 255      | ≠0       | quiet/signalling |

**Addition Algorithm** Steps (test loves order):

1. **Align** smaller exp → right‑shift mantissa (sticky bit!).
2. **Add/Sub** depending on signs.
3. **Normalize**: shift left/right & adjust exp, handle overflow into hidden 1.
4. **Round**: guard + round + sticky → round‑to‑nearest even.

### 3.4 Carry‑Lookahead Adder (if covered)

* Generate Gᵢ=AᵢBᵢ, Propagate Pᵢ=Aᵢ⊕Bᵢ.
* Carry Cᵢ₊₁ = Gᵢ + PᵢCᵢ. 4‑bit CLA reduces add time to gate‑levels ≈3.

---

## 4  Register‑Transfer & ALU Operations (Ch 4)

### 4.1 RTL Notation Cheats

* **Conditional**: `If (C) then R1←R2`.
* **Multiple micro‑ops same clock**: use comma: `R2←R1, R1←R2` (swap example 4‑1).

### 4.2 ALU Function Table (Mode M & S₂S₁)

| M | S2 S1 | Operation         |
| - | ----- | ----------------- |
| 0 | 00    | A + B             |
| 0 | 01    | A + B′ + 1 (A‑B)  |
| 0 | 10    | A + 1 (increment) |
| 0 | 11    | A − 1 (decrement) |
| 1 | 00    | A ∧ B             |
| 1 | 01    | A ∨ B             |
| 1 | 10    | A ⊕ B             |
| 1 | 11    | ¬A                |

ALU couples to 8‑way shifter (left/right logical, arithmetic, rotate) controlled by H1H0.

### 4.3 Common Bus Timing

* 16‑line bus driven by tri‑state outputs of every register; decoder selects one source at a time (`S₂S₁S₀`). Destination registers have LD lines.
* **Hazard Avoidance:** Only one driver active; others in High‑Z.

---

## 5  Basic Computer (Mano) – *Everything they love to ask*

### 5.1 Instruction Cycle Detailed Table

```
T0: AR←PC                           ⟶ Address fetch
T1: IR←M[AR], PC←PC+1              ⟶ Instruction fetch
T2: Decode IR[12‑14] → D_0…D_7
    AR←IR[0‑11]                    ⟶ Indirect address load
    I←IR[15]
T3: • If I=1 & D7=0 → Indirect cycle (AR←M[AR])
    • else go Exec
```

### 5.2 Execution: Memory‑Reference Example (ADD)

```
D1 T4: DR←M[AR]
D1 T5: AC←AC+DR, E←Cout
```

*Exam cue*: they provide timing diagram — you fill missing micro‑ops.

### 5.3 Register‑Reference Bits (IR\[0‑11])

| Bit | Mnemonic | Micro‑operation     |
| --- | -------- | ------------------- |
| 11  | **CLA**  | AC←0                |
| 10  | **CLE**  | E←0                 |
| 9   | **CMA**  | AC←¬AC              |
| 8   | **CME**  | E←¬E                |
| 7   | **CIR**  | (AC,E) right‑rotate |
| 6   | **CIL**  | (AC,E) left‑rotate  |
| 5   | **INC**  | AC←AC+1             |
| 4   | **SPA**  | Skip if AC ≥ 0      |
| …   | **HLT**  | S ← 0 (stop)        |

### 5.4 I/O Instructions Key Flags

* **INP**: AC\[7‑0]←INPR ; FGI←0
* **OUT**: OUTR←AC\[7‑0] ; FGO←0
* **SKI**/**SKO**: skip if flag set.

### 5.5 Hardwired Control Equations Example

```
LD(AC) = D1T5 + D7'IT3(CLA) + D7'IT3(CIR/CIL/INC) + ...
```

Memorize pattern: *OR of all times AC is destination*.

### 5.6 Interrupt Service

1. During execute, if **IEN=1 & (FGI+FGO)=1** set R=1.
2. On next T0 with R=1:

   * M\[0]←PC ; PC←1 ; IEN←0 ; R←0
3. Execute ISR at addr 1; return via **BUN 0**.

---

## 6  Night‑Before Blitz Checklist

1. **Run 3 K‑map reductions** (3‑,4‑,5‑var) until under 2 min each.
2. **Hand‑trace** Mano computer through `ISZ 100` twice: once when DR≠0, once zero → verify PC skip.
3. **Practice** floating‑point add: 1.001×2⁻² + (‑1.100×2⁻³). Must normalize & round.
4. **Write** RTL for `Swap R1,R2` and draw bus activity.
5. **Recite** register‑reference bit table without peeking.
6. **Sleep > 6 h.** Short‑term retention locks during REM.

---

## 7  Formula & Opcode Sheets

*(unchanged from previous version for quick look‑up)*

### Boolean Laws

```
X + X'Y = X + Y
(X + Y)(X + Z) = X + YZ
(XY)' = X' + Y'
```

### 2’s‑Comp Negation

Invert → add 1 ; overflow flag = Cout ⊕ C\_{n-1}.

### IEEE‑754 Constants

Bias=127; Exp=255 ⇒ special.

### Register Transfer Symbols

LD, INR, CLR, DR←M\[AR], etc.

---

**End of v3 – call out any topic still too shallow, we’ll append examples instantly.**
