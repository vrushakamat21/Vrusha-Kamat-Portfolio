import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.Executors;

/**
 * Vrusha Kamat Portfolio - Java Web Server & API Backend
 * Written in standard, zero-dependency Java (Java 11 - Java 25+)
 * 
 * Features:
 * - High-performance non-blocking static file server (HTML, CSS, JS, SVG, PDF)
 * - REST API Endpoints:
 *     GET  /api/health     - Server health & Java runtime status
 *     GET  /api/stats      - Portfolio metrics & uptime
 *     POST /api/contact    - Validates & saves incoming contact messages to messages.json
 *     GET  /api/messages   - View received contact inquiries
 */
public class PortfolioServer {

    private static final int[] DEFAULT_PORTS = {8080, 8000, 8081, 8888, 3000, 5000};
    private static final String MESSAGES_FILE = "messages.json";
    private static final long START_TIME = System.currentTimeMillis();

    public static void main(String[] args) throws IOException {
        int port = -1;
        if (args.length > 0) {
            try {
                port = Integer.parseInt(args[0]);
            } catch (NumberFormatException ignored) {}
        }

        HttpServer server = null;
        if (port > 0) {
            server = HttpServer.create(new InetSocketAddress(port), 0);
        } else {
            for (int p : DEFAULT_PORTS) {
                try {
                    server = HttpServer.create(new InetSocketAddress(p), 0);
                    port = p;
                    break;
                } catch (java.net.BindException e) {
                    System.out.println("Port " + p + " is occupied, trying next port...");
                }
            }
            if (server == null) {
                // Let OS allocate any free port
                server = HttpServer.create(new InetSocketAddress(0), 0);
                port = server.getAddress().getPort();
            }
        }
        server.setExecutor(Executors.newVirtualThreadPerTaskExecutor() != null 
            ? Executors.newVirtualThreadPerTaskExecutor() 
            : Executors.newCachedThreadPool());

        // API Contexts
        server.createContext("/api/health", new HealthHandler());
        server.createContext("/api/stats", new StatsHandler());
        server.createContext("/api/contact", new ContactHandler());
        server.createContext("/api/messages", new MessagesHandler());

        // Static Files Context (Root)
        server.createContext("/", new StaticFileHandler());

        server.start();

        System.out.println("===============================================================");
        System.out.println("   VRUSHA KAMAT PORTFOLIO - JAVA BACKEND SERVER");
        System.out.println("   Java Runtime: " + System.getProperty("java.version") + " (" + System.getProperty("java.vendor") + ")");
        System.out.println("   Server running at: http://localhost:" + port + "/");
        System.out.println("   Health Endpoint:   http://localhost:" + port + "/api/health");
        System.out.println("===============================================================");
        System.out.println("   Press Ctrl+C to stop the server.");
    }

    // =========================================================================
    // Static File Handler
    // =========================================================================
    static class StaticFileHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String path = exchange.getRequestURI().getPath();
            if (path == null || path.equals("/") || path.isEmpty()) {
                path = "/index.html";
            }

            // Prevent directory traversal
            if (path.contains("..")) {
                sendResponse(exchange, 403, "text/plain", "Forbidden");
                return;
            }

            // Remove leading slash for local relative path
            String localPath = path.startsWith("/") ? path.substring(1) : path;
            File file = new File(localPath);

            if (!file.exists() || file.isDirectory()) {
                // Check if file in root exists or 404
                File fallback = new File("index.html");
                if (fallback.exists()) {
                    file = fallback;
                } else {
                    sendResponse(exchange, 404, "text/plain", "404 Not Found");
                    return;
                }
            }

            String mimeType = getMimeType(file.getName());
            byte[] fileBytes = Files.readAllBytes(file.toPath());

            exchange.getResponseHeaders().set("Content-Type", mimeType);
            exchange.getResponseHeaders().set("Cache-Control", "no-cache");
            exchange.sendResponseHeaders(200, fileBytes.length);

