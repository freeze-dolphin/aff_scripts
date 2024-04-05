package io.sn.affproc.implementations

import com.tairitsu.compose.arcaea.ArcNote
import com.tairitsu.compose.arcaea.Position
import com.tairitsu.compose.arcaea.pos
import io.sn.affproc.utils.*
import kotlin.math.abs

@Suppress("DuplicatedCode")
val ddddddGetFrame = fun(
    hideTiming: Long,
    _: Double,
    _: Position,
    progress: Double,
    extraNoteOffset: Long,
    _: Any?,
): List<ArcNote> {
    val noteList = mutableListOf<ArcNote>()

    val offset = ((1 - easeInQuad(progress)) * 100).toLong() - extraNoteOffset * 3 / 4

    val easedProgress = easeOutCubic(progress) * 0.5 + 0.5

    val a = 0.5 - easedProgress / 2 pos easedProgress / 2 + 0.5 + 0.2
    val b = easedProgress / 2 + 0.5 pos easedProgress / 2 + 0.5 + 0.2
    val c = easedProgress / 2 + 0.5 pos 0.5 - easedProgress / 2 + 0.2
    val d = 0.5 - easedProgress / 2 pos 0.5 - easedProgress / 2 + 0.2

    val edge = 0.05
    val upStart = a.x pos a.y + edge
    val upEnd = b.x pos b.y + edge

    val leftStart = a.x - edge pos a.y
    val leftEnd = d.x - edge pos d.y

    val rightStart = b.x + edge pos b.y
    val rightEnd = c.x + edge pos c.y

    val downStart = c.x pos c.y - edge
    val downEnd = d.x pos d.y - edge

    if (progress < 0.75 || !flash(progress)) {
        noteList.addAll(
            listOf(
                genAnimationTrace(hideTiming + offset, a, b),
                genAnimationTrace(hideTiming + offset, b, c),
                genAnimationTrace(hideTiming + offset, c, d),
                genAnimationTrace(hideTiming + offset, d, a),

                genAnimationTrace(hideTiming + offset, upStart, upEnd),
                genAnimationTrace(hideTiming + offset, leftStart, leftEnd),
                genAnimationTrace(hideTiming + offset, rightStart, rightEnd),
                genAnimationTrace(hideTiming + offset, downStart, downEnd),

                genAnimationTrace(hideTiming + offset, leftStart, upStart),
                genAnimationTrace(hideTiming + offset, upEnd, rightStart),
                genAnimationTrace(hideTiming + offset, rightEnd, downStart),
                genAnimationTrace(hideTiming + offset, downEnd, leftEnd),

                genAnimationTrace(hideTiming + offset, a, c),
                genAnimationTrace(hideTiming + offset, b, d),
            )
        )
    }

    return noteList
}

fun flash(x: Double): Boolean {
    var nextC = 0.25
    var prevC = nextC
    while (nextC < x) {
        prevC = nextC
        nextC += (1 - nextC) / 2
    }

    return abs(x - prevC) <= abs(x - nextC)
}
