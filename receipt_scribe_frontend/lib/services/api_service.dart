import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:mime/mime.dart'; // Add this import
import '../models/expense.dart';
import '../models/api_response.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  static const String apiPrefix = '/api/expenses';

  final http.Client client;

  ApiService({http.Client? client}) : client = client ?? http.Client();

  Future<UploadResponse> uploadReceipt(File imageFile) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl$apiPrefix/upload'),
      );

      // Get the MIME type of the file
      String? mimeType = lookupMimeType(imageFile.path);
      
      request.files.add(await http.MultipartFile.fromPath(
        'file',
        imageFile.path,
        contentType: mimeType != null ? MediaType.parse(mimeType) : null,
      ));

      var response = await request.send();
      var responseData = await response.stream.bytesToString();
      var jsonResponse = json.decode(responseData);

      if (response.statusCode == 200) {
        return UploadResponse.fromJson(jsonResponse);
      } else {
        return UploadResponse(
          success: false,
          error: jsonResponse['detail'] ?? 'Upload failed',
        );
      }
    } catch (e) {
      return UploadResponse(
        success: false,
        error: 'Network error: $e',
      );
    }
  }
// ...existing code...

  Future<ApiResponse<ExpenseSummary>> getExpenses() async {
    try {
      final response = await client.get(
        Uri.parse('$baseUrl$apiPrefix/'),
      );

      if (response.statusCode == 200) {
        final jsonResponse = json.decode(response.body);
        return ApiResponse<ExpenseSummary>(
          success: true,
          data: ExpenseSummary.fromJson(jsonResponse),
        );
      } else {
        return ApiResponse<ExpenseSummary>(
          success: false,
          error: 'Failed to load expenses',
        );
      }
    } catch (e) {
      return ApiResponse<ExpenseSummary>(
        success: false,
        error: 'Network error: $e',
      );
    }
  }

  void dispose() {
    client.close();
  }
}