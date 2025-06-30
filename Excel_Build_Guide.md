# Step-by-Step Excel Build Guide
## Agile Teams Flow Metrics Simulation

### Step 1: Create the Workbook Structure

1. **Open Excel** and create a new workbook
2. **Rename sheets:**
   - Sheet1 → "Dashboard"
   - Sheet2 → "Calculations" 
   - Sheet3 → "DataTables"
3. **Hide sheets:** Right-click "Calculations" and "DataTables" → Hide

### Step 2: Build the Dashboard Sheet

#### A. Title and Headers (Row 1-2)
```
A1: Agile Teams Flow Metrics Simulation
```
- **Format:** Bold, 18pt, Center across A1:M1
- **Background:** Blue, White text

#### B. Parameter Input Section (A3:D20)

**Row 3 - Headers:**
```
A3: Parameter
B3: Value  
C3: Min
D3: Max
```
- **Format:** Bold, Blue background, White text

**Rows 4-20 - Parameters:**
```
A4: Teams                    B4: 1     C4: 1    D4: 40
A5: Developers (Count)       B5: 3     C5: 1    D5: 10
A6: Developers Time Min      B6: 1.0   C6: 0.5  D6: 3.0
A7: Developers Time Max      B7: 2.0   C7: 0.5  D7: 3.0
A8: Testers (Count)          B8: 2     C8: 1    D8: 10
A9: Testers Time Min         B9: 2.0   C9: 0.5  D9: 3.0
A10: Testers Time Max        B10: 3.0  C10: 0.5 D10: 3.0
A11: Architects (Count)      B11: 1    C11: 0   D11: 5
A12: Architects Time Min     B12: 1.5  C12: 0.5 D12: 3.0
A13: Architects Time Max     B13: 2.5  C13: 0.5 D13: 3.0
A14: Demand (Features/Sprint) B14: 10  C14: 5   D14: 20
A15: Proficiency (%)         B15: 0.8  C15: 0.5 D15: 1.0
A16: Defect Rate (%)         B16: 0.2  C16: 0   D16: 0.5
A17: Rework Factor           B17: 0.5  C17: 0   D17: 1.0
A18: Dependencies (%)        B18: 0.2  C18: 0   D18: 0.5
A19: AI Impact (%)           B19: 0.3  C19: 0   D19: 0.5
```

#### C. Data Validation for Input Cells (B4:B19)

**For each cell B4:B19:**
1. Select cell → Data → Data Validation
2. **Settings:**
   - Allow: Decimal
   - Data: Between
   - Minimum: =C4 (reference to min column)
   - Maximum: =D4 (reference to max column)
3. **Input Message:**
   - Title: "Parameter Input"
   - Message: "Enter value between " & C4 & " and " & D4
4. **Error Alert:**
   - Style: Stop
   - Title: "Invalid Input"
   - Message: "Value must be between " & C4 & " and " & D4

#### D. Key Metrics Display (F3:I20)

**Row 3 - Headers:**
```
F3: Metric
G3: Current
H3: Optimal  
I3: Warning
```

**Rows 4-20 - Metrics:**
```
F4: Current Utilization     G4: =Calculations!B42  H4: 75%    I4: >90%
F5: Lead Time (Days)        G5: =Calculations!B43  H5: 3.2    I5: >10
F6: Throughput (Features)   G6: =Calculations!B45  H6: 8.5    I6: <5
F7: Schedule Variability    G7: =Calculations!B47  H7: 2.1    I7: >5
F8: Service Rate            G8: =Calculations!B31  H8: 12.3   I8: -
F9: Effective Demand        G9: =Calculations!B40  H9: 11.0   I9: -
F10: Cost Impact ($K/Sprint) G10: =Calculations!B48 H10: 45   I10: >100
```

### Step 3: Build the Calculations Sheet

