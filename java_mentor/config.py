"""
JavaMentor AI — Configuration
Reads from .env file. All settings in one place.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Gemini settings ─────────────────────────────────────────────────────────
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

# ── App settings ─────────────────────────────────────────────────────────────
APP_NAME: str = "java_mentor"
APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT: int = int(os.getenv("APP_PORT", "8090"))

# ── Code execution ────────────────────────────────────────────────────────────
PISTON_API_URL: str = "https://emkc.org/api/v2/piston/execute"
PISTON_TIMEOUT: float = 15.0

# ── Java version database (ground truth for the news agent) ──────────────────
JAVA_VERSION_FEATURES: dict = {
    "8": {
        "release": "March 2014",
        "lts": True,
        "headline": "The Lambda Revolution",
        "features": [
            "Lambda Expressions & Functional Interfaces",
            "Stream API (map, filter, reduce)",
            "Optional<T> — no more NullPointerException",
            "Default & Static Interface Methods",
            "Method References (Class::method)",
            "Date/Time API — java.time (Joda-Time inspired)",
            "CompletableFuture for async programming",
            "Base64 API",
            "Nashorn JavaScript Engine",
            "Parallel Array Sorting",
        ],
        "jeps": [
            "JEP 126: Lambda Expressions & Virtual Extension Methods",
            "JEP 107: Bulk Data Operations for Collections (Streams)",
            "JEP 150: Date & Time API",
        ],
        "example": """// Lambda + Stream — Java 8 style
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
names.stream()
     .filter(name -> name.startsWith("A"))
     .map(String::toUpperCase)
     .forEach(System.out::println); // ALICE""",
    },
    "11": {
        "release": "September 2018",
        "lts": True,
        "headline": "First LTS after Java 8 — HTTP/2 & Quality of Life",
        "features": [
            "HTTP Client API (standardized, replaces HttpURLConnection)",
            "String: isBlank(), lines(), strip(), stripLeading(), stripTrailing(), repeat()",
            "Files.readString() / writeString()",
            "var in lambda parameters",
            "Run Java files directly: java HelloWorld.java",
            "Removal of Java EE & CORBA modules",
            "Epsilon GC (no-op garbage collector)",
            "ZGC — Low-latency GC (experimental)",
            "Flight Recorder (JFR) — open-sourced",
            "Nest-Based Access Control",
        ],
        "jeps": [
            "JEP 321: HTTP Client (Standard)",
            "JEP 330: Launch Single-File Source-Code Programs",
            "JEP 328: Flight Recorder",
        ],
        "example": """// HTTP Client — Java 11
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .GET()
    .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());""",
    },
    "17": {
        "release": "September 2021",
        "lts": True,
        "headline": "Sealed Classes, Records, Text Blocks — Modern Java Solidified",
        "features": [
            "Sealed Classes (final) — restrict class hierarchies",
            "Records (final) — concise immutable data classes",
            "Text Blocks (final) — multi-line string literals",
            "Pattern Matching for instanceof (final)",
            "Switch Expressions (final)",
            "Strong encapsulation of JDK internals",
            "Pseudo-Random Number Generators (new API)",
            "New macOS AArch64 port",
            "Deprecate Applet API",
            "Remove RMI Activation System",
        ],
        "jeps": [
            "JEP 409: Sealed Classes",
            "JEP 395: Records",
            "JEP 378: Text Blocks",
            "JEP 394: Pattern Matching for instanceof",
        ],
        "example": """// Records — Java 17
record Point(int x, int y) {}  // Replaces POJO with getters, equals, hashCode, toString

// Sealed classes
sealed interface Shape permits Circle, Rectangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double w, double h) implements Shape {}

// Pattern matching
Object obj = new Circle(5.0);
if (obj instanceof Circle c) {  // No cast needed!
    System.out.println("Radius: " + c.radius());
}

// Text blocks
String json = \"\"\"
    {
        "name": "Alice",
        "age": 30
    }
    \"\"\";""",
    },
    "21": {
        "release": "September 2023",
        "lts": True,
        "headline": "Virtual Threads + Pattern Matching — The Concurrency Revolution",
        "features": [
            "Virtual Threads (Project Loom) — final! Millions of lightweight threads",
            "Pattern Matching for switch (final)",
            "Record Patterns (final) — destructure records in patterns",
            "Sequenced Collections — SequencedCollection, SequencedMap interfaces",
            "String Templates (preview)",
            "Unnamed Classes & Instance Main Methods (preview)",
            "Unnamed Patterns & Variables (preview — use _ for ignored vars)",
            "Structured Concurrency (preview)",
            "Scoped Values (preview)",
            "Vector API (incubator — SIMD)",
        ],
        "jeps": [
            "JEP 444: Virtual Threads",
            "JEP 441: Pattern Matching for switch",
            "JEP 440: Record Patterns",
            "JEP 431: Sequenced Collections",
        ],
        "example": """// Virtual Threads — Java 21 (MASSIVE throughput improvement!)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i ->
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return i;
        })
    );
}  // All 10,000 tasks complete in ~1 second!

// Pattern Matching for switch
Shape shape = new Circle(5.0);
double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.w() * r.h();
};

// Record Patterns
record Person(String name, int age) {}
Object obj = new Person("Alice", 30);
if (obj instanceof Person(String name, int age)) {
    System.out.println(name + " is " + age);  // Destructured!
}""",
    },
    "22": {
        "release": "March 2024",
        "lts": False,
        "headline": "Unnamed Variables + FFM API — Developer Ergonomics",
        "features": [
            "Unnamed Variables & Patterns (final) — use _ to ignore",
            "Foreign Function & Memory API (final) — native interop without JNI",
            "String Templates (second preview)",
            "Implicitly Declared Classes (second preview)",
            "Statements before super() (preview)",
            "Structured Concurrency (second preview)",
            "Scoped Values (second preview)",
            "Stream Gatherers (preview) — custom stream intermediate ops",
            "Class-File API (preview)",
            "Vector API (seventh incubator)",
        ],
        "jeps": [
            "JEP 456: Unnamed Variables & Patterns",
            "JEP 454: Foreign Function & Memory API",
            "JEP 473: Stream Gatherers (Preview)",
        ],
        "example": """// Unnamed Variables — Java 22
try {
    int result = riskyOperation();
} catch (Exception _) {  // _ means "I don't care about this variable"
    System.out.println("Operation failed");
}

// Stream Gatherers (preview) — sliding window
Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowSliding(3))
    .forEach(System.out::println);
// [1, 2, 3], [2, 3, 4], [3, 4, 5]""",
    },
    "23": {
        "release": "September 2024",
        "lts": False,
        "headline": "Primitive Patterns & Flexible Constructors",
        "features": [
            "Primitive Types in Patterns (preview) — pattern match on int, double, etc.",
            "Flexible Constructor Bodies (second preview) — code before super()",
            "Module Import Declarations (preview) — import module com.example",
            "Implicitly Declared Classes (third preview)",
            "Structured Concurrency (third preview)",
            "Scoped Values (third preview)",
            "Stream Gatherers (second preview)",
            "Class-File API (second preview)",
            "ZGC — Generational mode default",
            "Deprecate sun.misc.Unsafe memory-access methods",
        ],
        "jeps": [
            "JEP 455: Primitive Types in Patterns",
            "JEP 482: Flexible Constructor Bodies",
            "JEP 476: Module Import Declarations",
        ],
        "example": """// Primitive types in patterns (preview) — Java 23
Object obj = 42;
switch (obj) {
    case Integer i when i > 0 -> System.out.println("Positive int: " + i);
    case Double d              -> System.out.println("Double: " + d);
    default                   -> System.out.println("Other");
}""",
    },
    "24": {
        "release": "March 2025",
        "lts": False,
        "headline": "Stream Gatherers Final + Quantum-Safe Cryptography",
        "features": [
            "Stream Gatherers (final) — custom intermediate stream operations",
            "Class-File API (final) — programmatic bytecode manipulation",
            "Structured Concurrency (final)",
            "Scoped Values (final)",
            "Ahead-of-Time Class Loading & Linking (preview) — faster startup",
            "Compact Object Headers (experimental) — reduce object memory footprint",
            "Quantum-Resistant Key Encapsulation (ML-KEM)",
            "Quantum-Resistant Digital Signatures (ML-DSA, SLH-DSA)",
            "Primitive Types in Patterns (second preview)",
            "Flexible Constructor Bodies (final)",
        ],
        "jeps": [
            "JEP 485: Stream Gatherers",
            "JEP 484: Class-File API",
            "JEP 480: Structured Concurrency",
            "JEP 487: Scoped Values",
            "JEP 483: Ahead-of-Time Class Loading & Linking",
            "JEP 450: Compact Object Headers (Experimental)",
        ],
        "example": """// Stream Gatherers (final) — Java 24
// Custom fold gatherer
Gatherer<Integer, ?, Integer> runningSum = Gatherer.ofSequential(
    () -> new int[]{0},
    (state, element, downstream) -> {
        state[0] += element;
        return downstream.push(state[0]);
    }
);
List<Integer> result = Stream.of(1, 2, 3, 4, 5)
    .gather(runningSum)
    .toList();  // [1, 3, 6, 10, 15]""",
    },
}