            try (OutputStream os = exchange.getResponseBody()) {
                os.write(fileBytes);
            }
        }
    }

    // =========================================================================
    // API: Health Check
    // =========================================================================
    static class HealthHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            setCORSHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            long uptimeSeconds = (System.currentTimeMillis() - START_TIME) / 1000;
            String json = "{\n" +
                "  \"status\": \"UP\",\n" +
                "  \"application\": \"Vrusha Kamat Portfolio Server\",\n" +
                "  \"runtime\": \"Java " + System.getProperty("java.version") + "\",\n" +
                "  \"uptimeSeconds\": " + uptimeSeconds + ",\n" +
                "  \"timestamp\": \"" + LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME) + "\"\n" +
                "}";

            sendResponse(exchange, 200, "application/json", json);
        }
    }

    // =========================================================================
    // API: Stats
    // =========================================================================
    static class StatsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            setCORSHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            int messageCount = countStoredMessages();
            String json = "{\n" +
                "  \"projectsCount\": 6,\n" +
                "  \"certificatesCount\": 6,\n" +
                "  \"experienceCount\": 4,\n" +
                "  \"academicCgpa\": 9.2,\n" +
                "  \"messagesReceived\": " + messageCount + "\n" +
                "}";

            sendResponse(exchange, 200, "application/json", json);
        }
    }

    // =========================================================================
    // API: Contact Form Submission Handler
    // =========================================================================
    static class ContactHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            setCORSHeaders(exchange);
            String method = exchange.getRequestMethod();

            if ("OPTIONS".equalsIgnoreCase(method)) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"POST".equalsIgnoreCase(method)) {
                sendResponse(exchange, 405, "application/json", "{\"error\": \"Method not allowed\"}");
                return;
            }

            // Read request body
            InputStream is = exchange.getRequestBody();
            String body = new String(is.readAllBytes(), StandardCharsets.UTF_8);

            // Simple robust JSON extractor
            String name = extractJsonField(body, "name");
            String email = extractJsonField(body, "email");
            String subject = extractJsonField(body, "subject");
            String message = extractJsonField(body, "message");

            // Server-side validation in Java
            if (name == null || name.isBlank() || email == null || email.isBlank() ||
                message == null || message.isBlank()) {
                sendResponse(exchange, 400, "application/json", 
                    "{\"success\": false, \"message\": \"Validation error: name, email, and message are required.\"}");
                return;
            }

            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            String messageId = "MSG-" + System.currentTimeMillis();

            // Save message to persistent messages.json
            saveMessageToJson(messageId, name, email, subject, message, timestamp);

            System.out.println("[Java Backend] New Contact Inquiry Received:");
            System.out.println("   ID:        " + messageId);
            System.out.println("   From:      " + name + " <" + email + ">");
            System.out.println("   Subject:   " + subject);
            System.out.println("   Timestamp: " + timestamp);

            String responseJson = "{\n" +
                "  \"success\": true,\n" +
                "  \"messageId\": \"" + messageId + "\",\n" +
                "  \"message\": \"Thank you, " + escapeJson(name) + "! Your message was received by the Java backend server.\",\n" +
                "  \"timestamp\": \"" + timestamp + "\"\n" +
                "}";

            sendResponse(exchange, 200, "application/json", responseJson);
        }
    }

    // =========================================================================
    // API: View Messages
    // =========================================================================
    static class MessagesHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            setCORSHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            File file = new File(MESSAGES_FILE);
            if (!file.exists()) {
                sendResponse(exchange, 200, "application/json", "[]");
                return;
            }

            String content = Files.readString(file.toPath(), StandardCharsets.UTF_8);
            sendResponse(exchange, 200, "application/json", content);
        }
    }

    // =========================================================================
    // Utilities
    // =========================================================================
    private static void sendResponse(HttpExchange exchange, int statusCode, String contentType, String content) throws IOException {
        byte[] bytes = content.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=utf-8");
        exchange.sendResponseHeaders(statusCode, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }

    private static void setCORSHeaders(HttpExchange exchange) {
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type, Authorization");
    }

    private static String getMimeType(String filename) {
        String lower = filename.toLowerCase();
        if (lower.endsWith(".html") || lower.endsWith(".htm")) return "text/html";
        if (lower.endsWith(".css")) return "text/css";
        if (lower.endsWith(".js")) return "application/javascript";
        if (lower.endsWith(".svg")) return "image/svg+xml";
        if (lower.endsWith(".pdf")) return "application/pdf";
        if (lower.endsWith(".png")) return "image/png";
        if (lower.endsWith(".jpg") || lower.endsWith(".jpeg")) return "image/jpeg";
        if (lower.endsWith(".json")) return "application/json";
        if (lower.endsWith(".txt")) return "text/plain";
        return "application/octet-stream";
    }

    private static synchronized void saveMessageToJson(String id, String name, String email, String subject, String message, String timestamp) {
        File file = new File(MESSAGES_FILE);
        StringBuilder sb = new StringBuilder();
        String entry = "  {\n" +
            "    \"id\": \"" + escapeJson(id) + "\",\n" +
            "    \"name\": \"" + escapeJson(name) + "\",\n" +
            "    \"email\": \"" + escapeJson(email) + "\",\n" +
            "    \"subject\": \"" + escapeJson(subject) + "\",\n" +
            "    \"message\": \"" + escapeJson(message) + "\",\n" +
            "    \"timestamp\": \"" + escapeJson(timestamp) + "\"\n" +
            "  }";

        try {
            if (!file.exists() || Files.readString(file.toPath()).trim().isEmpty()) {
                sb.append("[\n").append(entry).append("\n]");
            } else {
                String existing = Files.readString(file.toPath(), StandardCharsets.UTF_8).trim();
                if (existing.endsWith("]")) {
                    String withoutBracket = existing.substring(0, existing.length() - 1).trim();
                    if (withoutBracket.length() > 1 && withoutBracket.endsWith(",")) {
                        sb.append(withoutBracket).append("\n").append(entry).append("\n]");
                    } else if (withoutBracket.length() > 1) {
                        sb.append(withoutBracket).append(",\n").append(entry).append("\n]");
                    } else {
                        sb.append("[\n").append(entry).append("\n]");
                    }
                } else {
                    sb.append("[\n").append(entry).append("\n]");
                }
            }
            Files.writeString(file.toPath(), sb.toString(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            System.err.println("Error saving message: " + e.getMessage());
        }
    }

    private static int countStoredMessages() {
        File file = new File(MESSAGES_FILE);
        if (!file.exists()) return 0;
        try {
            String content = Files.readString(file.toPath(), StandardCharsets.UTF_8);
            int count = 0;
            int idx = 0;
            while ((idx = content.indexOf("\"id\":", idx)) != -1) {
                count++;
                idx += 5;
            }
            return count;
        } catch (IOException e) {
            return 0;
        }
    }

    private static String extractJsonField(String json, String field) {
        if (json == null) return "";
        String pattern = "\"" + field + "\"\\s*:\\s*\"([^\"]*)\"";
        java.util.regex.Pattern p = java.util.regex.Pattern.compile(pattern);
        java.util.regex.Matcher m = p.matcher(json);
        if (m.find()) {
            return m.group(1);
        }
        return "";
    }

    private static String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r");
    }
}