#### A. Parameter References (A1:B20)
```
A1: Parameter          B1: Value
A2: Teams              B2: =Dashboard!B4
A3: Dev_Count          B3: =Dashboard!B5
A4: Dev_Time_Min       B4: =Dashboard!B6
A5: Dev_Time_Max       B5: =Dashboard!B7
A6: Test_Count         B6: =Dashboard!B8
A7: Test_Time_Min      B7: =Dashboard!B9
A8: Test_Time_Max      B8: =Dashboard!B10
A9: Arch_Count         B9: =Dashboard!B11
A10: Arch_Time_Min     B10: =Dashboard!B12
A11: Arch_Time_Max     B11: =Dashboard!B13
A12: Demand            B12: =Dashboard!B14
A13: Proficiency       B13: =Dashboard!B15
A14: Defect_Rate       B14: =Dashboard!B16
A15: Rework_Factor     B15: =Dashboard!B17
A16: Dependencies      B16: =Dashboard!B18
A17: AI_Impact         B17: =Dashboard!B19
```

#### B. Service Rate Calculations (A25:B35)
```
A25: Dev_Avg_Time       B25: =(B4+B5)/2
A26: Test_Avg_Time      B26: =(B7+B8)/2
A27: Arch_Avg_Time      B27: =(B10+B11)/2

A28: Dev_Service_Rate   B28: =(1/B25)*B3*B13*(1-B16)*(1+B17)
A29: Test_Service_Rate  B29: =(1/B26)*B6*B13*(1-B16)*(1+B17)
A30: Arch_Service_Rate  B30: =(1/B27)*B9*B13*(1-B16)*(1+B17)

A31: Total_Service_Rate B31: =(B28+B29+B30)*B2
A32: Total_Resources    B32: =(B3+B6+B9)*B2
```

#### C. Flow Metrics (A40:B50)
```
A40: Effective_Demand   B40: =B12*(1+B14*B15*(1-B17*0.2))
A41: Base_Utilization   B41: =IF(B31>0,B40/B31,1)
A42: Current_Util_Pct   B42: =B41*100

A43: Lead_Time          B43: =2+3/(1-MIN(B41,0.999)+0.001)
A44: Max_Throughput     B44: =B31*(1-B14*(1-B17*0.2))
A45: Throughput         B45: =MIN(B40,B44*MAX(0,1-B41))
A46: WIP                B46: =B40*B43
A47: Variability        B47: =IF(B32>0,MAX(0,B43*(B41/MAX(1,B41))*(B46/B32)*0.1),0)
A48: Cost_Impact        B48: =B43*10
```

### Step 4: Build the DataTables Sheet

#### A. Utilization Scenarios (A1:E51)

**Headers (Row 1):**
```
A1: Util%
B1: Lead_Time  
C1: Throughput
D1: Variability
E1: Cost
```

**Data Rows (A2:E51):**
```
A2: 50
A3: 51
A4: 52
...
A51: 100
```

**Formulas for each row (starting at row 2):**
```
B2: =2+3/(1-MIN(A2/100,0.999)+0.001)
C2: =MIN(Calculations!$B$40,Calculations!$B$44*MAX(0,1-A2/100))
D2: =IF(Calculations!$B$32>0,MAX(0,B2*(A2/100)*(Calculations!$B$46/Calculations!$B$32)*0.1),0)
E2: =B2*10
```

**Copy formulas down:** Select B2:E2, copy, select B3:E51, paste

### Step 5: Create the Flow Chart

#### A. Insert Chart on Dashboard (A22:M40)

1. **Select data:** DataTables!A1:E51
2. **Insert → Combo Chart**
3. **Chart setup:**
   - Series 1 (Lead_Time): Line, Primary axis, Red
   - Series 2 (Throughput): Line, Secondary axis, Blue  
   - Series 3 (Variability): Scatter, Primary axis, Orange

#### B. Format Chart
1. **Chart Title:** "Flow Metrics vs Utilization"
2. **Primary Y-axis:** "Lead Time (Days) / Variability"
3. **Secondary Y-axis:** "Throughput (Features/Sprint)"
4. **X-axis:** "Resource Utilization (%)"

#### C. Add Threshold Lines
1. **Right-click chart → Select Data**
2. **Add Series:**
   - Name: "90% Threshold"
   - X values: {90,90}
   - Y values: {0,50}
   - Format: Red dashed line
3. **Repeat for 95% threshold**

### Step 6: Add Goal Seeking (A42:D50)

