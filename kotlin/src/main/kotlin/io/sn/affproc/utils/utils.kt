package io.sn.affproc.utils

import com.tairitsu.compose.arcaea.ArcNote
import java.io.Serializable

fun genTrace(timing: Long, endTiming: Long, startPosition: Position, endPosition: Position): ArcNote {
    return ArcNote(timing, endTiming, startPosition.toPair(), ArcNote.Type.S, endPosition.toPair(), ArcNote.Color.BLUE, true) {}
}

fun genAnimationTrace(timing: Long, startPosition: Position, endPosition: Position): ArcNote {
    return genTrace(timing, timing, startPosition, endPosition)
}

data class Position(
    var x: Double,
    var y: Double,
) : Serializable {

    /**
     * Returns string representation of the [Position] including its [x] and [y] values.
     */
    override fun toString(): String = "($x, $y)"

    fun toList(): List<Double> = listOf(x, y)

    fun toPair(): Pair<Double, Double> = x to y
}

infix fun <A : Number, B : Number> A.pos(that: B): Position = Position(this.toDouble(), that.toDouble())