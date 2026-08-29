/**
 * Vākya Calculator UI Logic
 *
 * This client script manages state, keyboard handling, and arithmetic operations
 * mirroring the exact semantics of `vakya/calculator.vakya`.
 */

// Core arithmetic functions corresponding directly to Vākya functions
const VakyaMath = {
  joda: (a, b) => a + b,
  ghatana: (a, b) => a - b,
  guna: (a, b) => a * b,
  bhaga: (a, b) => {
    if (b === 0) return null; // Division by zero
    return a / b;
  },
  ghata: (a, b) => Math.pow(a, b),
  sheshaphala: (a, b) => {
    if (b === 0) return null;
    return a % b;
  },
  ganana: (a, b, op) => {
    switch (op) {
      case "+": return VakyaMath.joda(a, b);
      case "-": return VakyaMath.ghatana(a, b);
      case "*": return VakyaMath.guna(a, b);
      case "/": return VakyaMath.bhaga(a, b);
      case "%": return VakyaMath.sheshaphala(a, b);
      case "**": return VakyaMath.ghata(a, b);
      default: return null;
    }
  }
};

class CalculatorApp {
  constructor() {
    this.previousOperand = null;
    this.currentOperand = "0";
    this.operation = null;
    this.shouldResetScreen = false;
    this.isError = false;

    this.expressionDisplay = document.getElementById("expressionDisplay");
    this.resultDisplay = document.getElementById("resultDisplay");

    this.initEventListeners();
  }

  initEventListeners() {
    // Number buttons
    document.querySelectorAll(".btn-num").forEach(btn => {
      btn.addEventListener("click", () => {
        this.appendNumber(btn.dataset.num);
        this.updateDisplay();
      });
    });

    // Operator buttons
    document.querySelectorAll(".btn-operator").forEach(btn => {
      btn.addEventListener("click", () => {
        this.chooseOperation(btn.dataset.op);
        this.updateDisplay();
      });
    });

    // Equals button
    document.getElementById("btnEquals").addEventListener("click", () => {
      this.compute();
      this.updateDisplay();
    });

    // Clear button
    document.getElementById("btnClear").addEventListener("click", () => {
      this.clear();
      this.updateDisplay();
    });

    // Backspace button
    document.getElementById("btnBackspace").addEventListener("click", () => {
      this.deleteLast();
      this.updateDisplay();
    });

    // Keyboard support
    window.addEventListener("keydown", (e) => this.handleKeyboard(e));
  }

  appendNumber(number) {
    if (this.isError) {
      this.clear();
    }
    if (this.shouldResetScreen) {
      this.currentOperand = "";
      this.shouldResetScreen = false;
    }
    if (number === "." && this.currentOperand.includes(".")) {
      return;
    }
    if (this.currentOperand === "0" && number !== ".") {
      this.currentOperand = number;
    } else {
      this.currentOperand += number;
    }
  }

  deleteLast() {
    if (this.isError || this.shouldResetScreen) {
      this.clear();
      return;
    }
    if (this.currentOperand.length === 1 || (this.currentOperand.length === 2 && this.currentOperand.startsWith("-"))) {
      this.currentOperand = "0";
    } else {
      this.currentOperand = this.currentOperand.slice(0, -1);
    }
  }

  chooseOperation(operation) {
    if (this.isError) return;
    if (this.currentOperand === "" && this.previousOperand === null) return;

    if (this.previousOperand !== null && !this.shouldResetScreen) {
      this.compute();
    }

    this.operation = operation;
    this.previousOperand = this.currentOperand;
    this.shouldResetScreen = true;
  }

  compute() {
    if (this.operation === null || this.previousOperand === null || this.isError) {
      return;
    }

    const prev = parseFloat(this.previousOperand);
    const curr = parseFloat(this.currentOperand);

    if (isNaN(prev) || isNaN(curr)) {
      return;
    }

    const computation = VakyaMath.ganana(prev, curr, this.operation);

    if (computation === null) {
      this.currentOperand = "Error: Division by 0";
      this.isError = true;
      this.operation = null;
      this.previousOperand = null;
      return;
    }

    // Format clean numbers (e.g. 10 instead of 10.000000000000002)
    this.currentOperand = Math.round(computation * 1e10) / 1e10 + "";
    this.operation = null;
    this.previousOperand = null;
    this.shouldResetScreen = true;
  }

  clear() {
    this.previousOperand = null;
    this.currentOperand = "0";
    this.operation = null;
    this.shouldResetScreen = false;
    this.isError = false;
  }

  getOpSymbol(op) {
    switch (op) {
      case "+": return "+";
      case "-": return "−";
      case "*": return "×";
      case "/": return "÷";
      case "%": return "%";
      case "**": return "^";
      default: return "";
    }
  }

  updateDisplay() {
    this.resultDisplay.innerText = this.currentOperand;

    if (this.operation !== null && this.previousOperand !== null) {
      this.expressionDisplay.innerText = `${this.previousOperand} ${this.getOpSymbol(this.operation)}`;
    } else {
      this.expressionDisplay.innerText = "";
    }

    // Highlight active operator
    document.querySelectorAll(".btn-operator").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.op === this.operation);
    });
  }

  handleKeyboard(e) {
    if ((e.key >= "0" && e.key <= "9") || e.key === ".") {
      this.appendNumber(e.key);
      this.updateDisplay();
    } else if (e.key === "+" || e.key === "-" || e.key === "*" || e.key === "/") {
      this.chooseOperation(e.key);
      this.updateDisplay();
    } else if (e.key === "%") {
      this.chooseOperation("%");
      this.updateDisplay();
    } else if (e.key === "^") {
      this.chooseOperation("**");
      this.updateDisplay();
    } else if (e.key === "Enter" || e.key === "=") {
      e.preventDefault();
      this.compute();
      this.updateDisplay();
    } else if (e.key === "Backspace") {
      this.deleteLast();
      this.updateDisplay();
    } else if (e.key === "Escape") {
      this.clear();
      this.updateDisplay();
    }
  }
}

// Instantiate on load
document.addEventListener("DOMContentLoaded", () => {
  window.calculator = new CalculatorApp();
});
