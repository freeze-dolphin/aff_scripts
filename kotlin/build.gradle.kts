plugins {
    alias(libs.plugins.jvm)
    id("io.ktor.plugin") version "2.3.10"
    id("com.autonomousapps.dependency-analysis") version "1.31.0"
}

val affComposeVersion = "8d463ccf1d"

repositories {
    mavenCentral()
    maven(url = "https://jitpack.io")
}

dependencies {
    testImplementation(libs.junit.jupiter.engine)
    testImplementation("org.junit.jupiter:junit-jupiter-api:5.10.0")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")

    implementation("com.github.freeze-dolphin:aff-compose:${affComposeVersion}")
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

tasks.named<Test>("test") {
    useJUnitPlatform()
}
