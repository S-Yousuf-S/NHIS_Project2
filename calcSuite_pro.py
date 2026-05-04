# ============================================================================= #
# PROGRAM : CalcSuite Pro (Version 7.6)                                         # 
# AUTHOR  : Yousuf S. R. Sakkaf                                                 #
# FILE    : calcSuite_pro.py                                                    #
# STATUS  : Stable / Final Release (2026-04-24)                                 #
# LICENSE : MIT (Open Source / Educational)                                     #
# REPO    : github.com/S-Yousuf-S/NHIS_Project2                                 #
# REQUIRES: customtkinter, pillow, cmath                                        #
# ============================================================================= #

"""
DESCRIPTION:
A professional multi-tool mathematical workstation built with CustomTkinter.
An evolution from a basic calculator into a high-density "Digi-ToolKit."

*Format Enforcement: Enforces strict Standard Form (RHS = pure number) 
for Quadratic and Multi-Bracket solving to guarantee engine stability.

-------------------------------------------------------------------------------
NEW IN v7.6 — ALGEBRA STABILITY & UX UPDATE
-------------------------------------------------------------------------------
✔ DISPATCHER: Hierarchical routing fix ensures perfect equation handling.
✔ POLYNOMIALS: Upgraded FOIL/Multi-bracket engine using robust dictionary mapping.
✔ DYNAMIC RHS: Smart right-hand-side subtraction for higher-degree expansions.
✔ EPSILON TOLERANCE: Implemented 1e-12 floating-point guards to prevent binary math errors.
✔ UX TIMING: Optimized state-transition delays to the 450ms "Goldilocks" zone.
✔ CLEAN CODE: Resolved regex syntax warnings and eliminated legacy zombie code.

-------------------------------------------------------------------------------
NEW IN v7.5 — THE "PRO" OVERHAUL
-------------------------------------------------------------------------------
✔ BRANDING: Finalized "CalcSuite Pro" identity with "Digi-ToolKit" interface.
✔ SMART REDIRECT: Scientific tab auto-detects variables; carries input to Algebra.
✔ UI TIMING: Implemented 800ms 'Human-Speed' delays for state transitions.
✔ TYPOGRAPHY: Integrated Bahnschrift (Tabs) and Consolas (Results) for precision.
✔ ROBUSTNESS: Modifier-key guards (Shift/Alt/Ctrl) to protect AST evaluation.
✔ PERSISTENCE: Multi-line history capture for Algebra and Quadratic roots.

═══════════════════════════════════════════════════════════════════════════════
TAB 1 — SCIENTIFIC CALCULATOR (The Engine)
═══════════════════════════════════════════════════════════════════════════════
✔ CORE: Basic arithmetic (+, -, ×, /) with implicit multiplication (e.g. 2π).
✔ MATH: sin, cos, tan, log, ln, √, ^, Factorials (!).
✔ ADVANCED: nPr, nCr, Fibonacci (Single value & full series pop-up).
✔ BASES: Real-time BIN / DEC / HEX conversion.
✔ MODES: Degree / Radian toggle with persistent UI status.
✔ SAFETY: Secured AST-based evaluation (zero use of unsafe eval()).
✔ UI: 24-hour auto-pruning history, hover-animations, and theme toggling.

═══════════════════════════════════════════════════════════════════════════════
TAB 2 — SOLVERS (The Specialist)
═══════════════════════════════════════════════════════════════════════════════
✔ QUADRATIC: Solves ax² + bx + c = 0.
    - Full Complex Number support via 'cmath' library.
    - Handles D>0, D=0, and D<0 (Complex) cases with detailed legends.
✔ LINEAR 2x2: Solves systems (ax+by=c, dx+ey=f) using Cramer's Rule.
    - Detects Infinite Solutions and Inconsistent (Parallel) systems.
✔ UI: Red-coded 'Clear' safety buttons and theme-aware coordinate legends.

═══════════════════════════════════════════════════════════════════════════════
TAB 3 — SMART ALGEBRA (The Master Logic)
═══════════════════════════════════════════════════════════════════════════════    
✔ INPUT: Natural language expression box—type equations exactly as written.
✔ DISPATCHER: Auto-detects and routes to 7 distinct mathematical states:
    - TYPE 1 — Numeric Bypass: Evaluates pure arithmetic without variables (e.g., 5+5).
    - TYPE 2 — Simplification: Collects and stacks like-terms for expressions (no '=').
    - TYPE 3 — Linear (1 Var): Solves standard equations with dynamic RHS handling.
    - TYPE 4 — Linear (2x2): Cramer's Rule execution via comma-separated input.
    - TYPE 5 — Quadratic: Root extraction for squared equations (real & complex).
    - TYPE 6 — Bracket Expansion: Iterative polynomial multiplication for (..)(..)(..).
    - TYPE 7 — Polynomial Guard: Traps degree > 2 and cross-terms, failing gracefully.

═══════════════════════════════════════════════════════════════════════════════
TAB 4 — HEALTH / BMI (The Analytical)
═══════════════════════════════════════════════════════════════════════════════
✔ DUAL SYSTEMS: Toggle between Metric (kg/cm) and Imperial (lb/ft/in).
✔ FEEDBACK: Color-coded categories (Underweight to Obese) with ideal ranges.
✔ SAFETY: Age-validation (under-18 redirects to percentile charts).
✔ CONTEXT: Gender-aware biological body-fat distribution notes.

═══════════════════════════════════════════════════════════════════════════════
TAB 5 — UNIT CONVERTER (The Utility)
═══════════════════════════════════════════════════════════════════════════════
✔ SCALE: Length, Weight, Temperature, Speed, and Area.
✔ UX: Instant live-conversion, "Swap ⇄" functionality, and 24hr history logging.
✔ DESIGN: Unified grid layout for pixel-perfect alignment.

-------------------------------------------------------------------------------
DEVELOPER NOTES & ARCHITECTURE:
-------------------------------------------------------------------------------
- Security       : Strict AST (Abstract Syntax Tree) parsing is used for the 
                   Scientific tab to prevent code-injection risks from eval().
- Engine Scope   : The Algebra tab relies on Pattern Extraction and Polynomial 
                   Dictionaries, establishing a deliberate architectural boundary 
                   against full CAS (Computer Algebra System) symbolic distribution.
- Precision Guard: "Epsilon" checks (abs(val) < 1e-12) are utilized across 
                   Solvers to neutralize floating-point binary rounding errors.                   
- Regex Standards: All regular expressions strictly utilize raw strings (r'...') 
                   to prevent 'invalid escape sequence' SyntaxWarnings in Python 3.12+.
- Fibonacci Logic: Use FIBS(n) for a full series, FIB(n) for the nth term.
- Orientation    : Optimized launch geometry (+100+50) for standard HD displays.
- Typography     : Bahnschrift utilized for high-density navigation without slicing.
-------------------------------------------------------------------------------

"""
# =========================================================

# ── Standard Library ──────────────────────────────────────
import customtkinter as ctk                 # The core UI framework used to build the modern, theme-aware (dark/light) interface.
import math                                 # Handles standard mathematical operations (sin, cos, factorials, square roots) in the Scientific tab.
import cmath                                # Handles complex number mathematics (specifically used in the Quadratic Solver for negative discriminants).
import re                                   # Regular expressions; heavily used in the Algebra engine for parsing variables, tokens, and polynomial degrees.
from collections import defaultdict         # Used in the Algebra simplifier to elegantly collect and stack like-terms without throwing KeyErrors.
from datetime import datetime, timedelta    # Used by the HistoryManager to timestamp calculations and automatically purge records older than 24 hours.
from tkinter import messagebox              # Used to trigger standard system popup dialogues (e.g., the "Exit the calculator?" prompt on hitting Escape).
import ast                                  # Abstract Syntax Tree; the backbone of the safe, custom evaluation engine that securely calculates math without using eval().

# ── Global appearance ────────────────────────────────────
ctk.set_appearance_mode("dark")


# ═════════════════════════════════════════════════════════
#   HISTORY MANAGER  (shared across all tabs)
# ═════════════════════════════════════════════════════════
class HistoryManager:
    """Stores calculator operations for the past 24 hours."""

    def __init__(self):
        self.records = []   #list of (timestamp, expression, result)

    def add(self, expr, result):
        """Add a new record and prune anything older than 24 h."""
        self.records.append((datetime.now(), expr, result))
        self._cleanup()

    def _cleanup(self):
        """Remove entries older than 24 hours."""
        cutoff = datetime.now() - timedelta(hours=24)
        self.records = [r for r in self.records if r[0] > cutoff]

    def get(self):
        """Return formatted strings for display."""
        return [f"{e} = {r}" for _, e, r in self.records]

    #   Adding new clear all feature
    def clear_all(self):
        """Manually wipe the session history."""
        self.records = []
# ═════════════════════════════════════════════════════════
#   UNIT CONVERSION DATA
#   All conversion factors are stored as multipliers TO a
#   common base unit, so any pair can be converted via:
#      value_in_base = value * from_factor
#      result        = value_in_base / to_factor
# ═════════════════════════════════════════════════════════
UNIT_DATA = {

    #   Base unit: metre
    "Length": {
        "Millimetre (mm)":  0.001,
        "Centimetre (cm)":  0.01,
        "Metre (m)":        1.0,
        "Kilometre (km)":   1000.0,
        "Inch (in)":        0.0254,
        "Foot (ft)":        0.3048,
        "Yard (yd)":        0.9144,
        "Mile (mi)":        1609.344,
        "Nautical Mile":    1852.0,
    },

    #   Base unit: kilogram
    "Weight": {
        "Milligram (mg)":   0.000001,
        "Gram (g)":         0.001,
        "Kilogram (kg)":    1.0,
        "Tonne (t)":        1000.0,
        "Ounce (oz)":       0.028349523,
        "Pound (lb)":       0.45359237,
        "Stone (st)":       6.35029318,
    },

    #   Temperature is a special case — NOT a simple multiplier.
    #   We handle it separately with dedicated formulas.
    "Temperature": {
        "Celsius (°C)":    "celsius",
        "Fahrenheit (°F)": "fahrenheit",
        "Kelvin (K)":      "kelvin",
    },

    #   Base unit: metre per second
    "Speed": {
        "m/s":          1.0,
        "km/h":         1/3.6,
        "mph":          0.44704,
        "Knot":         0.514444,
        "ft/s":         0.3048,
    },

    #   Base unit: square metre
    "Area": {
        "mm²":              1e-6,
        "cm²":              0.0001,
        "m²":               1.0,
        "km²":              1e6,
        "Hectare (ha)":     10000.0,
        "Acre":             4046.856,
        "sq inch (in²)":    0.00064516,
        "sq foot (ft²)":    0.092903,
        "sq yard (yd²)":    0.836127,
        "sq mile (mi²)":    2589988.11,
    },
}


def convert_temperature(value, from_unit, to_unit):
    """
    Convert between Celsius, Fahrenheit and Kelvin.
    Strategy: first convert everything to Celsius, then to the target.
    """
    #   Convert FROM unit to Celsius
    if from_unit == "celsius":
        c = value
    elif from_unit == "fahrenheit":
        c = (value - 32) * 5 / 9
    elif from_unit == "kelvin":
        c = value - 273.15
    else:
        raise ValueError("Unknown temperature unit")

    #   Convert FROM Celsius to target unit
    if to_unit == "celsius":
        return c
    elif to_unit == "fahrenheit":
        return c * 9 / 5 + 32
    elif to_unit == "kelvin":
        return c + 273.15
    else:
        raise ValueError("Unknown temperature unit")


def convert_units(value, category, from_label, to_label):
    """
    Convert a numeric value between two units in the given category.
    Dispatches to convert_temperature() for temperature, otherwise
    uses the ratio-based method for all other categories.
    """
    units = UNIT_DATA[category]
    from_factor = units[from_label]
    to_factor   = units[to_label]

    if category == "Temperature":
        #   Factors are string keys, not multipliers
        return convert_temperature(value, from_factor, to_factor)
    else:
        #   Universal: value × from_factor gives base unit, ÷ to_factor gives result
        base  = value * from_factor
        return base / to_factor


# ═════════════════════════════════════════════════════════
#   HELPER — Consistent styled label
# ═════════════════════════════════════════════════════════
def make_label(parent, text, font_size=12, bold=False, italic=False, color=None):
    """Convenience wrapper for CTkLabel with consistent styling."""
    f_weight = "bold" if bold else "normal"
    f_slant = "italic" if italic else "roman" # 'roman' is the default upright text
    
    #   Build the CustomTkinter font
    custom_font = ctk.CTkFont(family="Segoe UI", size=font_size, weight=f_weight, slant=f_slant)
    
    #   Create and return the label
    lbl = ctk.CTkLabel(parent, text=text, font=custom_font)
    if color:
        lbl.configure(text_color=color)
    return lbl


