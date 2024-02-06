plugins {
    alias(libs.plugins.jvm)
    application
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
    implementation("com.github.freeze-dolphin:aff-compose:302a6020c3")
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

application {
    mainClass = "io.sn.affproc.Main"
}

tasks.named<Test>("test") {
    useJUnitPlatform()
}
