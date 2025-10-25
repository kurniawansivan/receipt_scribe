class Expense {
  final int id;
  final String? vendorName;
  final DateTime? date;
  final double? totalAmount;
  final double? taxAmount;
  final List<ExpenseItem> items;

  Expense({
    required this.id,
    this.vendorName,
    this.date,
    this.totalAmount,
    this.taxAmount,
    this.items = const [],
  });

  factory Expense.fromJson(Map<String, dynamic> json) {
    return Expense(
      id: json['id'],
      vendorName: json['vendor_name'],
      date: json['date'] != null ? DateTime.parse(json['date']) : null,
      totalAmount: json['total_amount']?.toDouble(),
      taxAmount: json['tax_amount']?.toDouble(),
      items: json['items'] != null 
          ? (json['items'] as List).map((item) => ExpenseItem.fromJson(item)).toList()
          : [],
    );
  }
}

class ExpenseItem {
  final String description;
  final double amount;

  ExpenseItem({required this.description, required this.amount});

  factory ExpenseItem.fromJson(Map<String, dynamic> json) {
    return ExpenseItem(
      description: json['description'],
      amount: json['amount']?.toDouble(),
    );
  }
}

class ExpenseSummary {
  final double totalExpenses;
  final int expenseCount;
  final List<Expense> recentExpenses;

  ExpenseSummary({
    required this.totalExpenses,
    required this.expenseCount,
    required this.recentExpenses,
  });

  factory ExpenseSummary.fromJson(Map<String, dynamic> json) {
    return ExpenseSummary(
      totalExpenses: json['total_expenses']?.toDouble(),
      expenseCount: json['expense_count'],
      recentExpenses: (json['recent_expenses'] as List)
          .map((expense) => Expense.fromJson(expense))
          .toList(),
    );
  }
}