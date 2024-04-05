plugins {
    alias(libs.plugins.jvm)
}

repositories {
    mavenCentral()
    maven(url = "https://jitpack.io")
}

dependencies {
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
    testImplementation(libs.junit.jupiter.engine)
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")

    implementation(libs.guava)
    implementation("com.github.freeze-dolphin:aff-compose:cef7fbdb5a")
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

tasks.named<Test>("test") {
    useJUnitPlatform()
}
