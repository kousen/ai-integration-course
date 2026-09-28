import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * The key stays on the server. Standard library only (JDK 21+).
 *
 *   export OPENROUTER_API_KEY=... CHAT_MODEL=minimax/minimax-m3
 *   java Server.java             # then open http://localhost:8000
 *
 * Same contract as server.py: the browser sends only the question as plain text.
 * No JSON parser needed: the server builds one small JSON body and passes the reply through.
 */
public class Server {
    static final String BASE_URL = System.getenv().getOrDefault("CHAT_BASE_URL", "https://openrouter.ai/api/v1").replaceAll("/$", "");
    static final String KEY = System.getenv("OPENROUTER_API_KEY");   // never sent to the browser
    static final String MODEL = System.getenv("CHAT_MODEL");         // the server decides which model is paid for
    static final HttpClient CLIENT = HttpClient.newHttpClient();

    public static void main(String[] args) throws IOException {
        byte[] page = Files.readAllBytes(Path.of("index.html"));
        HttpServer server = HttpServer.create(new InetSocketAddress("localhost", 8000), 0);
        server.createContext("/", ex -> reply(ex, 200, "text/html; charset=utf-8", page));
        server.createContext("/api/ask", Server::ask);
        server.start();
        System.out.println("http://localhost:8000  (model " + MODEL + ")");
    }

    static void ask(HttpExchange ex) throws IOException {
        if (!ex.getRequestMethod().equals("POST")) {
            reply(ex, 405, "text/plain", "POST only".getBytes());
            return;
        }
        String question = new String(ex.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
        if (question.length() > 2000) question = question.substring(0, 2000);   // cap what a visitor can send
        String body = """
                {"model": "%s", "max_tokens": 500, "messages": [{"role": "user", "content": "%s"}]}"""
                .formatted(MODEL, escape(question));
        HttpRequest req = HttpRequest.newBuilder(URI.create(BASE_URL + "/chat/completions"))
                .header("Authorization", "Bearer " + KEY)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .build();
        try {
            HttpResponse<byte[]> res = CLIENT.send(req, HttpResponse.BodyHandlers.ofByteArray());
            reply(ex, res.statusCode(), "application/json", res.body());   // provider's JSON, passed through
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            reply(ex, 502, "text/plain", "upstream call interrupted".getBytes());
        }
    }

    /** Minimal JSON string escaping: enough for a question typed into a form. */
    static String escape(String s) {
        StringBuilder out = new StringBuilder();
        for (char c : s.toCharArray()) {
            switch (c) {
                case '"' -> out.append("\\\"");
                case '\\' -> out.append("\\\\");
                case '\n' -> out.append("\\n");
                case '\r' -> out.append("\\r");
                case '\t' -> out.append("\\t");
                default -> {
                    if (c < 0x20) out.append(String.format("\\u%04x", (int) c));
                    else out.append(c);
                }
            }
        }
        return out.toString();
    }

    static void reply(HttpExchange ex, int status, String type, byte[] data) throws IOException {
        ex.getResponseHeaders().set("Content-Type", type);
        ex.sendResponseHeaders(status, data.length);
        try (var os = ex.getResponseBody()) {
            os.write(data);
        }
    }
}
