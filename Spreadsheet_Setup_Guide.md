# Agile Flow Metrics Simulation - Spreadsheet Setup Guide

## 📁 Files Created

I've created a complete Excel simulation in CSV format that you can import into any spreadsheet application:

- **`Dashboard.csv`** - Main interface with parameters and metrics
- **`Calculations.csv`** - Hidden calculation engine with all formulas  
- **`DataTables.csv`** - Chart data for utilization scenarios (50-100%)
- **`VBA_Macros.txt`** - Goal seeking and optimization macros
- **`Spreadsheet_Setup_Guide.md`** - This setup guide

## 🚀 Quick Start (5 minutes)

### Option 1: Microsoft Excel
1. **Open Excel** → Create new workbook
2. **Import CSVs:**
   - File → Open → Select `Dashboard.csv` → Import as first sheet
   - Right-click sheet tab → Rename to "Dashboard"
   - Insert new sheet → Import `Calculations.csv` → Rename to "Calculations"
   - Insert new sheet → Import `DataTables.csv` → Rename to "DataTables"
3. **Fix formulas:** Find/Replace `=Calculations.` with `=Calculations!`
4. **Ready to use!** Modify parameters in Dashboard column B

### Option 2: Google Sheets
1. **Open Google Sheets** → Create new spreadsheet
2. **Import sheets:**
   - File → Import → Upload `Dashboard.csv` → "Insert new sheets"
   - Repeat for `Calculations.csv` and `DataTables.csv`
3. **Fix cross-sheet references:** Replace `=Calculations.` with `=Calculations!`
4. **Enable iterative calculation:** File → Settings → Calculation → Enable iterative calculation

### Option 3: LibreOffice Calc
1. **Open LibreOffice Calc**
2. **Import CSVs** as separate sheets
3. **Fix formula references** using Find & Replace
4. **Tools → Options → Calc → Iterative References** → Enable

## 📊 Detailed Excel Setup

### Step 1: Import and Structure

**Import Each CSV File:**
```
1. File → Open → Select Dashboard.csv
2. Text Import Wizard:
   - Delimited
   - Comma separated
   - Text qualifier: None
3. Click Finish
```

**Create Multi-Sheet Workbook:**
```
1. Right-click sheet tab → "Move or Copy"
2. Select "Dashboard" → Rename
3. Add new sheet → Import Calculations.csv → Rename to "Calculations"
4. Add new sheet → Import DataTables.csv → Rename to "DataTables"
```

### Step 2: Fix Cross-Sheet References

**Find and Replace (Ctrl+H):**
```
Find: =Calculations.
Replace: =Calculations!

Find: =Dashboard.
Replace: =Dashboard!
```

**Test Formula Links:**
- Dashboard G4 should show calculated utilization
- Modify Dashboard B14 (Demand) and verify metrics update

### Step 3: Add Data Validation

**For Parameter Cells (Dashboard B4:B19):**
```
1. Select B4:B19
2. Data → Data Validation
3. Settings:
   - Allow: Decimal
   - Data: Between
   - Minimum: =C4 (reference to min column)
   - Maximum: =D4 (reference to max column)
4. Input Message: "Enter value between minimum and maximum"
5. Error Alert: "Value must be within specified range"
```

### Step 4: Add Conditional Formatting

**Utilization Warning Colors (Dashboard G4):**
```
1. Select G4
2. Home → Conditional Formatting → New Rule
3. Use Formula: =G4<80 → Green fill
4. Add Rule: =AND(G4>=80,G4<90) → Yellow fill  
5. Add Rule: =G4>=90 → Red fill
```

**Parameter Range Validation (Dashboard B4:B19):**
```
1. Select B4:B19
2. Conditional Formatting → New Rule
3. Formula: =OR(B4<C4,B4>D4) → Red fill
```

### Step 5: Create the Flow Chart

**Insert Combination Chart:**
```
1. Select DataTables A1:E51
2. Insert → Charts → Combo Chart
3. Series Configuration:
   - Lead_Time: Line chart, Primary axis, Red
   - Throughput: Line chart, Secondary axis, Blue
   - Variability: Scatter, Primary axis, Orange
4. Chart Title: "Flow Metrics vs Resource Utilization"
5. Move chart to Dashboard F22:M40
```

**Format Chart:**
```
- Primary Y-axis: "Lead Time (Days) / Variability"
- Secondary Y-axis: "Throughput (Features/Sprint)"  
- X-axis: "Resource Utilization (%)"
- Add vertical lines at 90% and 95% utilization
```