# ═════════════════════════════════════════════════════════
#   MAIN APPLICATION
# ═════════════════════════════════════════════════════════
class Calculator(ctk.CTk):
    """
    The root window.
    Contains a CTkTabview that hosts all four tool tabs.
    Each tab is built by a dedicated _build_*() method.
    """
    # --- DEFINING APPLICATION NAME ---
    APP_NAME = "CalcSuite Pro v7.6"
    # ---------------------------------

    def __init__(self):
        super().__init__()

        self.title("CalcSuite Pro")
        #   Professional Centering Logic
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        width, height = 400, 750
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) - 50   #Offset slightly up
        
        #   Format: WIDTH x HEIGHT + X_OFFSET + Y_OFFSET
        self.geometry(f"{width}x{height}+{x}+{y}")

        #   Lowering the Y_OFFSET (e.g., to 50) moves the window UP the screen.      
        self.minsize(380, 650)
        self.maxsize(450,800)

        # ── Shared state ──────────────────────────────────
        self.expression    = ""
        self.last_result   = ""
        self.last_op       = None
        self.last_expr_tail= ""
        self.reset_next    = False
        self.history       = HistoryManager()   # shared by all tabs
        self.fib_window    = None
        self.mode          = "DEG"              # Degree / Radian mode
        self.history_win   = None               # reuse history popup

        # ── Build UI ──────────────────────────────────────
        self._build_toolbar()                   # top strip: title + history
        self._build_tabs()                      # CTkTabview with four tabs
        self.bind("<Key>", self.handle_keys)

        
    # ─────────────────────────────────────────────────────
    #   TOP TOOLBAR
    # ─────────────────────────────────────────────────────
    def _build_toolbar(self):
        """Top bar: app title on the left, history + theme on the right."""
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=10, pady=(8, 0))

        ctk.CTkLabel(
            bar, text="💻 Digi-ToolKit",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left")

        ctk.CTkButton(
            bar, text="🌙/☀️", width=55, height=28,
            command=self.toggle_theme
        ).pack(side="right", padx=4)

        ctk.CTkButton(
            bar, text="📜", width=55, height=28,
            command=self.show_history
        ).pack(side="right")
        
        #   NEW: "Invisible" About Button
        self.about_btn = ctk.CTkButton(
            bar, 
            text="ℹ",                                   # Standard info icon
            width=35, 
            height=28,
            fg_color="transparent",                     # Removes the blue box
            hover_color=("gray85","gray25"),            # Optional: or set to a very subtle grey
            text_color=("gray20", "gray90"),            # Theme-aware icon color
            command=self.show_about
        )
        self.about_btn.pack(side="right", padx=2)
    
    # ─────────────────────────────────────────────────────
    #   TAB CONTAINER
    # ─────────────────────────────────────────────────────
    def _build_tabs(self):
        """Create the CTkTabview and call each tab's builder."""
        self.tabs = ctk.CTkTabview(self, anchor="nw")
        self.tabs.pack(fill="both", expand=True, padx=6, pady=4)
        
        #   Add all five tabs
        self.tabs.add("🔢 Scientific ")
        self.tabs.add("📐 Solvers ") #Formerly Equations
        self.tabs.add("🔣 Algebra ")
        self.tabs.add("⚖️ BMI ")
        self.tabs.add("🔄 Converter ")

        #   Target the internal segmented button
        #   This is the 'secret' way to bold CTkTabview headers
        self.tabs._segmented_button.configure(
            font=ctk.CTkFont(family="Bahnschrift", size=12, weight="bold")
        )

        #   Build the content of each tab
        self._build_calculator_tab(self.tabs.tab("🔢 Scientific "))
        self._build_equations_tab(self.tabs.tab("📐 Solvers "))
        self._build_algebra_tab(self.tabs.tab("🔣 Algebra "))
        self._build_bmi_tab(self.tabs.tab("⚖️ BMI "))
        self._build_converter_tab(self.tabs.tab("🔄 Converter "))


    # ═════════════════════════════════════════════════════
    #   TAB 1 — SCIENTIFIC CALCULATOR
    # ═════════════════════════════════════════════════════
    def _build_calculator_tab(self, parent):
        """
        Builds the full scientific calculator inside the given parent frame.
        Identical layout to v5.5 — display, mode/theme controls, button grid.
        """

        # ── Main display ──────────────────────────────────
        self.display = ctk.CTkEntry(
            parent,
            font=("Consolas", 26, "bold"), 
            justify="right",
            fg_color="#ccffcc",
            text_color="black",
            height=65, 
            state="readonly"
        )
      
        self.display.pack(fill="x", padx=6, pady=(8, 4))
        
        # ── Mode / Theme control bar ──────────────────────
        ctrl = ctk.CTkFrame(parent, fg_color="transparent")
        ctrl.pack(fill="x", padx=6, pady=(5,5))
        
        self.mode_label = ctk.CTkLabel(ctrl, text="DEG",
                                        font=("Arial", 10, "bold"))
        self.mode_label.pack(side="left")

        ctk.CTkButton(ctrl, text="DEG/RAD", width=72, height=26,
                      command=self.toggle_mode).pack(side="left", padx=4)

        # ── Button grid ───────────────────────────────────
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="both", expand=True, padx=4,pady=(8,4))

        #   Four equal columns
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1, uniform="c")


        #----------------Buttons Layout--------------------#
        layout = [
            #   row 0 — Constants + Conversions
            [("e","e"),       ("BIN","bin("), ("DEC","dec("), ("HEX","hex(")],
            #   row 1 — Trig
            [("π","pi"),      ("sin","sin("), ("cos","cos("), ("tan","tan(")],
            #   row 2 — Permutations/Combinations + fibonacci
            [("!","!"),       ("nPr","npr("), ("nCr","ncr("), ("FIBS","fibs(")],
            #   row 3 — Roots + Logs
            [("√","sqrt("),   ("log","log("), ("ln","ln("),   ("FIB","fib(")],
            #   row 4 — Power + Clear
            [("^","**"),      ("C",None),     ("CE",None),    ("⌫",None)],
            #   row 5 — Percent + Brackets + Divide
            [("%","%"),       ("(","("),      (")",")"),      ("/","/")],
            #   rows 6-9 — Number pad + Basic Operators + Equals
            [("7","7"),       ("8","8"),      ("9","9"),      ("×","×")],
            [("4","4"),       ("5","5"),      ("6","6"),      ("-","-")],
            [("1","1"),       ("2","2"),      ("3","3"),      ("+","+")],
            [(",",","),       ("0","0"),      (".","." ),     ("=",None)],
        ]

        for row_idx, row in enumerate(layout):
            btn_frame.grid_rowconfigure(row_idx, weight=1)
            for col_idx, (label, val) in enumerate(row):
                if label == "C":
                    self._make_calc_btn(btn_frame, label, row_idx, col_idx,
                                        cmd=self.clear)
                elif label == "CE":
                    self._make_calc_btn(btn_frame, label, row_idx, col_idx,
                                        cmd=self.clear_entry)
                elif label == "⌫":
                    self._make_calc_btn(btn_frame, label, row_idx, col_idx,
                                        cmd=self.backspace)
                elif label == "=":
                    self._make_calc_btn(btn_frame, label, row_idx, col_idx,
                                        cmd=self.calculate)
                else:
                    self._make_calc_btn(btn_frame, label, row_idx, col_idx,
                                        val=val)

    def _make_calc_btn(self, parent, text, row, col, val=None, cmd=None):
        """
        Create one calculator button with colour coding, hover animation,
        and click flash effect. All the same logic as v5.5.
        """
        # ── Colour assignment by function ────────────────
       
        NUM  = "#1e1e1e"    # Deep Charcoal - NUMPAD
        OP   = "#3b4cca"    # blue          — operators + equals
        SCI  = "#2a9d8f"    # teal          — scientific functions
        CTRL = "#4f4e69"    # slate         — control keys

        if text in ["+", "-", "×", "/", "="]:
            color = OP
        elif text in ["sin","cos","tan","log","ln",
                      "BIN","HEX","DEC","nPr","nCr","FIB","FIBS"]:
            color = SCI
        elif text in ["C","CE","⌫","!","e","π","√","^"]:
            color = CTRL
        else:
            color = NUM

        # ── Click handler with flash animation ────────────
        def on_click():
            btn.configure(fg_color="#6c4f8c")                       # brief purple flash
            self.after(200, lambda: btn.configure(fg_color=color))
            if cmd:
                cmd()
            else:
                self.insert(text, val)

        btn = ctk.CTkButton(
            parent, text=text,
            font=("Segoe UI", 13, "bold"),
            height=38,
            fg_color=color, text_color="white",
            corner_radius=8,
            command=on_click,
        )

        # ── Hover effect — colour depends on theme ────────
        app_mode  = ctk.get_appearance_mode().lower()
        normal_bg = color
        if app_mode == "light":
            hover_bg, normal_text, hover_text = "#111111", "black", "white"
        else:
            hover_bg, normal_text, hover_text = "#bbbbbb", "white", "black"

        btn.configure(text_color=normal_text)
        btn.bind("<Enter>", lambda e: btn.configure(fg_color=hover_bg,
                                                    text_color=hover_text))
        btn.bind("<Leave>", lambda e: btn.configure(fg_color=normal_bg,
                                                    text_color=normal_text))

        btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

    # ═════════════════════════════════════════════════════
    #   TAB 2 — EQUATION SOLVER
    # ═════════════════════════════════════════════════════
    def _build_equations_tab(self, parent):
        """
        Two sub-sections inside a scrollable frame:
          A) Quadratic Equations Solver  — ax² + bx + c = 0
          B) 2×2 Linear Algebra Solver — solve for x and y
        """
        #   Scrollable container so content fits on any screen
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        # ════════ A) QUADRATIC ════════════════════════════
        sec_a = ctk.CTkFrame(scroll, corner_radius=10)
        sec_a.pack(fill="x", pady=(0, 10))

        make_label(sec_a, "📐  Quadratic Equation Solver",
                   font_size=14, bold=True).pack(anchor="w", padx=10, pady=(8,2))

        #   Create a shared row frame to hold both labels side by side
        label_row = ctk.CTkFrame(sec_a, fg_color="transparent")
        label_row.pack(fill="x", padx=10, pady=(0, 2))

        #   Both labels use the SAME theme-aware color — fixes light mode invisibility
        #   Left label
        make_label(label_row, "  ax²  +  bx  +  c  =  0",
                    font_size=11, color="gray", bold=True, italic=True).pack(side="left")

        #   Right label — pushed to the right edge of the same row
        make_label(label_row, "Discriminant D = b² - 4ac", 
                    font_size=11, color="gray", bold=True, italic=True).pack(side="right")
        
        #   Create a frame to hold the two legend lines together
        legend_frame = ctk.CTkFrame(sec_a, fg_color="transparent")
        legend_frame.pack(anchor="w", padx=10, pady=(0, 2))

        #   Each line is its own label — guarantees perfect left alignment
        ctk.CTkLabel(legend_frame, text=" D>0 → 2 real roots  ||  D=0 → 1 repeated root  |",
                    font=("Segoe UI", 10), text_color=("black","white")).pack(anchor="w",side ="left")
        ctk.CTkLabel(legend_frame, text="|  D<0 → 2 complex roots",
                    font=("Segoe UI", 10), text_color=("black","white")).pack(anchor="w",side="right")

        #   Coefficient input row
        coeff_row = ctk.CTkFrame(sec_a, fg_color="transparent")
        coeff_row.pack(fill="x", padx=10, pady=6)

        for i, lbl in enumerate(["a :", "b :", "c :"]):  
            ctk.CTkLabel(coeff_row, text=lbl,
                         font=ctk.CTkFont(family="Segoe UI",size=11,slant="italic")).grid(row=0, column=i*2,
                                                      padx=(8,2), pady=4)
            coeff_row.grid_columnconfigure(i*2+1, weight=1)

        #   Store entry widgets as instance variables so solve() can read them
        self.quad_a = ctk.CTkEntry(coeff_row, width=60, justify="center",
                                    placeholder_text="0",placeholder_text_color="gray")
        self.quad_b = ctk.CTkEntry(coeff_row, width=60, justify="center",
                                    placeholder_text="0",placeholder_text_color="gray")
        self.quad_c = ctk.CTkEntry(coeff_row, width=60, justify="center",
                                    placeholder_text="0",placeholder_text_color="gray")

        self.quad_a.grid(row=0, column=1, padx=(0,8))
        self.quad_b.grid(row=0, column=3, padx=(0,8))
        self.quad_c.grid(row=0, column=5, padx=(0,8))

        # ── Solve + Clear buttons side by side ───────────────
        quad_btn_row = ctk.CTkFrame(sec_a, fg_color="transparent")
        quad_btn_row.pack(fill="x", padx=10, pady=(0, 6))

        #   Solve button — primary action, takes most of the row
        ctk.CTkButton(
            quad_btn_row,
            text="Solve ↵",
            height=34, corner_radius=8,
            fg_color="#3b4cca",
            hover_color="#2a3aaa",
            command=self.solve_quadratic
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        #   Clear button — red to signal it wipes both inputs AND the output box
        ctk.CTkButton(
            quad_btn_row,
            text="🗑 Clear",
            height=34, corner_radius=8, width=90,
            fg_color="#8b1a1a",
            hover_color="#b22222",
            command=self.clear_quadratic
        ).pack(side="left")

        #   Result display — updated by solve_quadratic(), cleared by clear_quadratic()
        self.quad_result = ctk.CTkTextbox(sec_a, height=80,
                                           font=("Consolas", 12),
                                           state="disabled")
        self.quad_result.pack(fill="x", padx=10, pady=(0, 10))

        # ════════ B) LINEAR SYSTEM ════════════════════════
        sec_b = ctk.CTkFrame(scroll, corner_radius=10)
        sec_b.pack(fill="x", pady=(0, 10))

        make_label(sec_b, "🔣  2×2 Linear System Solver",
                   font_size=14, bold=True).pack(anchor="w", padx=10, pady=(8,2))
        
        #   Create a shared row frame to hold both labels side by side
        label_row = ctk.CTkFrame(sec_b, fg_color="transparent")
        label_row.pack(fill="x", padx=10, pady=(0, 4))

        #   Left label
        make_label(label_row, "  a₁x + b₁y = c₁\n  a₂x + b₂y = c₂",
                    font_size=11, color="gray",bold=True, italic=True).pack(side="left")

        #   Right label — pushed to the right edge of the same row
        make_label(label_row, "Determinant det() = a₁b₂ - a₂b₁",
                    font_size=11, color="gray",bold=True,italic=True).pack(side="right")
        
        #   Create a frame to hold the two legend lines together 
        legend_frame = ctk.CTkFrame(sec_b, fg_color="transparent")
        legend_frame.pack(anchor="w", padx=10, pady=(0, 2))
        
        #   Each line is its own label — guarantees perfect left alignment
        ctk.CTkLabel(legend_frame, text="|| det() ≠ 0 → Lines Intersect |",
                    font=("Segoe UI", 10), text_color=("black","white")).pack(anchor="w",side ="left")
        ctk.CTkLabel(legend_frame, text="| det() = 0 → Lines are Parallel ||",
                    font=("Segoe UI", 10), text_color=("black","white")).pack(anchor="w",side="right")
        

        #   Two-equation input table
        eq_grid = ctk.CTkFrame(sec_b, fg_color="transparent")
        eq_grid.pack(fill="x", padx=10, pady=6)

        headers = ["", "coeff x", "coeff y", "= constant"]
        for c, h in enumerate(headers):
            ctk.CTkLabel(eq_grid, text=h,
                         font=ctk.CTkFont(family="Segoe UI",size= 10,slant="italic"),
                         text_color=("black","white")).grid(row=0, column=c, padx=4)

        #   Row labels
        ctk.CTkLabel(eq_grid, text="EQ I:",
                     font=("Segoe UI", 11, "bold")).grid(row=1, column=0, padx=4, pady=3)
        ctk.CTkLabel(eq_grid, text="EQ II:",
                     font=("Segoe UI", 11, "bold")).grid(row=2, column=0, padx=4, pady=3)

        #   Entry widgets  a1, b1, c1, a2, b2, c2
        self.lin_a1 = ctk.CTkEntry(eq_grid, width=65, justify="center", placeholder_text="0",
                                   placeholder_text_color="gray")
        self.lin_b1 = ctk.CTkEntry(eq_grid, width=65, justify="center", placeholder_text="0",
                                   placeholder_text_color="gray")
        self.lin_c1 = ctk.CTkEntry(eq_grid, width=65, justify="center", placeholder_text="0",
                                   placeholder_text_color="gray")
        self.lin_a2 = ctk.CTkEntry(eq_grid, width=65, justify="center", placeholder_text="0",
                                   placeholder_text_color="gray")
        self.lin_b2 = ctk.CTkEntry(eq_grid, width=65, justify="center", placeholder_text="0",
                                   placeholder_text_color="gray")
        self.lin_c2 = ctk.CTkEntry(eq_grid, width=65, justify="center", placeholder_text="0",
                                   placeholder_text_color="gray")

        for c, w in enumerate([self.lin_a1, self.lin_b1, self.lin_c1], start=1):
            w.grid(row=1, column=c, padx=4, pady=3)
        for c, w in enumerate([self.lin_a2, self.lin_b2, self.lin_c2], start=1):
            w.grid(row=2, column=c, padx=4, pady=3)

        # ── Solve + Clear buttons side by side ───────────────
        lin_btn_row = ctk.CTkFrame(sec_b, fg_color="transparent")
        lin_btn_row.pack(fill="x", padx=10, pady=(0, 6))

        #   Solve button — primary action
        ctk.CTkButton(
            lin_btn_row,
            text="Solve ↵",
            height=34, corner_radius=8,
            fg_color="#3b4cca",
            hover_color="#2a3aaa",
            command=self.solve_linear
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        #   Clear button — clears all 6 input fields AND the result textbox
        ctk.CTkButton(
            lin_btn_row,
            text="🗑 Clear",
            height=34, corner_radius=8, width=90,
            fg_color="#8b1a1a",
            hover_color="#b22222",
            command=self.clear_linear
        ).pack(side="left")

        #   Result display — updated by solve_linear(), cleared by clear_linear()
        self.lin_result = ctk.CTkTextbox(sec_b, height=70,
                                          font=("Consolas", 12),
                                          state="disabled")
        self.lin_result.pack(fill="x", padx=10, pady=(0, 10))

    # ── Quadratic Solver Logic ────────────────────────────
    def solve_quadratic(self):
        """
        Solve  ax² + bx + c = 0  using the quadratic formula.
        Uses Python's cmath module so complex roots are handled gracefully.

        Discriminant D = b² - 4ac:
          D > 0  →  two distinct real roots
          D = 0  →  one repeated real root
          D < 0  →  two complex conjugate roots
        """
        try:
            a = float(self.quad_a.get() or 1)
            b = float(self.quad_b.get() or 0)
            c = float(self.quad_c.get() or 0)
        except ValueError:
            self._write_textbox(self.quad_result,
                                "⚠  Please enter valid numbers for a, b, c.")
            return
        if abs(a) < 1e-12:
            # Degenerate case: not a quadratic equation
            if abs(b) < 1e-12:
                if abs(c) < 1e-12:
                    msg = "ℹ Note: Infinite Solutions.\n\nEquation reduces to 0 = 0."
                else:
                    msg = f"ℹ Note: Inconsistent Equation.\n\nEquation reduces to {c} = 0, which has no solution."

            else:
                # Linear equation: bx + c = 0  →  x = -c/b
                x = (-c / b) + 0.0
                vi = int(x) if x == int(x) else round(x, 8)
                msg = f"ℹ Note: Linear Fallback (a=0)\n\n  x  =  {vi}"
            
            self._write_textbox(self.quad_result, msg)
            self.history.add(f"[Linear Fallback] {b}x+{c}=0", msg.split('\n')[-1].strip())
            return

        discriminant = b**2 - 4*a*c
        di = int(discriminant) if discriminant == int(discriminant) else round(discriminant, 4)

        if discriminant > 1e-10:
            #   Two distinct real roots — standard formula
            sqrt_d = math.sqrt(discriminant)
            x1 = ((-b + sqrt_d) / (2*a)) + 0.0
            x2 = ((-b - sqrt_d) / (2*a)) + 0.0
            
            # Clean integer formatting
            v1 = int(x1) if x1 == int(x1) else round(x1, 8)
            v2 = int(x2) if x2 == int(x2) else round(x2, 8)
            
            msg = (f"Root Type:   Two distinct real roots (D = {di})\n"
                   f"  x₁  =  {v1}\n"
                   f"  x₂  =  {v2}")
            hist_val = f"x₁={v1}, x₂={v2}"

        elif abs(discriminant) <= 1e-10:
            #   One repeated root
            x = (-b / (2*a)) + 0.0
            v = int(x) if x == int(x) else round(x, 8)
            msg = (f"Root Type:   One repeated real root (D = 0)\n"
                   f"  x  =  {v}")
            hist_val = f"x={v}"

        else:
            #   Complex roots — use cmath
            sqrt_d = cmath.sqrt(discriminant)
            x1 = (-b + sqrt_d) / (2*a)
            x2 = (-b - sqrt_d) / (2*a)

            def fmt_complex(z):
                """Format a complex number as  a ± bi  cleanly."""
                r, i = z.real + 0.0 , z.imag + 0.0
                r_fmt = int(r) if r == int(r) else round(r, 6)
                i_fmt = abs(int(i)) if i == int(i) else round(abs(i), 6)
                sign = "+" if i >= 0 else "-"
                return f"{r_fmt} {sign} {i_fmt}i"
            
            c1, c2 = fmt_complex(x1), fmt_complex(x2)
            msg = (f"Root Type:   Two complex conjugate roots (D = {di})\n"
                   f"  x₁  =  {c1}\n"
                   f"  x₂  =  {c2}")
            hist_val = f"x₁={c1}, x₂={c2}"

        self._write_textbox(self.quad_result, msg)
        #   Clean history formatting for the polynomial string
        poly_str = f"{a}x²{'+' if b>=0 else ''}{b}x{'+' if c>=0 else ''}{c}=0"
        self.history.add(f"[Quadratic] {poly_str}", hist_val)

    # ── Linear System Solver Logic ────────────────────────
    def solve_linear(self):
        """
        Solve the 2×2 linear system:
            a1*x + b1*y = c1
            a2*x + b2*y = c2

        Uses Cramer's Rule:
            D  = a1*b2 - a2*b1        (main determinant)
            Dx = c1*b2 - c2*b1        (x-numerator determinant)
            Dy = a1*c2 - a2*c1        (y-numerator determinant)
            x  = Dx / D,   y = Dy / D
        """
        try:
            a1 = float(self.lin_a1.get() or 0)
            b1 = float(self.lin_b1.get() or 0)
            c1 = float(self.lin_c1.get() or 0)
            a2 = float(self.lin_a2.get() or 0)
            b2 = float(self.lin_b2.get() or 0)
            c2 = float(self.lin_c2.get() or 0)
        except ValueError:
            self._write_textbox(self.lin_result,
                                "⚠  Please enter valid numbers in all fields.")
            return

        D  = a1*b2 - a2*b1     # Main determinant

        if abs(D) < 1e-12:
            #   Check whether the system is inconsistent or dependent
            Dx = c1*b2 - c2*b1
            if abs(Dx) < 1e-12:
                msg = ("ℹ Note: Infinitely many solutions.\n\n"
                       "The equations describe the same line\n"
                       "(dependent system).")
                hist_val = "Infinite Solutions"
            else:
                msg = ("ℹ Note: No solution exists.\n\n"
                       "The equations describe parallel lines\n"
                       "(inconsistent system).")
                hist_val = "No Solution"
        else:
            Dx = c1*b2 - c2*b1
            Dy = a1*c2 - a2*c1

        # --- NEGATIVE ZERO FIX APPLIED HERE ---
            x = (Dx / D) + 0.0
            y = (Dy / D) + 0.0            
        
        #   Clean integer formatting
            xi = int(x) if x == int(x) else round(x, 8)
            yi = int(y) if y == int(y) else round(y, 8)
            di = int(D) if D == int(D) else round(D, 4)
            msg = (f"System Type: Unique solution (D = {di})\n\n"
                   f"  x  =  {xi}\n"
                   f"  y  =  {yi}")
            hist_val = f"x={xi}, y={yi}"

        self._write_textbox(self.lin_result, msg)
        # Clean polynomial string formatting for the history panel
        eq1 = f"{a1}x{'+' if b1>=0 else ''}{b1}y={c1}"
        eq2 = f"{a2}x{'+' if b2>=0 else ''}{b2}y={c2}"
        self.history.add(f"[Linear] {eq1} | {eq2}", hist_val)

    # ── Clear Quadratic ───────────────────────────────────
    def clear_quadratic(self):
        """
        Reset the quadratic solver completely:
        - Deletes all text from the three coefficient entry boxes (a, b, c)
        - Clears the result textbox
        Ready for a brand new equation.
        """
        #   Clear all three input fields
        for entry in (self.quad_a, self.quad_b, self.quad_c):
            entry.delete(0, "end")

        #   Clear the result/output textbox
        self._write_textbox(self.quad_result, "")

    # ── Clear Linear System ───────────────────────────────
    def clear_linear(self):
        """
        Reset the linear system solver completely:
        - Deletes all text from all six entry boxes (a1,b1,c1, a2,b2,c2)
        - Clears the result textbox
        Ready for a brand new system of equations.
        """
        #   Clear all six input fields
        for entry in (self.lin_a1, self.lin_b1, self.lin_c1,
                      self.lin_a2, self.lin_b2, self.lin_c2):
            entry.delete(0, "end")

        #   Clear the result/output textbox
        self._write_textbox(self.lin_result, "")

    # ── Utility: write text into a read-only CTkTextbox ───
    def _write_textbox(self, box, text):
        """Enable the textbox, overwrite content, then lock it again."""
        box.configure(state="normal")
        box.delete("0.0", "end")
        box.insert("end", text)
        box.configure(state="disabled")


    # ═════════════════════════════════════════════════════
    #   TAB 3 — ALGEBRA MODE  (NEW in v7.0)
    # ═════════════════════════════════════════════════════
    def _build_algebra_tab(self, parent):
        """
        Algebra Mode — smart natural-language expression input.

        The user types an expression or equation in a large text box
        and presses Solve. The engine auto-detects the type and routes
        to the appropriate solver:

          TYPE 1 — No '=' sign         → simplify like terms
          TYPE 2 — ax+b=c (1 var)      → solve linear single variable
          TYPE 3 — eq1,eq2 (2 eqs)     → solve 2×2 linear system
          TYPE 4 — ax²+bx+c=0          → quadratic formula (real + complex)
          TYPE 5 — (ax+b)(cx+d)=0      → expand bracket product then solve
          TYPE 6 — Degree > 2           → guidance message (not solvable here)

        The '=' key is used as input here (not execution), unlike the
        Scientific tab where '=' runs the calculation.
        """
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=6, pady=6)

        # ── Header ────────────────────────────────────────
        make_label(frame, "🔣  Algebra Mode",
                   font_size=14, bold=True).pack(anchor="w", pady=(0, 2))

        # ── Input display (large, editable, white bg) ──────
        #   Twice the height of the scientific display
        inp_card = ctk.CTkFrame(frame, corner_radius=10)
        inp_card.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(inp_card, text="Enter expression or equation:",
                     font=("Segoe UI", 11), text_color=("#333333", "#DCE4EE"),
                     anchor="w").pack(anchor="w", padx=10, pady=(6, 0))        

        self.alg_input = ctk.CTkTextbox(
            inp_card,
            font=("Consolas", 18), 
            height=90,          
            fg_color="#ccffcc",
            text_color="black",
            corner_radius=6,
        )
        self.alg_input.pack(fill="x", padx=8, pady=(2, 4)) 

        # ── Type indicator (shown after detection) ─────────
        self.alg_type_lbl = ctk.CTkLabel(
            frame, text="",
            font=("Segoe UI", 10, "bold"),
            text_color=("#2a9d8f"),  # teal
            anchor="w"
        )
        self.alg_type_lbl.pack(fill="x",padx=12, pady=(2, 6)) 

        # ── Solve + Clear buttons ──────────────────────────
        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(fill="x",padx=8, pady=(0, 4) ) 

        ctk.CTkButton(
            btn_row,
            text="Solve ↵",
            height=32, corner_radius=8, 
            fg_color="#3b4cca", hover_color="#2a3aaa",
            command=self.solve_algebra
        ).pack(side="left", expand=True, fill="x", padx=(0,10)) 

        ctk.CTkButton(
            btn_row,
            text="🗑 Clear",
            height=32, corner_radius=8, width=80, 
            fg_color="#8b1a1a", hover_color="#b22222",
            command=self.clear_algebra
        ).pack(side="right",padx=0)     

        # ── Result textbox ────────────────────────────────
        res_card = ctk.CTkFrame(frame, corner_radius=10)
        res_card.pack(fill="both", expand=False, pady=(0, 4)) 
        make_label(res_card, "Result:", font_size=11,
                   color=("#666666", "#AAB4BE")).pack(anchor="w", padx=10, pady=(6, 0))

        self.alg_result = ctk.CTkTextbox(
            res_card,
            font=("Consolas", 12),  
            height=130,     
            state="disabled",
            corner_radius=6
        )
        self.alg_result.pack(fill="both", expand=True,
                              padx=8, pady=(0, 8))
        
        self.alg_result._textbox.configure(wrap="word")

        #   Quick reference card (Condensed Full Text)
        ref_card = ctk.CTkFrame(frame, corner_radius=8)
        ref_card.pack(fill="x", pady=(5, 2))                # Reduced top padding

        make_label(ref_card, "Input guide", font_size=10, bold=True).pack(anchor="w", padx=8, pady=(2, 0))

        #   We keep the full explanations here!
        guide_lines = [
            ("Simplify     : 2a+3b-a+b", " (multivariable/powers)"),
            ("Linear 1v    : 2x+5=11", ""),
            ("Linear 2x2   : 2a-6b=19, 4a+b=12", " (comma separated)"),
            ("Quadratic    : x^2+4x-7=0", " (real/complex roots)"),
            ("Brackets     : (x+7)(x-4)=0", " (FOIL expansion)"),
            ("Higher Poly  : x^3+2x-5=0", " (degree > 2 detection)"),
            ("Smart Routing: Detects variables", " (Auto-Redirect)")
        ]

        for main_text, italic_text in guide_lines:
            line_frame = ctk.CTkFrame(ref_card, fg_color="transparent")
            #   CRITICAL: Setting pady to -1 or 0 and ipady to 0 
            #   to literally squeeze the lines together
            line_frame.pack(fill="x", padx=8, pady=0) 

            ctk.CTkLabel(line_frame, text=f"• {main_text}", 
                         font=("Consolas", 9), # Font 9 is the secret weapon
                         text_color=("#333333", "#DCE4EE")).pack(side="left")

            if italic_text:
                ctk.CTkLabel(line_frame, text=italic_text, 
                             font=("Consolas", 9, "italic"),
                             text_color=("#666666", "#A0A0A0")).pack(side="left")

        # No empty labels at the bottom, just a tiny bit of frame padding

    # ─────────────────────────────────────────────────────
    #   ALGEBRA ENGINE — helper methods
    # ─────────────────────────────────────────────────────

    def _alg_tokenise(self, expr):
        """
        Split 'ax+by-cz+d' into signed token strings.
        e.g. '2a+3b-4a+b' → ['+2a', '+3b', '-4a', '+b']
        """
        expr = expr.replace(" ", "")
        if expr and expr[0] not in "+-":
            expr = "+" + expr
        return re.findall(r'[+\-][^+\-]+', expr)

    def _alg_parse_term(self, term):
        """
        Parse a signed term into (coefficient, variable_key).
        variable_key is:
          ''      for constants  (e.g. '+8'   → (8.0, ''))
          'a'     for linear     (e.g. '+5a'  → (5.0, 'a'))
          'a^2'   for quadratic  (e.g. '+4a^2'→ (4.0, 'a^2'))
          'a^n'   for degree n   (e.g. '-3x^3'→ (-3.0,'x^3'))
        Returns None if the term cannot be parsed.
        """
        term = term.strip()
        sign = 1.0 if term[0] == "+" else -1.0
        body = term[1:]

        #   Pure number
        try:
            return (sign * float(body), "")
        except ValueError:
            pass

        #   Power term: optional_coeff + letter + ^degree  e.g. 4a^2, a^2, 3x^3
        m = re.fullmatch(r'(\d*\.?\d*)([a-zA-Z])\^(\d+)', body)
        if m:
            coeff_str, var, deg_str = m.groups()
            coeff = float(coeff_str) if coeff_str else 1.0
            return (sign * coeff, f"{var}^{deg_str}")

        #   Linear term: optional_coeff + single letter  e.g. 4a, b, 3.5x
        m = re.fullmatch(r'(\d*\.?\d*)([a-zA-Z])', body)
        if m:
            coeff_str, var = m.groups()
            coeff = float(coeff_str) if coeff_str else 1.0
            return (sign * coeff, var)

        return None   # cross-terms like 'xy' — caught by cross-term guard

    def _alg_max_degree(self, expr_str):
        """
        Return the maximum power/degree found in expr_str.
        Looks for patterns like x^3, a^4, etc.
        Returns 1 if no explicit powers found.
        """
        powers = re.findall(r'\^(\d+)', expr_str)
        if not powers:
            return 1
        return max(int(p) for p in powers)

    def _alg_simplify(self, expr_str):
        """
        Collect like terms in expr_str.
        Returns (result_string, coefficients_dict, error_string).

        coefficients_dict keys are variable_keys from _alg_parse_term:
          ''    → constant
          'a'   → linear term in a
          'a^2' → quadratic term in a  (NEW — power terms now parsed here)
        """
        
        # --- ADD THIS TRAP ---
        if "(" in expr_str or ")" in expr_str:
            return None, {}, "Brackets detected.\nTo expand/solve, please use equation format\n(e.g., = 0)"
        # ---------------------
        
        tokens = self._alg_tokenise(expr_str)
        coeffs = defaultdict(float)

        for tok in tokens:
            parsed = self._alg_parse_term(tok)
            if parsed is None:
                return None, {}, f"Cannot parse term: {tok!r}"
            coeff, var_key = parsed
            coeffs[var_key] += coeff

        def sort_key(k):
            """Sort: higher degree first, then alphabetical, constant last."""
            if k == "":
                return (0, "")                      # constant sorts last (degree 0)
            if "^" in k:
                var, deg = k.split("^")
                return (-int(deg), var)             # negative so higher degree sorts first
            return (-1, k)                          # linear = degree 1

        all_keys = sorted(coeffs.keys(), key=sort_key)

        parts = []
        for var_key in all_keys:
            c = coeffs[var_key]
            if abs(c) < 1e-12:
                continue
            ci = int(c) if c == int(c) else round(c, 8)

            #   Build the display term
            if var_key == "":
                term_str = str(ci)
            elif "^" in var_key:
                term_str = var_key if abs(ci) == 1 else f"{ci}{var_key}"
            else:
                term_str = var_key if abs(ci) == 1 else f"{ci}{var_key}"

            if parts:
                parts.append(f"+{term_str}" if c > 0 else str(term_str))
            else:
                #   First term: include minus sign for negative
                if c < 0 and abs(ci) == 1 and var_key:
                    parts.append(f"-{var_key if '^' not in var_key else var_key}")
                else:
                    parts.append(str(term_str))

        result = "".join(parts) if parts else "0"
        return result, dict(coeffs), None

    def _alg_extract_constant_from_lhs(self, lhs, variables):
        """
        Extract variable coefficients AND the embedded constant
        from a LHS that may have the constant baked in, e.g. '5x-8y-9'.

        Returns (var_coeffs_dict, embedded_constant).
        The embedded constant should be subtracted from the RHS:
          5x - 8y - 9 = 0  means  5x - 8y = 9
        """
        var_coeffs = {}
        for v in variables:
            pattern = r'([+\-]?\d*\.?\d*)' + re.escape(v) + r'(?!\^)'
            m = re.search(pattern, lhs)
            if m:
                s = m.group(1)
                var_coeffs[v] = (float(s) if s not in ("", "+", "-")
                                 else (1.0 if s != "-" else -1.0))
            else:
                var_coeffs[v] = 0.0

        #   Remove all variable terms to find the embedded constant
        remainder = lhs
        for v in variables:
            remainder = re.sub(
                r'[+\-]?\d*\.?\d*' + re.escape(v) + r'(?!\^)', '', remainder)
        remainder = remainder.replace(" ", "")
        try:
            embedded_const = float(remainder) if remainder else 0.0
        except ValueError:
            embedded_const = 0.0

        return var_coeffs, embedded_const

    def _alg_detect_vars(self, expr_str):
        """
        Return sorted list of unique single-letter variable names in expr_str.

        The old pattern excluded variables in power terms (x in x^2, y in y^2)
        because the lookahead (?!^) fired on them. '6x^2-2y^2' reported zero variables,
        bypassing the multi-variable quadratic guard.

        New approach: strip known function/constant names first, then find all
        remaining single letters.
        """
        
        #   Remove known multi-letter function names and pi constant.
        #   NOTE: 'e' is intentionally NOT in this list — in the Algebra tab,
        #   'e' is treated as a variable, not Euler's number. Euler's 'e' is
        #   only special in the Scientific calculator tab.
        
        known = ["sqrt", "fibs", "fact", "sin", "cos", "tan", "log", "ln",
                 "fib", "npr", "ncr", "bin", "dec", "hex", "pi"]
        clean = expr_str
        for name in sorted(known, key=len, reverse=True):
            #   Replace whole-word occurrences only (not part of a longer name)
            clean = re.sub(r'(?<![a-zA-Z])' + re.escape(name) + r'(?![a-zA-Z])',
                           " " * len(name), clean)

        #   Find all single letters — includes those before ^ (power vars like x^2)
        return sorted(set(re.findall(r'(?<![a-zA-Z])[a-zA-Z](?![a-zA-Z])', clean)))

    def _alg_parse_quad_coeffs(self, lhs, var):
        """
        Extract (a, b, c) from a quadratic lhs like 'x^2+4x-7'.
        var is the variable letter.
        """
        s = lhs.replace(var + "²", var + "^2")

        m_a = re.search(r'([+\-]?\d*\.?\d*)' + re.escape(var) + r'\^2', s)
        if not m_a:
            return None
        a_str = m_a.group(1)
        a = (float(a_str) if a_str not in ("", "+", "-")
             else (1.0 if a_str != "-" else -1.0))

        rest = re.sub(r'[+\-]?\d*\.?\d*' + re.escape(var) + r'\^2', '', s)

        m_b = re.search(r'([+\-]?\d*\.?\d*)' + re.escape(var) + r'(?!\^)', rest)
        if m_b:
            b_str = m_b.group(1)
            b = (float(b_str) if b_str not in ("", "+", "-")
                 else (1.0 if b_str != "-" else -1.0))
            rest2 = re.sub(r'[+\-]?\d*\.?\d*' + re.escape(var), '', rest)
        else:
            b = 0.0
            rest2 = rest

        try:
            c = float(rest2.strip()) if rest2.strip() else 0.0
        except ValueError:
            c = 0.0

        return a, b, c

    # ─────────────────────────────────────────────────────
    #   ALGEBRA SOLVER — Main Dispatcher
    # ─────────────────────────────────────────────────────

    def solve_algebra(self):
        
        
        """
        Read algebra input, detect expression type, and route to solver.

        Detection order:
          0. Cross-term guard (e.g. xy) → unsupported, explain why
          1. Degree > 2 guard → cubic/quartic message
          2. Comma → linear system (2 equations)
          3. No '=' → simplify like terms
          4. (…)(…)(…) → multi-bracket → expand iteratively → check degree
          5. (…)(…) → single bracket pair → expand then solve
          6. ^2 in equation → quadratic (only if 1 variable)
          7. = present, linear → 1 var or 2 var
        """
        
        raw = self.alg_input.get("0.0", "end").strip()
        if not raw:
            self._alg_show("Please enter an expression or equation.")
            return

        raw = raw.replace("×", "*").replace("÷", "/")
        expr = raw.replace("²", "^2").strip()

        #   NUMERIC BYPASS (NEW)
        #   Check if there are ANY letters. If not, and no '=', it's pure math.
        vars_in = self._alg_detect_vars(expr)
        if len(vars_in) == 0 and "=" not in expr:
            try:
                #   Use your existing eval logic
                res = eval(expr.replace("^", "**"), {"__builtins__": {}}, {})
                self.alg_type_lbl.configure(text="TYPE: Numeric Simplification")
                self._alg_show(f"Result:  {res}")
                return          # CRITICAL: Stop here so it never hits the Guards below
            except: pass 
        # ------------------------------------

        try:
            # ── Cross-variable terms (xy, ab) ────
            #   These create a different class of equation that cannot be
            #   solved by coefficient extraction. Detect and explain.
            cross = re.findall(r'[a-zA-Z]{2,}(?!\^)', expr.replace("^","~"))
            if cross:
                #   Extract individual letters from the cross-terms
                found_vars = sorted(list(set("".join(cross))))
                vars_str = " , ".join(found_vars)
                
                self.alg_type_lbl.configure(
                    text="TYPE: Multi-variable — Hint")
                
                self._alg_show(
                    f"ℹ Tip: Cross-variable terms (like {', '.join(set(cross))}) detected.\n\n"
                    f"While the engine can simplify these expressions,\n"
                    f"unique root solving for variables (e.g: {vars_str})\n" 
                    f"requires a single-variable format in\n"
                    f"{self.APP_NAME}."
                )
                return
 
            
            #   Degree > 2
            #   Detect the maximum power in the expression.
            #   Cubics and beyond are beyond this solver's scope.
            max_deg = self._alg_max_degree(expr)
            # --- Only block higher degrees if it is an equation! ---
            if max_deg == 3 and "=" in expr:
                self.alg_type_lbl.configure(
                    text="TYPE: Cubic (Degree 3) — Hint")
                self._alg_show(
                    f"ℹ Note: Cubic equation (Degree 3) detected.\n\n"
                    f"Analytic solvers for polynomials beyond Degree 2\n"
                    f"(Quadratic) are outside the scope of\n"
                    f"{self.APP_NAME}.\n\n"
                    f"   Tip: Numerical estimation for higher-order\n"
                    f"   polynomials is planned for a future update."
                )
                return            

            if max_deg > 3 and "=" in expr:
                self.alg_type_lbl.configure(
                    text=f"TYPE: Degree-{max_deg} Polynomial — Hint")
                self._alg_show(
                    f"ℹ Note: Degree-{max_deg} Polynomial detected.\n\n"
                    f"Analytic root extraction for polynomials beyond\n"
                    f"Degree 2 (Quadratic) is outside the scope of\n"
                    f"{self.APP_NAME}.\n\n"
                    f"   Tip: Numerical estimation for higher-order\n"
                    f"   polynomials is planned for a future update."
                )
                return

            #   TYPE: Comma → 2-equation linear system
            if "," in expr:
                parts = [p.strip() for p in expr.split(",", 1)]
                self._solve_linear_system(parts, raw)

            #   TYPE: No '=' → Simplify
            elif "=" not in expr:
                self._solve_simplify(expr, raw)

            #   TYPE: Equation with = 
            else:
                lhs, rhs = expr.split("=", 1)
                rhs = rhs.strip()
                lhs = lhs.strip()                   # Added this to ensure clean peeling

                # --- UPDATED PEELING LOGIC STARTS HERE ---
                #   Added `.count("(") == 1` so it doesn't accidentally destroy FOIL brackets
                if lhs.startswith("(") and lhs.endswith(")") and lhs.count("(") == 1:
                    lhs = lhs[1:-1].strip()
                if rhs.startswith("(") and rhs.endswith(")") and rhs.count("(") == 1:
                    rhs = rhs[1:-1].strip()    
                # --- UPDATED PEELING LOGIC ENDS HERE ---
                
                #   Now your existing variable detection/solving logic follows...
                vars_in = self._alg_detect_vars(lhs + rhs)
                bracket_groups = re.findall(r'\([^()]+\)', lhs)
                
                #   Multi-bracket: 3+ groups → expand iteratively
                if len(bracket_groups) >= 3:
                    self._solve_multi_bracket(lhs, rhs, raw)

                #   Single bracket pair
                elif len(bracket_groups) == 2 and re.search(r'\([^()]+\)\([^()]+\)', lhs):
                    self._solve_bracket_product(lhs, rhs, raw)

                #   UNIFORM QUADRATIC POWER GUARD
                elif re.search(r'\([^()]+\)\^2', lhs) or re.search(r'\([^()]+\)\^2', rhs):
                    self.alg_type_lbl.configure(text="TYPE: Quadratic (Degree 2) — Hint")
                    self._alg_show(
                        f"ℹ Note: Quadratic power bracket detected.\n\n"
                        f"Algebraic expansion of binomials raised to a power\n"
                        f"is outside the scope of {self.APP_NAME}.\n\n"
                        f"   Tip: Please write out the brackets explicitly\n"
                        f"   (e.g., (x-3)(x-3) = 5) to trigger the\n"
                        f"   FOIL expansion engine."
                    )

                #   SPECIFIC CHECK FIRST: Is it a FOIL/Bracket Product?
                #   We check this BEFORE the guard so it doesn't get blocked.
                elif "(" in lhs or ")" in lhs or "(" in rhs or ")" in rhs:
                    self.alg_type_lbl.configure(text="TYPE: Linear — Hint")
                    self._alg_show(
                        f"ℹ Note: Simplification limited.\n\n"
                        f"Brackets detected. Algebraic expansion (FOIL/Distribution)\n"
                        f"is outside the scope of {self.APP_NAME}\n\n"
                        f"   Tip: Please use a standard equation format\n"
                        f"   without brackets (e.g., 2x + 15 = 0)."
                    )

            #   Quadratic: contains ^2
                elif "^2" in lhs or "^2" in rhs:
                    if len(vars_in) > 1:
                        self.alg_type_lbl.configure(
                            text="TYPE: Multi-variable Quadratic — Hint")
                        self._alg_show(
                            f"ℹ Note: Multiple variables ({', '.join(vars_in)}) detected.\n\n"
                            f"Analytic root extraction for quadratics with more\n"
                            f"than one variable is outside the scope of\n"
                            f"{self.APP_NAME}.\n\n"
                            f"   Tip: Please reduce the expression to a\n"
                            f"   single-variable format (e.g., just {vars_in[0]})."
                        )

                    else:
                        self._solve_quadratic_from_str(lhs, rhs, raw)

                #   Linear
                else:
                    if len(vars_in) == 0:
                        #   Numeric equality check
                        try:
                            lv = eval(lhs.replace("^","**"), {"__builtins__": {}}, {})
                            rv = eval(rhs.replace("^","**"), {"__builtins__": {}}, {})
                            
                            self.alg_type_lbl.configure(
                                text="TYPE: Numeric Equality — Statement")
                            
                            if abs(lv - rv) < 1e-10:
                                msg = (
                                    f"ℹ Note: Mathematical Statement is True.\n\n"
                                    f"  LHS: {lv}\n"
                                    f"  RHS: {rv}\n\n"
                                    f"The values are identical."
                                )
                            else:
                                msg = (
                                    f"ℹ Note: Mathematical Statement is False.\n\n"
                                    f"  LHS: {lv}\n"
                                    f"  RHS: {rv}\n\n"
                                    "The two sides do not equate."
                                )
                            self._alg_show(msg)
                            
                        except Exception:
                            self._alg_show(f"ℹ Note: Evaluation Error.\n\nCould not process the numeric values.")

                    elif len(vars_in) == 1:
                        self._solve_linear_one_var(lhs, rhs, vars_in[0], raw)
                    
                    elif len(vars_in) == 2:
                        #   Single equation, 2 unknowns — underdetermined
                        v1, v2 = vars_in[0], vars_in[1]
                        # --- THE REAL FIX: Invert RHS signs without brackets ---
                        rhs_tokens = self._alg_tokenise(rhs)
                        inverted_rhs = "".join("+" + t[1:] if t.startswith("-") else "-" + t[1:] for t in rhs_tokens)
                        combined_expr = f"{lhs}{inverted_rhs}"
                        
                        #combined_expr = f"{lhs} - ({rhs})"
                        #simp, _, err = self._alg_simplify(lhs)
                        simp, _, err = self._alg_simplify(combined_expr)
                        #   Determine the clean display string
                        display_eq = f"{simp} = 0" if not err else f"{lhs} = {rhs}"
                        self.alg_type_lbl.configure(
                            text="TYPE: Linear — Hint")
                        
                        self._alg_show(
                            f"Rearranged:     {display_eq}\n\n"
                            f"ℹ Note: System is underdetermined.\n\n"
                            f"One equation with two unknowns {v1}, {v2} has\n"
                            f"infinitely many solutions in {self.APP_NAME}.\n\n"
                            f"   Tip: To find unique values for both, provide\n"
                            f"   two equations separated by a comma:\n\n"
                            f"   Example: {display_eq}, [second equation]"
                        )
                    else:
                        #   3+ variables in a single equation
                        n = len(vars_in)
                        vars_list = ", ".join(vars_in)
                        
                        self.alg_type_lbl.configure(
                            text=f"TYPE: Linear ({n} Variables) — Hint")
                        
                        self._alg_show(
                            f"ℹ Note: {n} variables detected ({vars_list}).\n\n"
                            f"A unique solution for {n} unknowns requires {n} independent equations.\n"
                            f"{self.APP_NAME} currently supports up to 2×2 linear systems.\n\n"
                            f"   Tip: Higher-order matrix solvers (≥ 3x3)\n"
                            f"   are not available in this build. Support for larger\n"
                            f"   systems is planned for a future update."
                        )                   
     
        except Exception as exc:
            print("ALGEBRA DEBUG:", exc)
            self._alg_show(f"Error: {exc}")

    #   Solver: Simplification
    def _solve_simplify(self, expr, raw):
        """Collect like terms. Show simplified form."""
        simp, coeffs, err = self._alg_simplify(expr)
        if err:
            self.alg_type_lbl.configure(text="TYPE: Simplification — Hint") #Previos value was text="TYPE: Simplification — Error"
            self._alg_show(f"ℹ Note: Simplification limited.\n\n{err}")
            return

        vars_present = [k for k in coeffs if k != "" and abs(coeffs[k]) > 1e-12]
        const = coeffs.get("", 0.0)
        

        if not vars_present:
            self.alg_type_lbl.configure(text="TYPE: Numeric Simplification")
            msg = f"Result:  {simp}"
        elif abs(const) < 1e-12 and vars_present:
            self.alg_type_lbl.configure(text="Expression - Hint")
            msg = (
                f"Simplified:  {simp}\n\n"
                f"ℹ Note: Expression detected (no '=' found).\n\n"
                f"Unique root solving requires a right-hand side\n"
                f"to equate the variables in {self.APP_NAME}.\n\n"
                f"   Tip: To solve for roots, add '= [value]'\n"
                f"   Example: {raw} = 0"
            )
        else:
            self.alg_type_lbl.configure(text="TYPE: Algebraic Simplification")
            msg = (
                f"ℹ Note: Expression simplified.\n\n"
                f"Simplified:  {simp}\n\n"
                "The engine has combined like-terms. To solve for\n"
                "specific roots, please provide an equation (e.g., = 0)."
            )

        self._alg_show(msg)
        self.history.add(f"[Algebra] Simplify: {raw}", simp)

    #   Solver: Linear 1 variable
    def _solve_linear_one_var(self, lhs, rhs, var, raw):
        """Solve ax + b = c. Using the robust _alg_simplify engine."""
        
        #   1. Combine LHS and RHS without creating "illegal" brackets
        #   We strip the sides and subtract them directly
        # --- THE REAL FIX: Invert RHS signs without brackets ---
        rhs_tokens = self._alg_tokenise(rhs)
        inverted_rhs = "".join("+" + t[1:] if t.startswith("-") else "-" + t[1:] for t in rhs_tokens)
        combined_expr = f"{lhs}{inverted_rhs}"
        #combined_expr = f"{lhs} - {rhs}"

        #   We use a simpler combination if the user input is "clean"

        simp, coeffs, err = self._alg_simplify(combined_expr)
        if err:
            #   Catching the bracket error or other parsing issues professionally
            self.alg_type_lbl.configure(text="TYPE: Error")
            self._alg_show(f"⚠  Parsing Error: {err}")
            return
            
        #   2. Extract coefficients
        a = coeffs.get(var, 0.0)
        constant_term = coeffs.get("", 0.0)        
        
        #   3. Logical Checks (Identity/Contradiction)
        if abs(a) < 1e-12:
            self.alg_type_lbl.configure(text="TYPE: Logical Result")
            if abs(constant_term) < 1e-10:
                self._alg_show("ℹ Note: Equation is an Identity.\n\n"
                               "Infinitely many solutions.")
            else:
                self._alg_show("ℹ Note: Equation is a Contradiction.\n\n"
                               "No solution exists.")
            return

        #   4. Final Calculation
        value = (-constant_term / a) + 0.0
        ci = int(value) if value == int(value) else round(value, 8)
        
        #   Using 'simp' here to show the user the simplified equation!
        msg = (
            f"ℹ Note: Linear equation solved.\n\n"
            f"Rearranged:     {simp} = 0\n"
            f"Variable:       {var}\n\n"
            f"   {var}  =  {ci}"
        )
        self._alg_show(msg)
        self.history.add(f"[Algebra] {raw}", f"{var} = {ci}")

    #   Solver: 2×2 Linear system
    def _solve_linear_system(self, parts, raw):
        """
        Solve 2-equation linear system using Cramer's Rule.
        Handles constants embedded in LHS (e.g. 5x-8y-9=0).
        Handles 3+ variables with a clear message.
        """
        self.alg_type_lbl.configure(
            text="TYPE: Linear system  (2×2 — Cramer's Rule)")

        if len(parts) != 2:
            self._alg_show("ℹ Note: Input format error.\n\nPlease enter exactly 2 equations separated by a comma.")
            return

        eq1, eq2 = parts[0], parts[1]

        #   Both must contain '='
        if "=" not in eq1 or "=" not in eq2:
            self.alg_type_lbl.configure(text="TYPE: Format Error")
            self._alg_show(
                "ℹ Note: Missing '=' operator.\n\n"
                "Both equations must contain an equals sign.\n"
                "Example:  2a-6b=19, 4a+4b=12\n\n"
                "Tip: You can also write constants on the left:\n"
                "   5x-8y-9=0, 2x+10y-16=0"
            )
            return

        lhs1, rhs1 = eq1.split("=", 1)
        lhs2, rhs2 = eq2.split("=", 1)
        #   BRACKET GUARD: Check both sides for brackets
        #   This prevents the solver from crashing on complex distribution
        all_sides = lhs1 + rhs1 + lhs2 + rhs2
        if "(" in all_sides or ")" in all_sides:
            self.alg_type_lbl.configure(text="TYPE: Linear System — Hint")
            self._alg_show(
                f"ℹ Note: Simplification limited.\n\n"
                f"Brackets detected. Algebraic expansion (FOIL/Distribution)\n"
                f"is outside the scope of {self.APP_NAME}.\n\n"
                f"   Tip: Please provide equations in standard\n"
                f"   linear format (e.g., 2x + 3y = 10)."
            )
            return
        
        try:
            rhs1_val = float(rhs1.strip())
            rhs2_val = float(rhs2.strip())
        except ValueError:
            self.alg_type_lbl.configure(text="TYPE: Format Error")
            self._alg_show("ℹ Note: Invalid Right-Hand Side.\n\n"
                           "The value after the '=' must be a number in both equations.") 
            return

        #   Detect variables from both LHS strings
        vars_all = self._alg_detect_vars(lhs1 + lhs2)

        #   3+ variable guard
        if len(vars_all) > 2:
            n = len(vars_all)
            vars_list = ", ".join(vars_all)
            
            self.alg_type_lbl.configure(
                text=f"TYPE: Linear ({n} Variables) — Hint")
            
            self._alg_show(
                f"ℹ Note: {n} variables detected ({vars_list}).\n\n"
                f"A unique solution for {n} unknowns requires {n} independent equations.\n"
                f"{self.APP_NAME} currently supports up to 2×2 linear systems.\n\n"
                f"   Tip: Higher-order matrix solvers (≥ 3x3)\n"
                f"   are not available in this build. Support for\n"
                f"   larger systems is planned for a future update."
            )
            return
        
        if len(vars_all) < 2:
            #   Might be two equations of one variable — handle gracefully
            self.alg_type_lbl.configure(text="TYPE: Format Error")
            self._alg_show(
                "ℹ Note: Insufficient variables.\n\n"
                "Expected at least 2 unique variables across the equations.\n"
                "For a single-variable equation, enter it without a comma."
            )
            return

        v1, v2 = vars_all[0], vars_all[1]

        # --- THE MASTER FIX APPLIED HERE ---
        #   Use the simplification engine to extract coefficients perfectly
        _, co1, err1 = self._alg_simplify(lhs1)
        _, co2, err2 = self._alg_simplify(lhs2)

        if err1 or err2:
            self.alg_type_lbl.configure(text="TYPE: Parsing Error")
            self._alg_show(f"ℹ Note: Could not parse coefficients.\n\n"
                           f"Equation 1 error: {err1 if err1 else 'None'}\n"
                           f"Equation 2 error: {err2 if err2 else 'None'}")
            return

        #   Extract the embedded constants
        const1 = co1.get("", 0.0)
        const2 = co2.get("", 0.0)
        
        #   Effective RHS = stated RHS − embedded LHS constant
        c1 = rhs1_val - const1
        c2 = rhs2_val - const2

        #   Extract variable coefficients safely using .get()
        a1, b1 = co1.get(v1, 0.0), co1.get(v2, 0.0)
        a2, b2 = co2.get(v1, 0.0), co2.get(v2, 0.0)
        # -----------------------------------
        
        D  = a1*b2 - a2*b1

        if abs(D) < 1e-12:
            self.alg_type_lbl.configure(text="TYPE: Logical Result")
            Dx = c1*b2 - c2*b1
            if abs(Dx) < 1e-12:
                msg = ("ℹ Note: Infinitely many solutions.\n\n"
                       "The equations describe the same line (dependent system).")
            else:
                msg = ("ℹ Note: No solution exists.\n\n"
                       "The equations describe parallel lines (inconsistent system).")
            self._alg_show(msg)
            self.history.add(f"[Algebra] {raw}", msg.split('\n')[0])
            return

        # --- NEGATIVE ZERO FIX APPLIED HERE ---
        x  = ((c1*b2 - c2*b1) / D) + 0.0
        y  = ((a1*c2 - a2*c1) / D) + 0.0

        xi = int(x) if x == int(x) else round(x, 8)
        yi = int(y) if y == int(y) else round(y, 8)

        #   Show hint if constants were embedded in LHS
        hint = ""
        if abs(const1) > 1e-12 or abs(const2) > 1e-12:
            hint = (f"\nℹ Note: Constants on LHS moved to RHS:\n"
                    f"   Eq 1: {lhs1} = {rhs1_val} → eff. RHS = {c1}\n"
                    f"   Eq 2: {lhs2} = {rhs2_val} → eff. RHS = {c2}\n")
            

        #   x= and y= appear FIRST so they are always visible at the top
        #   of the result box regardless of hint length.
        msg = (
            f"ℹ Note: Linear system solved.\n\n"
            f"Equation type:  Linear system (2×2)\n"
            f"Variables:      {v1}, {v2}\n"
            f"Determinant:    D = {int(D) if D==int(D) else round(D,4)}\n\n"
            f"   {v1}  =  {xi}\n"
            f"   {v2}  =  {yi}\n"
            f"{hint}"
            )
        self._alg_show(msg)
        self.history.add(f"[Algebra] {raw}", f"{v1}={xi}, {v2}={yi}")

    #   Solver: Quadratic
    def _solve_quadratic_from_str(self, lhs, rhs, raw):
        """Solve ax²+bx+c=k. : Only called when single variable confirmed."""
        self.alg_type_lbl.configure(
            text="TYPE: Quadratic equation  (ax²+bx+c=0)")

        try:
            rhs_val = float(rhs)
        except ValueError:
            self.alg_type_lbl.configure(text="TYPE: Format Error")
            self._alg_show(
                "ℹ Note: Invalid Right-Hand Side.\n\n"
                "For this type of equation, please move all variables\n"
                "to the left side so the right side is a pure number.\n\n"
                "Example: = 0  or  = 15"
            )
            return
            #rhs_val = 0.0

        m = re.search(r'([a-zA-Z])\^2', lhs)
        if not m:
            self.alg_type_lbl.configure(text="TYPE: Format Error")
            self._alg_show("ℹ Note: Could not find squared variable.\n\n"
                           "A quadratic equation requires a squared term\n"
                           "(e.g., x^2 or x²).")
            return
        var = m.group(1)

        coeffs = self._alg_parse_quad_coeffs(lhs, var)
        if coeffs is None:
            self.alg_type_lbl.configure(text="TYPE: Parsing Error")
            self._alg_show("ℹ Note: Could not parse quadratic equation.\n\n"
                           "Ensure the equation follows the standard format:\n"
                           "ax^2 + bx + c = 0")
            return

        a, b, c = coeffs
        c -= rhs_val

        if abs(a) < 1e-12:
            self.alg_type_lbl.configure(text="TYPE: Degenerate Case")
            self._alg_show(
                f"ℹ Note: Leading coefficient 'a' is zero.\n\n"
                f"This is not a quadratic equation. It simplifies to linear:\n"
                f"   {b}·{var} + {c} = 0"
            )
            return

        discriminant = b**2 - 4*a*c

        def fmt(z):
            if isinstance(z, complex) and abs(z.imag) < 1e-10:
                z = z.real
            if isinstance(z, (int, float)) and z == int(z):
                return str(int(z))
            if isinstance(z, complex):
                r = round(z.real, 6); i = round(z.imag, 6)
                sign = "+" if i >= 0 else "-"
                ri = int(r) if r==int(r) else r
                ii = abs(int(i)) if abs(i)==int(abs(i)) else abs(i)
                return f"{ri} {sign} {ii}i"
            return str(round(z, 8))

        sqrt_d = cmath.sqrt(discriminant)
        
        #   Adding Negative Zero Fix here!
        x1 = ((-b + sqrt_d) / (2*a)) + 0.0
        x2 = ((-b - sqrt_d) / (2*a)) + 0.0

        if discriminant > 1e-10:
            root_type = "Two distinct real roots"
        elif abs(discriminant) <= 1e-10:
            root_type = "One repeated real root"
        else:
            root_type = "Two complex conjugate roots"

        di = int(discriminant) if discriminant==int(discriminant) else round(discriminant,4)

        msg = (
            f"ℹ Note: Quadratic equation solved.\n\n"
            f"Equation type:  Quadratic\n"
            f"Variable:       {var}\n"
            f"Coefficients:   a={a}  b={b}  c={c}\n"
            f"Discriminant:   D = {di}\n"
            f"Root type:      {root_type}\n\n"
            f"   {var}₁  =  {fmt(x1)}\n"
            f"   {var}₂  =  {fmt(x2)}"
            )
        self._alg_show(msg)
        self.history.add(f"[Algebra] {raw}", f"{var}1={fmt(x1)}, {var}2={fmt(x2)}")

    #   Solver: Single bracket pair 
    def _solve_bracket_product(self, lhs, rhs, raw):
        """Expand (ax+b)(cx+d) then solve resulting quadratic."""
        self.alg_type_lbl.configure(
            text="TYPE: Bracket product  (expand → solve)")

        expanded, err = self._alg_expand_brackets(lhs)
        if err:
            self.alg_type_lbl.configure(text="TYPE: Expansion Error")
            self._alg_show(f"ℹ Note: Bracket expansion failed.\n\n{err}")
            return

        try:
            rhs_val = float(rhs)
        except ValueError:
            self.alg_type_lbl.configure(text="TYPE: Format Error")
            self._alg_show(
                "ℹ Note: Invalid Right-Hand Side.\n\n"
                "For this type of equation, please move all variables\n"
                "to the left side so the right side is a pure number.\n\n"
                "Example: = 0  or  = 15"
            )
            return

        simp, coeffs, err2 = self._alg_simplify(expanded)
        if err2:
            self._alg_show(f"ℹ Note: Simplification error.\n\n{err2}")
            return

        expand_info = f"Expanded:    {lhs}  =  {simp}\n"

        if abs(rhs_val) > 1e-12:
            expand_info += f"Rearranged:  {simp} − {rhs_val} = 0\n"
        expand_info += "\n"

        #   Now solve the expanded form
        if "^2" in expanded:
            m = re.search(r'([a-zA-Z])\^2', expanded)
            if not m:
                self._alg_show(expand_info + "Error: Could not identify variable.")
                return
            var = m.group(1)
            
            # --- Using robust dictionary extraction ---
            #   Bypasses the fragile regex parser entirely
            a = coeffs.get(f"{var}^2", 0.0)
            b = coeffs.get(var, 0.0)
            c = coeffs.get("", 0.0)
            c -= rhs_val
            
            if abs(a) < 1e-12:
                self._alg_show(expand_info + "Error: Quadratic coefficient 'a' is zero.")
                return
            
            discriminant = b**2 - 4*a*c
            sqrt_d = cmath.sqrt(discriminant)
            
            #   Applying Negative Zeros Fix Here!
            x1 = ((-b + sqrt_d) / (2*a)) + 0.0
            x2 = ((-b - sqrt_d) / (2*a)) + 0.0

            def fmt(z):
                if isinstance(z, complex) and abs(z.imag) < 1e-10:
                    z = z.real
                if isinstance(z, (int, float)) and z == int(z):
                    return str(int(z))
                if isinstance(z, complex):
                    r = round(z.real, 6); i = round(z.imag, 6)
                    sign = "+" if i >= 0 else "-"
                    return f"{r} {sign} {abs(i)}i"
                return str(round(z, 8))

            if discriminant > 1e-10:
                rt = "Two distinct real roots"
            elif abs(discriminant) <= 1e-10:
                rt = "One repeated real root"
            else:
                rt = "Two complex conjugate roots"

            di = int(discriminant) if discriminant==int(discriminant) else round(discriminant,4)
            msg = (expand_info +
                   f"Root type:   {rt}  (D = {di})\n\n"
                   f"  {var}₁  =  {fmt(x1)}\n"
                   f"  {var}₂  =  {fmt(x2)}")
        else:
            #   Expanded to linear
            m = re.search(r'([a-zA-Z])', expanded)
            var = m.group(1) if m else "x"

            #   Since we already ran simplify above, we can use the 'a' and 'b' from those coeffs
            a = coeffs.get(var, 0.0)
            b = coeffs.get("", 0.0)
            if abs(a) < 1e-12:
                msg = expand_info + "ℹ Note: No variable term found after expansion."
            else:
                val = (rhs_val - b) / a
                vi = int(val) if val == int(val) else round(val, 8)
                msg = expand_info + f"  {var}  =  {vi}"

        self._alg_show(msg)
        self.history.add(f"[Algebra] {raw}", msg.split('\n')[-1].strip())

    #   Solver: Multi-bracket (3+)
    def _solve_multi_bracket(self, lhs, rhs, raw):
        """
        Expand 3 or more bracket groups iteratively using polynomial
        multiplication (not FOIL — FOIL only works for binomial×binomial).

        Strategy: represent each polynomial as a dict {degree: coefficient},
        multiply them together term by term, then check the resulting degree.

        e.g. (m+1)(m-4)(m+2):
          poly1 = {1:1, 0:1}        → m + 1
          poly2 = {1:1, 0:-4}       → m - 4
          poly3 = {1:1, 0:2}        → m + 2
          poly1×poly2 = {2:1, 1:-3, 0:-4}   → m²-3m-4
          result × poly3 = {3:1, 2:-1, 1:-10, 0:-8} → m³-m²-10m-8
          degree 3 → cubic → show message
        """
        self.alg_type_lbl.configure(
            text="TYPE: Multi-bracket product  (polynomial expansion)")

        # ── Parse each bracket group into a polynomial dict ──
        #   {degree: coefficient}  e.g. 'm+1' → {1:1.0, 0:1.0}
        def parse_to_poly(bracket_str):
            """Parse 'ax+b' string into {degree: coeff} dict."""
            s = bracket_str.strip()
            if s and s[0] not in "+-":
                s = "+" + s
            tokens = re.findall(r'[+\-][^+\-]+', s)
            poly = {}
            for tok in tokens:
                tok = tok.strip()
                sign = 1.0 if tok[0] == "+" else -1.0
                body = tok[1:]

                #   power term: cx^n
                m_pow = re.fullmatch(r'(\d*\.?\d*)([a-zA-Z])\^(\d+)', body)
                if m_pow:
                    cs, _, deg = m_pow.groups()
                    coeff = float(cs) if cs else 1.0
                    poly[int(deg)] = poly.get(int(deg), 0.0) + sign * coeff
                    continue
                
                #   linear term: cx
                m_lin = re.fullmatch(r'(\d*\.?\d*)([a-zA-Z])', body)
                if m_lin:
                    cs, _ = m_lin.groups()
                    coeff = float(cs) if cs else 1.0
                    poly[1] = poly.get(1, 0.0) + sign * coeff
                    continue
                
                #   constant
                try:
                    poly[0] = poly.get(0, 0.0) + sign * float(body)
                except ValueError:
                    return None
            return poly

        def poly_multiply(p1, p2):
            """Multiply two polynomial dicts together."""
            result = {}
            for d1, c1 in p1.items():
                for d2, c2 in p2.items():
                    key = d1 + d2
                    result[key] = result.get(key, 0.0) + c1 * c2
            return result

        def poly_to_str(poly, var):
            """Format polynomial dict as readable string."""
            if not poly:
                return "0"
            terms = []
            for deg in sorted(poly.keys(), reverse=True):
                c = poly[deg]
                if abs(c) < 1e-12:
                    continue
                ci = int(c) if c == int(c) else round(c, 6)
                if deg == 0:
                    label = str(ci)
                elif deg == 1:
                    label = f"{var}" if abs(ci) == 1 else f"{ci}{var}"
                else:
                    label = f"{var}^{deg}" if abs(ci) == 1 else f"{ci}{var}^{deg}"

                if terms:
                    if c > 0:
                        terms.append(f"+{label}")
                    else:
                        #   For coeff=-1 with var, label is "var" not "-var"
                        #   so we must prefix the minus explicitly
                        if label.startswith("-"):
                            terms.append(label)
                        else:
                            terms.append(f"-{label}")
                else:
                    #   First term: include minus for negative unit-coefficient var terms
                    if c < 0 and abs(ci) == 1 and deg > 0:
                        terms.append(f"-{label}")
                    else:
                        terms.append(str(label))
            return "".join(terms) if terms else "0"

        #   Find all bracket groups
        groups = re.findall(r'\([^()]+\)', lhs)
        if len(groups) < 2:
            self.alg_type_lbl.configure(text="TYPE: Bracket Expansion Error")
            self._alg_show("⚠ Error: Expected multiple bracket groups (e.g., (x+1)(x+2)).")
            return

        #   Detect variable name
        var_list = self._alg_detect_vars(lhs)
        if len(var_list) > 1:
            self.alg_type_lbl.configure(text="TYPE: Polynomial Guard")
            self._alg_show(
                f"⚠ Unsupported Input: Multiple variables detected ({', '.join(var_list)}).\n\n"
                f"Multi-bracket expansion with multiple variables\n"
                f"produces complex cross-terms (e.g., xy, x²y).\n\n"
                f"Support for multi-variable polynomial expansion\n"
                f"is planned for a future update of {self.APP_NAME}."
            )
            return
        var = var_list[0] if var_list else "x"

        #   Parse each bracket into a polynomial dict
        polys = []
        steps = [f"Input:  {lhs} = {rhs}"]
        for grp in groups:
            inner = grp[1:-1]       # strip parentheses
            p = parse_to_poly(inner)
            if p is None:
                self._alg_show(f"Error: Cannot parse bracket {grp!r}")
                return
            polys.append(p)

        #   Multiply iteratively
        result_poly = polys[0]
        for i, p in enumerate(polys[1:], start=1):
            prev_str = poly_to_str(result_poly, var)
            result_poly = poly_multiply(result_poly, p)
            result_str = poly_to_str(result_poly, var)
            bracket_str = f"({poly_to_str(p, var)})"
            steps.append(f"Step {i}: ({prev_str}) × {bracket_str} = {result_str}")

        final_str = poly_to_str(result_poly, var)
        #try:
        #    rhs_val = float(rhs)
        #except ValueError:
        #    rhs_val = 0.0
        try:
            rhs_val = float(rhs)
        except ValueError:
            self.alg_type_lbl.configure(text="TYPE: Format Error")
            self._alg_show(
                "ℹ Note: Invalid Right-Hand Side.\n\n"
                "For this type of equation, please move all variables\n"
                "to the left side so the right side is a pure number.\n\n"
                "Example: = 0  or  = 15"
            )
            return
        # --- THE PRO FIX: Dynamic RHS Rearrangement ---
        if abs(rhs_val) > 1e-12:
            steps.append(f"\nExpanded:    {final_str} = {rhs_val}")
            # Subtract RHS from the constant term in the dictionary
            result_poly[0] = result_poly.get(0, 0.0) - rhs_val
            rearranged_str = poly_to_str(result_poly, var)
            steps.append(f"Rearranged:  {rearranged_str} = 0")
            final_str = rearranged_str  # Update for the UI output
        else:
            steps.append(f"\nFinal expanded form:  {final_str} = 0")
        
        header = "\n".join(steps) + "\n"
        final_deg  = max(result_poly.keys()) if result_poly else 0

        #   Now handle by degree
        if final_deg > 2:
            self._alg_show(
                header +
                f"\nℹ Note: Degree-{final_deg} Polynomial detected.\n\n"
                f"Analytic root extraction for degrees higher\n"
                f"than 2 (Quadratic) is outside the scope of {self.APP_NAME}.\n\n"
                f"  Tip: Numerical estimation for higher-order\n"
                f"  polynomials is planned for a future update."
            )

            self.history.add(f"[Algebra] {raw}",
                             f"Degree {final_deg} — expanded: {final_str}")
            return

        if final_deg == 2:
            #   Solve as quadratic from the polynomial dict
            a = result_poly.get(2, 0.0)
            b = result_poly.get(1, 0.0)
            c = result_poly.get(0, 0.0)

            if abs(a) < 1e-12:
                self._alg_show(header + "\nError: Quadratic coefficient is zero.")
                return

            disc = b**2 - 4*a*c
            sq   = cmath.sqrt(disc)
            x1   = (-b + sq) / (2*a)
            x2   = (-b - sq) / (2*a)

            def fmt(z):
                if isinstance(z, complex) and abs(z.imag) < 1e-10:
                    z = z.real
                if isinstance(z, (int, float)) and z == int(z):
                    return str(int(z))
                if isinstance(z, complex):
                    r = round(z.real, 6); im = round(z.imag, 6)
                    sign = "+" if im >= 0 else "-"
                    return f"{r} {sign} {abs(im)}i"
                return str(round(z, 8))

            di  = int(disc) if disc == int(disc) else round(disc, 4)
            rt  = ("Two distinct real roots" if disc > 1e-10
                   else "One repeated real root" if abs(disc) <= 1e-10
                   else "Two complex roots")

            msg = (header +
                   f"\nQuadratic:  a={a}  b={b}  c={c}\n"
                   f"D = {di}  →  {rt}\n\n"
                   f"  {var}₁  =  {fmt(x1)}\n"
                   f"  {var}₂  =  {fmt(x2)}")
            self._alg_show(msg)
            self.history.add(f"[Algebra] {raw}",
                             f"{var}1={fmt(x1)}, {var}2={fmt(x2)}")
            return

        #   Degree ≤ 1 — linear or constant
        a = result_poly.get(1, 0.0)
        c = result_poly.get(0, 0.0)
        if abs(a) < 1e-12:
            self._alg_show(header + f"\nResult is a constant: {c}")
        else:
            val = (-c) / a + 0.0
            vi  = int(val) if val == int(val) else round(val, 8)
            self._alg_show(header + f"\n  {var}  =  {vi}")
            self.history.add(f"[Algebra] {raw}", f"{var} = {vi}")
        
    def _alg_expand_brackets(self, expr):
        """
        Expand (ax+b)(cx+d) product.
        Returns (expanded_string, error_string).
        """
        expr = expr.replace(" ", "").replace("²", "^2")
        pat = r'\(([^()]+)\)\(([^()]+)\)'
        m   = re.search(pat, expr)
        if not m:
            return None, "Cannot expand — use the form (ax+b)(cx+d)"

        def parse_bin(s):
            if s and s[0] not in "+-":
                s = "+" + s
            tokens = re.findall(r'[+\-][^+\-]+', s)
            result = []
            for tok in tokens:
                parsed = self._alg_parse_term(tok)
                if parsed is None:
                    return None
                result.append(parsed)
            return result

        t1 = parse_bin(m.group(1))
        t2 = parse_bin(m.group(2))

        if t1 is None or t2 is None:
            return None, "Cannot parse terms inside brackets"

        prod = defaultdict(float)
        for (c1, v1) in t1:
            for (c2, v2) in t2:
                cc = c1 * c2
                if v1 and v2 and v1 == v2:
                    key = v1 + "^2"
                elif v1 and v2:
                    key = v1 + v2   # cross term
                else:
                    key = v1 + v2
                prod[key] += cc

        sq_keys  = sorted(k for k in prod if "^2" in k)
        lin_keys = sorted(k for k in prod if "^2" not in k and k != "")
        con_keys = [""] if "" in prod else []
        order    = sq_keys + lin_keys + con_keys

        parts = []
        for k in order:
            c = prod[k]
            if abs(c) < 1e-12:
                continue
            ci = int(c) if c == int(c) else round(c, 8)
            ts = k if abs(ci) == 1 and k else f"{ci}{k}"
            if parts:
                parts.append(f"+{ts}" if c > 0 else str(ts))
            else:
                parts.append(str(ts))

        expanded = "".join(parts) if parts else "0"
        return expanded, None

    #   Helpers
    def _alg_show(self, text):
        """Write text into the algebra result textbox."""
        self.alg_result.configure(state="normal")
        self.alg_result.delete("0.0", "end")
        self.alg_result.insert("end", text)
        self.alg_result.configure(state="disabled")

    def clear_algebra(self):
        """Clear both the input box and the result box."""
        self.alg_input.delete("0.0", "end")
        self.alg_type_lbl.configure(text="")
        self._alg_show("")

    # ═════════════════════════════════════════════════════
    #   TAB 4 — BMI CALCULATOR
    # ═════════════════════════════════════════════════════
    def _build_bmi_tab(self, parent):
        """
        BMI calculator with four enhancements:
          CHANGE 1 — Age field: under-18 shows a chart-redirect note
          CHANGE 2 — Gender field: shows body-fat context note for females
          CHANGE 3 — Imperial now uses Feet + Inches (not just inches)
          CHANGE 4 — Clear button resets all inputs and result panel
         
        """
        #   Plain frame — no scrollable wrapper needed, content fits the window
        scroll = ctk.CTkFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=4, pady=4)
        
        make_label(scroll, "⚖️  BMI Calculator",
                   font_size=14, bold=True).pack(anchor="w", pady=(0, 4))

        # ── Unit system selector ──────────────────────────
        inp_card = ctk.CTkFrame(scroll, corner_radius=10)
        inp_card.pack(fill="x", pady=(0, 6))

        unit_row = ctk.CTkFrame(inp_card, fg_color="transparent")
        unit_row.pack(fill="x", padx=10, pady=(8, 4))
        make_label(unit_row, "Unit system:", font_size=12).pack(side="left")

        self.bmi_unit = ctk.StringVar(value="metric")

        ctk.CTkRadioButton(
            unit_row, text="Metric",font=("Segoe UI", 12),
            variable=self.bmi_unit, value="metric",
            command=self._bmi_update_labels
        ).pack(side="left", padx=10)

        ctk.CTkRadioButton(
            unit_row, text="Imperial",font=("Segoe UI", 12),
            variable=self.bmi_unit, value="imperial",
            command=self._bmi_update_labels
        ).pack(side="left")

        # ── CHANGE 1: Age input ───────────────────────────
        age_row = ctk.CTkFrame(inp_card, fg_color="transparent")
        age_row.pack(fill="x", padx=10, pady=4)

        ctk.CTkLabel(age_row, text="Age (years):",
                     font=("Segoe UI", 12), width=110,
                     anchor="w").pack(side="left")
        self.bmi_age = ctk.CTkEntry(age_row, width=80, justify="center",
                                     placeholder_text="eg. 25")
        self.bmi_age.pack(side="left", padx=6)
        ctk.CTkLabel(age_row, text="(optional)",
                     font=ctk.CTkFont(family="Segoe UI",size= 10,slant="italic"),
                     text_color="gray").pack(side="left")

        # ── CHANGE 2: Gender selector ─────────────────────
        gender_row = ctk.CTkFrame(inp_card, fg_color="transparent")
        gender_row.pack(fill="x", padx=10, pady=4) 

        ctk.CTkLabel(gender_row, text="Gender:",
                     font=("Segoe UI", 12), width=70,  
                     anchor="w").pack(side="left")

        self.bmi_gender = ctk.StringVar(value="male")  # Default

        for label, val in [("Male", "male"),
                            ("Female", "female"),
                            ("Others", "not_specified")]:
            ctk.CTkRadioButton(
                gender_row, text=label,
                variable=self.bmi_gender, value=val,
                font=("Segoe UI", 12)
            ).pack(side="left", padx=1)  

        # ── Weight input ──────────────────────────────────
        weight_row = ctk.CTkFrame(inp_card, fg_color="transparent")
        weight_row.pack(fill="x", padx=10, pady=4)

        self.bmi_weight_lbl = ctk.CTkLabel(
            weight_row, text="Weight (kg):",
            font=("Segoe UI", 12), width=110, anchor="w")
        self.bmi_weight_lbl.pack(side="left")

        self.bmi_weight = ctk.CTkEntry(weight_row, width=90,
                                        justify="center",
                                        placeholder_text="eg. 100",
                                        placeholder_text_color="gray")
        self.bmi_weight.pack(side="left", padx=6)

        # ── CHANGE 3: Height — Metric (single cm field) ───
        #   For imperial we show TWO fields: feet and inches
        height_row = ctk.CTkFrame(inp_card, fg_color="transparent")
        height_row.pack(fill="x", padx=10, pady=(4, 10))

        self.bmi_height_lbl = ctk.CTkLabel(
            height_row, text="Height (cm):",
            font=("Segoe UI", 12), width=110, anchor="w")
        self.bmi_height_lbl.pack(side="left")

        #   Metric: one entry for cm
        self.bmi_height_cm = ctk.CTkEntry(height_row, width=90,
                                           justify="center",
                                           placeholder_text="eg. 170",
                                           placeholder_text_color="gray")
        self.bmi_height_cm.pack(side="left", padx=6)

        #   Imperial: feet + inches (hidden until imperial is selected)
        self.bmi_height_ft = ctk.CTkEntry(height_row, width=55,
                                           justify="center",
                                           placeholder_text="5",
                                           placeholder_text_color="gray")
        self.bmi_height_in = ctk.CTkEntry(height_row, width=55,
                                           justify="center",
                                           placeholder_text="11",
                                           placeholder_text_color="gray")
        self.bmi_ft_lbl  = ctk.CTkLabel(height_row, text="ft",
                                          font=ctk.CTkFont(family="Segoe UI",size= 11,slant="italic"))
        self.bmi_in_lbl  = ctk.CTkLabel(height_row, text="in",
                                          font=ctk.CTkFont(family="Segoe UI",size= 11,slant="italic"))
        #   Imperial fields are hidden by default (metric is default)

        # ── CHANGE 4: Calculate + Clear buttons ───────────
        bmi_btn_row = ctk.CTkFrame(scroll, fg_color="transparent")
        bmi_btn_row.pack(fill="x", pady=(0, 6))

        ctk.CTkButton(
            bmi_btn_row,
            text="Calculate BMI ↵",
            height=36, corner_radius=8,
            fg_color="#3b4cca", hover_color="#2a3aaa",
            command=self.calculate_bmi
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ctk.CTkButton(
            bmi_btn_row,
            text="🗑 Clear",
            height=36, corner_radius=8, width=90,
            fg_color="#8b1a1a", hover_color="#b22222",
            command=self.clear_bmi
        ).pack(side="left")

        # ── Result panel ──────────────────────────────────
        res_frame = ctk.CTkFrame(scroll, corner_radius=10)
        res_frame.pack(fill="x", pady=4)

        #   Large BMI number display
        self.bmi_value_lbl = ctk.CTkLabel(
            res_frame, text="—",
            font=("Segoe UI", 40, "bold")
        )
        self.bmi_value_lbl.pack(pady=(10, 0))

        #   Category with colour coding
        self.bmi_cat_lbl = ctk.CTkLabel(
            res_frame, text="Enter values above",
            font=("Segoe UI", 14), text_color="gray"
        )
        self.bmi_cat_lbl.pack(pady=(0, 2))

        #   Ideal weight range
        self.bmi_ideal_lbl = ctk.CTkLabel(
            res_frame, text="",
            font=("Segoe UI", 11), text_color="gray"
        )
        self.bmi_ideal_lbl.pack(pady=(0, 4))
        
        #   CHANGE 1 & 2: Context note
        self.bmi_note_lbl = ctk.CTkLabel(
            res_frame, text="",
            font=("Segoe UI", 10), 
            #   Light Mode: Warning Brown/ Gold (#856404) | Dark Mode: Original Amber (#f0a500)
            text_color=("#856404", "#f0a500"), 
            wraplength=340, justify="center"
        )

        self.bmi_note_lbl.pack(pady=(0, 10))

        # ── BMI scale reference ───────────────────────────
        scale_frame = ctk.CTkFrame(scroll, corner_radius=10)
        scale_frame.pack(fill="x", pady=4)

        make_label(scale_frame, "BMI Scale Reference",
                   font_size=11, bold=True).pack(anchor="w", padx=10, pady=(6, 2))

        #   Create a transparent sub-frame specifically for the grid alignment
        grid_frame = ctk.CTkFrame(scale_frame, fg_color="transparent")
        grid_frame.pack(anchor="w", padx=12)

        scale_data = [
            ("< 18.5", "Underweight", "#3a9bd5"),
            ("18.5 – 24.9", "Normal", "#27ae60"),
            ("25.0 – 29.9", "Overweight", "#e67e22"),
            ("≥ 30.0", "Obese", "#c0392b"),
        ]

        for r, (range_val, category, color) in enumerate(scale_data):
            #   Bullet point
            ctk.CTkLabel(grid_frame, text="●", font=("Segoe UI", 11, "bold"), 
                         text_color=color).grid(row=r, column=0, sticky="w", padx=(0, 6))
            #   Number range
            ctk.CTkLabel(grid_frame, text=range_val, font=("Segoe UI", 11, "bold"), 
                         text_color=color).grid(row=r, column=1, sticky="w", padx=(0, 15))
            #   Category name
            ctk.CTkLabel(grid_frame, text=category, font=("Segoe UI", 11, "bold"), 
                         text_color=color).grid(row=r, column=2, sticky="w")

        ctk.CTkLabel(scale_frame,
                     text="  ⚠  BMI is a general indicator. Muscle mass,\n"
                          "  age and gender affect its accuracy.",
                     font=ctk.CTkFont(family="Segoe UI",size= 9,slant="italic"), text_color="gray",
                     justify="left").pack(anchor="w", padx=12, pady=(4, 8))

    #   Update labels + show/hide fields
    def _bmi_update_labels(self):
        """
        Called when the user switches between Metric and Imperial.
        - Updates the weight label text
        - For Metric:   shows the single cm entry, hides ft/in entries
        - For Imperial: hides the cm entry, shows ft + in entries side by side
        """
        if self.bmi_unit.get() == "metric":
            #   Weight label
            self.bmi_weight_lbl.configure(text="Weight (kg):")
            #   Height label
            self.bmi_height_lbl.configure(text="Height (cm):")
            #   Show cm field, hide ft/in fields
            self.bmi_height_cm.pack(side="left", padx=6)
            self.bmi_height_ft.pack_forget()
            self.bmi_ft_lbl.pack_forget()
            self.bmi_height_in.pack_forget()
            self.bmi_in_lbl.pack_forget()
        else:
            #   Weight label
            self.bmi_weight_lbl.configure(text="Weight (lb):")
            #   Height label — imperial uses ft + in, not a single value
            self.bmi_height_lbl.configure(text="Height (ft/in):")
            #   Hide cm field, show ft and in fields
            self.bmi_height_cm.pack_forget()
            self.bmi_height_ft.pack(side="left", padx=(6, 2))
            self.bmi_ft_lbl.pack(side="left", padx=(0, 6))
            self.bmi_height_in.pack(side="left", padx=(0, 2))
            self.bmi_in_lbl.pack(side="left")

    def calculate_bmi(self):
        """
        Compute BMI and display result + category + ideal range + context note.

        Formulas:
          Metric   — BMI = weight_kg / height_m²
          Imperial — BMI = 703 × weight_lb / total_inches²
                     where total_inches = (feet × 12) + inches

        CHANGE 1 — Age:
          If age < 18 → BMI number is shown but category is replaced with
          a note to consult a BMI-for-age chart (adult thresholds don't apply).

        CHANGE 2 — Gender:
          If female → an informational note explains that women naturally
          carry higher body fat at the same BMI. The number is unchanged.

        CHANGE 3 — Imperial height:
          Two separate fields (feet + inches) are read and converted to
          total inches before applying the standard formula.

        CHANGE 4 — Clear: handled by clear_bmi() method below.
        """
        # ── Read age (optional) ───────────────────────────
        age_str = self.bmi_age.get().strip()
        age = None
        if age_str:
            try:
                age = int(age_str)
                if age <= 0:
                    raise ValueError
            except ValueError:
                self.bmi_cat_lbl.configure(
                    text="Enter a valid age (whole number)", text_color="red")
                return

        gender = self.bmi_gender.get()
        unit   = self.bmi_unit.get()

        # ── Read weight ───────────────────────────────────
        try:
            weight = float(self.bmi_weight.get())
            if weight <= 0:
                raise ValueError
        except ValueError:
            self.bmi_value_lbl.configure(text="⚠")
            self.bmi_cat_lbl.configure(
                text="Enter a valid weight", text_color="red")
            self.bmi_ideal_lbl.configure(text="")
            self.bmi_note_lbl.configure(text="")
            return

        # ── Read height and compute BMI ───────────────────
        try:
            if unit == "metric":
                height_cm = float(self.bmi_height_cm.get())
                if height_cm <= 0:
                    raise ValueError
                height_m  = height_cm / 100.0
                bmi       = weight / (height_m ** 2)
                # Ideal weight range in kg
                ideal_low  = 18.5 * height_m ** 2
                ideal_high = 24.9 * height_m ** 2
                ideal_unit = "kg"

            else:
                #   Read feet and inches separately
                feet_str = self.bmi_height_ft.get().strip()
                inch_str = self.bmi_height_in.get().strip()

                #   Allow feet-only or feet+inches
                feet   = float(feet_str) if feet_str else 0
                inches = float(inch_str) if inch_str else 0

                total_inches = feet * 12 + inches   # convert to total inches

                if total_inches <= 0:
                    raise ValueError("Height must be greater than zero")

                bmi = 703 * weight / (total_inches ** 2)

                #   Ideal range in lb — back-calculated from BMI 18.5–24.9
                height_m   = total_inches * 0.0254   # inches → metres
                ideal_low  = 18.5 * height_m ** 2 / 0.453592
                ideal_high = 24.9 * height_m ** 2 / 0.453592
                ideal_unit = "lb"

        except ValueError as ve:
            self.bmi_value_lbl.configure(text="⚠")
            self.bmi_cat_lbl.configure(
                text=f"Enter valid height values", text_color="red")
            self.bmi_ideal_lbl.configure(text="")
            self.bmi_note_lbl.configure(text="")
            return

        #   Under-18 check
        if age is not None and age < 18:
            #   Show BMI number but override category with child-specific note
            self.bmi_value_lbl.configure(text=f"{bmi:.1f}")
            self.bmi_cat_lbl.configure(
                text="Age < 18 — see BMI-for-age chart",
                text_color=("#856404", "#f0a500")
            )
            self.bmi_ideal_lbl.configure(text="")
            self.bmi_note_lbl.configure(
                text="⚠  Adult BMI thresholds (18.5 / 25 / 30) do not apply\n"
                     "to children and teenagers. Please consult a\n"
                     "paediatrician or use a BMI-for-age percentile chart.",
                text_color=("#856404", "#f0a500")         

            )
            self.history.add(
                
                f"[BMI] Age={age} | Weight={weight} | BMI",
                f"{bmi:.1f} (child — chart required)"
            )
            return

        # ── Standard adult category ───────────────────────
        if bmi < 18.5:
            category, color = "Underweight",      "#3a9bd5"
        elif bmi < 25.0:
            category, color = "Normal weight ✓",  "#27ae60"
        elif bmi < 30.0:
            category, color = "Overweight",       "#e67e22"
        else:
            category, color = "Obese",            "#c0392b"

        # ── CHANGE 2: Gender-based context note ──────────
        note = ""
        if gender == "female":
            note = ("ℹ  Women naturally carry higher body fat than men\n"
                    "at the same BMI. BMI may slightly overestimate risk\n"
                    "for women at the higher end of 'Normal'.")
        elif gender == "male" and 30.0 >= bmi >= 25.0:
            note = ("ℹ  If you are muscular or athletic, BMI may\n"
                    "overestimate body fat. Consider waist measurement\n"
                    "as an additional health indicator.")

        # ── Update result panel ───────────────────────────
        self.bmi_value_lbl.configure(text=f"{bmi:.1f}")
        self.bmi_cat_lbl.configure(text=category, text_color=color)
        self.bmi_ideal_lbl.configure(
            text=f"Ideal weight for this height: "
                 f"{ideal_low:.1f} – {ideal_high:.1f} {ideal_unit}"
        )
        self.bmi_note_lbl.configure(text=note)

        # ── Save to shared history ────────────────────────
        self.history.add(
            f"[BMI] | {'Metric' if unit=='metric' else 'Imperial'} | "
            f"W:{weight} | "
            f"H:{self.bmi_height_cm.get() if unit=='metric' else str(feet)+'ft '+str(inches)+'in'} | BMI",
            f"{bmi:.1f} ({category})"

        )

    #   Clear BMI
    def clear_bmi(self):
        """
        Reset the BMI calculator completely:
        - Clears all input fields (weight, height cm, height ft/in, age)
        - Resets gender to 'not specified'
        - Resets result panel to its initial placeholder state
        """
        #   Clear all entry widgets
        for entry in (self.bmi_weight, self.bmi_height_cm,
                      self.bmi_height_ft, self.bmi_height_in, self.bmi_age):
            entry.delete(0, "end")

        #   Reset gender radio back to default
        self.bmi_gender.set("male")

        #   Reset the result panel to its blank/placeholder state
        self.bmi_value_lbl.configure(text="—")
        self.bmi_cat_lbl.configure(text="Enter values above", text_color="gray")
        self.bmi_ideal_lbl.configure(text="")
        self.bmi_note_lbl.configure(text="")


    # ═════════════════════════════════════════════════════
    #   TAB 4 — UNIT CONVERTER
    # ═════════════════════════════════════════════════════
    def _build_converter_tab(self, parent):
        """
        Unit converter with:
          - Category selector (Length / Weight / Temperature / Speed / Area)
          - Dynamic from/to unit dropdowns
          - Swap button
          - Live update on every keystroke
        """
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        make_label(frame, "🔄  Unit Converter",
                   font_size=14, bold=True).pack(anchor="w", pady=(0, 6))
        
        # ── Unified Form Grid ─────────────────────────────
        #   We put everything in one frame using a grid for pixel-perfect alignment
        form_frame = ctk.CTkFrame(frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=10, pady=(10, 20))

        #   Define grid columns: 0=Labels, 1=Dropdowns, 2=Input Box
        form_frame.grid_columnconfigure(0, weight=0, minsize=70)  
        form_frame.grid_columnconfigure(1, weight=0, minsize=190) 
        form_frame.grid_columnconfigure(2, weight=1)              

        #   Category Row
        make_label(form_frame, "Category:", font_size=12).grid(row=0, column=0, sticky="w", pady=(0, 15))
        self.conv_category = ctk.CTkOptionMenu(
            form_frame, 
            values=list(UNIT_DATA.keys()), 
            command=self._conv_category_changed, 
            width=180
        )
        self.conv_category.grid(row=0, column=1, sticky="w", pady=(0, 15))
        self.conv_category.set("Length")   # default

        #   From Row
        make_label(form_frame, "From:", font_size=12).grid(row=1, column=0, sticky="w", pady=4)
        self.conv_from_unit = ctk.CTkOptionMenu(
            form_frame, values=[], width=180,
            command=lambda _: self._do_conversion(save_to_history=True)
        )
        self.conv_from_unit.grid(row=1, column=1, sticky="w", pady=4)
        
        #   Define the fonts for swapping ---
        italic_font = ctk.CTkFont(slant="italic")
        normal_font = ctk.CTkFont(slant="roman")
        
        self.conv_input = ctk.CTkEntry(
            form_frame, width=110, justify="center", placeholder_text="value",
            placeholder_text_color= "gray",font = italic_font
        )
        self.conv_input.grid(row=1, column=2, sticky="w", padx=10, pady=4)
        # --- 3. Create a combined handler that protects your conversion logic ---
        def handle_key_release(_):
            # Swap the font
            if self.conv_input.get() == "":
                self.conv_input.configure(font=italic_font)
            else:
                self.conv_input.configure(font=normal_font)
            # Run your original live conversion
            self._do_conversion()
        #   Bindings for input
        self.conv_input.bind("<KeyRelease>", handle_key_release)
        self.conv_input.bind("<Return>", lambda _: self._do_conversion(save_to_history=True))

        #   Swap Button Row
        #   Notice we put it in column=1 so it aligns perfectly UNDER the dropdowns
        swap_btn = ctk.CTkButton(
            form_frame, text="⇄  Swap units", width=140, height=28, 
            corner_radius=6, command=self._conv_swap
        )
        swap_btn.grid(row=2, column=1, sticky="w", padx=20, pady=8)

        #   To Row
        make_label(form_frame, "To:", font_size=12).grid(row=3, column=0, sticky="w", pady=4)
        self.conv_to_unit = ctk.CTkOptionMenu(
            form_frame, values=[], width=180,
            command=lambda _: self._do_conversion(save_to_history=True)
        )
        self.conv_to_unit.grid(row=3, column=1, sticky="w", pady=4)


        # ── Result display ────────────────────────────────
        res_frame = ctk.CTkFrame(frame, corner_radius=10)
        res_frame.pack(fill="x", pady=6)

        make_label(res_frame, "Result:", font_size=11,
                   color="gray").pack(anchor="w", padx=10, pady=(6,0))

        self.conv_result_lbl = ctk.CTkLabel(
            res_frame, text="—",
            font=("Segoe UI", 26, "bold"),
            anchor="center",
        )
        self.conv_result_lbl.pack(fill="x", padx=10, pady=(0,4))

        self.conv_formula_lbl = ctk.CTkLabel(
            res_frame, text="",
            font=("Segoe UI", 10,"italic"), text_color="gray"
        )
        self.conv_formula_lbl.pack(pady=(0,8))
        
        # --- ADD HISTORY HINT HERE ---
        self.conv_hint_lbl = ctk.CTkLabel(
            res_frame, 
            text="ℹ Press Enter ↵ to save to history", 
            text_color="gray", 
            font=ctk.CTkFont(family="Segoe UI", size=11,weight="bold",slant= "italic") 
        )
        self.conv_hint_lbl.pack(pady=(0, 10))
        # -------------------------
        
        #   Populate unit dropdowns for the default category
        self._conv_category_changed("Length")

    def _conv_category_changed(self, category):
        """Called when the user selects a new category. Repopulate the unit dropdowns."""
        units = list(UNIT_DATA[category].keys())

        self.conv_from_unit.configure(values=units)
        self.conv_to_unit.configure(values=units)

        #   Sensible defaults: first unit → second unit
        self.conv_from_unit.set(units[0])
        self.conv_to_unit.set(units[1] if len(units) > 1 else units[0])

        #   Clear result when category changes — no history save,
        #   this is just a UI reset not a completed conversion
        self.conv_result_lbl.configure(text="—")
        self.conv_formula_lbl.configure(text="")
        self._do_conversion()

    def _conv_swap(self):
        """Swap the from and to unit selections, then re-convert.
        Saves to history — swapping units with a value present is
        a deliberate user action that produces a meaningful result."""
        f = self.conv_from_unit.get()
        t = self.conv_to_unit.get()
        self.conv_from_unit.set(t)
        self.conv_to_unit.set(f)
        self._do_conversion(save_to_history=True)

    def _do_conversion(self, save_to_history=False):
        """
        Read input value and selected units, call convert_units(),
        and update the result label.

        Called on every keystroke (save_to_history=False) so the display
        updates live, but only saves to history when save_to_history=True
        — triggered by Enter key or unit dropdown change — to avoid
        flooding history with a new entry for every digit typed.
        """
        raw = self.conv_input.get().strip()
        if not raw:
            self.conv_result_lbl.configure(text="—")
            self.conv_formula_lbl.configure(text="")
            return

        try:
            value = float(raw)
        except ValueError:
            self.conv_result_lbl.configure(text="⚠ Invalid Input")
            self.conv_formula_lbl.configure(text="")
            return

        category  = self.conv_category.get()
        from_unit = self.conv_from_unit.get()
        to_unit   = self.conv_to_unit.get()

        try:
            result = convert_units(value, category, from_unit, to_unit)
        except Exception as ex:
            self.conv_result_lbl.configure(text=f"Error: {ex}")
            return

        #   Format result — avoid very long floats
        if result == int(result) and abs(result) < 1e12:
            result_str = f"{int(result):,}"
        elif abs(result) > 1e10 or (abs(result) < 1e-4 and result != 0):
            result_str = f"{result:.6e}"
        else:
            result_str = f"{result:.8g}"

        #   Friendly unit labels — strip the bracketed abbreviation for display
        from_label = from_unit.split('(')[0].strip()
        to_label   = to_unit.split('(')[0].strip()

        self.conv_result_lbl.configure(
            text=f"{result_str}  {to_label}"
        )
        self.conv_formula_lbl.configure(
            text=f"{value} {from_label}  →  {result_str} {to_label}"
        )

        #   Save to shared history — only when explicitly requested
        #   (Enter key press or dropdown unit change), never on raw keystrokes
        if save_to_history:
            self.history.add(
                f"[Converter] {value} {from_label} → {to_label}",
                f"{result_str} {to_label}"
            )


    # ═════════════════════════════════════════════════════
    #   SCIENTIFIC CALCULATOR — INPUT HANDLING
    # ═════════════════════════════════════════════════════
    def insert(self, d, v=None):
        """
        Handle button/keyboard input for the scientific calculator.
        d = display character(s),  v = backend expression value (may differ).

        POSTFIX FUNCTION MODE:
        When a function button (sin, cos, tan, log, ln, sqrt) is pressed
        and the current expression already ends with a number, the number
        is wrapped inside the function instead of appending 'func(' after it.

        Example:
          User presses 9, 0  → display shows "90"
          User presses sin   → display shows "sin(90)"  ✓
          (old behaviour would show "90sin(" which is wrong)

        This matches the Windows Calculator style where you type the number
        first and then press the function.
        """
        
        self.display.configure(state="normal")
        current_display = self.display.get()

        #   Clear error state before accepting new input
        if "Error" in current_display or "Domain" in current_display \
                or "Go to" in current_display or "Close" in current_display:
            self.clear()
            current_display = ""

        #   Postfix function wrapping ─────────────────
        #   Detect if a function button was pressed (v ends with "(")
        #   AND the expression currently ends with a number.
        if v and v.endswith("(") and self.expression:
            #   Extract the trailing number from the current expression
            #   using a regex that matches integers and decimals
            trailing = re.search(r'(\d+\.?\d*)$', self.expression)
            if trailing:
                number     = trailing.group(1)       # e.g. "90"
                before_num = self.expression[:trailing.start()]  # everything before it

                #   Rebuild expression as: prefix + func(number)
                #   e.g. expression="90"  → "sin(90)"
                #   e.g. expression="1+90" → "1+sin(90)"
                self.expression = f"{before_num}{v}{number})"

                #   Rebuild display to match
                display_before = current_display[:len(current_display) - len(number)]
                self.display.delete(0, "end")
                self.display.insert("end", f"{display_before}{d}({number})")
                self.display.configure(state="readonly")
                return

        #   Post-result input handling
        if self.reset_next:
            if v and v.endswith("("):
                #   Pressed a function right after = result → wrap result in it
                self.expression = f"{v}{self.last_result})"
                self.display.configure(state="normal")
                self.display.delete(0, "end")
                self.display.insert("end", f"{d}({self.last_result})")
                self.reset_next = False
                self.display.configure(state="readonly")
                return

            if d in "+-*/^÷×":
                #   Operator after result → continue from result
                self.expression = self.last_result + (v if v is not None else d)
                self.display.configure(state="normal")
                self.display.delete(0, "end")
                self.display.insert("end", self.expression)
                self.reset_next = False
                self.display.configure(state="readonly")
                return
            
            #   Handle % right after = (Ensures decimal integrity)
            if d == "%" and self.reset_next:
                #   Use float() to ensure we are dealing with the true numerical value
                #   and format it to 10 decimal places to avoid scientific notation bugs
                val = float(self.last_result)
                clean_val = "{:.10f}".format(val).rstrip('0').rstrip('.')
                self.expression = f"({clean_val})%"
    
                self.display.configure(state="normal")
                self.display.delete(0, "end")
                self.display.insert("end", self.expression)
                self.reset_next = False
                self.display.configure(state="readonly")
                return
            
            if d.isdigit() or d == ".":
                #   New number → clear and start fresh
                self.display.configure(state="normal")
                self.display.delete(0, "end")
                self.expression = v if v is not None else d
                self.display.insert("end", d)
                self.reset_next = False
                self.display.configure(state="readonly")
                return

        #   Normal append
        self.display.insert("end", d)
        self.expression += v if v is not None else d
        self.display.configure(state="readonly")

    # ─────────────────────────────────────────────────────
    #   EDITING COMMANDS
    # ─────────────────────────────────────────────────────
    def clear(self):
        """AC — clear everything."""
        self.expression = ""
        self.last_result = ""
        self.reset_next = False
        self.display.configure(state="normal")
        self.display.delete(0, "end")
        self.display.configure(state="readonly")

    def clear_entry(self):
        """CE — remove the last number token from the expression."""
        self.expression = re.sub(r'[\d.]+$', '', self.expression)
        self.display.configure(state="normal")
        self.display.delete(0, "end")
        self.display.insert("end", self.expression)
        self.display.configure(state="readonly")

    def backspace(self):
        """⌫ — delete the last character; keep display in sync with expression."""
        if not self.expression:
            return
        self.expression = self.expression[:-1]
        self.display.configure(state="normal")
        self.display.delete(0, "end")
        self.display.insert("end", self.expression)
        self.display.configure(state="readonly")

    # ═════════════════════════════════════════════════════
    #   SCIENTIFIC CALCULATOR — CALCULATION ENGINE
    # ═════════════════════════════════════════════════════
    def calculate(self):
        """
        Evaluate self.expression and display the result.
        Pipeline:
          1. Repeat-= tail restore (if expression is empty)
          2. Alphabet/variable detection
          3. Remove leading zeros safely (e.g. "007" → "7", but "0.05" stays "0.05")
          4. Capture repeat-= tail for next time (e.g. "45+3" → last_expr_tail = "+3")
          5. Symbol normalisation (×→*, ^→**)
          6. Constant substitution (π, e)
          7. FIBS early-exit handler (series cannot be part of arithmetic)
          8. Auto-close open brackets
          9. Factorial / percent expansion
          10. Shorthand function notation  (sin30 → sin(30))
          11. Implicit multiplication  (2π, 2sin(30), 2(5+3))
          12. AST parse + safe evaluation
          13. Format result + update display + history

        """
        
        try:
            #   Repeat = uses last operator tail
            if not self.expression and self.last_expr_tail:
                expr = self.display.get() + self.last_expr_tail
            else:
                expr = self.expression.lower()

            #   Alphabet / variable detection
            #   If the expression contains letters that are NOT part of a known
            #   function or constant name (e.g. 'a', 'b', 'x', 'y'), the user
            #   is trying to write an algebraic expression like "6a+2b".
            #   We detect this BEFORE any processing and show a helpful message.
            #   Known safe identifiers that should NOT trigger this warning:
            KNOWN_NAMES = {
                "sin", "cos", "tan", "log", "ln", "sqrt",
                "fib", "fibs", "npr", "ncr", "fact",
                "bin", "dec", "hex", "pi", "e"
            }
            #   Strip all known names from a copy, then check if any letters remain
            expr_check = expr
            for name in sorted(KNOWN_NAMES, key=len, reverse=True):
                expr_check = expr_check.replace(name, "")
            if re.search(r'[a-z]', expr_check):
            #   Letters remain after removing all known function/constant names
            #   → user typed a variable like 'a', 'b', 'x', 'y'
            #   self.show_error("Go to Algebra Tab") 0riginal statement
            #   1. Update Scientific display with the message
                self.display.configure(font=("Consolas", 18, "bold"))
                self.show_error("Redirecting to Algebra Mode...")
            
            #   2. Prepare the Algebra tab (background work)
                self.alg_input.delete("0.0", "end")
                self.alg_input.insert("0.0", expr) # Carry over the text
            
            #   3. DELAYED SWITCH: Wait 450ms so the user can read the display
                self.after(450, lambda: [
                    self.tabs.set("🔣 Algebra "),
                    # Reset Scientific font for the next time the user comes back
                    self.display.configure(state="normal"), # Unlock display
                    self.display.delete(0, "end"),          # CLEAR the stale message
                    self.display.configure(
                        font=("Consolas", 28, "bold"),      # Reset font size
                        state="readonly"                    # Lock display back
                    )               
                ])
                return

            #   Remove leading zeros SAFELY
            #   Using a negative lookbehind (?<!\.) to ensure we don't strip 
            #   zeros that come after a decimal point.
            expr = re.sub(r'(?<!\.)\b0+(\d+)', r'\1', expr)

            #   Capture repeat-= tail before replacing symbols
            match = re.search(r'([\+\-\*/]\d+\.?\d*)$', expr)
            if match:
                self.last_expr_tail = match.group(1)

            #   Symbol → Python operator
            expr = expr.replace("×", "*")
            expr = expr.replace("^", "**")

            #   Constants
            expr = expr.replace("π", str(math.pi))
            expr = re.sub(r'\be\b', str(math.e), expr)

            #   Auto-close FIRST, then run the fibs check on the completed string.
            open_count = expr.count("(") - expr.count(")")
            if open_count > 0:
                expr += ")" * open_count

            #   FIBS short-circuit (Now runs on auto-closed expression)
            if "fibs(" in expr and any(o in expr for o in "+-*/"):
                self.show_error("Standalone FIBS only")
                return

            fibs_match = re.search(r'fibs\((\d+)\)', expr)
            if fibs_match:
                self._handle_fibs(int(fibs_match.group(1)))
                return

            #   Smart bracket handling
            #   Only auto-close when exactly 1 bracket is unclosed.
            #   That case is always safe: e.g. sqrt(16 → sqrt(16) is unambiguous.
            #   When 2+ brackets are open, the nesting is ambiguous — we cannot
            #   know if the user meant sin(90)+cos(0) or sin(90+cos(0)).
            #   Silently closing all of them produces wrong answers (sin(91)≈0.99).
            #   Instead, tell the user exactly how many brackets to close.
            open_count = expr.count("(") - expr.count(")")
            if open_count == 1:
                expr += ")"     # safe — single trailing bracket, auto-close
            elif open_count > 1:
                self.show_error(f"Close {open_count} bracket(s) first")
                return
            expr = re.sub(r'(\d+)!', r'fact(\1)', expr)
            
            #   Ironclad Percentage Handler
            #   We use a loop to ensure nested or multiple percentages are all resolved.
            #   It matches digits (56%) or closed parentheses ((...)) followed by %.
            while "%" in expr:
                idx = expr.find("%")
                #   If % follows a bracket, find the matching start bracket
                if idx > 0 and expr[idx-1] == ")":
                    stack, target_start = 0, -1
                    for i in range(idx-1, -1, -1):
                        if expr[i] == ")": stack += 1
                        if expr[i] == "(": stack -= 1
                        if stack == 0:
                            target_start = i
                            break
                    if target_start != -1:
                        expr = expr[:target_start] + f"({expr[target_start:idx]}/100)" + expr[idx+1:]
                    else: break 
                else:
                    #   If % follows a number
                    match = re.search(r'(\d+\.?\d*)%$', expr[:idx+1])
                    if match:
                        expr = expr[:match.start()] + f"({match.group(1)}/100)" + expr[idx+1:]
                    else:
                        expr = expr.replace("%", "/100", 1) # Fallback for solo %
                        break

            #   Shorthand  (sin30 → sin(30))
            for fn in ["sin", "cos", "tan", "log", "ln", "sqrt"]:
                expr = re.sub(rf'{fn}(\d+)', rf'{fn}(\1)', expr)

            #   Implicit multiplication
            expr = re.sub(r'(\d)(pi|e)', r'\1*\2', expr)

            #   (FIBS): 'fib(?!s)' matches 'fib(' but NOT 'fibs(' 
            #   The old pattern 'fib' is a prefix of 'fibs', so fibs(5) was
            #   being rewritten to fib*s(5) before the fibs check could catch it.
            #   The negative lookahead (?!s) prevents that mangling.
            expr = re.sub(r'(\d)(sin|cos|tan|log|ln|sqrt|fib(?!s))\(', r'\1*\2(', expr)
            expr = re.sub(r'(\d)\(', r'\1*(', expr)

            #   AST safe evaluation
            tree   = ast.parse(expr, mode='eval')
            result = self.eval_ast(tree.body)

            #   Format result
            result = self._fmt_result(result)

            #   Update display
            self.display.configure(state="normal")
            self.display.delete(0, "end")
            self.display.insert("end", result)
            self.display.configure(state="readonly")

            #   Preserve state for chaining
            self.expression = ""
            self.last_result = str(result)
            self.reset_next  = True
            self.history.add(f"[Scientific] {expr}", result)

        except ZeroDivisionError:
            self.show_error("Zero Division Error")
        except ValueError as e:
            if "math domain error" in str(e).lower():
                self.show_error("Math Domain Error")
            else:
                self.show_error("Error: Invalid Expression")
        except Exception as e:
            print("DEBUG:", e)
            self.show_error("Error: Invalid Expression")

    def _fmt_result(self, result):
        """Format a numeric result — apply scientific notation for very large/small values."""
        if isinstance(result, float):
            if abs(result) > 1e12 or (abs(result) < 1e-8 and result != 0):
                return f"{result:.8e}"
            else:
                return f"{result:.8g}"
        return result                                   # int or already-formatted string

    def _handle_fibs(self, n):
        """Generate Fibonacci series and display in popup for n > 10."""
        a, b = 0, 1
        series = []
        for _ in range(n):
            series.append(str(a))
            a, b = b, a + b
        result_text = ", ".join(series)

        self.history.add(f"[Scientific] FIBS({n})", result_text)

        if n <= 8:
            self.display.configure(state="normal")
            self.display.delete(0, "end")
            self.display.insert("end", result_text)
            self.display.configure(state="readonly")
            return

        #   Reuse or create popup window
        if self.fib_window is None or not self.fib_window.winfo_exists():
            self.fib_window = ctk.CTkToplevel(self)
            self.fib_window.title("Fibonacci Series")
            self.update_idletasks()
            x = self.winfo_x() + self.winfo_width() + 50
            y = self.winfo_y() + self.winfo_height() - 280
            self.fib_window.geometry(f"320x220+{x}+{y}")
            self.fib_box = ctk.CTkTextbox(self.fib_window, wrap="word",font=("Consolas", 13))
            self.fib_box.pack(fill="both", expand=True, padx=6, pady=6)

        self.fib_box.delete("0.0", "end")
        self.fib_box.insert("end", result_text)


    # ═════════════════════════════════════════════════════
    #   AST EVALUATION ENGINE  (safe — no eval() or exec())
    # ═════════════════════════════════════════════════════
    def eval_ast(self, node):
        """
        Recursively evaluate a Python AST node using only explicitly
        whitelisted operations and functions.
        No eval() or exec() — this is the secure approach.
        """
        #   Literal number
        if isinstance(node, ast.Constant):
            return node.value

        #   Binary operation: left OP right
        elif isinstance(node, ast.BinOp):
            left  = self.eval_ast(node.left)
            right = self.eval_ast(node.right)
            if isinstance(node.op, ast.Add):  return left + right
            if isinstance(node.op, ast.Sub):  return left - right
            if isinstance(node.op, ast.Mult): return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError
                return left / right
            if isinstance(node.op, ast.Pow):  return left ** right

        #   Unary operation: -x or +x
        elif isinstance(node, ast.UnaryOp):
            val = self.eval_ast(node.operand)
            if isinstance(node.op, ast.UAdd): return +val
            if isinstance(node.op, ast.USub): return -val

        #   Named constant: pi, e
        elif isinstance(node, ast.Name):
            if node.id == "pi": return math.pi
            if node.id == "e":  return math.e
            raise Exception(f"Unknown name: {node.id}")

        #   Function call: sin(x), sqrt(x), etc.
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise Exception("Invalid function call")
            func = node.func.id
            args = [self.eval_ast(a) for a in node.args]

            #   Trigonometric
            if func == "sin":
                return math.sin(math.radians(args[0])) if self.mode == "DEG" \
                       else math.sin(args[0])
            if func == "cos":
                return math.cos(math.radians(args[0])) if self.mode == "DEG" \
                       else math.cos(args[0])
            if func == "tan":
                return math.tan(math.radians(args[0])) if self.mode == "DEG" \
                       else math.tan(args[0])

            #   Logarithms / Roots
            if func == "log":  return math.log10(args[0])
            if func == "ln":   return math.log(args[0])
            if func == "sqrt": return math.sqrt(args[0])

            #   Combinatorics
            if func == "fact":
                return math.factorial(int(args[0]))
            if func == "npr":
                n, r = int(args[0]), int(args[1])
                return math.factorial(n) // math.factorial(n - r)
            if func == "ncr":
                n, r = int(args[0]), int(args[1])
                return math.factorial(n) // (math.factorial(r) *
                                             math.factorial(n - r))

            #   Base conversion
            if func == "bin": return bin(int(args[0]))[2:]
            if func == "hex": return hex(int(args[0]))[2:].upper()
            if func == "dec": return int(str(args[0]), 2)

            #   Fibonacci (single value)
            if func == "fib":
                n = int(args[0])
                if n == 0: return 0
                a, b = 0, 1
                for _ in range(n - 1):   # range(n-1) is correct
                    a, b = b, a + b
                return b

            raise Exception(f"Unknown function: {func}")

        else:
            raise Exception("Invalid expression node")


    # ═════════════════════════════════════════════════════
    #   UI HELPERS
    # ═════════════════════════════════════════════════════
 
    def show_about(self):
        """Opens a single About window and shakes if already open."""
        #   1. Check if window exists and is not destroyed
        if hasattr(self, 'about_win') and self.about_win.winfo_exists():
            self.about_win.focus()  # Bring to front
            self._shake_window(self.about_win) # Trigger the "No" shake
            return

        #   2. If it doesn't exist, create it
        self.about_win = ctk.CTkToplevel(self)
        self.about_win.title("About CalcSuite Pro")
        self.about_win.attributes("-topmost", True)
        
        #   Center the window
        x = self.winfo_x() + 40
        y = self.winfo_y() + 100
        self.about_win.geometry(f"330x320+{x}+{y}")
        
        #   CONTENT
        make_label(self.about_win, self.APP_NAME, font_size=20, bold=True).pack(pady=(20, 5))
        make_label(self.about_win, "Developed by:", font_size=10, color="gray").pack()
        make_label(self.about_win, "Yousuf S. R. Sakkaf", font_size=14, bold=True).pack(pady=(0, 10))
        
        #   The Bridge Note
        make_label(self.about_win, "Powered by the Digi-ToolKit Interface", 
                   font_size=10,bold=True, italic=True, color="#2a9d8f").pack()
        
        desc = "From its humble beginnings as a basic calculator (v1.0) \n" \
                "to the advanced Digi-ToolKit interface of today,\n" \
                " CalcSuite Pro has evolved into a professional workstation for :\n" \
                "algebraic, scientific, and analytical logic."
        
        make_label(self.about_win, desc, font_size=11,italic=True).pack(pady=10)
        
        features = "Scientific Calculator  |  Algebra Workspace\n  Health (BMI)            |       Unit Conversion"
        make_label(self.about_win, features, font_size=10, bold=True).pack(pady=5)
        
        ctk.CTkButton(self.about_win, text="Close", width=100,fg_color="Teal", 
                      command=self.about_win.destroy).pack(pady=(15, 20))

    def _shake_window(self, window):
        """Creates the professional Windows-style shake effect."""
        orig_x = window.winfo_x()
        orig_y = window.winfo_y()
        #   Shake left and right 3 times
        for i in range(3):
            for offset in [5, -5]:
                window.geometry(f"+{orig_x + offset}+{orig_y}")
                window.update()
                window.after(30)
        #   Snap back to original position
        window.geometry(f"+{orig_x}+{orig_y}")    


    def show_error(self, msg):
        """Display an error message in the calculator display."""
        self.display.configure(state="normal")
        self.display.delete(0, "end")
        self.display.insert("end", msg)
        self.display.configure(state="readonly")
        self.expression = ""
        self.reset_next = False

    def toggle_mode(self):
        """Switch the trig angle mode between DEG and RAD."""
        self.mode = "RAD" if self.mode == "DEG" else "DEG"
        self.mode_label.configure(text=self.mode)

    def toggle_theme(self):
        """Switch between dark and light appearance modes."""
        current = ctk.get_appearance_mode().lower()
        ctk.set_appearance_mode("light" if current == "dark" else "dark")

    def show_history(self):
        """
        Open (or bring to front) the shared 24-hour history window.
        Reuses the same popup instead of opening a new one each time.
        """
        if self.history_win and self.history_win.winfo_exists():
            self.history_win.focus()
            #   Refresh content
            self.history_box.configure(state="normal")
            self.history_box.delete("0.0", "end")
            for line in self.history.get():
                self.history_box.insert("end", line + "\n")
            self.history_box.configure(state="disabled")
            return

        self.history_win = ctk.CTkToplevel(self)
        self.history_win.title("📜Calculation History")
        self.update_idletasks()
        x = self.winfo_x() + self.winfo_width() + 50
        y = self.winfo_y() + 0
        self.history_win.geometry(f"320x340+{x}+{y}")

        #   Create a single row frame to hold both the text and the button
        header_frame = ctk.CTkFrame(self.history_win, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(8, 4))

        ctk.CTkLabel(
            header_frame, text="All-Tabs (Last 24 hours)",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left")    #Previous value : (padx=10, pady=(8, 4), anchor="w")

        ctk.CTkButton(
            header_frame, 
            text="🗑 Clear",  # Shortened text slightly to keep it compact
            width=60, 
            height=24,
            fg_color="transparent",        
            border_width=1,                
            border_color="#8b1a1a",        
            text_color="#ff6666",          
            hover_color="#331414",         
            command=lambda: [self.history.clear_all(), self.show_history()]
        ).pack(side="right")


        #   The font size and name considered for a change in next version
        self.history_box = ctk.CTkTextbox(
            self.history_win, font=("Consolas", 11), state="normal"
        )
        self.history_box.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        entries = self.history.get()
        if entries:
            for line in entries:
                self.history_box.insert("end", line + "\n")
        else:
            self.history_box.insert("end", "(no history yet)")
        self.history_box.configure(state="disabled")

    def handle_keys(self, event):
        """Map physical keyboard keys to calculator actions."""
        if self.tabs.get() != "🔢 Scientific ":
            return

        #   THE GUARD: Filter out 'modifier' signals
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Caps_Lock"):
            return

        #   Allow alphabets to be typed and shown on display.
        #   Only when = or Enter is pressed does calculate() check for
        #   unknown variables and show "Go to Algebra Tab".
        if event.char in "0123456789.+-*/()%,^":
            self.insert(event.char)
        elif event.char and event.char.isalpha():
            #   Let the letter appear on screen — insert it as-is.
            #   The alphabet check in calculate() will intercept it on =.
            self.insert(event.char)
        elif event.keysym == "Return":
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Delete":
            self.clear()
        elif event.keysym == "Escape":
            if messagebox.askyesno("Exit", "Exit the calculator?"):
                self.destroy()
        elif event.char and event.char.isprintable():
            self.show_error("Error: Invalid key")


# ═════════════════════════════════════════════════════════
#   ENTRY POINT
# ═════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()