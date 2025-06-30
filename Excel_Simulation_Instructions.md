# Agile Teams Flow Metrics Simulation - Excel Version

## Overview
This Excel workbook replicates the Python simulation using formulas, data tables, and charts to model agile team flow metrics based on queuing theory and Little's Law.

## Workbook Structure

### Sheet 1: "Dashboard" (Main Interface)
**Layout:**
- **A1:M1** - Title: "Agile Teams Flow Metrics Simulation"
- **A3:D20** - Parameter Input Section
- **F3:M20** - Key Metrics Display
- **A22:M40** - Flow Chart (Utilization vs Lead Time/Throughput)
- **A42:M50** - Goal Seeking Controls

### Sheet 2: "Calculations" (Hidden formulas)
**Layout:**
- **A1:Z100** - All calculation tables and intermediate results

### Sheet 3: "Data Tables" (Lookup tables)
**Layout:**
- **A1:E50** - Utilization scenarios (50-100%)
- **G1:K50** - Corresponding metrics for each scenario

---

## Dashboard Sheet Setup

### Parameter Input Section (A3:D20)

**A3:D3** - Headers
```
| Parameter | Value | Min | Max |
```

**A4:D20** - Input Parameters with Data Validation
```
| Teams                    | 1    | 1   | 40  |
| Developers (Count)       | 3    | 1   | 10  |
| Developers Time Min      | 1.0  | 0.5 | 3.0 |
| Developers Time Max      | 2.0  | 0.5 | 3.0 |
| Testers (Count)          | 2    | 1   | 10  |
| Testers Time Min         | 2.0  | 0.5 | 3.0 |
| Testers Time Max         | 3.0  | 0.5 | 3.0 |
| Architects (Count)       | 1    | 0   | 5   |
| Architects Time Min      | 1.5  | 0.5 | 3.0 |
| Architects Time Max      | 2.5  | 0.5 | 3.0 |
| Demand (Features/Sprint) | 10   | 5   | 20  |
| Proficiency (%)          | 80%  | 50% | 100%|
| Defect Rate (%)          | 20%  | 0%  | 50% |
| Rework Factor            | 0.5  | 0   | 1.0 |
| Dependencies (%)         | 20%  | 0%  | 50% |
| AI Impact (%)            | 30%  | 0%  | 50% |
```

### Key Metrics Display (F3:M20)

**F3:M3** - Headers
```
| Metric | Current | Optimal | Warning |
```

**F4:M20** - Calculated Results
```
| Current Utilization     | =CALC!B5  | 75%    | >90%   |
| Lead Time (Days)        | =CALC!B6  | 3.2    | >10    |
| Throughput (Features)   | =CALC!B7  | 8.5    | <5     |
| Schedule Variability    | =CALC!B8  | 2.1    | >5     |
| Service Rate            | =CALC!B9  | 12.3   | -      |
| Effective Demand        | =CALC!B10 | 11.0   | -      |
| Cost Impact ($K/Sprint) | =CALC!B11 | 45     | >100   |
```

---

## Calculations Sheet Formulas

### Core Calculations (CALC!A1:Z100)

**A1:B1** - Labels
```
| Parameter | Value |
```

**A2:B20** - Input References
```
A2: Teams                B2: =Dashboard!B4
A3: Dev_Count           B3: =Dashboard!B5
A4: Dev_Time_Min        B4: =Dashboard!B6
A5: Dev_Time_Max        B5: =Dashboard!B7
... (continue for all parameters)
```

**A25:B35** - Service Rate Calculations
```
A25: Dev_Avg_Time       B25: =(B4+B5)/2
A26: Test_Avg_Time      B26: =(B8+B9)/2
A27: Arch_Avg_Time      B27: =(B12+B13)/2

A28: Dev_Service_Rate   B28: =(1/B25)*B3*B16*(1-B19)*(1+B20)
A29: Test_Service_Rate  B29: =(1/B26)*B6*B16*(1-B19)*(1+B20)
A30: Arch_Service_Rate  B30: =(1/B27)*B10*B16*(1-B19)*(1+B20)

A31: Total_Service_Rate B31: =(B28+B29+B30)*B2
A32: Total_Resources    B32: =(B3+B6+B10)*B2
```

**A40:B50** - Flow Metrics
```
A40: Effective_Demand   B40: =B14*(1+B17*B18*(1-B20*0.2))
A41: Base_Utilization   B41: =B40/B31
A42: Current_Util_Pct   B42: =B41*100

A43: Lead_Time          B43: =2+3/(1-MIN(B41,0.999)+0.001)
A44: Max_Throughput     B44: =B31*(1-B17*(1-B20*0.2))
A45: Throughput         B45: =MIN(B40,B44*MAX(0,1-B41))
A46: WIP                B46: =B40*B43
A47: Variability        B47: =MAX(0,B43*(B41/MAX(1,B41))*(B46/B32)*0.1)
A48: Cost_Impact        B48: =B43*10
```

---

## Data Tables Sheet

### Utilization Scenarios (A1:E50)

**A1:E1** - Headers
```
| Util% | Lead_Time | Throughput | Variability | Cost |
```