### Step 6: Add VBA Macros (Excel Only)

**Enable Developer Tab:**
```
File → Options → Customize Ribbon → Check "Developer"
```

**Add Macros:**
```
1. Developer → Visual Basic (Alt+F11)
2. Insert → Module
3. Copy/paste code from VBA_Macros.txt
4. Save and close VBA editor
```

**Create Buttons:**
```
1. Developer → Insert → Button (Form Control)
2. Draw button in Dashboard C43
3. Assign macro: OptimizeUtilization
4. Right-click → Edit Text: "Optimize Utilization"
5. Repeat for Throughput and Variability buttons
```

### Step 7: Final Configuration

**Hide Supporting Sheets:**
```
Right-click "Calculations" → Hide
Right-click "DataTables" → Hide
```

**Protect Dashboard:**
```
1. Review → Protect Sheet
2. Allow: Select unlocked cells
3. Unlock only B4:B19 and B43 before protecting
```

**Set Calculation Mode:**
```
Formulas → Calculation Options → Automatic
```

## 🎯 Usage Instructions

### Basic Operation
1. **Modify parameters** in Dashboard column B (rows 4-19)
2. **Observe real-time updates** in metrics (column G)
3. **Review chart** to see utilization impact curves
4. **Use goal seeking** buttons for optimization

### Key Parameters to Experiment With

**Team Scaling:**
- **Teams** (B4): Scale from 1 to 10+ teams
- **Team composition**: Adjust developer/tester/architect counts

**Service Time Modeling:**
- **Min/Max times**: Model task uncertainty and skill variations
- **Proficiency**: Impact of team experience (50-100%)

**Quality Factors:**
- **Defect Rate**: How bugs affect throughput (0-50%)
- **Rework Factor**: Time spent fixing issues (0-1.0)

**Modern Factors:**
- **Dependencies**: Cross-team coordination overhead (0-50%)
- **AI Impact**: Productivity boost from AI tools (0-50%)

### Optimization Goals

**Target Utilization (80%):**
- Optimal efficiency without overload
- Use "Optimize Utilization" button

**Maximize Throughput:**
- Find highest sustainable feature delivery
- Use "Optimize Throughput" button  

**Minimize Variability:**
- Most predictable delivery schedules
- Use "Optimize Variability" button

## 📈 Reading the Results

### Key Metrics Interpretation

**Current Utilization:**
- **<80%**: Underutilized capacity, room for more work
- **80-90%**: Optimal range, high efficiency with manageable risk
- **>90%**: Overloaded, quality and schedule at risk

**Lead Time:**
- **<5 days**: Excellent flow, fast delivery
- **5-10 days**: Good flow, reasonable delivery time
- **>10 days**: Poor flow, bottlenecks present

**Throughput:**
- **Features per sprint** that team can sustain
- Compare to demand to identify capacity gaps

**Schedule Variability:**
- **<2**: Highly predictable delivery
- **2-5**: Moderate predictability  
- **>5**: High uncertainty, difficult to plan

### Chart Analysis

**Flow Curves Show:**
- **Lead time explosion** around 90-95% utilization
- **Throughput plateau** as utilization increases
- **Variability growth** under high utilization

**Sweet Spot:** Usually 75-85% utilization for optimal balance

## 🔧 Troubleshooting

### Common Issues

**Formulas Not Calculating:**
- Ensure Automatic calculation is enabled
- Check cross-sheet references use `!` not `.`
- Verify sheet names match exactly

**Chart Not Updating:**
- Right-click chart → Refresh Data
- Check DataTables formulas reference Calculations sheet correctly

**Goal Seeking Not Working:**
- Ensure target cell contains a number, not text
- Check changing cell is unlocked
- Verify formula chain is complete

**VBA Errors:**
- Enable macros when opening file
- For Solver functions, ensure Solver add-in is enabled

### Performance Optimization

**For Large Models:**
- Set calculation to Manual during parameter entry
- Use Ctrl+Alt+F9 to force full recalculation
- Limit DataTables range if chart is slow

## 🎉 You're Ready!

Your Agile Flow Metrics Simulation is now ready to use! You have:

✅ **Interactive parameter controls** with validation  
✅ **Real-time metric calculations** using queuing theory  
✅ **Professional flow visualization** with utilization curves  
✅ **Goal seeking optimization** for capacity planning  
✅ **Scenario analysis capability** for team scaling decisions  

**Start exploring:** Try increasing team size, adjusting AI impact, or finding optimal utilization levels for your organization!