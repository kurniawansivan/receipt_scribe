class ApiResponse<T> {
  final bool success;
  final String? message;
  final T? data;
  final String? error;

  ApiResponse({
    required this.success,
    this.message,
    this.data,
    this.error,
  });

  factory ApiResponse.fromJson(Map<String, dynamic> json, T Function(dynamic) fromJson) {
    return ApiResponse(
      success: json['success'],
      message: json['message'],
      data: json['data'] != null ? fromJson(json['data']) : null,
      error: json['error'],
    );
  }
}

class UploadResponse {
  final bool success;
  final int? expenseId;
  final String? message;
  final String? error;

  UploadResponse({
    required this.success,
    this.expenseId,
    this.message,
    this.error,
  });

  factory UploadResponse.fromJson(Map<String, dynamic> json) {
    return UploadResponse(
      success: json['success'],
      expenseId: json['expense_id'],
      message: json['message'],
      error: json['error'],
    );
  }
}