import 'dart:io';
import 'package:flutter/foundation.dart';
import '../models/expense.dart';
import '../models/api_response.dart';
import '../services/api_service.dart';

class ExpenseProvider with ChangeNotifier {
  final ApiService _apiService;
  
  List<Expense> _expenses = [];
  double _totalAmount = 0;
  int _expenseCount = 0;
  bool _isLoading = false;
  String? _error;

  ExpenseProvider({ApiService? apiService}) 
      : _apiService = apiService ?? ApiService();

  // Getters
  List<Expense> get expenses => _expenses;
  double get totalAmount => _totalAmount;
  int get expenseCount => _expenseCount;
  bool get isLoading => _isLoading;
  String? get error => _error;

  // Load all expenses
  Future<void> loadExpenses() async {
    _setLoading(true);
    _error = null;

    try {
      final response = await _apiService.getExpenses();
      
      if (response.success && response.data != null) {
        _expenses = response.data!.recentExpenses;
        _totalAmount = response.data!.totalExpenses;
        _expenseCount = response.data!.expenseCount;
      } else {
        _error = response.error ?? 'Failed to load expenses';
      }
    } catch (e) {
      _error = 'Error loading expenses: $e';
    } finally {
      _setLoading(false);
    }
  }

  // Upload receipt
  Future<UploadResponse> uploadReceipt(File imageFile) async {
    _setLoading(true);
    _error = null;

    try {
      final response = await _apiService.uploadReceipt(imageFile);
      
      if (response.success) {
        // Reload expenses to get updated list
        await loadExpenses();
      } else {
        _error = response.error;
      }
      
      return response;
    } catch (e) {
      final errorResponse = UploadResponse(
        success: false,
        error: 'Upload failed: $e',
      );
      _error = errorResponse.error;
      return errorResponse;
    } finally {
      _setLoading(false);
    }
  }

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _apiService.dispose();
    super.dispose();
  }
}