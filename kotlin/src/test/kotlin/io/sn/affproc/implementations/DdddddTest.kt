package io.sn.affproc.implementations

import org.junit.jupiter.api.Test

class DdddddTest {

    @Test
    fun testFlash() {
        val sb = StringBuilder()
        var flsCnt = 0
        var prevFls: Boolean
        var currFls = false
        (510..1000 step 1).map {
            val a = it.toDouble() / 1000
            prevFls = currFls
            currFls = flash(a)
            println(String.format("%.3f", a))
            if (prevFls != currFls) {
                println("flash!")
                flsCnt += 1
                sb.append("F")
            } else sb.append(".")
        }
        println("flash count: $flsCnt")
        println(sb.toString())
    }
}