#### A. Goal Seek Section Headers
```
A42: Goal Seeking Optimization
A43: Target Utilization (%)
A44: Maximize Throughput  
A45: Minimize Variability
```

#### B. Input Controls
```
B43: 80     (Target utilization input)
C43: [Button: "Optimize Utilization"]
C44: [Button: "Optimize Throughput"]  
C45: [Button: "Optimize Variability"]
```

#### C. Button Macros (Developer → Insert → Button)

**Optimize Utilization Button:**
```vb
Sub OptimizeUtilization()
    Dim targetUtil As Double
    targetUtil = Range("Dashboard!B43").Value
    
    ' Use Goal Seek
    Range("Calculations!B42").GoalSeek _
        Goal:=targetUtil, _
        ChangingCell:=Range("Dashboard!B14")
End Sub
```

**Optimize Throughput Button:**
```vb
Sub OptimizeThroughput()
    ' Use Solver to maximize throughput
    SolverReset
    SolverOk SetCell:="Calculations!B45", _
             MaxMinVal:=1, _
             ByChange:="Dashboard!B14"
    SolverAdd CellRef:="Dashboard!B14", _
             Relation:=1, _
             FormulaText:="5"
    SolverAdd CellRef:="Dashboard!B14", _
             Relation:=3, _
             FormulaText:="20"
    SolverSolve UserFinish:=True
End Sub
```

### Step 7: Add Conditional Formatting

#### A. Parameter Values (B4:B19)
1. **Select B4:B19**
2. **Home → Conditional Formatting → New Rule**
3. **Use Formula:** `=B4<C4` (Red for below minimum)
4. **Add another rule:** `=B4>D4` (Red for above maximum)
5. **Add another rule:** `=AND(B4>=C4*0.8,B4<=D4*0.8)` (Green for optimal)

#### B. Metrics Display (G4:G10)
1. **Select G4** (Utilization)
2. **Conditional Formatting:**
   - Green: `=G4<0.8`
   - Yellow: `=AND(G4>=0.8,G4<0.9)`
   - Red: `=G4>=0.9`

### Step 8: Create Utilization Gauge

#### A. Insert Gauge Chart (F22:H30)
1. **Create data for gauge:**
   ```
   F23: 0    G23: Current
   F24: 50   G24: =Calculations!B42
   F25: 80   G25: Warning  
   F26: 90   G26: Critical
   F27: 100  G27: Maximum
   ```

2. **Insert Doughnut Chart** from F23:G27
3. **Format as speedometer** with conditional colors

### Step 9: Final Touches

#### A. Protect Sheets
1. **Dashboard:** Protect, allow input in B4:B19 only
2. **Calculations:** Hide and protect completely
3. **DataTables:** Hide and protect completely

#### B. Create Named Ranges
1. **Formulas → Name Manager**
2. **Create names:**
   - `Parameters` = Dashboard!B4:B19
   - `Metrics` = Dashboard!G4:G10
   - `UtilData` = DataTables!A1:E51

#### C. Add Instructions
1. **Insert Text Box** on Dashboard
2. **Add usage instructions:**
   ```
   Instructions:
   1. Modify parameters in yellow cells
   2. Observe real-time metric updates
   3. Use goal seeking buttons for optimization
   4. Review chart for utilization impacts
   ```

### Step 10: Testing and Validation

#### A. Test Parameter Changes
1. **Change team sizes** → Verify metrics update
2. **Modify service times** → Check calculation accuracy
3. **Test extreme values** → Ensure no errors

#### B. Validate Formulas
1. **Compare with Python simulation** results
2. **Check edge cases** (0% and 100% utilization)
3. **Verify goal seeking** functions work correctly

#### C. Performance Optimization
1. **Set calculation to Manual** during data entry
2. **Use efficient formulas** (avoid volatile functions)
3. **Minimize chart data range** if needed

### Final File Structure:
```
AgileFlowMetrics.xlsx
├── Dashboard (Visible, Interactive)
├── Calculations (Hidden, Formulas)  
└── DataTables (Hidden, Chart Data)
```

This Excel version provides the same insights as the Python simulation with an intuitive spreadsheet interface that's familiar to most business users.