**A2:E50** - Data Table (using Table function)
```
=TABLE(Dashboard!B4,{50;51;52;...;100},
       {CALC formulas for each utilization level})
```

**Key Formula Pattern for each row:**
```
B2: =2+3/(1-MIN(A2/100,0.999)+0.001)  // Lead Time
C2: =MIN($B$40,$B$44*MAX(0,1-A2/100)) // Throughput  
D2: =MAX(0,B2*(A2/100)*($B$46/$B$32)*0.1) // Variability
E2: =B2*10  // Cost Impact
```

---

## Charts and Visualizations

### Primary Chart: Utilization vs Metrics (Dashboard A22:M40)

**Chart Type:** Combination Chart
- **Primary Axis:** Lead Time (Red Line)
- **Secondary Axis:** Throughput (Blue Line)
- **Scatter Series:** Variability (Orange bubbles, size varies)

**Data Source:** Data Tables!A1:E50

**Chart Elements:**
- Vertical lines at 90% and 95% utilization
- Data labels for current position
- Cost impact annotation

### Secondary Charts:

**Utilization Gauge (F22:H30)**
- Speedometer-style gauge showing current utilization
- Color coding: Green (<80%), Yellow (80-90%), Red (>90%)

**Throughput Trend (J22:M30)**
- Simple line chart showing throughput vs utilization
- Highlights optimal range

---

## Goal Seeking Controls (Dashboard A42:M50)

### Goal Seek Buttons (Using Solver Add-in)

**A43:C43** - Target Utilization
```
| Target Util% | 80% | [Optimize Button] |
```

**A44:C44** - Maximize Throughput  
```
| Max Throughput | Auto | [Optimize Button] |
```

**A45:C45** - Minimize Variability
```
| Min Variability | Auto | [Optimize Button] |
```

### Solver Configurations:

**Target Utilization:**
```
Objective: Set CALC!B42 to Value 80
By changing: Dashboard!B14 (Demand)
Constraints: Dashboard!B14 >= 5, <= 20
```

**Maximize Throughput:**
```
Objective: Maximize CALC!B45
By changing: Dashboard!B14 (Demand)
Constraints: Dashboard!B14 >= 5, <= 20
```

**Minimize Variability:**
```
Objective: Minimize CALC!B47
By changing: Dashboard!B14 (Demand)  
Constraints: Dashboard!B14 >= 5, <= 20
```

---

## Advanced Features

### Conditional Formatting

**Parameter Values:**
- Red if outside recommended ranges
- Yellow if approaching limits
- Green for optimal values

**Metrics Display:**
- Traffic light colors based on thresholds
- Data bars for relative comparison

### Data Validation

**All Input Cells:**
```
Data > Data Validation > Settings:
- Allow: Decimal
- Between: Min and Max values
- Input Message: Parameter description
- Error Alert: "Value must be between X and Y"
```

### Dynamic Charts

**Chart Updates:**
- Automatically refresh when parameters change
- Current position highlighted with different marker
- Threshold lines adjust based on context

---

## Macros and Automation

### Auto-Calculate Macro
```vb
Sub RecalculateMetrics()
    Application.CalculationMode = xlCalculationManual
    Range("Calculations!A1:Z100").Calculate
    Range("DataTables!A1:E50").Calculate
    Charts("FlowChart").Refresh
    Application.CalculationMode = xlCalculationAutomatic
End Sub
```

### Goal Seek Macros
```vb
Sub OptimizeUtilization()
    Dim targetUtil As Double
    targetUtil = Range("Dashboard!C43").Value
    
    SolverReset
    SolverOk SetCell:="Calculations!B42", _
             MaxMinVal:=3, _
             ValueOf:=targetUtil, _
             ByChange:="Dashboard!B14"
    SolverSolve UserFinish:=True
End Sub
```

---

## Usage Instructions

### Getting Started:
1. **Open the workbook** and enable macros if prompted
2. **Review default parameters** in the input section
3. **Observe initial metrics** and chart
4. **Modify parameters** using dropdown lists and input cells

### Parameter Exploration:
1. **Adjust team sizes** to see capacity impact
2. **Change service times** to model skill variations  
3. **Modify quality parameters** to see rework effects
4. **Test AI impact** scenarios

### Goal Seeking:
1. **Set target utilization** and click optimize
2. **Use throughput maximization** for capacity planning
3. **Minimize variability** for schedule predictability

### Scenario Analysis:
1. **Save current parameters** as named scenarios
2. **Compare multiple team configurations**
3. **Export charts** for presentations

---

## File Structure

```
AgileFl owMetrics.xlsx
├── Dashboard (Visible)
│   ├── Parameter Inputs
│   ├── Key Metrics
│   ├── Flow Chart
│   └── Goal Seeking
├── Calculations (Hidden)
│   ├── Core Formulas
│   ├── Intermediate Results
│   └── Validation Logic
└── DataTables (Hidden)
    ├── Utilization Scenarios
    ├── Lookup Tables
    └── Chart Data Sources
```

This Excel version provides the same analytical capabilities as the Python simulation while being accessible to users who prefer spreadsheet interfaces.